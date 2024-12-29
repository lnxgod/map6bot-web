# JB4/Lap3 Log Analyzer

A free tool to parse and analyze JB4 or Lap3 CSV logs. It automatically checks for:
- Timing deviations (with adjustable sensitivity for 4-cylinder and 6-cylinder modes).
- HPFP issues, throttle closures, meth flow, boost deviations, high intake temps, etc.
- Log length warnings (for example, ensures you have a 0–100 mph or 1/4-mile run, not just 0–60).
- Summaries of repeated throttle closures, timing crashes, and more.

The tool spins up a local Dash server, automatically opens your default browser (when not run via SSH), and presents a web-based UI. You can then upload your log file, tweak sensitivity settings, re-scan, and view multi-axis Plotly graphs.

## Features

1. CSV Parsing:
   - Skips the first 5 header lines (typical JB4/Lap3 logs).
   - Reads columns like `timestamp`, `rpm`, `throttle`, `ign_1..ign_6`, etc.

2. Adjustable Timing Deviation Sensitivity:
   - 4Cyl Sensitivity replaces the old 3.5 threshold.
   - 6Cyl Sensitivity replaces the old 6.5 threshold.

3. Detailed Checks:
   - HPFP: Warn if under 10 psi at high throttle.
   - Throttle Closure: Summarize if more than 5 closures.
   - Meth Flow: Check if meth is below 90% during WOT.
   - Boost Deviation: Compare Boost1 and Boost2.
   - IAT: Alert if intake temps exceed 118°F under load.
   - Fuel Trims: High/low fuel trim detection.
   - Timing Crashes: Summarize how many times IGN1 crashed (above 20 mph).

4. Log Length Check:
   - If throttle was above 90% but the mph range is below 65, displays a top-level log length warning.
   - Urges users to do a 0–100 mph or 1/4-mile run.

5. Multi-Axis Plot:
   - Allows selecting parameters for up to 4 separate y-axes.
   - Each axis can be set to linear or log scale.
   - Hover over the chart to view data values at each timestamp.

6. Local Webserver:
   - The script launches Dash at http://127.0.0.1:8050.
   - If not running via SSH, it automatically opens your browser.

## Installation

1. Clone or download this repository.
2. Set up a virtual environment (recommended). For example:
   - `python -m venv venv`
   - Activate it: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`

## Usage

1. Run the script: `python my_log_analyzer.py`
   - If running locally (not SSH), it auto-opens your browser at http://127.0.0.1:8050
2. Upload a CSV log (drag-and-drop or click to select the file).
3. Adjust 4Cyl/6Cyl sensitivity values and click Re-Scan Log to analyze with updated thresholds.
4. Review:
   - Top: Warnings if log range is under 65 mph at wide-open throttle.
   - Other checks: IAT, timing crashes, HPFP, etc.
   - Multi-Axis Plot: Scroll to choose parameters for up to 4 y-axes, with linear/log scale. Hover over the chart to see data values.

## Compiling into a Single Executable

If you want a standalone `.exe` (Windows) or single binary (macOS/Linux), use PyInstaller:
1. Install PyInstaller: `pip install pyinstaller`
2. Create the executable: `pyinstaller --onefile --noconsole my_log_analyzer.py`
   - The compiled file goes to `dist/my_log_analyzer` (or `.exe` on Windows).
3. Run `my_log_analyzer.exe`; it starts a local server on port 8050 and opens your browser if local.

## Contributing

- Submit pull requests for bug fixes, new checks, or enhancements.
- Open issues for errors or questions.

## License

This tool is free of charge under the [MIT License](https://opensource.org/licenses/MIT). Refer to the LICENSE file for details.
