# Parallel Execution Guide for Playwright/Pytest

## Important Note: Playwright vs Selenium Grid

**Playwright does NOT use Selenium Grid.** Playwright has its own browser management system and doesn't need Selenium Grid. However, you can run Playwright tests in parallel using pytest-xdist.

## Running Tests in Parallel

### Method 1: Using pytest-xdist (Recommended)

Your project already has `pytest-xdist` installed. Here's how to use it:

#### Basic Parallel Execution

```bash
# Auto-detect number of CPU cores
pytest -n auto

# Use specific number of workers
pytest -n 4

# Run with 2 workers
pytest -n 2
```

#### Parallel Execution with Browser Grid

```bash
# Run tests on all browsers in parallel
pytest --grid-mode all -n auto

# Run with specific number of workers
pytest --grid-mode all -n 4

# Run specific test file in parallel
pytest tests/test_ebay.py -n auto
```

#### Parallel Execution with Markers

```bash
# Run smoke tests in parallel
pytest -m smoke -n auto

# Run regression tests in parallel
pytest -m regression -n auto
```

### Method 2: Using pytest-parallel (Alternative)

If you want more control, you can use `pytest-parallel`:

```bash
pip install pytest-parallel
```

```bash
# Run tests in parallel
pytest --workers auto

# Specific number of workers
pytest --workers 4
```

### Method 3: Using pytest-xdist with Specific Options

```bash
# Distribute tests across multiple processes
pytest -n auto --dist loadgroup

# Run tests in load-balanced mode
pytest -n auto --dist loadfile

# Run tests in work-stealing mode (default)
pytest -n auto --dist worksteal
```

## Configuration

### Update pytest.ini for Default Parallel Execution

You can add parallel execution to your default pytest options:

```ini
[pytest]
addopts = 
    -v
    --strict-markers
    --alluredir=allure-results
    -n auto  # Add this for automatic parallel execution
```

### Environment Variable

You can also set the number of workers via environment variable:

```bash
# Windows PowerShell
$env:PYTEST_XDIST_WORKER_COUNT=4
pytest

# Linux/macOS
export PYTEST_XDIST_WORKER_COUNT=4
pytest
```

## Distributed Testing (Alternative to Selenium Grid)

If you need distributed testing across multiple machines, Playwright offers different solutions:

### Option 1: Playwright Test Runner (Official)

Playwright has its own test runner that supports sharding:

```bash
# Install Playwright test runner
pip install playwright pytest-playwright

# Run tests in sharded mode
playwright test --shard=1/4  # Run shard 1 of 4
playwright test --shard=2/4  # Run shard 2 of 4
```

### Option 2: CI/CD Parallel Execution

Most CI/CD platforms support parallel execution:

**GitHub Actions:**
```yaml
strategy:
  matrix:
    shard: [1, 2, 3, 4]
steps:
  - run: pytest --grid-mode all -n auto
```

**Jenkins:**
- Use Jenkins parallel test execution plugin
- Configure multiple agents to run tests

### Option 3: Docker Compose (Multiple Containers)

Run tests in parallel across multiple Docker containers:

```yaml
version: '3.8'
services:
  test-worker-1:
    image: your-test-image
    command: pytest --grid-mode chromium -n auto
    
  test-worker-2:
    image: your-test-image
    command: pytest --grid-mode firefox -n auto
    
  test-worker-3:
    image: your-test-image
    command: pytest --grid-mode webkit -n auto
```

## Performance Tips

### 1. Optimal Worker Count

```bash
# For CPU-bound tests: number of CPU cores
pytest -n $(nproc)  # Linux
pytest -n 4  # If you have 4 cores

# For I/O-bound tests: 2x CPU cores
pytest -n 8  # If you have 4 cores
```

### 2. Combine with Browser Grid

```bash
# Run on all browsers with parallel execution
pytest --grid-mode all -n auto

# This will run:
# - Each test on all browsers (grid mode)
# - Multiple tests in parallel (xdist)
```

### 3. Test Isolation

Ensure tests are properly isolated:
- Use fixtures with proper scope
- Avoid shared state
- Use unique test data

## Example: Full Parallel Execution

```bash
# Run all tests on all browsers in parallel
pytest --grid-mode all -n auto -v

# This command will:
# 1. Run each test on chromium, firefox, and webkit (grid mode)
# 2. Execute multiple test instances in parallel (xdist)
# 3. Generate Allure reports for all results
```

## Troubleshooting

### Issue: Tests failing due to resource contention

**Solution:** Reduce number of workers
```bash
pytest -n 2  # Instead of auto
```

### Issue: Out of memory errors

**Solution:** 
- Reduce workers
- Run headless mode: `HEADLESS=true pytest -n auto`
- Close browsers properly in fixtures

### Issue: Flaky tests in parallel

**Solution:**
- Ensure proper test isolation
- Use unique test data
- Add proper waits and timeouts

## Comparison: Playwright vs Selenium Grid

| Feature | Playwright | Selenium Grid |
|---------|-----------|---------------|
| Browser Management | Built-in | Requires Grid Hub/Nodes |
| Parallel Execution | pytest-xdist | Grid distributes tests |
| Setup Complexity | Simple | Complex (Hub + Nodes) |
| Performance | Fast | Slower (network overhead) |
| Browser Support | Chromium, Firefox, WebKit | All Selenium-supported browsers |
| Distributed Testing | CI/CD sharding | Grid architecture |

## Recommendation

For your Playwright project:
1. **Use pytest-xdist** for parallel execution (already installed)
2. **Use browser grid mode** for cross-browser testing
3. **Combine both** for maximum efficiency:
   ```bash
   pytest --grid-mode all -n auto
   ```

This gives you:
- Parallel test execution (faster)
- Cross-browser testing (comprehensive)
- No need for Selenium Grid (simpler setup)
