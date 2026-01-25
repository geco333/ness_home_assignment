import pytest
import allure
from playwright.sync_api import Page
from tests.pages.ebay_page import EbayPage


@allure.epic("eBay Tests")
@allure.feature("Homepage Navigation")
@pytest.mark.smoke
def test_ebay_homepage_loads(page: Page, browser_name: str):
    """Test that eBay homepage loads correctly"""
    
    with allure.step(f"Navigate to eBay homepage on {browser_name}"):
        ebay_page = EbayPage(page)
        ebay_page.navigate_to()
        ebay_page.wait_for_page_load()
        
        allure.attach(
            page.url,
            name="Current URL",
            attachment_type=allure.attachment_type.TEXT
        )
    
    with allure.step(f"Verify search box is visible on {browser_name}"):
        # Uses automatic fallback: XPath first, then CSS
        assert ebay_page.is_search_box_visible(), \
            f"Search box should be visible on {browser_name}"
    
    with allure.step(f"Verify cart is visible on {browser_name}"):
        # Uses automatic fallback: XPath first, then CSS
        assert ebay_page.is_cart_visible(), \
            f"Cart should be visible on {browser_name}"


@allure.epic("eBay Tests")
@allure.feature("Search Functionality")
@pytest.mark.regression
def test_ebay_search_functionality(page: Page, browser_name: str):
    """Test eBay search functionality using both CSS and XPath selectors"""
    
    with allure.step(f"Navigate to eBay and search for item on {browser_name}"):
        ebay_page = EbayPage(page)
        ebay_page.navigate_to()
        ebay_page.wait_for_page_load()
        
        # Search with automatic fallback: XPath first, then CSS
        ebay_page.search_for_item("laptop")
        
        # Wait for results page
        page.wait_for_load_state("networkidle")
        
        allure.attach(
            page.url,
            name="Search Results URL",
            attachment_type=allure.attachment_type.TEXT
        )
    
    with allure.step(f"Verify search results page loaded on {browser_name}"):
        # Verify we're on search results page
        assert "laptop" in page.url.lower() or "srp" in page.url.lower(), \
            f"Should be on search results page on {browser_name}"


@allure.epic("eBay Tests")
@allure.feature("Navigation Elements")
@pytest.mark.regression
def test_ebay_navigation_elements(page: Page, browser_name: str):
    """Test that major navigation elements are present and clickable"""
    
    with allure.step(f"Navigate to eBay homepage on {browser_name}"):
        ebay_page = EbayPage(page)
        ebay_page.navigate_to()
        ebay_page.wait_for_page_load()
    
    with allure.step(f"Verify logo is present on {browser_name}"):
        # Uses automatic fallback: XPath first, then CSS
        logo_present = ebay_page.is_element_present_with_fallback(
            ebay_page.LOGO_XPATH,
            ebay_page.LOGO_CSS
        )
        assert logo_present, f"Logo should be present on {browser_name}"
    
    with allure.step(f"Verify Daily Deals link is present on {browser_name}"):
        daily_deals_present = ebay_page.is_element_present_with_fallback(
            ebay_page.DAILY_DEALS_XPATH,
            ebay_page.DAILY_DEALS_CSS
        )
        assert daily_deals_present, f"Daily Deals link should be present on {browser_name}"
    
    with allure.step(f"Verify Sell link is present on {browser_name}"):
        sell_present = ebay_page.is_element_present_with_fallback(
            ebay_page.SELL_LINK_XPATH,
            ebay_page.SELL_LINK_CSS
        )
        assert sell_present, f"Sell link should be present on {browser_name}"


@allure.epic("eBay Tests")
@allure.feature("User Account Elements")
@pytest.mark.smoke
def test_ebay_account_elements(page: Page, browser_name: str):
    """Test that account-related elements are present"""
    
    with allure.step(f"Navigate to eBay homepage on {browser_name}"):
        ebay_page = EbayPage(page)
        ebay_page.navigate_to()
        ebay_page.wait_for_page_load()
    
    with allure.step(f"Verify Sign in link is present on {browser_name}"):
        # Uses automatic fallback: XPath first, then CSS
        sign_in_present = ebay_page.is_element_present_with_fallback(
            ebay_page.SIGN_IN_XPATH,
            ebay_page.SIGN_IN_CSS,
            timeout=5000
        )
        assert sign_in_present, f"Sign in link should be present on {browser_name}"
    
    with allure.step(f"Verify My eBay dropdown is present on {browser_name}"):
        # Uses automatic fallback: XPath first, then CSS
        my_ebay_present = ebay_page.is_element_present_with_fallback(
            ebay_page.MY_EBAY_DROPDOWN_XPATH,
            ebay_page.MY_EBAY_DROPDOWN_CSS,
            timeout=5000
        )
        assert my_ebay_present, f"My eBay dropdown should be present on {browser_name}"
