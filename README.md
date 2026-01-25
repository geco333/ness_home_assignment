# Playwright Testing Project

A Playwright testing framework using Python, pytest, and Allure reporting.

## Prerequisites

- Python 3.8+
- pip
- Java 8+ (for Allure commandline tool)

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pom
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**
   ```bash
   playwright install
   ```
   
   Or install specific browsers:
   ```bash
   playwright install chromium
   playwright install firefox
   playwright install webkit
   ```

4. **Install Allure commandline tool** (optional, for viewing reports)
   
   **Windows (using Scoop):**
   ```bash
   scoop install allure
   ```
   
   **Windows (using Chocolatey):**
   ```bash
   choco install allure
   ```
   
   **macOS:**
   ```bash
   brew install allure
   ```
   
   **Linux:**
   ```bash
   # Download from https://github.com/allure-framework/allure2/releases
   # Extract and add to PATH
   ```
   
   Or download manually from: https://github.com/allure-framework/allure2/releases

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

## Running Tests

### Single Browser

```bash
# Run all tests on default browser
pytest

# Run with specific browser
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit

# Run with specific markers
pytest -m smoke
pytest -m chromium
pytest -m firefox
pytest -m webkit

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_example.py -v
```

### Browser Grid (Multiple Browsers)

Run tests across multiple browsers in parallel:

```bash
# Run on all browsers (chromium, firefox, webkit) in parallel
python run_grid.py --mode all

# Run on desktop browsers only (chromium, firefox)
python run_grid.py --mode desktop

# Run on specific browser
python run_grid.py --mode chromium

# Run without parallel execution
python run_grid.py --mode all --no-parallel

# Run with specific number of workers
python run_grid.py --mode all --workers 4

# Using pytest directly with grid mode
pytest --grid-mode all -n auto
pytest --grid-mode desktop -n auto
pytest --grid-mode chromium -n auto
```

### Parallel Execution

**Note:** Playwright does NOT use Selenium Grid. Playwright has its own browser management. Use pytest-xdist for parallel execution.

```bash
# Run in parallel (auto-detect workers)
pytest -n auto

# Run with specific number of workers
pytest -n 4

# Combine grid mode with parallel execution
pytest --grid-mode all -n auto

# Run specific tests in parallel
pytest tests/test_ebay.py -n auto
```

For detailed parallel execution guide, see [PARALLEL_EXECUTION.md](PARALLEL_EXECUTION.md)

## Generating Allure Reports

After running tests, generate and view the Allure report:

```bash
# Generate report from results
allure generate allure-results --clean -o allure-report

# Open report in browser
allure open allure-report
```

Or use the serve command (generates and opens automatically):
```bash
allure serve allure-results
```

## Project Structure

```
pom/
├── config/              # Configuration files
│   ├── settings.py      # Application settings
│   └── browser_grid.py  # Browser grid configuration
├── tests/               # Test files
│   ├── pages/           # Page Object Model classes
│   │   └── base_page.py
│   ├── conftest.py      # Pytest fixtures
│   └── test_*.py        # Test files
├── utils/               # Utility functions
│   ├── browser_factory.py
│   └── helpers.py
├── scripts/             # Helper scripts
│   ├── run_all_browsers.sh
│   └── run_all_browsers.bat
├── run_grid.py          # Browser grid runner
├── allure-results/      # Allure test results (generated)
└── allure-report/       # Allure HTML report (generated)
```

## Configuration

Edit the `.env` file to configure:

- `BROWSER`: Browser to use (chromium, firefox, or webkit) - default: chromium
- `HEADLESS`: Run in headless mode (true/false) - default: false
- `SLOW_MO`: Slow down operations by milliseconds (0 = no slowdown) - default: 0
- `NAVIGATION_TIMEOUT`: Navigation timeout in milliseconds - default: 30000
- `ACTION_TIMEOUT`: Action timeout in milliseconds - default: 10000
- `BASE_URL`: Base URL for your application under test

## Playwright Features

This project uses Playwright which provides:

- **Auto-waiting**: Playwright automatically waits for elements to be ready
- **Multiple browsers**: Support for Chromium, Firefox, and WebKit
- **Network interception**: Mock and stub network requests
- **Mobile emulation**: Test mobile viewports and touch events
- **Screenshots & videos**: Automatic screenshot capture on failures
- **Fast execution**: Built-in parallelization support

## Writing Tests

### Basic Test

Example test using Page Object Model:

```python
import pytest
import allure
from playwright.sync_api import Page
from tests.pages.base_page import BasePage

@allure.epic("Example Tests")
@allure.feature("Basic Navigation")
@pytest.mark.smoke
def test_example(page: Page):
    """Example test case"""
    base_page = BasePage(page)
    base_page.navigate_to()
    
    title = base_page.get_title()
    assert title is not None
```

### Grid Test (Runs on Multiple Browsers)

To run a test on multiple browsers, add the `browser_name` parameter:

```python
import pytest
import allure
from playwright.sync_api import Page
from tests.pages.base_page import BasePage

@allure.epic("Example Tests")
@allure.feature("Basic Navigation")
@pytest.mark.smoke
def test_example(page: Page, browser_name: str):
    """Example test that runs on all browsers in grid mode"""
    base_page = BasePage(page)
    base_page.navigate_to()
    
    title = base_page.get_title()
    assert title is not None, f"Title should not be empty on {browser_name}"
    
    # Browser name is automatically available
    allure.attach(browser_name, name="Browser", attachment_type=allure.attachment_type.TEXT)
```

When you run with `--grid-mode all`, this test will automatically run on chromium, firefox, and webkit.

## Browser Grid Modes

The grid supports the following modes:

- `all`: Run on all browsers (chromium, firefox, webkit)
- `desktop`: Run on desktop browsers (chromium, firefox)
- `chromium`: Run on Chromium only
- `firefox`: Run on Firefox only
- `webkit`: Run on WebKit only
- `mobile`: Run on mobile browser (webkit)

Configure grid modes in `config/browser_grid.py`.

## Troubleshooting

- **Browser not found**: Run `playwright install` to download browsers
- **Tests timeout**: Increase `NAVIGATION_TIMEOUT` or `ACTION_TIMEOUT` in `.env`
- **Headless mode issues**: Set `HEADLESS=false` in `.env` to see browser actions
- **Slow execution**: Use `SLOW_MO` in `.env` to slow down for debugging
- **Grid tests not running on multiple browsers**: Ensure test function includes `browser_name` parameter
- **Parallel execution issues**: Reduce number of workers with `--workers 2` if system resources are limited