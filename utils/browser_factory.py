from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
from config.settings import Settings


class BrowserFactory:
    """Factory class for creating Playwright browser instances"""
    
    @staticmethod
    def create_browser(playwright) -> Browser:
        """Create and return a Browser instance"""
        browser_name = Settings.BROWSER
        
        launch_options = {
            "headless": Settings.HEADLESS,
            "slow_mo": Settings.SLOW_MO,
        }
        
        if browser_name == "chromium":
            browser = playwright.chromium.launch(**launch_options)
        elif browser_name == "firefox":
            browser = playwright.firefox.launch(**launch_options)
        elif browser_name == "webkit":
            browser = playwright.webkit.launch(**launch_options)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}. Use 'chromium', 'firefox', or 'webkit'")
        
        return browser
    
    @staticmethod
    def create_context(browser: Browser) -> BrowserContext:
        """Create and return a BrowserContext instance"""
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,
        )
        context.set_default_navigation_timeout(Settings.NAVIGATION_TIMEOUT)
        context.set_default_timeout(Settings.ACTION_TIMEOUT)
        return context
    
    @staticmethod
    def create_page(context: BrowserContext) -> Page:
        """Create and return a Page instance"""
        return context.new_page()
    
    @staticmethod
    def close_browser(browser: Browser):
        """Safely close the browser"""
        try:
            browser.close()
        except Exception as e:
            print(f"Error closing browser: {e}")
