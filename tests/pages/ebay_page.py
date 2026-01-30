import os
import random
import re
from datetime import datetime

from playwright.sync_api import Page

from tests.pages.base_page import BasePage


class EbayPage(BasePage):
    """Page Object Model for eBay.com homepage"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.base_url = "https://www.ebay.com"

    # ==================== SEARCH ELEMENTS ====================

    # Search input box
    SEARCH_INPUT_XPATH = "//input[@id='gh-ac']"
    SEARCH_INPUT_CSS = "input#gh-ac"

    # Search button
    SEARCH_BUTTON_XPATH = "//*[@id='gh-search-btn']"
    SEARCH_BUTTON_CSS = "#gh-search-btn"

    # Advanced search link
    ADVANCED_SEARCH_XPATH = "//a[@id='gh-as-a']"
    ADVANCED_SEARCH_CSS = "a#gh-as-a"

    # Category dropdown
    CATEGORY_DROPDOWN_XPATH = "//select[@id='gh-cat']"
    CATEGORY_DROPDOWN_CSS = "select#gh-cat"

    # ==================== NAVIGATION ELEMENTS ====================

    # eBay logo
    LOGO_XPATH = "//a[@id='gh-la']"
    LOGO_CSS = "a#gh-la"

    # Daily Deals link
    DAILY_DEALS_XPATH = "//a[contains(@href, 'deals') and contains(text(), 'Daily Deals')]"
    DAILY_DEALS_CSS = "a[href*='deals']"

    # Sell link
    SELL_LINK_XPATH = "//a[contains(@href, 'sell') and contains(text(), 'Sell')]"
    SELL_LINK_CSS = "a[href*='sell']"

    # Help & Contact link
    HELP_CONTACT_XPATH = "//a[contains(@href, 'help') and contains(text(), 'Help')]"
    HELP_CONTACT_CSS = "a[href*='help']"

    # ==================== USER ACCOUNT ELEMENTS ====================

    # Sign in link
    SIGN_IN_XPATH = "//a[contains(@href, 'signin') or contains(text(), 'Sign in')]"
    SIGN_IN_CSS = "a[href*='signin'], .gh-eb-li-ghr"

    # Register link
    REGISTER_XPATH = "//a[contains(@href, 'register') or contains(text(), 'Register')]"
    REGISTER_CSS = "a[href*='register']"

    # My eBay dropdown
    MY_EBAY_DROPDOWN_XPATH = "//a[@id='gh-eb-My']"
    MY_EBAY_DROPDOWN_CSS = "a#gh-eb-My"

    # Summary link in My eBay
    SUMMARY_XPATH = "//a[contains(@href, 'summary') and contains(text(), 'Summary')]"
    SUMMARY_CSS = "a[href*='summary']"

    # ==================== SHOPPING ELEMENTS ====================

    # Shopping cart icon/link
    CART_XPATH = "//a[@id='gh-cart-i']"
    CART_CSS = "a#gh-cart-i"

    # Cart count badge
    CART_COUNT_XPATH = "//span[@id='gh-cart-n']"
    CART_COUNT_CSS = "span#gh-cart-n"

    # Watchlist link
    WATCHLIST_XPATH = "//a[contains(@href, 'watchlist') or contains(text(), 'Watchlist')]"
    WATCHLIST_CSS = "a[href*='watchlist']"

    # ==================== CATEGORY NAVIGATION ====================

    # All Categories link
    ALL_CATEGORIES_XPATH = "//button[contains(@class, 'gh-menu') or contains(text(), 'All Categories')]"
    ALL_CATEGORIES_CSS = "button.gh-menu, button[aria-label*='Categories']"

    # Electronics category
    ELECTRONICS_XPATH = "//a[contains(@href, 'Electronics') and contains(text(), 'Electronics')]"
    ELECTRONICS_CSS = "a[href*='Electronics']"

    # Fashion category
    FASHION_XPATH = "//a[contains(@href, 'Fashion') and contains(text(), 'Fashion')]"
    FASHION_CSS = "a[href*='Fashion']"

    # Home & Garden category
    HOME_GARDEN_XPATH = "//a[contains(@href, 'Home-Garden') and contains(text(), 'Home & Garden')]"
    HOME_GARDEN_CSS = "a[href*='Home-Garden']"

    # Motors category
    MOTORS_XPATH = "//a[contains(@href, 'Motors') and contains(text(), 'Motors')]"
    MOTORS_CSS = "a[href*='Motors']"

    # ==================== FOOTER ELEMENTS ====================

    # About eBay link
    ABOUT_EBAY_XPATH = "//a[contains(@href, 'about') and contains(text(), 'About')]"
    ABOUT_EBAY_CSS = "a[href*='about']"

    # Announcements link
    ANNOUNCEMENTS_XPATH = "//a[contains(@href, 'announcements')]"
    ANNOUNCEMENTS_CSS = "a[href*='announcements']"

    # Security Center link
    SECURITY_CENTER_XPATH = "//a[contains(@href, 'security')]"
    SECURITY_CENTER_CSS = "a[href*='security']"

    # ==================== SEARCH RESULTS ELEMENTS ====================

    # Search results count
    RESULTS_COUNT_XPATH = "//h1[contains(@class, 'srp-controls__count-heading')]"
    RESULTS_COUNT_CSS = "h1.srp-controls__count-heading"

    # Sort dropdown
    SORT_DROPDOWN_XPATH = "//select[@id='s0-1-17-6-5-4[0]-72[1]-_salic']"
    SORT_DROPDOWN_CSS = "select#s0-1-17-6-5-4\\[0\\]-72\\[1\\]-_salic"

    # Price filter input (max price)
    PRICE_FILTER_MAX_XPATH = "//*[@id='s0-2-54-0-9-8-0-1-2-0-4-1-26[4]-@textrange-@endParamValue-textbox']"
    PRICE_FILTER_MAX_CSS = "#s0-2-54-0-9-8-0-1-2-0-4-1-26\[4\]-\@textrange-\@endParamValue-textbox"

    # Price filter apply button
    PRICE_FILTER_APPLY_XPATH = "//*[@id='x-refine__group__4']/div[1]/div[2]/div[1]/div/div[3]/button"
    PRICE_FILTER_APPLY_CSS = "#x-refine__group__4 > div.x-refine__price > div:nth-child(2) > div.x-item > div > div.x-textrange__button > button"

    # Search result items container
    SEARCH_RESULT_ITEMS_XPATH = "//*[@id='srp-river-results']/ul/li"
    SEARCH_RESULT_ITEMS_CSS = "#srp-river-results > ul > li"

    # Individual item price XPath (various formats)
    ITEM_PRICE_XPATH = "div/div[2]/div[2]/div/div/span"
    ITEM_URL_XPATH = "div/div[2]/div/a"

    # Next page button
    NEXT_PAGE_XPATH = "//a[@aria-label='Go to next search page'] | //a[contains(@class, 'pagination__next')] | //a[contains(text(), 'Next')] | //button[contains(@aria-label, 'next')]"
    NEXT_PAGE_CSS = "a[aria-label*='next'], a.pagination__next, a:has-text('Next')"

    # ==================== PRODUCT PAGE ELEMENTS ====================

    # Add to cart button
    ADD_TO_CART_XPATH = "//a[contains(@id, 'isCartBtn')] | //a[contains(text(), 'Add to cart')] | //button[contains(text(), 'Add to cart')] | //span[contains(text(), 'Add to cart')]/parent::a | //a[contains(@aria-label, 'Add to cart')]"
    ADD_TO_CART_CSS = "a#isCartBtn, a:has-text('Add to cart'), button:has-text('Add to cart')"

    # Color selector/options
    COLOR_SELECTOR_XPATH = "//select[contains(@name, 'Color') or contains(@id, 'Color')] | //select[contains(@aria-label, 'Color')] | //div[contains(@class, 'color')]//select | //select[contains(@name, 'color')]"
    COLOR_OPTIONS_XPATH = "//select[contains(@name, 'Color') or contains(@id, 'Color')]//option | //select[contains(@aria-label, 'Color')]//option | //div[contains(@class, 'color')]//select//option"

    # Size selector/options
    SIZE_SELECTOR_XPATH = "//select[contains(@name, 'Size') or contains(@id, 'Size')] | //select[contains(@aria-label, 'Size')] | //div[contains(@class, 'size')]//select | //select[contains(@name, 'size')]"
    SIZE_OPTIONS_XPATH = "//select[contains(@name, 'Size') or contains(@id, 'Size')]//option | //select[contains(@aria-label, 'Size')]//option | //div[contains(@class, 'size')]//select//option"

    # Generic option selectors (for any dropdown/select)
    OPTION_SELECTORS_XPATH = "//select[contains(@name, 'Color') or contains(@name, 'Size') or contains(@name, 'color') or contains(@name, 'size')] | //select[contains(@id, 'Color') or contains(@id, 'Size')]"

    # ==================== CART PAGE ELEMENTS ====================

    # Cart total/subtotal
    CART_TOTAL_XPATH = "//span[contains(@class, 'cart-summary-total')] | //span[contains(@id, 'cart-total')] | //div[contains(@class, 'cart-total')]//span[contains(text(), '$')] | //span[contains(@class, 'total') and contains(text(), '$')] | //div[contains(@class, 'summary')]//span[contains(text(), '$')]"
    CART_TOTAL_CSS = ".cart-summary-total, #cart-total, .cart-total span, .total"

    # Cart subtotal (alternative selector)
    CART_SUBTOTAL_XPATH = "//span[contains(@class, 'subtotal')] | //div[contains(@class, 'subtotal')]//span[contains(text(), '$')] | //span[contains(@id, 'subtotal')]"
    CART_SUBTOTAL_CSS = ".subtotal, #subtotal"

    # ==================== HELPER METHODS ====================

    def search_for_item(self, search_term: str):
        """Search for an item on eBay with fallback mechanism"""
        # Find search input with fallback
        search_input = self.find_element_with_fallback(
            self.SEARCH_INPUT_XPATH,
            self.SEARCH_INPUT_CSS
        )
        search_input.fill(search_term)

        # Find and click search button with fallback
        search_button = self.find_element_with_fallback(
            self.SEARCH_BUTTON_XPATH,
            self.SEARCH_BUTTON_CSS
        )
        search_button.click()

    def click_sign_in(self):
        """Click the Sign in link with fallback mechanism"""
        sign_in_element = self.find_element_with_fallback(
            self.SIGN_IN_XPATH,
            self.SIGN_IN_CSS
        )
        sign_in_element.click()

    def click_cart(self):
        """Click the shopping cart with fallback mechanism"""
        cart_element = self.find_element_with_fallback(
            self.CART_XPATH,
            self.CART_CSS
        )
        cart_element.click()

    def get_cart_count(self) -> str:
        """Get the number of items in cart with fallback mechanism"""
        cart_count_element = self.find_element_with_fallback(
            self.CART_COUNT_XPATH,
            self.CART_COUNT_CSS,
            timeout=2000  # Shorter timeout for optional element
        )
        return cart_count_element.inner_text()

    def click_daily_deals(self):
        """Click Daily Deals link with fallback mechanism"""
        daily_deals_element = self.find_element_with_fallback(
            self.DAILY_DEALS_XPATH,
            self.DAILY_DEALS_CSS
        )
        daily_deals_element.click()

    def click_sell_link(self):
        """Click Sell link with fallback mechanism"""
        sell_element = self.find_element_with_fallback(
            self.SELL_LINK_XPATH,
            self.SELL_LINK_CSS
        )
        sell_element.click()

    def select_category(self, category_name: str):
        """Select a category from dropdown with fallback mechanism"""
        category_dropdown = self.find_element_with_fallback(
            self.CATEGORY_DROPDOWN_XPATH,
            self.CATEGORY_DROPDOWN_CSS
        )
        category_dropdown.select_option(label=category_name)

    def click_category(self, category: str):
        """Click a category link with fallback mechanism"""
        category_map = {
            "electronics": (self.ELECTRONICS_XPATH, self.ELECTRONICS_CSS),
            "fashion": (self.FASHION_XPATH, self.FASHION_CSS),
            "home_garden": (self.HOME_GARDEN_XPATH, self.HOME_GARDEN_CSS),
            "motors": (self.MOTORS_XPATH, self.MOTORS_CSS),
        }
        if category.lower() in category_map:
            xpath, css = category_map[category.lower()]
            category_element = self.find_element_with_fallback(xpath, css)
            category_element.click()
        else:
            raise ValueError(f"Unknown category: {category}")

    def click_logo(self):
        """Click eBay logo to go to homepage with fallback mechanism"""
        logo_element = self.find_element_with_fallback(
            self.LOGO_XPATH,
            self.LOGO_CSS
        )
        logo_element.click()

    def click_advanced_search(self):
        """Click Advanced search link with fallback mechanism"""
        advanced_search_element = self.find_element_with_fallback(
            self.ADVANCED_SEARCH_XPATH,
            self.ADVANCED_SEARCH_CSS
        )
        advanced_search_element.click()

    def click_my_ebay(self):
        """Click My eBay dropdown with fallback mechanism"""
        my_ebay_element = self.find_element_with_fallback(
            self.MY_EBAY_DROPDOWN_XPATH,
            self.MY_EBAY_DROPDOWN_CSS
        )
        my_ebay_element.click()

    def click_watchlist(self):
        """Click Watchlist link with fallback mechanism"""
        watchlist_element = self.find_element_with_fallback(
            self.WATCHLIST_XPATH,
            self.WATCHLIST_CSS
        )
        watchlist_element.click()

    def is_search_box_visible(self) -> bool:
        """Check if search box is visible with fallback mechanism"""
        return self.is_element_present_with_fallback(
            self.SEARCH_INPUT_XPATH,
            self.SEARCH_INPUT_CSS,
            timeout=2000
        )

    def is_cart_visible(self) -> bool:
        """Check if cart is visible with fallback mechanism"""
        return self.is_element_present_with_fallback(
            self.CART_XPATH,
            self.CART_CSS,
            timeout=2000
        )

    def wait_for_page_load(self):
        """Wait for eBay page to load with fallback mechanism"""
        # Wait for search input with fallback
        try:
            self.find_element_with_fallback(
                self.SEARCH_INPUT_XPATH,
                self.SEARCH_INPUT_CSS
            )
        except (TimeoutError, ValueError):
            pass  # Continue even if search box not immediately found

        # Wait for logo with fallback
        try:
            self.find_element_with_fallback(
                self.LOGO_XPATH,
                self.LOGO_CSS
            )
        except (TimeoutError, ValueError):
            pass  # Continue even if logo not immediately found

    def search_items_by_name_under_price(self, query: str, max_price: float, limit: int) -> list:
        """
        Search eBay with price filtering and pagination.

        Args:
            query: Search query string
            max_price: Maximum price filter (items must be <= this price)
            limit: Minimum number of items to retrieve

        Returns:
            list: List of URLs for found items (at least 'limit' items, or fewer if not enough found)
        """

        # Helper function to extract price from text
        def extract_price(price_text: str) -> float:
            """Extract numeric price from text like '$19.99' or '$19.99 to $29.99'"""
            if not price_text:
                return float('inf')

            # Remove currency symbols and extract first number
            price_text = price_text.replace('$', '').replace(',', '').strip()

            # Handle price ranges (take the first/lower price)
            if 'to' in price_text.lower():
                price_text = price_text.split('to')[0].strip()

            # Extract first number
            match = re.search(r'(\d+\.?\d*)', price_text)

            if match:
                return float(match.group(1))

            return float('inf')

        # Navigate to eBay landing page
        self.navigate_to()
        self.wait_for_page_load()

        # Perform the search
        self.search_for_item(query)
        # Use "load" instead of "networkidle" to avoid hanging on sites with ongoing requests (e.g. eBay)
        self.page.wait_for_load_state("load", timeout=15000)

        # Look for max price filter input (with timeout to avoid hanging if element missing)
        try:
            price_filter_input = self.page.locator(self.PRICE_FILTER_MAX_XPATH).first
            # Short timeout so we don't hang if selector is wrong or element not present
            price_filter_input.wait_for(state="visible", timeout=8000)
            price_filter_input.scroll_into_view_if_needed(timeout=5000)
            self.page.wait_for_timeout(1500)

            filled_price = str(max_price)
            price_filter_input.press_sequentially(filled_price)

            apply_button = self.page.locator(self.PRICE_FILTER_APPLY_XPATH).first
            apply_button.click(timeout=5000)

            # Wait for filtered results to load (use "load" to avoid hanging on networkidle)
            self.page.wait_for_load_state("load", timeout=15000)
        except Exception as e:
            print(f"Price filter step skipped or failed: {e}. Continuing to collect items.")

        items: list[str] = []
        page_count = 0
        max_pages = 10  # Limit pagination to prevent infinite loops

        # Collect items across pages until we have enough
        while len(items) < limit and page_count < max_pages:
            # Wait for results to be visible
            try:
                self.page.wait_for_selector(self.SEARCH_RESULT_ITEMS_XPATH, timeout=10000)
                result_items = self.page.locator(self.SEARCH_RESULT_ITEMS_XPATH).all()

                if not result_items or len(result_items) == 0:
                    print(f"No result items found on page {page_count + 1}")
                    break

                print(f"Found {len(result_items)} result items on page {page_count + 1}")
            except Exception as e:
                print(f"No search results found on page {page_count + 1}: {e}")
                break

            for i, item in enumerate(result_items, start=1):
                if len(items) >= limit:
                    break

                try:
                    # Extract price
                    price = float('inf')  # Default to infinity if price not found
                    price_element = item.locator(f"//{self.ITEM_PRICE_XPATH}").first

                    try:
                        if price_element.is_visible(timeout=1000):
                            price_text = price_element.inner_text()
                            price = extract_price(price_text)
                    except:
                        # Price element not found or not visible, try alternative methods
                        price = 0

                    # Only include items with price <= max_price
                    if price <= max_price:
                        # Try multiple methods to get URL
                        url = None

                        url = item.locator(f"//{self.ITEM_URL_XPATH}").first.get_attribute('href')

                        # Clean and validate URL
                        if url:
                            # Convert to string and strip whitespace
                            url = str(url).strip()

                            # Skip empty URLs
                            if not url or url == 'None' or url == 'null':
                                continue

                            # Remove query parameters that might cause duplicates (but keep important ones)
                            if '?' in url:
                                # Keep the URL up to the query string for now, or split if needed
                                base_url = url.split('?')[0]
                                
                                # Only use base URL if it contains /itm/
                                if '/itm/' in base_url:
                                    url = base_url

                            # Validate URL contains ebay.com or /itm/
                            if 'ebay.com' not in url and '/itm/' not in url:
                                continue

                            # Avoid duplicates
                            if url and url not in items:
                                items.append(url)
                                print(f"Collected URL {len(items)}/{limit}: {url[:80]}...")
                except Exception as e:
                    # Skip items that can't be processed
                    print(f"Error processing item: {e}")
                    continue

            # Check if we need more items and if there's a next page
            if len(items) < limit:
                try:
                    next_button = self.page.locator(self.NEXT_PAGE_XPATH).first

                    if next_button.is_visible(timeout=2000) and next_button.is_enabled():
                        next_button.click()
                        self.page.wait_for_load_state("load", timeout=15000)
                        page_count += 1
                    else:
                        # No more pages available
                        break
                except:
                    # No next page button found
                    break
            else:
                # We have enough items
                break

        # Return exactly 'limit' items (or fewer if not enough found)
        return items[:limit]

    def add_item_to_cart(self, product_urls: list[str]) -> None:
        """
        Add multiple items to cart from product URLs.

        Args:
            product_urls: List of product URLs to add to cart

        For each URL:
        - Navigates to product page
        - Takes a screenshot
        - Randomly selects color/size options if available
        - Adds product to cart
        - Returns to main page
        """

        # Create screenshots directory if it doesn't exist
        screenshots_dir = "reports/product_screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)

        for i, url in enumerate(product_urls, 1):
            try:
                # Navigate to product page
                self.page.goto(url)
                self.page.wait_for_load_state("load", timeout=15000)

                # Wait a bit for page to fully render
                self.page.wait_for_timeout(1000)

                # Take screenshot of product page
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"{screenshots_dir}/product_{i}_{timestamp}.png"
                self.page.screenshot(path=screenshot_path)

                # Handle product options (color, size, etc.) - randomly select if available
                try:
                    # Try to find and select color option
                    color_select = self.page.locator(
                        self.COLOR_SELECTOR_XPATH).first
                    if color_select.is_visible(timeout=2000):
                        # Get all color options
                        color_options = color_select.locator(
                            "option:not([value='']):not([disabled])").all()
                        if len(color_options) > 1:  # More than just the default/placeholder
                            # Get option values
                            option_values = []
                            for opt in color_options:
                                value = opt.get_attribute('value')
                                if value and value.strip():
                                    option_values.append(value)

                            if option_values:
                                # Randomly select a color
                                selected_color = random.choice(option_values)
                                color_select.select_option(
                                    value=selected_color)
                                # Wait for page to update
                                self.page.wait_for_timeout(500)
                except:
                    pass  # No color selector available

                try:
                    # Try to find and select size option
                    size_select = self.page.locator(
                        self.SIZE_SELECTOR_XPATH).first
                    if size_select.is_visible(timeout=2000):
                        # Get all size options
                        size_options = size_select.locator(
                            "option:not([value='']):not([disabled])").all()
                        if len(size_options) > 1:  # More than just the default/placeholder
                            # Get option values
                            option_values = []
                            for opt in size_options:
                                value = opt.get_attribute('value')
                                if value and value.strip():
                                    option_values.append(value)

                            if option_values:
                                # Randomly select a size
                                selected_size = random.choice(option_values)
                                size_select.select_option(value=selected_size)
                                # Wait for page to update
                                self.page.wait_for_timeout(500)
                except:
                    pass  # No size selector available

                # Try generic option selectors if color/size didn't work
                try:
                    generic_selects = self.page.locator(
                        self.OPTION_SELECTORS_XPATH).all()
                    for select in generic_selects:
                        if select.is_visible(timeout=1000):
                            options = select.locator(
                                "option:not([value='']):not([disabled])").all()
                            if len(options) > 1:
                                option_values = []
                                for opt in options:
                                    value = opt.get_attribute('value')
                                    if value and value.strip():
                                        option_values.append(value)

                                if option_values:
                                    selected_value = random.choice(
                                        option_values)
                                    select.select_option(value=selected_value)
                                    self.page.wait_for_timeout(500)
                except:
                    pass

                # Add item to cart
                try:
                    add_to_cart_button = self.page.locator(
                        self.ADD_TO_CART_XPATH).first
                    if add_to_cart_button.is_visible(timeout=3000):
                        add_to_cart_button.click()
                        # Wait for cart action to complete
                        self.page.wait_for_timeout(2000)
                except Exception as e:
                    # If add to cart fails, log but continue
                    print(f"Failed to add item {i} to cart: {e}")

                # Return to main page (eBay homepage)
                self.navigate_to()
                self.wait_for_page_load()

            except Exception as e:
                # If processing a product fails, log and continue with next item
                print(f"Error processing product {i} (URL: {url}): {e}")
                # Try to return to main page even if there was an error
                try:
                    self.navigate_to()
                    self.wait_for_page_load()
                except:
                    pass
                continue

    def assert_cart_total_not_exceeds(self, budget_per_item: float, item_count: int) -> None:
        """
        Open cart and assert that the total cost does not exceed item_count * budget_per_item.
        
        Args:
            budget_per_item: Maximum budget allowed per item
            item_count: Number of items expected in cart
            
        Raises:
            AssertionError: If cart total exceeds the budget limit
        """

        # Open the cart
        self.click_cart()
        self.page.wait_for_load_state("load", timeout=15000)

        # Wait a bit for cart page to fully load
        self.page.wait_for_timeout(1000)

        # Take screenshot of cart page
        screenshots_dir = "reports/product_screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"{screenshots_dir}/cart_{timestamp}.png"
        self.page.screenshot(path=screenshot_path)

        # Calculate maximum allowed total
        max_total = item_count * budget_per_item

        # Try to find cart total using multiple selectors
        cart_total = None
        cart_total_text = None

        # Try cart total selector first
        try:
            total_element = self.page.locator(self.CART_TOTAL_XPATH).first

            if total_element.is_visible(timeout=3000):
                cart_total_text = total_element.inner_text()
        except:
            pass

        # If not found, try subtotal selector
        if not cart_total_text:
            try:
                subtotal_element = self.page.locator(self.CART_SUBTOTAL_XPATH).first
                if subtotal_element.is_visible(timeout=3000):
                    cart_total_text = subtotal_element.inner_text()
            except:
                pass

        # If still not found, try to find any element containing total/subtotal text
        if not cart_total_text:
            try:
                # Look for common cart total patterns
                total_patterns = [
                    "//span[contains(text(), 'Total') and contains(text(), '$')]",
                    "//span[contains(text(), 'Subtotal') and contains(text(), '$')]",
                    "//div[contains(text(), 'Total') and contains(text(), '$')]",
                    "//*[contains(@class, 'total') and contains(text(), '$')]",
                ]

                for pattern in total_patterns:
                    try:
                        element = self.page.locator(pattern).first
                        if element.is_visible(timeout=1000):
                            cart_total_text = element.inner_text()
                            break
                    except:
                        continue
            except:
                pass

        # Extract numeric value from cart total text
        if cart_total_text:
            # Remove currency symbols and extract number
            total_text = cart_total_text.replace('$', '').replace(',', '').strip()

            # Extract first number (handles cases like "Total: $123.45")
            match = re.search(r'(\d+\.?\d*)', total_text)

            if match:
                cart_total = float(match.group(1))

        # Assert that cart total does not exceed budget
        if cart_total is None:
            raise AssertionError(
                f"Could not find cart total on cart page. "
                f"Expected maximum total: ${max_total:.2f} (${budget_per_item:.2f} × {item_count} items)"
            )

        assert cart_total <= max_total, (
            f"Cart total ${cart_total:.2f} exceeds maximum allowed budget of ${max_total:.2f} "
            f"(${budget_per_item:.2f} per item × {item_count} items)"
        )
