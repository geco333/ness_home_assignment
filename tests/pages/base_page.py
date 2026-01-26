from typing import Optional, List
from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError
from config.settings import Settings


class BasePage:
    """Base page class with common methods using Playwright"""
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = Settings.BASE_URL
    
    def navigate_to(self, url: str = ""):
        """Navigate to a URL"""
        
        full_url = f"{self.base_url}/{url}" if url else self.base_url
        
        self.page.goto(full_url, wait_until="networkidle")
    
    def find_element(self, selector: str) -> Locator:
        """Find an element by selector"""

        return self.page.locator(selector)
    
    def click_element(self, selector: str):
        """Click an element"""

        self.page.locator(selector).click()
    
    def fill_input(self, selector: str, text: str):
        """Fill an input field"""

        self.page.locator(selector).fill(text)
    
    def type_text(self, selector: str, text: str):
        """Type text into an element (with keyboard simulation)"""

        self.page.locator(selector).type(text)
    
    def get_text(self, selector: str) -> str:
        """Get text from an element"""

        return self.page.locator(selector).inner_text()
    
    def is_element_present(self, selector: str, timeout: Optional[int] = None) -> bool:
        """Check if element is present"""

        try:
            timeout_ms = timeout * 1000 if timeout else Settings.ACTION_TIMEOUT
            self.page.locator(selector).wait_for(state="visible", timeout=timeout_ms)
            
            return True
        except PlaywrightTimeoutError:
            return False
    
    def is_element_visible(self, selector: str) -> bool:
        """Check if element is visible"""

        return self.page.locator(selector).is_visible()
    
    def wait_for_element(self, selector: str, timeout: Optional[int] = None):
        """Wait for element to be visible"""

        timeout_ms = timeout * 1000 if timeout else Settings.ACTION_TIMEOUT
        self.page.locator(selector).wait_for(state="visible", timeout=timeout_ms)
    
    def get_title(self) -> str:
        """Get page title"""

        return self.page.title()
    
    def get_url(self) -> str:
        """Get current URL"""

        return self.page.url
    
    def take_screenshot(self, path: Optional[str] = None):
        """Take a screenshot"""

        if path is None:
            path = f"reports/screenshot_{self.page.url.split('/')[-1]}.png"

        self.page.screenshot(path=path)

        return path
    
    def find_element_with_fallback(self, *selectors: str, timeout: Optional[int] = None) -> Locator:
        """
        Find element with fallback mechanism: tries all provided selectors until one succeeds
        
        Args:
            *selectors: Variable number of selector strings. Can be any selector type 
                       (XPath, CSS, text, etc.). Can also pass a single list which will be unpacked.
            timeout: Timeout in milliseconds (default from settings)
            
        Returns:
            Locator: The found element locator (first successful selector)
            
        Raises:
            TimeoutError: If none of the selectors find the element
            ValueError: If no selectors are provided
            
        Examples:
            # Two selectors (XPath and CSS)
            element = self.find_element_with_fallback(xpath, css_selector)
            
            # Multiple selectors (XPath, CSS, and text selector)
            element = self.find_element_with_fallback(xpath, css_selector, "text=Search")
            
            # Single list of selectors (unpacked)
            selectors = [xpath, css_selector, "text=Click here"]
            element = self.find_element_with_fallback(*selectors)
            
            # Any number of selectors - tries each until one succeeds
            element = self.find_element_with_fallback(
                "//div[@id='element']",
                "div#element",
                "text=Element Text",
                "[data-testid='element']"
            )
        """
        if not selectors:
            raise ValueError("At least one selector must be provided")
        
        # Flatten selectors if a list is passed as first argument
        selector_list: List[str] = []
        if len(selectors) == 1 and isinstance(selectors[0], list):
            selector_list = list(selectors[0])
        else:
            # Convert tuple to list, ensuring all items are strings
            selector_list = [str(sel) for sel in selectors]
        
        if not selector_list:
            raise ValueError("At least one selector must be provided")
        
        timeout_ms = timeout if timeout else Settings.ACTION_TIMEOUT
        errors = []
        
        # Try each selector in order until one succeeds
        for i, selector in enumerate(selector_list):
            try:
                locator = self.page.locator(selector)
                locator.wait_for(state="visible", timeout=timeout_ms)
                return locator
            except PlaywrightTimeoutError as e:
                errors.append(f"Selector {i+1} ('{selector}'): {str(e)}")
                continue
        
        # If all selectors failed, raise an error with details
        error_message = f"Element not found with any of {len(selector_list)} selector(s). Errors:\n"
        error_message += "\n".join(f"  - {error}" for error in errors)

        raise TimeoutError(error_message)
    
    def is_element_present_with_fallback(self, *selectors: str, timeout: Optional[int] = None) -> bool:
        """
        Check if element is present with fallback mechanism
        
        Args:
            *selectors: Variable number of selector strings or a single list of selectors.
                       Can be any selector type (XPath, CSS, text, etc.)
            timeout: Timeout in milliseconds (default from settings)
            
        Returns:
            bool: True if element is found with any selector, False otherwise
        """
        try:
            self.find_element_with_fallback(*selectors, timeout=timeout)
            return True
        except (TimeoutError, PlaywrightTimeoutError, ValueError):
            return False