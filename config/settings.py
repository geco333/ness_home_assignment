import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings"""
    
    # Browser configuration
    BROWSER = os.getenv("BROWSER", "chromium").lower()  # chromium, firefox, webkit
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    SLOW_MO = int(os.getenv("SLOW_MO", "0"))  # Slow down operations by milliseconds
    
    # Timeouts
    NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT", "30000"))  # milliseconds
    ACTION_TIMEOUT = int(os.getenv("ACTION_TIMEOUT", "10000"))  # milliseconds
    
    # Test URLs
    BASE_URL = os.getenv("BASE_URL", "https://example.com")
