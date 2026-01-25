# Browser Grid Usage Guide

This guide explains how to use the browser grid to run tests across multiple browsers and versions.

## Quick Start

### Run on All Browsers (Parallel)

```bash
# Using the grid runner script
python run_grid.py --mode all

# Using pytest directly
pytest --grid-mode all -n auto
```

### Run on Specific Browser Set

```bash
# Desktop browsers only (chromium + firefox)
python run_grid.py --mode desktop

# Single browser
python run_grid.py --mode chromium
```

## How It Works

### 1. Grid Modes

The grid supports these modes (defined in `config/browser_grid.py`):

- **all**: Runs on all browsers (chromium, firefox, webkit)
- **desktop**: Runs on desktop browsers (chromium, firefox)
- **chromium**: Runs on Chromium only
- **firefox**: Runs on Firefox only
- **webkit**: Runs on WebKit only
- **mobile**: Runs on mobile browser (webkit)
- **single**: Single browser mode (uses settings)

### 2. Writing Grid Tests

To make a test run on multiple browsers, add the `browser_name` parameter:

```python
def test_example(page: Page, browser_name: str):
    """This test will run on all browsers in grid mode"""
    # browser_name will be "chromium", "firefox", or "webkit"
    print(f"Running on {browser_name}")
    # Your test code here
```

### 3. Execution Modes

#### Single Browser (Default)
```bash
pytest tests/test_example.py
# Runs once on the browser specified in .env or --browser
```

#### Grid Mode (Multiple Browsers)
```bash
pytest --grid-mode all tests/test_example.py
# Runs the test 3 times (once per browser)
```

#### Parallel Grid Execution
```bash
pytest --grid-mode all -n auto tests/test_example.py
# Runs tests in parallel across all browsers
```

## Examples

### Example 1: Run All Tests on All Browsers

```bash
python run_grid.py --mode all
```

This will:
1. Run each test on chromium, firefox, and webkit
2. Execute in parallel (auto-detected workers)
3. Generate Allure reports with browser labels

### Example 2: Run Smoke Tests on Desktop Browsers

```bash
pytest --grid-mode desktop -m smoke -n auto
```

### Example 3: Run Specific Test File on All Browsers

```bash
pytest --grid-mode all tests/test_example.py -v
```

### Example 4: Sequential Execution (No Parallel)

```bash
python run_grid.py --mode all --no-parallel
```

## Allure Reports

When running in grid mode, Allure reports will:
- Show separate test results for each browser
- Include browser name in test labels
- Attach browser-specific screenshots on failure

View reports:
```bash
allure serve allure-results
```

## Configuration

### Environment Variables

Set in `.env` file:
```env
BROWSER=chromium  # Default browser for single mode
HEADLESS=false
GRID_MODE=all     # Default grid mode
```

### Command Line Options

```bash
# Override grid mode
pytest --grid-mode desktop

# Override browser (single browser mode)
pytest --browser firefox

# Combine with parallel execution
pytest --grid-mode all -n 4
```

## Performance Tips

1. **Use parallel execution**: `-n auto` or `-n 4` for faster runs
2. **Use headless mode**: Set `HEADLESS=true` in `.env` for faster execution
3. **Selective grid modes**: Use `desktop` instead of `all` if webkit isn't needed
4. **Filter tests**: Use markers like `-m smoke` to run only critical tests

## Troubleshooting

### Tests not running on multiple browsers

- Ensure test function includes `browser_name` parameter
- Check that `--grid-mode` is set (not "single")
- Verify browsers are installed: `playwright install`

### Parallel execution issues

- Reduce workers: `--workers 2` instead of `auto`
- Check system resources (CPU, memory)
- Run sequentially: `--no-parallel`

### Browser-specific failures

- Check Allure reports for browser-specific screenshots
- Use `HEADLESS=false` to see browser actions
- Increase timeouts in `.env` if needed
