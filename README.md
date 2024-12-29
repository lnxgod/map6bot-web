# JB4/Lap3 Log Analyzer

A free tool to parse and analyze JB4 or Lap3 CSV logs. It automatically checks for:
- Timing deviations (with adjustable sensitivity for 4-cylinder and 6-cylinder modes).
- HPFP issues, throttle closures, meth flow, boost deviations, high intake temps, etc.
- Log length warnings (e.g., ensures you have a 0-100 or 1/4-mile run, not just 0-60).
- Summaries of repeated throttle closures, timing crashes, and more.

The tool spins up a **local Dash server**, automatically opens your default browser (when not run via SSH), and presents a web-based UI. You can then upload your log file, tweak sensitivity settings, re-scan, and see multi-axis Plotly graphs.

---

## **Features**

1. **CSV Parsing**  
   - Skips the first 5 header lines (typical JB4/Lap3 logs).  
   - Reads columns like `timestamp`, `rpm`, `throttle`, `ign_1..ign_6`, etc.

2. **Adjustable Timing Deviation Sensitivity**  
   - **4Cyl Sensitivity** replaces the old 3.5 threshold.  
   - **6Cyl Sensitivity** replaces the old 6.5 threshold.  

3. **Detailed Checks**  
   - **HPFP**: Warn if under 10 psi at high throttle.  
   - **Throttle Closure**: Summarize if more than 5 closures.  
   - **Meth Flow**: Check if meth is below 90% during WOT.  
   - **Boost Deviation**: Compare Boost1 and Boost2.  
   - **IAT**: Alert if intake temps exceed 118°F under load.  
   - **Fuel Trims**: High/low fuel trim detection.  
   - **Timing Crashes**: Summarize how many times IGN1 crashed (above 20 mph).  

4. **Log Length Check**  
   - If throttle was > 90% but the mph range is < 65, print a top-level **log length warning**.  
   - Urges users to do a 0–100 mph or 1/4-mile run.  

5. **Multi-Axis Plot**  
   - Use multiple dropdowns to select parameters for up to 4 separate y-axes.  
   - Each axis can be **linear** or **log** scale.  
   - Hover tooltips show values at each time step.

6. **Local Webserver**  
   - The script launches a Dash server at `http://127.0.0.1:8050`.  
   - If not running via SSH, it automatically opens your browser.

---

## **Installation**

1. **Clone this repository** (or download the files).

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
3. pip install -r requirements.txt
