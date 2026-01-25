@echo off
REM Script to run tests on all browsers sequentially (Windows)

echo Running tests on all browsers...
echo ==================================

REM Run on Chromium
echo.
echo Running on Chromium...
pytest --browser chromium -v

REM Run on Firefox
echo.
echo Running on Firefox...
pytest --browser firefox -v

REM Run on WebKit
echo.
echo Running on WebKit...
pytest --browser webkit -v

echo.
echo All browser tests completed!
