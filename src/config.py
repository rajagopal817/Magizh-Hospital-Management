"""
config.py
---------
All application settings in one place.
"""

# ---------------- Names ----------------
COMPANY_NAME = "Makizh Tech"
PROJECT_NAME = "Real-Time Smart Sensor and PPG Data Analytics"
LOGIN_TITLE = COMPANY_NAME + " - " + PROJECT_NAME
APP_TITLE = "Makizh PPG Analytics"
DASHBOARD_TITLE = "KPlot"
BANNER_TEXT = "Makizh Tech serial plotter for PPG data analysis"

# ---------------- Login (demo) ----------------
USERS = {"admin": "admin123"}

# ---------------- Demo devices (shown after "Scan") ----------------
DEMO_DEVICES = [
    "PPG Sensor BT-01 (Bluetooth)",
    "Smart Band PPG-02 (Bluetooth)",
    "Demo (no device)",
]

BAUD_RATES = ["9600", "19200", "38400", "57600", "115200", "230400"]
DEFAULT_BAUD = "115200"

# Signal units -> label shown on the graph's Y axis
SIGNAL_UNITS = {
    "a.u.": "Signal (a.u.)",
    "nA": "Current (nA)",
    "mV": "Voltage (mV)",
}
DEFAULT_UNIT = "nA"

# ---------------- Recording ----------------
SAMPLE_INTERVAL_MS = 10        # one sample every 10 ms (100 samples per second)
MAX_SAMPLES = 100_000          # CSV keeps the latest 100,000 samples
DEFAULT_WINDOW_MS = 10000      # graph shows the last 10 seconds
WINDOW_MIN_MS = 1000
WINDOW_MAX_MS = 60000
WINDOW_STEP_MS = 1000
REFRESH_MS = 100               # graph refresh every 100 ms (smooth on phones)

FOOTER_INFO = ("Input: one number per line  |  CSV retains the latest 100,000 samples  |  "
               "Demo is synthetic, not a clinical measurement")

# ---------------- Button colours (same as the desktop app) ----------------
BUTTON_BG = "#E1E1E1"
BUTTON_FG = "#222222"
GREEN_BG = "#D4EDDA"
GREEN_FG = "#1E5E2E"
RED_BG = "#E8A0A0"
RED_FG = "#5A1010"

# ---------------- Colours ----------------
PRIMARY = "#0F5C7A"      # dark teal (banner, login button)
LIGHT_BG = "#F2F6F8"     # login page background
WHITE = "#FFFFFF"
PLOT_LINE = "#2E6DA4"    # PPG line colour
GRID_MAJOR = "#E3E3E3"
GRID_MINOR = "#F2F2F2"
AXIS = "#9A9A9A"
