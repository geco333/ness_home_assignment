import allure
import pytest
import os
import requests
import json
from typing import Generator, Callable
from playwright.sync_api import Browser, Page

from config.settings import Settings


# @pytest.fixture(scope="session")
# def browser_context_args(request, browser_context_args):
#     return {
#         **browser_context_args,
#         **request.param
#     }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": Settings.HEADLESS,
        "slow_mo": Settings.SLOW_MO
    }


def _get_cdp_url_from_selenium_grid(selenium_remote_url: str, max_retries: int = 3) -> str:
    """
    Create a session in Selenium Grid and get the WebSocket URL for CDP connection.
    
    Args:
        selenium_remote_url: The base URL of Selenium Grid (e.g., http://localhost:4444)
        max_retries: Maximum number of retries for session creation
    
    Returns:
        The WebSocket URL for connecting via CDP
    """
    # Ensure the URL doesn't have trailing slash
    base_url = selenium_remote_url.rstrip("/")
    
    # W3C WebDriver protocol capabilities for Chrome with CDP support
    payload = {
        "capabilities": {
            "alwaysMatch": {
                "browserName": "chrome"
            }
        }
    }
    
    last_error = None
    for attempt in range(max_retries):
        try:
            print(f"Attempting to create Selenium Grid session (attempt {attempt + 1}/{max_retries})...")
            
            # Create session via Selenium Grid with increased timeout (30 seconds)
            response = requests.post(
                f"{base_url}/session",
                json=payload,
                timeout=30
            )
            
            # Debug: print response if there's an error
            if response.status_code != 200:
                print(f"Selenium Grid response status: {response.status_code}")
                print(f"Response body: {response.text}")
            
            response.raise_for_status()
            session_data = response.json()
            
            # Extract session ID from W3C WebDriver response
            session_id = session_data.get("sessionId") or session_data.get("value", {}).get("sessionId")
            
            if not session_id:
                raise ValueError("No sessionId found in Selenium Grid response")
            
            print(f"Successfully created Selenium Grid session: {session_id}")
            
            # Get the WebSocket URL from the CDP endpoint
            # Selenium Grid exposes CDP via ws://selenium-hub:4444/session/{sessionId}/se/cdp
            cdp_url = f"{base_url.replace('http://', 'ws://').replace('https://', 'wss://')}/session/{session_id}/se/cdp"
            
            return cdp_url
            
        except requests.exceptions.Timeout as e:
            last_error = e
            print(f"Timeout creating session (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                import time
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                print(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            continue
            
        except requests.exceptions.RequestException as e:
            last_error = e
            print(f"Request error creating session: {e}")
            raise RuntimeError(f"Failed to create Selenium Grid session: {e}")
            
        except (ValueError, KeyError) as e:
            last_error = e
            print(f"Parse error in session response: {e}")
            raise RuntimeError(f"Failed to parse Selenium Grid session response: {e}")
    
    # All retries exhausted
    raise RuntimeError(f"Failed to create Selenium Grid session after {max_retries} attempts: {last_error}")


@pytest.fixture(scope="session")
def browser(playwright, launch_browser: Callable[[], Browser]) -> Generator[Browser, None, None]:
    """
    Custom browser fixture that handles both local and Selenium Grid remote connections.
    If SELENIUM_REMOTE_URL is set, connects via CDP instead of launching locally.
    """
    selenium_remote_url = os.getenv("SELENIUM_REMOTE_URL")
    
    if selenium_remote_url:
        # Get the WebSocket URL from Selenium Grid
        cdp_url = _get_cdp_url_from_selenium_grid(selenium_remote_url)
        # Connect to Selenium Grid via CDP (Chrome DevTools Protocol)
        browser = playwright.chromium.connect_over_cdp(cdp_url)
    else:
        # Launch browser locally
        browser = launch_browser()
    
    yield browser
    
    # Close browser after tests
    browser.close()


@pytest.fixture(scope="session")
def playwright_browser_name(request):
    """Browser name for Playwright - can be parametrized via --browser flag"""

    # If parametrized, use the param
    if hasattr(request, "param"):
        return request.param

    # Otherwise use settings
    return Settings.BROWSER


@pytest.fixture(scope="function", autouse=True)
def allure_test_metadata(request, playwright_browser_name):
    """
    Automatically set Allure metadata for each test to ensure unique test cases.
    This fixture runs automatically for every test (autouse=True).
    """

    # Set browser label for each test
    allure.dynamic.label("browser", playwright_browser_name)

    # Ensure test name includes browser for clarity in reports
    test_name = request.node.name

    if playwright_browser_name not in test_name:
        # The parametrization already adds [browser_name] to the test name
        # but we add it as a label for better filtering
        allure.dynamic.label("parametrized_browser", playwright_browser_name)

    yield


# Add command-line option for browser config
def pytest_addoption(parser):
    """Add custom pytest options"""
    parser.addoption(
        "--browser-config",
        action="store",
        default=None,
        help="Path to browser configuration JSON file (default: config/browser_config.json)",
    )


# Use Playwright's built-in browser matrix by parametrizing playwright_browser_name
# @pytest.hookimpl(tryfirst=True)
# def pytest_generate_tests(metafunc):
#     """Generate browser testing matrix from JSON config using Playwright's built-in mechanisms"""
# 
#     if "playwright_browser_name" in metafunc.fixturenames:
#         # Check if already parametrized
#         already_parametrized = False
# 
#         # Check markers
#         for marker in metafunc.definition.iter_markers("parametrize"):
#             if marker.args and len(marker.args) > 0 and marker.args[0] == "playwright_browser_name":
#                 already_parametrized = True
#                 break
# 
#         # Check callspec
#         if not already_parametrized and hasattr(metafunc, 'callspec') and metafunc.callspec:
#             if "playwright_browser_name" in metafunc.callspec.params:
#                 already_parametrized = True
# 
#         if not already_parametrized:
#             # Get browsers from JSON configuration
#             try:
#                 config_path = metafunc.config.getoption("--browser-config", default=None)
#                 browsers = get_browsers_from_config(config_path)
# 
#                 # If no browsers in config, use default from settings
#                 if not browsers:
#                     browsers = [Settings.BROWSER]
#             except Exception as e:
#                 # Fallback to single browser from settings if JSON read fails
#                 print(f"Warning: Could not load browser config: {e}. Using single browser mode.")
#                 browsers = [Settings.BROWSER]
# 
#             try:
#                 arguments = [
#                     "playwright_browser_name",
#                     "browser_type_launch_args",
#                     "browser_context_args"
#                 ]
#                 values = [
#                     [b['browser_name'],
#                      b['capabilities'],
#                      b['context']]
#                     for b in browsers
#                 ]
# 
#                 metafunc.parametrize(arguments, values, indirect=True, scope="session")
#             except KeyError as e:
#                 raise f"Error in browser configuration: {e}"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test failure status and take screenshots on failure"""

    outcome = yield
    rep = outcome.get_result()

    setattr(pytest, 'current_test_failed', rep.failed)

    # Take screenshot on test failure
    if rep.failed and hasattr(item, 'funcargs') and 'page' in item.funcargs:
        page = item.funcargs['page']
        try:
            # Create screenshots directory if it doesn't exist
            screenshots_dir = "reports/failure_screenshots"
            import os
            os.makedirs(screenshots_dir, exist_ok=True)

            # Generate unique filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name.replace('[', '_').replace(']', '_').replace('::', '_')
            screenshot_path = f"{screenshots_dir}/{test_name}_{timestamp}_failure.png"

            # Take screenshot
            page.screenshot(path=screenshot_path, full_page=True)

            # Attach screenshot to Allure report
            with open(screenshot_path, 'rb') as f:
                screenshot_data = f.read()
                allure.attach(
                    screenshot_data,
                    name=f"Failure Screenshot - {item.name}",
                    attachment_type=allure.attachment_type.PNG
                )

        except Exception as e:
            # Log screenshot failure but don't fail the test
            print(f"Warning: Failed to take screenshot on test failure: {e}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    """Hook to set up Allure test metadata for each test to ensure unique test cases"""

    # Get browser name from parametrization if available
    browser_name = None

    if hasattr(item, 'callspec') and item.callspec:
        if 'playwright_browser_name' in item.callspec.params:
            browser_name = item.callspec.params['playwright_browser_name']
        elif 'browser_name' in item.callspec.params:
            browser_name = item.callspec.params['browser_name']

    # Set Allure labels and metadata to ensure each parametrized test is unique
    if browser_name:
        # Add browser label for filtering and grouping
        allure.dynamic.label("browser", browser_name)

        # Update test display name to include browser for clarity
        original_name = item.name

        if browser_name not in original_name:
            # Set a unique test name that includes the browser parameter
            allure.dynamic.label("test_name", f"{original_name}[{browser_name}]")

    yield
