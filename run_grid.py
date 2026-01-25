#!/usr/bin/env python3
"""
Browser Grid Runner
Runs tests across multiple browsers in parallel
"""

import subprocess
import sys
import os
from config.browser_grid import GRID_MODES


def run_grid(mode: str = "all", parallel: bool = True, workers: str = "auto"):
    """
    Run tests on browser grid
    
    Args:
        mode: Grid mode (all, chromium, firefox, webkit, desktop, mobile)
        parallel: Run tests in parallel
        workers: Number of parallel workers (auto, or number)
    """

    if mode not in GRID_MODES:
        print(f"Invalid grid mode: {mode}")
        print(f"Available modes: {', '.join(GRID_MODES.keys())}")

        sys.exit(1)
    
    browsers = GRID_MODES[mode]

    print(f"Running tests on browser grid mode: {mode}")
    print(f"Browsers: {', '.join(browsers)}")
    
    # Build pytest command
    cmd = ["pytest"]
    
    # Add grid mode
    cmd.extend(["--grid-mode", mode])
    
    # Add parallel execution if enabled
    if parallel:
        cmd.extend(["-n", workers])
        print(f"Running in parallel with {workers} workers")
    
    # Add verbose output
    cmd.append("-v")
    
    # Add any additional arguments
    cmd.extend(sys.argv[1:])
    
    print(f"\nExecuting: {' '.join(cmd)}\n")
    
    # Run pytest
    result = subprocess.run(cmd)
    
    return result.returncode


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run tests on browser grid")
    parser.add_argument(
        "--mode",
        default="all",
        choices=list(GRID_MODES.keys()),
        help="Grid mode to run (default: all)"
    )
    parser.add_argument(
        "--no-parallel",
        action="store_true",
        help="Disable parallel execution"
    )
    parser.add_argument(
        "--workers",
        default="auto",
        help="Number of parallel workers (default: auto)"
    )
    
    args, remaining = parser.parse_known_args()
    
    # Pass remaining args to pytest
    sys.argv = [sys.argv[0]] + remaining
    
    exit_code = run_grid(
        mode=args.mode,
        parallel=not args.no_parallel,
        workers=args.workers
    )
    sys.exit(exit_code)
