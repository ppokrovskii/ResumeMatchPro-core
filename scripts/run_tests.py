#!/usr/bin/env python
import subprocess
import sys
from pathlib import Path


def main() -> None:
    # Get the project root directory
    project_root = Path(__file__).parent.parent

    # Run pytest with coverage
    cmd = [
        "pytest",
        "--cov=repositories",
        "--cov=shared",
        "--cov-report=term-missing",
        "tests/"
    ]

    # Run the command and capture the output
    result = subprocess.run(cmd, cwd=project_root, check=False)

    # Exit with the same code as pytest
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
