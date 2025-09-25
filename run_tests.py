#!/usr/bin/env python3
"""
Script to run all tests for the Mihomo-Mosdns synchronization service.
"""
import subprocess
import sys
import os

def run_tests():
    """Run all tests using pytest."""
    try:
        # Run pytest with coverage and verbose output
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v", 
            "--tb=short",
            "--disable-warnings"
        ], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Tests failed with return code: {e.returncode}")
        return False
    except FileNotFoundError:
        print("Error: pytest not found. Please install test dependencies:")
        print("pip install pytest pytest-asyncio")
        return False

def run_tests_with_coverage():
    """Run tests with coverage report."""
    try:
        # Check if coverage is installed
        subprocess.run([sys.executable, "-m", "coverage", "--version"], 
                      check=True, capture_output=True)
        
        # Run tests with coverage
        subprocess.run([
            sys.executable, "-m", "coverage", "run", "-m", "pytest", 
            "tests/", 
            "-v", 
            "--tb=short",
            "--disable-warnings"
        ], check=True)
        
        # Generate coverage report
        subprocess.run([sys.executable, "-m", "coverage", "report", "-m"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Coverage tests failed with return code: {e.returncode}")
        return False
    except FileNotFoundError:
        print("Error: coverage not found. Please install it:")
        print("pip install coverage")
        return False

def main():
    """Main function to run tests."""
    print("Mihomo-Mosdns Synchronization Service - Test Runner")
    print("=" * 50)
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Check if tests directory exists
    if not os.path.exists("tests"):
        print("Error: tests directory not found")
        return 1
    
    # Check if pytest is installed
    try:
        import pytest
    except ImportError:
        print("Error: pytest not found. Please install test dependencies:")
        print("pip install pytest pytest-asyncio")
        return 1
    
    # Ask user what type of tests to run
    print("\nSelect test option:")
    print("1. Run basic tests")
    print("2. Run tests with coverage report")
    print("3. Run specific test file")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
    except KeyboardInterrupt:
        print("\nTest execution cancelled")
        return 1
    
    if choice == "1":
        print("\nRunning basic tests...")
        success = run_tests()
    elif choice == "2":
        print("\nRunning tests with coverage...")
        success = run_tests_with_coverage()
    elif choice == "3":
        test_file = input("Enter test file path (e.g., tests/test_config.py): ").strip()
        if os.path.exists(test_file):
            print(f"\nRunning {test_file}...")
            try:
                subprocess.run([
                    sys.executable, "-m", "pytest", 
                    test_file, 
                    "-v", 
                    "--tb=short"
                ], check=True)
                success = True
            except subprocess.CalledProcessError:
                success = False
        else:
            print(f"Error: File {test_file} not found")
            success = False
    else:
        print("Invalid choice")
        return 1
    
    if success:
        print("\nAll tests completed successfully!")
        return 0
    else:
        print("\nSome tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())