#!/usr/bin/env python3
"""
AI Agent Engineering Training - Setup Verification Script
Checks that your environment is ready for the training program.
"""

import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print a section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")


def check_python_version() -> Tuple[bool, str]:
    """Verify Python version is 3.11+"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python {version.major}.{version.minor}.{version.micro} (need 3.11+)"


def check_package(package: str) -> Tuple[bool, str]:
    """Check if a Python package is installed"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", package],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            # Extract version from output
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    version = line.split(':')[1].strip()
                    return True, version
        return False, "Not installed"
    except Exception as e:
        return False, f"Error: {str(e)}"


def check_env_file() -> Tuple[bool, str]:
    """Check if .env file exists"""
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        return True, str(env_path)
    return False, "Not found (copy .env.example to .env)"


def check_git() -> Tuple[bool, str]:
    """Check if git is available and repo is initialized"""
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            return True, version
        return False, "Not installed"
    except Exception as e:
        return False, f"Error: {str(e)}"


def check_ollama() -> Tuple[bool, str]:
    """Check if Ollama is available (optional)"""
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, "Not installed"
    except FileNotFoundError:
        return False, "Not installed (optional)"
    except Exception as e:
        return False, f"Error: {str(e)}"


def check_directories() -> Dict[str, bool]:
    """Verify all training directories exist"""
    base = Path(__file__).parent.parent
    required_dirs = [
        "setup",
        "module_1_foundations",
        "module_2_memory",
        "module_3_tools",
        "module_4_multi_agent",
        "mcp_addon",
        "shared"
    ]
    return {dir_name: (base / dir_name).exists() for dir_name in required_dirs}


def print_status(check_name: str, success: bool, details: str):
    """Print a check result with color coding"""
    status = f"{Colors.GREEN}✓{Colors.RESET}" if success else f"{Colors.RED}✗{Colors.RESET}"
    print(f"  {status} {check_name:.<40} {details}")


def main():
    """Run all verification checks"""
    print_header("AI Agent Engineering Training")
    print_header("Environment Setup Verification")

    all_passed = True

    # Python version
    print(f"{Colors.BOLD}Core Requirements:{Colors.RESET}")
    success, details = check_python_version()
    print_status("Python Version", success, details)
    all_passed = all_passed and success

    success, details = check_git()
    print_status("Git", success, details)
    all_passed = all_passed and success

    success, details = check_env_file()
    print_status(".env file", success, details)
    if not success:
        print(f"    {Colors.YELLOW}→ Run: cp setup/.env.example .env{Colors.RESET}")

    # Required packages
    print(f"\n{Colors.BOLD}Required Python Packages:{Colors.RESET}")
    required_packages = [
        "openai",
        "pydantic",
        "python-dotenv",
        "chromadb",
        "requests",
        "structlog"
    ]

    for package in required_packages:
        success, details = check_package(package)
        print_status(package, success, details)
        all_passed = all_passed and success

    if not all_passed:
        print(f"\n    {Colors.YELLOW}→ Install: pip install -r setup/requirements.txt{Colors.RESET}")

    # Optional tools
    print(f"\n{Colors.BOLD}Optional Tools:{Colors.RESET}")
    success, details = check_ollama()
    print_status("Ollama (local models)", success, details)
    if not success:
        print(f"    {Colors.YELLOW}→ Visit: https://ollama.ai to install{Colors.RESET}")

    # Directory structure
    print(f"\n{Colors.BOLD}Directory Structure:{Colors.RESET}")
    dirs = check_directories()
    for dir_name, exists in dirs.items():
        print_status(dir_name, exists, "Present" if exists else "Missing")
        all_passed = all_passed and exists

    # Final summary
    print_header("Verification Summary")
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ All core checks passed! You're ready to begin.{Colors.RESET}\n")
        print(f"Next steps:")
        print(f"  1. Copy setup/.env.example to .env and add your API keys")
        print(f"  2. Tell your AI professor: 'I'm ready to start Module 1'")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Some checks failed. Please address the issues above.{Colors.RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
