"""
Browser Grid Configuration
Defines all browser types and versions to run tests against
"""

# Available browsers in Playwright
BROWSERS = ["chromium", "firefox", "webkit"]

# Browser-specific configurations
BROWSER_CONFIGS = {
    "chromium": {
        "name": "Chromium",
        "channel": None,  # Can be "chrome", "msedge", "chrome-beta", etc.
        "versions": ["default"],  # Playwright manages versions automatically
    },
    "firefox": {
        "name": "Firefox",
        "channel": None,
        "versions": ["default"],
    },
    "webkit": {
        "name": "WebKit",
        "channel": None,
        "versions": ["default"],
    },
}

# Grid execution modes
GRID_MODES = {
    "all": BROWSERS,  # Run on all browsers
    "chromium": ["chromium"],
    "firefox": ["firefox"],
    "webkit": ["webkit"],
    "desktop": ["chromium", "firefox"],  # Desktop browsers
    "mobile": ["webkit"],  # Mobile browser
}

def get_browsers_for_mode(mode: str = "all") -> list:
    """Get list of browsers for a given grid mode"""
    return GRID_MODES.get(mode.lower(), GRID_MODES["all"])
