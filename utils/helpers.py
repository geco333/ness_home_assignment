import time
import allure
from playwright.sync_api import Page


def take_screenshot(page: Page, filename: str = None, attach_to_allure: bool = True):
    """Take a screenshot and optionally attach to Allure"""
    import os
    os.makedirs("reports", exist_ok=True)
    
    if filename is None:
        filename = f"screenshot_{int(time.time())}.png"
    
    screenshot_path = f"reports/{filename}"
    screenshot_bytes = page.screenshot(path=screenshot_path)
    
    if attach_to_allure:
        allure.attach(
            screenshot_bytes,
            name=filename,
            attachment_type=allure.attachment_type.PNG
        )
    
    return screenshot_path


def attach_page_source(page: Page):
    """Attach page source to Allure report"""
    page_source = page.content()
    allure.attach(
        page_source,
        name="page_source",
        attachment_type=allure.attachment_type.HTML
    )


def get_page_source(page: Page) -> str:
    """Get page source"""
    return page.content()


def wait_for_network_idle(page: Page, timeout: int = 30000):
    """Wait for network to be idle"""
    page.wait_for_load_state("networkidle", timeout=timeout)


def wait_for_dom_loaded(page: Page, timeout: int = 30000):
    """Wait for DOM to be loaded"""
    page.wait_for_load_state("domcontentloaded", timeout=timeout)
