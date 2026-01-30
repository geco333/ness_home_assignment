import allure
import pytest

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
    """Hook to capture test failure status"""

    outcome = yield
    rep = outcome.get_result()

    setattr(pytest, 'current_test_failed', rep.failed)


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
