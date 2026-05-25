"""
Cycle 3 Mesa environment smoke test.

Purpose:
Verify that Cycle 3 ABM work is running under the captured known-good
environment, not system Python, and that Mesa imports at the captured version.

This test clears L1 implementation/environment only. It says nothing about
observable validity, steady-state eligibility, or manuscript interpretation.
"""

import argparse
import sys
from pathlib import Path

import mesa


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--expected-mesa",
        default="3.5.1",
        help="Expected Mesa version from cycle3/ENVIRONMENT_SNAPSHOT.md",
    )
    parser.add_argument(
        "--expected-env-fragment",
        default=r"EE_Theory_Lab\venv\Scripts\python.exe",
        help="Required substring in sys.executable",
    )
    args = parser.parse_args()

    executable = str(Path(sys.executable))
    mesa_version = getattr(mesa, "__version__", "UNKNOWN")

    print("--- Cycle 3 Mesa smoke test ---")
    print(f"Python executable: {executable}")
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Mesa version: {mesa_version}")

    if args.expected_env_fragment not in executable:
        print("SMOKE TEST FAIL: Python executable is not the captured Cycle 3 venv.")
        print(f"Expected path fragment: {args.expected_env_fragment}")
        return 1

    if mesa_version != args.expected_mesa:
        print("SMOKE TEST FAIL: Mesa version mismatch.")
        print(f"Expected Mesa: {args.expected_mesa}")
        print(f"Actual Mesa:   {mesa_version}")
        return 1

    print("SMOKE TEST OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
