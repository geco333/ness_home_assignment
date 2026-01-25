import pytest
import allure
import os
from playwright.sync_api import Page, BrowserContext
from config.settings import Settings
from config.browser_grid import get_browsers_for_mode, BROWSERS


# Get grid mode from environment or pytest option
def pytest_addoption(parser):
    """Add custom pytest options"""

    parser.addoption(
        "--grid-mode",
        action="store",
        default=os.getenv("GRID_MODE", "single"),
        help="Browser grid mode: all, chromium, firefox, webkit, desktop, mobile, single",
    )
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        help="Single browser to use: chromium, firefox, webkit (overrides grid-mode)",
    )


@pytest.fixture(scope="session")
def grid_mode(request):
    """Get the grid mode from command line or environment"""

    return request.config.getoption("--grid-mode")


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Configure browser launch arguments"""

    return {
        **browser_type_launch_args,
        "headless": Settings.HEADLESS,
        "slow_mo": Settings.SLOW_MO,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context arguments"""

    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
    }


# Parametrize tests to run on multiple browsers when browser_name is in fixture names
def pytest_generate_tests(metafunc):
    """Generate tests for multiple browsers when using browser_name fixture"""
    
    if "browser_name" in metafunc.fixturenames:
        grid_mode = metafunc.config.getoption("--grid-mode", default="single")
        cmd_browser = metafunc.config.getoption("--browser")
        
        # If --browser is specified, use single browser
        if cmd_browser:
            browsers = [cmd_browser.lower()]
        elif grid_mode == "single":
            # Single browser mode - use settings
            browsers = [Settings.BROWSER]
        else:
            # Grid mode - get browsers for mode
            browsers = get_browsers_for_mode(grid_mode)
        
        # Parametrize both browser_name and playwright_browser_name
        metafunc.parametrize("browser_name", browsers, indirect=True)
        metafunc.parametrize("playwright_browser_name", browsers, indirect=True, scope="session")


@pytest.fixture(scope="function")
def browser_name(request):
    """Browser name fixture for grid execution"""
    # If test is parametrized with browser_name, use that
    if hasattr(request, "param"):
        return request.param
    # Otherwise use settings or command line option
    cmd_browser = request.config.getoption("--browser")
    if cmd_browser:
        return cmd_browser.lower()
    return Settings.BROWSER


@pytest.fixture(scope="session")
def playwright_browser_name(request):
    """Set the browser to use - can be parametrized for grid mode"""
    # If parametrized (grid mode), use the param
    if hasattr(request, "param"):
        return request.param
    
    # Command line --browser option takes precedence
    cmd_browser = request.config.getoption("--browser")
    if cmd_browser:
        return cmd_browser.lower()
    
    # Otherwise use settings
    return Settings.BROWSER


@pytest.fixture(scope="function")
def page(browser_context: BrowserContext, browser_name, request) -> Page:
    """Create a new page for each test with Allure screenshot on failure"""
    page = browser_context.new_page()
    
    # Set timeouts
    page.set_default_navigation_timeout(Settings.NAVIGATION_TIMEOUT)
    page.set_default_timeout(Settings.ACTION_TIMEOUT)
    
    # Add browser name to Allure report
    allure.dynamic.label("browser", browser_name)
    
    yield page
    
    # Take screenshot on test failure
    if hasattr(pytest, 'current_test_failed') and pytest.current_test_failed:
        try:
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name=f"screenshot_{browser_name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
    
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test failure status"""
    outcome = yield
    rep = outcome.get_result()
    setattr(pytest, 'current_test_failed', rep.failed)
