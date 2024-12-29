<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>User Manual: JB4/Lap3 HTML Log Analyzer</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 2em auto;
      max-width: 800px;
      line-height: 1.5;
    }
    h1, h2, h3 {
      margin-top: 1.2em;
      margin-bottom: 0.6em;
    }
    code, pre {
      background-color: #f8f8f8;
      padding: 0.2em 0.4em;
      font-size: 0.9em;
    }
    hr {
      margin: 2em 0;
    }
  </style>
</head>
<body>

<h1>User Manual: JB4/Lap3 HTML Log Analyzer</h1>

<p>
  This page is an all-in-one tool for analyzing JB4/Lap3 logs by:
</p>
<ul>
  <li>Parsing a CSV file (entirely client-side—no server required).</li>
  <li>Running “check” functions to look for potential issues in the data (timing deviations, fuel trims, etc.).</li>
  <li>Generating text-based reports summarizing warnings or anomalies.</li>
  <li>Plotting multiple columns of data on a single Plotly chart with up to four Y-axes.</li>
</ul>

<hr/>

<h2>1. Opening the Analyzer</h2>
<ol>
  <li>
    <strong>Double-Click the <code>index.html</code> File</strong>:  
    Simply open it in any modern browser (Chrome, Firefox, etc.).<br>
    Alternatively, if you have it hosted online (e.g., via GitHub Pages), navigate to that public URL in your browser.
  </li>
  <li>
    <strong>Check for Plotly</strong>:  
    Ensure Plotly.js and any other scripts load successfully. If something fails, open your browser’s DevTools console to check for errors.
  </li>
  <li>
    <strong>Familiarize Yourself with the Layout</strong>:  
    After loading, you’ll see:
    <ul>
      <li>A dashed “Drag/Drop or Click to Select CSV” box for uploading logs.</li>
      <li>4Cyl/6Cyl sensitivity fields and a “Re-Scan Log” button.</li>
      <li>Two text regions for the “Log Length Warning” and “Report Output.”</li>
      <li>A “Plotly Multi-Axis Controls” section with four dropdowns (Axis1–Axis4) and scale toggles (linear or log).</li>
      <li>A large chart area at the bottom.</li>
    </ul>
  </li>
</ol>

<hr/>

<h2>2. Uploading Your CSV File</h2>

<p>The page is designed to work with JB4/Lap3 logs that have roughly 37 columns, including <em>timestamp</em>, <em>rpm</em>, <em>boost</em>, etc. When you upload the file, it attempts to parse those columns automatically.</p>

<h3>2.1 CSV Format</h3>
<ul>
  <li>The script reads lines 5 onward as data rows (because some JB4 logs have 5 lines of header info).</li>
  <li>If your file is too short (fewer than 10 lines total), you’ll see an error.</li>
  <li>You can adapt the parsing in the code if your CSV differs significantly from the default JB4 format.</li>
</ul>

<h3>2.2 How to Upload</h3>
<ul>
  <li><strong>Drag &amp; Drop:</strong> Drag the CSV file from your file explorer onto the dashed area.</li>
  <li><strong>Click to Browse:</strong> Click inside the dashed area to open a file dialog, then select your CSV.</li>
</ul>

<p>Once loaded, it parses your CSV into an array of objects (each column is turned into a numeric field, if possible).</p>

<hr/>

<h2>3. Checking the Log</h2>

<h3>3.1 Automatic Check</h3>
<ul>
  <li>As soon as a valid CSV is parsed, the script <em>immediately</em> runs a series of “check” functions.</li>
  <li>These checks look for things like timing deviation, high fuel trims, HPFP issues, meth flow problems, etc.</li>
  <li>The <strong>“Report Output”</strong> box will populate with textual findings. Sections that are empty or have no findings may be omitted or appear only as headers.</li>
  <li>A <strong>“Log Length Warning”</strong> might appear in the red-bordered box, telling you whether your log covers a sufficient speed range (e.g., 0–100 mph) at wide-open throttle.</li>
</ul>

<h3>3.2 Sensitivity Controls</h3>
<p>
  You’ll see two fields for controlling the detection threshold:
</p>
<ul>
  <li><strong>4Cyl Sensitivity</strong></li>
  <li><strong>6Cyl Sensitivity</strong></li>
</ul>
<p>
  These are used for the ignition checks. If you get too many false positives, increase the sensitivity; if you want to catch smaller deviations, decrease it. After changing the values, click <strong>“Re-Scan Log”</strong> to re-run all checks with the new thresholds.
</p>

<h3>3.3 Report Sections</h3>
<ul>
  <li><strong>IAT</strong> – Looks for high IATs during wide-open throttle, indicating potential heat soak.</li>
  <li><strong>HPFP Report</strong> – Alerts if high-pressure fuel pump (HPFP) pressure is too low under load.</li>
  <li><strong>Meth Flow Report</strong> – Checks for insufficient meth flow if meth injection is active.</li>
  <li><strong>Boost Deviations</strong> – Compares <em>boost</em> vs. <em>boost2</em> for large discrepancies.</li>
  <li><strong>Fuel Trims</strong> – Warns about big differences between <em>trims_val</em> and <em>trims2</em> or extremely high/low trim levels.</li>
  <li><strong>Timing Crash</strong> – Logs times when timing may drop to zero under load.</li>
  <li><strong>Throttle Closure</strong> – Notes if throttle closes when pedal is still near 100%.</li>
  <li><strong>Timing Deviations</strong> – Reports if one or more cylinders deviate significantly from the expected ignition timing threshold.</li>
</ul>

<p>These sections are sorted so non-empty findings appear first, making it easier to see real issues at a glance.</p>

<hr/>

<h2>4. Plotting Data</h2>
<p>The bottom portion of the page lets you visualize the CSV data with up to four separate Y-axes.</p>

<h3>4.1 Axis Dropdowns</h3>
<p>
  Each axis (Axis1–Axis4) has a dropdown listing the CSV columns (except <em>timestamp</em>). 
  Select multiple columns to plot on the same axis. For example:
</p>
<ul>
  <li>Axis1: <em>rpm</em> + <em>pedal</em></li>
  <li>Axis2: <em>boost</em> + <em>boost2</em></li>
  <li>Axis3: <em>meth</em></li>
  <li>Axis4: <em>iat</em></li>
</ul>
<p>The chart updates automatically when you change the dropdown selections.</p>

<h3>4.2 Scale (Linear or Log)</h3>
<p>
  Under each dropdown are radio buttons to toggle <strong>Linear</strong> or <strong>Log</strong> scale on that axis. 
  Choose <em>Log</em> if your data covers large ranges.
</p>

<h3>4.3 Hover &amp; Interact</h3>
<ul>
  <li><strong>Hover</strong> your mouse over the chart to see all traces’ Y-values at that timestamp. The “Hover Status” box will show them in text form.</li>
  <li><strong>Zoom &amp; Pan</strong> using Plotly’s built-in toolbar at the top-right of the chart.</li>
  <li><strong>Export</strong> the chart as an image (PNG, JPEG, etc.) from the Plotly toolbar.</li>
</ul>

<hr/>

<h2>5. Re-Scanning &amp; Updating</h2>
<p>
  After you upload a CSV, if you want to adjust sensitivity or re-check the data, click <strong>“Re-Scan Log”</strong>. 
  If you upload a new CSV, it replaces the old data, re-runs checks automatically, and refreshes the axis dropdowns.
</p>

<hr/>

<h2>6. Common Issues &amp; Tips</h2>
<ul>
  <li><strong>CSV Format Mismatch</strong>: If your log has columns in a different order or fewer columns, you might see unexpected results or zeros.</li>
  <li><strong>CORS Errors</strong>: Some browsers may block file references. Typically, drag/drop should work fine. If not, try hosting the file or using a local HTTP server.</li>
  <li><strong>Performance</strong>: For very large CSVs, parsing might take a few seconds. Watch the console if it freezes or errors out.</li>
  <li><strong>Saving Your Output</strong>: The “Report Output” is displayed in the browser. If you need to share it, copy/paste into a text document.</li>
</ul>

<hr/>

<h2>7. Advanced Use</h2>
<ul>
  <li><strong>Modifying Check Functions</strong>: All checks are in the same HTML/JS file. You can freely edit them to match your own criteria or columns.</li>
  <li><strong>Hosting Options</strong>: To share with others, host the HTML on GitHub Pages, Netlify, or any static site host. They just need to open the link.</li>
  <li><strong>Embedding / iFrames</strong>: If you use a site builder like Wix, you can embed this HTML via an iFrame.</li>
</ul>

<hr/>

<h2>Summary</h2>
<p>
  Using the HTML-based JB4/Lap3 Log Analyzer is straightforward:
</p>
<ol>
  <li><strong>Open</strong> the page in your browser.</li>
  <li><strong>Upload</strong> (or drag/drop) your CSV.</li>
  <li><strong>Check</strong> warnings in the “Report Output.”</li>
  <li><strong>Tune</strong> sensitivity (4Cyl/6Cyl) and re-scan.</li>
  <li><strong>Plot</strong> columns on up to four Y-axes to visualize the data.</li>
</ol>
<p>
  This tool helps quickly spot potential issues in JB4/Lap3 logs—heat soak, fuel trim problems, timing crashes, and more—without needing a server or a standalone Python environment.
</p>

</body>
</html>
