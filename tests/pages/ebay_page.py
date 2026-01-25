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
    SEARCH_BUTTON_XPATH = "//input[@id='gh-btn']"
    SEARCH_BUTTON_CSS = "input#gh-btn"
    
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
