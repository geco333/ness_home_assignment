"""
Browser Configuration
Reads browser types, versions, and capabilities from JSON file
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

# Default path to browser config JSON file
_DEFAULT_CONFIG_JSON_PATH = Path(__file__).parent / "browser_config.json"

# Available browsers in Playwright
BROWSERS = ["chromium", "firefox", "webkit"]


def load_browser_config(config_path: Optional[str] = None) -> Dict:
    if config_path:
        json_path = Path(config_path)
    else:
        json_path = _DEFAULT_CONFIG_JSON_PATH
    
    if not json_path.exists():
        # Return default configuration if file doesn't exist
        return {
            "browsers": [
                {
                    "name": "chromium",
                    "version": "default",
                    "capabilities": {}
                }
            ]
        }
    
    try:
        with open(json_path, 'r') as f:
            config = json.load(f)
            
        return config
    except (json.JSONDecodeError, IOError) as e:
        raise ValueError(f"Error loading browser configuration from {json_path}: {e}")


def get_browsers_from_config(config_path: Optional[str] = None):
    """
    Get list of browser names from JSON configuration
    
    Args:
        config_path: Optional path to JSON file. If None, uses default.
    
    Returns:
        list: List of browser names to run tests against
    """
    config = load_browser_config(config_path)
    
    if config:
        return config
    
    raise ValueError("No browsers configured")


def get_browser_config(browser_name: str, config_path: Optional[str] = None) -> Optional[Dict]:
    """
    Get configuration for a specific browser from JSON config
    
    Args:
        browser_name: Name of the browser (chromium, firefox, webkit)
        config_path: Optional path to JSON file. If None, uses default.
    
    Returns:
        dict: Browser configuration with name, version, and capabilities, or None if not found
    """
    config = load_browser_config(config_path)
    
    if "browsers" in config:
        for browser_config in config["browsers"]:
            if browser_config.get("name") == browser_name:
                return browser_config
    
    return None


def get_browser_capabilities(browser_name: str, config_path: Optional[str] = None) -> Dict:
    """
    Get capabilities for a specific browser from JSON config
    
    Args:
        browser_name: Name of the browser (chromium, firefox, webkit)
        config_path: Optional path to JSON file. If None, uses default.
    
    Returns:
        dict: Browser capabilities (launch args and context args)
    """
    browser_config = get_browser_config(browser_name, config_path)
    
    if browser_config and "capabilities" in browser_config:
        return browser_config["capabilities"]
    
    return {}
