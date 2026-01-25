import pytest
import allure
from playwright.sync_api import Page
from tests.pages.base_page import BasePage


@allure.epic("Example Tests")
@allure.feature("Basic Navigation")
@pytest.mark.smoke
def test_example(page: Page, browser_name: str):
    """Example test case demonstrating Allure reporting with Playwright Grid"""
    
    with allure.step(f"Navigate to base URL on {browser_name}"):
        base_page = BasePage(page)
        base_page.navigate_to()
        
        allure.attach(
            page.url,
            name="Current URL",
            attachment_type=allure.attachment_type.TEXT
        )
    
    with allure.step(f"Verify page title on {browser_name}"):
        title = page.title()
        
        assert title is not None, f"Page title should not be empty on {browser_name}"
        
        allure.attach(
            title,
            name="Page Title",
            attachment_type=allure.attachment_type.TEXT
        )
        
        allure.attach(
            browser_name,
            name="Browser",
            attachment_type=allure.attachment_type.TEXT
        )