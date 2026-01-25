#!/bin/bash
# Script to run tests on all browsers sequentially

echo "Running tests on all browsers..."
echo "=================================="

# Run on Chromium
echo ""
echo "Running on Chromium..."
pytest --browser chromium -v

# Run on Firefox
echo ""
echo "Running on Firefox..."
pytest --browser firefox -v

# Run on WebKit
echo ""
echo "Running on WebKit..."
pytest --browser webkit -v

echo ""
echo "All browser tests completed!"
