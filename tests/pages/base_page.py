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
        
        if self.page.url != self.base_url:
            self.page.goto(full_url, wait_until="load")
            
            # Check for modal popup and dismiss it if present
            self._dismiss_modal_if_present()
    
    def _dismiss_modal_if_present(self):
        """Check for and dismiss modal popup on page load with robust retry logic"""
        try:
            # Wait a bit for any dynamic content to load
            self.page.wait_for_timeout(3000)

            # Take a screenshot to debug what's on the page
            debug_screenshot = "reports/debug_modal_check.png"
            self.page.screenshot(path=debug_screenshot, full_page=True)
            print(f"Debug screenshot saved to: {debug_screenshot}")

            # Try multiple strategies to dismiss modals
            modal_dismissed = False

            # Strategy 1: Try specific selectors for common modal patterns
            modal_selectors = [
                '//*[@id="mainContent"]/div/div/form/button',  # Original specific selector
                '//button[contains(@class, "modal") or contains(@class, "popup") or contains(@class, "dialog")]',
                '//button[contains(text(), "Continue") or contains(text(), "Accept") or contains(text(), "Close") or contains(text(), "OK") or contains(text(), "Yes")]',
                '//div[@role="dialog"]//button',
                '//div[contains(@class, "modal")]//button',
                '//div[contains(@class, "popup")]//button',
                '//button[contains(@aria-label, "Close") or contains(@aria-label, "Dismiss")]',
                '//button[@type="button" and contains(@class, "btn")]',
                '//a[contains(@class, "close") or contains(@class, "dismiss")]',
                '//span[contains(@class, "close") or contains(@class, "dismiss")]',
                '//div[contains(@class, "overlay")]//button',
                '//div[contains(@id, "modal")]//button',
                '//div[contains(@id, "popup")]//button',
                '//button[contains(@class, "close") or contains(@class, "x-close")]',
                '//button[@aria-label="Close"]',
                '//button[@data-testid="close-button"]'
            ]

            # Try each selector with retry logic
            for selector in modal_selectors:
                for attempt in range(2):  # Try each selector up to 2 times
                    try:
                        modal_button = self.page.locator(selector).first  # Use .first to avoid strict mode violations
                        if modal_button.is_visible(timeout=2000):
                            print(f"Modal popup detected with selector '{selector}' (attempt {attempt + 1}), dismissing...")

                            # Get button text for debugging
                            try:
                                button_text = modal_button.inner_text(timeout=1000)
                                print(f"Button text: '{button_text}'")
                            except:
                                print("Could not get button text")

                            # Try to click the button
                            modal_button.click(timeout=5000)

                            # Wait for modal to close
                            self.page.wait_for_timeout(2000)

                            # Check if modal is gone by verifying the button is no longer visible
                            if not modal_button.is_visible(timeout=1000):
                                print("Modal popup successfully dismissed")
                                modal_dismissed = True
                                break
                            else:
                                print(f"Warning: Modal popup may not have closed properly with selector '{selector}'")
                    except Exception as e:
                        print(f"Failed to dismiss modal with selector '{selector}' (attempt {attempt + 1}): {e}")
                        continue

                if modal_dismissed:
                    break

            # Strategy 2: If specific selectors didn't work, try keyboard shortcuts
            if not modal_dismissed:
                print("Trying keyboard shortcuts to dismiss modal...")
                try:
                    # Try Escape key
                    self.page.keyboard.press('Escape')
                    self.page.wait_for_timeout(1000)

                    # Check if any modal is still visible
                    modal_check_selectors = [
                        '//div[@role="dialog"]',
                        '//div[contains(@class, "modal")]',
                        '//div[contains(@class, "popup")]',
                        '//div[contains(@class, "overlay")]'
                    ]

                    modal_still_present = False
                    for check_selector in modal_check_selectors:
                        if self.page.locator(check_selector).is_visible(timeout=1000):
                            modal_still_present = True
                            break

                    if not modal_still_present:
                        print("Modal dismissed successfully with Escape key")
                        modal_dismissed = True

                except Exception as e:
                    print(f"Failed to dismiss modal with keyboard: {e}")

            # Strategy 3: As last resort, try clicking outside the modal area
            if not modal_dismissed:
                print("Trying to click outside modal area...")
                try:
                    # Click on the top-left corner of the page (usually outside modal)
                    self.page.mouse.click(10, 10)
                    self.page.wait_for_timeout(1000)

                    # Check again if modal is gone
                    modal_still_present = False
                    for check_selector in modal_check_selectors:
                        if self.page.locator(check_selector).is_visible(timeout=1000):
                            modal_still_present = True
                            break

                    if not modal_still_present:
                        print("Modal dismissed successfully by clicking outside")
                        modal_dismissed = True

                except Exception as e:
                    print(f"Failed to dismiss modal by clicking outside: {e}")

            if not modal_dismissed:
                print("Warning: No modal popup was found or could be dismissed")
                # Take another screenshot to show what remains
                final_screenshot = "reports/debug_modal_final.png"
                self.page.screenshot(path=final_screenshot, full_page=True)
                print(f"Final state screenshot saved to: {final_screenshot}")
            else:
                print("Modal dismissal process completed successfully")

        except Exception as e:
            print(f"Error during modal dismissal: {e}")
            # Modal not present or couldn't be dismissed, continue normally
            pass
    
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
    
    def find_element_with_fallback(self,
                                   *selectors: str,
                                   timeout: Optional[int] = None,
                                   optional: bool = False) -> Optional[Locator]:
        """
        Find element with fallback mechanism: tries all provided selectors until one succeeds
        
        Args:
            *selectors: Variable number of selector strings. Can be any selector type 
                       (XPath, CSS, text, etc.). Can also pass a single list which will be unpacked.
            timeout: Timeout in milliseconds (default from settings)
            optional: If true, return only the first selector found.
            
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
                locator.first.scroll_into_view_if_needed(timeout=timeout_ms)
                locator.first.wait_for(state="visible", timeout=timeout_ms)
                
                return locator
            except (Exception, PlaywrightTimeoutError) as e:
                if optional:
                    return
                    
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