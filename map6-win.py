import os
import sys
import webbrowser
import csv
import io
import base64
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash

######################################################
# GLOBAL MESSAGES
######################################################
timing_deviation_messages = []
timing_crash_events = []
throttleclose_events = []

######################################################
# CHECK FUNCTIONS (SAME AS BEFORE)
######################################################

def checktiming(
    mythrottle, mypedal, myign1, myign2, myign3, myign4, myign5, myign6,
    myrpm, mytimestamp, mytrigger, afr2, mph,
    four_cyl_sensitivity, six_cyl_sensitivity
):
    global timing_deviation_messages, timing_crash_events
    if afr2 > 10:
        # 6-cyl mode
        if mythrottle > 95 and mypedal > 96:
            myigndev = myign2 + myign3 + myign4 + myign5 + myign6
            if (
                myigndev > six_cyl_sensitivity and
                myigndev < ((myign1 - six_cyl_sensitivity) * 6)
            ):
                msg = (
                    f"Timing Deviation Detected at Timestamp {mytimestamp}, RPM: {myrpm}, "
                    f"Correction: {myigndev}\n"
                    f"   IGN1: {myign1}, IGN2: {myign2}, IGN3: {myign3}, "
                    f"IGN4: {myign4}, IGN5: {myign5}, IGN6: {myign6}"
                )
                timing_deviation_messages.append(msg)
    else:
        # 4-cyl mode
        if mythrottle > 95 and mypedal > 96:
            myigndev = myign2 + myign3 + myign4
            if (
                myigndev > four_cyl_sensitivity and
                myigndev < ((myign1 - four_cyl_sensitivity) * 4)
            ):
                msg = (
                    f"(4Cyl Mode) Timing Deviation Detected at Timestamp {mytimestamp}, RPM: {myrpm}, "
                    f"Correction: {myigndev}\n"
                    f"   IGN1: {myign1}, IGN2: {myign2}, IGN3: {myign3}, IGN4: {myign4}"
                )
                timing_deviation_messages.append(msg)

            # Crash
            if mph >= 20 and myign1 < 0.01:
                timing_crash_events.append((mytimestamp, mph))


def checktrims(mythrottle, mypedal, myrpm, mytimestamp, mytrims, mytrims2, myafr1, myafr2):
    output = io.StringIO()
    myspread = mytrims2 - mytrims
    if mythrottle > 95 and myspread > 10:
        print(
            f"Fuel Trim Separation Detected -- RPM: {myrpm}, Trim1: {mytrims}, "
            f"Trim2: {mytrims2}, Spread: {myspread}, TS: {mytimestamp}, AFR1: {myafr1}, AFR2: {myafr2}",
            file=output
        )
    if mythrottle > 95 and mytrims > 50:
        print(
            f"High Fuel Trim Detected (NORMAL for E30 / Map3; could be bad for meth). "
            f"Trim1: {mytrims}, Trim2: {mytrims2}, RPM: {myrpm}",
            file=output
        )
    if mythrottle > 95 and mytrims < 7:
        print(
            f"Low Fuel Trim Detected. Watch for potentially frozen trims. Trim1: {mytrims}",
            file=output
        )
    return output.getvalue()


def checkhpfp(mythrottle, mypedal, myrpm, mytimestamp, myfp_h):
    output = io.StringIO()
    if myfp_h == 0:
        return output.getvalue()
    if mythrottle > 95 and mypedal > 90 and myfp_h < 10:
        print(
            f"HPFP Issue Detected -- Consider using less E85. Timestamp: {mytimestamp}, "
            f"RPM: {myrpm}, HPFP: {myfp_h}",
            file=output
        )
    return output.getvalue()


def checkthrottleclose(mythrottle, mypedal, myrpm, myboost, myboost2, mytimestamp):
    global throttleclose_events
    if mypedal > 95 and myrpm > 4000 and mythrottle < 85:
        msg = (
            f"Throttle Closure Detected (Consider paddle shifting instead). "
            f"TS: {mytimestamp}, RPM: {myrpm}, Throttle: {mythrottle}, Pedal: {mypedal}"
        )
        if (myboost - myboost2) > 3:
            msg += (
                f"\n   Large Boost Drop Detected at RPM: {myrpm}, "
                f"Boost1: {myboost}, Boost2: {myboost2}"
            )
        throttleclose_events.append(msg)


def checkmethflow(mythrottle, mypedal, myrpm, myboost, mytimestamp, mymeth, mytriggercount):
    output = io.StringIO()
    if mymeth == 0:
        return output.getvalue()
    if mypedal > 95 and mymeth < 90 and mytriggercount > 1 and myboost > 10:
        print(
            f"Meth Flow Issue Detected! Fix This First (possible air bubbles, purge, or out of meth). "
            f"TS: {mytimestamp}, RPM: {myrpm}, Boost: {myboost}, Meth Flow: {mymeth}",
            file=output
        )
    return output.getvalue()


def checkboostdeviation(mythrottle, mypedal, myboost, myboost2, mytimestamp):
    output = io.StringIO()
    if mythrottle > 95 and abs(myboost - myboost2) > 1.9:
        print(
            f"Boost1 and Boost2 differ significantly (B1: {myboost}, B2: {myboost2}, "
            f"Diff: {myboost - myboost2}) -- TS: {mytimestamp}",
            file=output
        )
    return output.getvalue()


def checkiat(myrpm, mythrottle, mypedal, myiat):
    output = io.StringIO()
    if myrpm > 2500 and mythrottle > 95 and myiat > 118:
        print(
            f"Heat Soak Detected! Consider using methanol injection, a better FMIC, or allowing the car to cool. "
            f"RPM: {myrpm}, IAT: {myiat}",
            file=output
        )
    return output.getvalue()

######################################################
# run_all_checks
######################################################
def run_all_checks(df, four_cyl_sens=3.5, six_cyl_sens=6.5):
    global timing_deviation_messages, timing_crash_events, throttleclose_events
    timing_deviation_messages = []
    timing_crash_events = []
    throttleclose_events = []

    iatOut = "\nIAT\n-------------------\n"
    hpfpOut = "\nHPFP Report\n--------------------\n"
    methflowOut = "\nMeth Flow Report\n-----------------\n"
    boostdevOut = "\nBoost Deviations\n--------------------\n"
    trimsOut = "\nFuel Trims\n-------------------------\n"

    triggercount = 4

    for _, row_data in df.iterrows():
        timestamp  = row_data["timestamp"]
        rpm        = row_data["rpm"]
        boost      = row_data["boost"]
        throttle   = row_data["throttle"]
        pedal      = row_data["pedal"]
        iat        = row_data["iat"]
        fp_h       = row_data["fp_h"]
        ign_1      = row_data["ign_1"]
        ign_2      = row_data["ign_2"]
        ign_3      = row_data["ign_3"]
        ign_4      = row_data["ign_4"]
        ign_5      = row_data["ign_5"]
        ign_6      = row_data["ign_6"]
        afr        = row_data["afr"]
        afr2       = row_data["afr2"]
        boost2     = row_data["boost2"]
        meth       = row_data["meth"]
        trims_val  = row_data["trims_val"]
        trims2     = row_data["trims2"]
        mph        = row_data["mph"]

        iatOut += checkiat(rpm, throttle, pedal, iat)
        checktiming(
            throttle, pedal, ign_1, ign_2, ign_3, ign_4, ign_5, ign_6,
            rpm, timestamp, triggercount, afr2, mph,
            four_cyl_sensitivity=four_cyl_sens,
            six_cyl_sensitivity=six_cyl_sens
        )
        hpfpOut += checkhpfp(throttle, pedal, rpm, timestamp, fp_h)
        checkthrottleclose(throttle, pedal, rpm, boost, boost2, timestamp)
        methflowOut += checkmethflow(throttle, pedal, rpm, boost, timestamp, meth, triggercount)
        boostdevOut += checkboostdeviation(throttle, pedal, boost, boost2, timestamp)
        trimsOut += checktrims(throttle, pedal, rpm, timestamp, trims_val, trims2, afr, afr2)

    # Summaries
    timing_crash_summary = ""
    if timing_crash_events:
        mph_values = [evt[1] for evt in timing_crash_events]
        min_mph = min(mph_values)
        max_mph = max(mph_values)
        crash_count = len(timing_crash_events)
        timing_crash_summary = (
            "\nTiming Crash Summary\n----------------\n"
            f"Detected {crash_count} instance(s) of timing crashing to zero.\n"
            f"Lowest mph observed: {min_mph}, highest mph observed: {max_mph}.\n"
            "Possible traction control or real ignition issue.\n"
        )

    throttleclose_summary = ""
    if len(throttleclose_events) > 5:
        throttleclose_summary = "\nThrottle Closure Report\n--------------------\n"
        throttleclose_summary += (
            f"Detected {len(throttleclose_events)} throttle closures.\n"
        )
        for msg in throttleclose_events:
            throttleclose_summary += msg + "\n"

    # Log length check
    high_throttle_df = df[df["throttle"] > 90]
    log_length_warning = ""
    if not high_throttle_df.empty:
        min_mph_90 = high_throttle_df["mph"].min()
        max_mph_90 = high_throttle_df["mph"].max()
        if (max_mph_90 - min_mph_90) < 65:
            log_length_warning = (
                "Log Length Warning:\n"
                "Your log does not show a >= 65 mph range at throttle > 90%. "
                "Consider 0-100 mph or 1/4 mile.\n\n"
            )
    else:
        log_length_warning = (
            "Log Length Warning:\n"
            "Never detected throttle >90%. Provide a more robust WOT log.\n\n"
        )

    final_report = (
        f"{iatOut}\n{hpfpOut}\n{methflowOut}\n{boostdevOut}\n{trimsOut}"
        f"{timing_crash_summary}"
        f"{throttleclose_summary}"
    )
    if timing_deviation_messages:
        final_report += (
            "\nTiming Deviations Detected\n------------------\n"
            + "\n".join(timing_deviation_messages) + "\n"
        )

    return log_length_warning, final_report

######################################################
# SINGLE-CALLBACK-STYLE DASH APP
######################################################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Log Analyzer"

app.layout = dbc.Container([
    html.H1("JB4/Lap3 Log Analyzer"),
    html.P("Upload CSV, adjust timing sensitivity, re-scan."),

    # 1) Hidden store
    dcc.Store(id='stored-data', storage_type='memory'),

    # 2) Outputs: Log length at top, main report
    html.Div(id='log-length-warning', style={
        'whiteSpace': 'pre-wrap',
        'border': '1px solid red',
        'padding': '10px',
        'margin-bottom': '10px',
        'backgroundColor': '#fff0f0'
    }),
    html.Div(id='report-output', style={
        'whiteSpace': 'pre-wrap',
        'border': '1px solid #ddd',
        'padding': '10px',
        'height': '300px',
        'overflowY': 'auto'
    }),

    # 3) Controls
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div(['Drag/Drop or Click to Select CSV']),
            style={
                'width': '100%', 'height': '60px',
                'lineHeight': '60px', 'borderWidth': '1px',
                'borderStyle': 'dashed', 'borderRadius': '5px',
                'textAlign': 'center'
            },
            multiple=False
        ),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Label("4Cyl Sensitivity:"),
                dcc.Input(id='four-cyl-sens', type='number', value=3.5, min=0, max=20, step=0.1)
            ], width=6),
            dbc.Col([
                html.Label("6Cyl Sensitivity:"),
                dcc.Input(id='six-cyl-sens', type='number', value=6.5, min=0, max=20, step=0.1)
            ], width=6)
        ]),
        html.Br(),
        dbc.Button("Re-Scan Log", id="rescan-button", color="primary")
    ]),

    # 4) Graph with multi-axis controls
    html.Hr(),
    html.H4("Plotly Multi-Axis Controls"),
    dbc.Row([
        dbc.Col([
            html.Label("Axis1"),
            dcc.Dropdown(id='axis1-dropdown', multi=True),
            dcc.RadioItems(
                id='axis1-scale',
                options=[{'label':'Linear','value':'linear'}, {'label':'Log','value':'log'}],
                value='linear', inline=True
            )
        ], width=3),
        dbc.Col([
            html.Label("Axis2"),
            dcc.Dropdown(id='axis2-dropdown', multi=True),
            dcc.RadioItems(
                id='axis2-scale',
                options=[{'label':'Linear','value':'linear'}, {'label':'Log','value':'log'}],
                value='linear', inline=True
            )
        ], width=3),
        dbc.Col([
            html.Label("Axis3"),
            dcc.Dropdown(id='axis3-dropdown', multi=True),
            dcc.RadioItems(
                id='axis3-scale',
                options=[{'label':'Linear','value':'linear'}, {'label':'Log','value':'log'}],
                value='linear', inline=True
            )
        ], width=3),
        dbc.Col([
            html.Label("Axis4"),
            dcc.Dropdown(id='axis4-dropdown', multi=True),
            dcc.RadioItems(
                id='axis4-scale',
                options=[{'label':'Linear','value':'linear'}, {'label':'Log','value':'log'}],
                value='linear', inline=True
            )
        ], width=3),
    ]),
    dcc.Graph(id='graph-output'),
    html.Div(id='hover-status', style={'height':'60px','border':'1px solid #ccc','padding':'10px'})
], fluid=True)


######################################################
# Single callback for file upload or re-scan
######################################################
@app.callback(
    Output('stored-data', 'data'),
    Output('log-length-warning', 'children'),
    Output('report-output', 'children'),
    [Input('upload-data', 'contents'), Input('rescan-button', 'n_clicks')],
    [State('four-cyl-sens','value'), State('six-cyl-sens','value'), State('stored-data','data')]
)
def handle_upload_or_rescan(contents, n_clicks, four_sens, six_sens, stored_json):
    global timing_deviation_messages, timing_crash_events, throttleclose_events
    timing_deviation_messages = []
    timing_crash_events = []
    throttleclose_events = []

    # Which triggered?
    ctx = callback_context
    if not ctx.triggered:
        return stored_json, "", "No input yet."
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # If user uploaded a new CSV
    if triggered_id == 'upload-data' and contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        data = decoded.decode('utf-8').splitlines()
        rows = list(csv.reader(data))
        if len(rows) < 10:
            return None, "", "File too short/invalid"

        data_rows = rows[5:]
        columns = [
            "timestamp","rpm","ecu_psi","target","boost","pedal","iat","fuelen",
            "wgdc","throttle","fp_h","ign_1","avg_ign","calc_torque","trims_val",
            "dme_bt","meth","fp_l","afr","gear","ff","load","clock","map",
            "afr2","ign_2","ign_3","ign_4","ign_5","ign_6","oilf","waterf",
            "transf","e85","boost2","trims2","mph"
        ]
        df = pd.DataFrame(data_rows, columns=columns)
        for c in columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')

        log_warn, final_rep = run_all_checks(df, four_sens, six_sens)
        store_json = df.to_json(orient='records')
        return store_json, log_warn, final_rep

    # If user clicked re-scan
    elif triggered_id == 'rescan-button' and stored_json is not None:
        df = pd.read_json(stored_json, orient='records')
        log_warn, final_rep = run_all_checks(df, four_sens, six_sens)
        return stored_json, log_warn, final_rep

    return stored_json, "", "No file yet."


######################################################
#  Populate axis dropdowns
######################################################
@app.callback(
    [Output('axis1-dropdown','options'),
     Output('axis2-dropdown','options'),
     Output('axis3-dropdown','options'),
     Output('axis4-dropdown','options')],
    Input('stored-data','data')
)
def update_dropdown_options(stored_json):
    if not stored_json:
        return [],[],[],[]
    df = pd.read_json(stored_json, orient='records')
    columns = [c for c in df.columns if c != 'timestamp']
    opts = [{'label':c,'value':c} for c in columns]
    return opts, opts, opts, opts


######################################################
# Build the 4-axis figure
######################################################
@app.callback(
    Output('graph-output','figure'),
    [Input('axis1-dropdown','value'),
     Input('axis2-dropdown','value'),
     Input('axis3-dropdown','value'),
     Input('axis4-dropdown','value'),
     Input('axis1-scale','value'),
     Input('axis2-scale','value'),
     Input('axis3-scale','value'),
     Input('axis4-scale','value')],
    State('stored-data','data')
)
def build_four_axis_figure(a1,a2,a3,a4, s1,s2,s3,s4, stored_json):
    if not stored_json:
        return {}
    df = pd.read_json(stored_json, orient='records')
    if 'timestamp' not in df.columns:
        return {}

    fig = go.Figure()
    # axis1
    if a1:
        for param in a1:
            fig.add_trace(go.Scatter(
                x=df['timestamp'], y=df[param],
                mode='lines', name=f"{param}(Axis1)",
                yaxis='y'
            ))
    # axis2
    if a2:
        for param in a2:
            fig.add_trace(go.Scatter(
                x=df['timestamp'], y=df[param],
                mode='lines', name=f"{param}(Axis2)",
                yaxis='y2'
            ))
    # axis3
    if a3:
        for param in a3:
            fig.add_trace(go.Scatter(
                x=df['timestamp'], y=df[param],
                mode='lines', name=f"{param}(Axis3)",
                yaxis='y3'
            ))
    # axis4
    if a4:
        for param in a4:
            fig.add_trace(go.Scatter(
                x=df['timestamp'], y=df[param],
                mode='lines', name=f"{param}(Axis4)",
                yaxis='y4'
            ))

    fig.update_layout(
        title="Multi-Axis Chart",
        xaxis=dict(title="Timestamp"),
        yaxis=dict(title="Axis1",type=s1),
        yaxis2=dict(title="Axis2", overlaying='y', side='right', type=s2),
        yaxis3=dict(title="Axis3", overlaying='y', side='left', anchor='free', position=0.15, type=s3),
        yaxis4=dict(title="Axis4", overlaying='y', side='right', anchor='free', position=0.85, type=s4),
        hovermode='x unified',
        legend_title="Parameters"
    )
    return fig

######################################################
# Hover status
######################################################
@app.callback(
    Output('hover-status','children'),
    Input('graph-output','hoverData')
)
def update_hover(hoverData):
    if not hoverData or 'points' not in hoverData:
        return "Hover over the chart to see values."
    lines_info = []
    for pt in hoverData['points']:
        nm = pt.get('data',{}).get('name')
        xv = pt.get('x')
        yv = pt.get('y')
        if nm:
            lines_info.append(f"{nm}: X={xv}, Y={yv}")
    return " | ".join(lines_info)

######################################################
# MAIN => LAUNCH BROWSER IF NOT SSH
######################################################
def main():
    # Only open browser if NOT over SSH
    # A simple check: if 'SSH_CONNECTION' not in env => local
    is_ssh = bool(os.environ.get("SSH_CONNECTION",""))
    if not is_ssh:
        # We'll open the browser
        import webbrowser
        webbrowser.open("http://127.0.0.1:8050", new=1)

    app.run_server(debug=False, host="127.0.0.1", port=8050)

if __name__ == "__main__":
    main()
