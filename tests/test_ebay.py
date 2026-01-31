import allure
import pytest
from playwright.sync_api import Page

from tests.pages.ebay_page import EbayPage


@allure.epic("eBay Tests")
@allure.feature("Homepage Navigation")
@pytest.mark.smoke
def test_ebay_homepage_loads(page: Page, playwright_browser_name):
    """Test that eBay homepage loads correctly"""

    with allure.step(f"Navigate to eBay homepage on {playwright_browser_name}"):
        ebay_page = EbayPage(page)
        ebay_page.navigate_to()
        ebay_page.wait_for_page_load()

        allure.attach(
            page.url,
            name="Current URL",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step(f"Verify search box is visible on {playwright_browser_name}"):
        assert ebay_page.is_search_box_visible(), \
            f"Search box should be visible on {playwright_browser_name}"


@allure.epic("eBay Tests")
@allure.feature("Search with Price Filter")
@pytest.mark.regression
def test_ebay_search_with_price_filter(page: Page, playwright_browser_name: str):
    """Test eBay search with price filtering and pagination"""

    ebay_page = EbayPage(page)
    query = "laptop"
    max_price = 500.0
    limit = 5

    with allure.step(f"Search for '{query}' with max price ${max_price} on {playwright_browser_name}"):
        items = ebay_page.search_items_by_name_under_price(
            query=query,
            max_price=max_price,
            limit=limit
        )

        allure.attach(
            f"Found {len(items)} items matching criteria",
            name="Search Results Count",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step(f"Verify items were returned on {playwright_browser_name}"):
        assert len(items) > 0, \
            f"Should find at least one item for '{query}' with max price ${max_price} on {playwright_browser_name}"

    with allure.step(f"Verify all returned items are URLs on {playwright_browser_name}"):
        for i, url in enumerate(items):
            assert isinstance(url, str), \
                f"Item {i + 1} should be a URL string on {playwright_browser_name}"
            assert url.startswith('http'), \
                f"Item {i + 1} should be a valid URL starting with 'http' on {playwright_browser_name}"

    with allure.step(f"Attach search results summary on {playwright_browser_name}"):
        results_summary = f"Found {len(items)} items for '{query}' with max price ${max_price}:\n\n"

        for i, url in enumerate(items, 1):
            results_summary += f"{i}. {url}\n"

        allure.attach(
            results_summary,
            name="Search Results URLs",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.epic("eBay Tests")
@allure.feature("Add Items to Cart")
@pytest.mark.regression
def test_ebay_add_items_to_cart(page: Page, playwright_browser_name: str):
    """Test adding multiple items to cart from search results"""

    ebay_page = EbayPage(page)
    query = "laptop"
    max_price = 500.0
    limit = 3  # Limit to 3 items for testing
     
    with allure.step(f"Search for '{query}' with max price ${max_price} on {playwright_browser_name}"):
        product_urls = ebay_page.search_items_by_name_under_price(
            query=query,
            max_price=max_price,
            limit=limit
        )

        allure.attach(
            f"Found {len(product_urls)} product URLs to add to cart",
            name="Products to Add",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step(f"Verify product URLs were found on {playwright_browser_name}"):
        assert len(product_urls) > 0, \
            f"Should find at least one product URL for '{query}' with max price ${max_price} on {playwright_browser_name}"

    with allure.step(f"Add items to cart on {playwright_browser_name}"):
        # Add items to cart
        ebay_page.add_item_to_cart(product_urls)

        allure.attach(
            f"Attempted to add {len(product_urls)} items to cart",
            name="Cart Addition Summary",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step(f"Verify we're back on main page on {playwright_browser_name}"):
        # Verify we're back on the main page after adding items
        assert "ebay.com" in page.url.lower(), \
            f"Should be on eBay main page after adding items on {playwright_browser_name}"

        # Verify search box is visible (indicates we're on main page)
        assert ebay_page.is_search_box_visible(), \
            f"Search box should be visible on main page on {playwright_browser_name}"

    with allure.step(f"Attach product URLs that were processed on {playwright_browser_name}"):
        urls_summary = f"Processed {len(product_urls)} product URLs:\n\n"
        for i, url in enumerate(product_urls, 1):
            urls_summary += f"{i}. {url}\n"

        allure.attach(
            urls_summary,
            name="Product URLs Processed",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.epic("eBay Tests")
@allure.feature("Cart Total Assertion")
@pytest.mark.regression
def test_cart_total_does_not_exceed_budget(page: Page, playwright_browser_name: str):
    """Test that cart total does not exceed budget_per_item * item_count after adding items."""

    ebay_page = EbayPage(page)
    query = "laptop"
    budget_per_item = 500.0
    limit = 3

    with allure.step(f"Search for '{query}' with max price ${budget_per_item} on {playwright_browser_name}"):
        product_urls = ebay_page.search_items_by_name_under_price(
            query=query,
            max_price=budget_per_item,
            limit=limit
        )

        allure.attach(
            f"Found {len(product_urls)} product URLs",
            name="Products to Add",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step(f"Verify product URLs were found on {playwright_browser_name}"):
        assert len(product_urls) > 0, \
            f"Should find at least one product for '{query}' with max price ${budget_per_item} on {playwright_browser_name}"

    with allure.step(f"Add items to cart on {playwright_browser_name}"):
        ebay_page.add_item_to_cart(product_urls)

    with allure.step(f"Navigate to eBay homepage so cart icon is visible on {playwright_browser_name}"):
        ebay_page.navigate_to()
        ebay_page.wait_for_page_load()

    with allure.step(f"Assert cart total does not exceed {limit} * ${budget_per_item} on {playwright_browser_name}"):
        ebay_page.assert_cart_total_not_exceeds(
            budget_per_item=budget_per_item,
            item_count=len(product_urls)
        )
