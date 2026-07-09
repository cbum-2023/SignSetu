"""Convenience runner for the SignSetu API test suite."""

from __future__ import annotations

import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Run SignSetu API tests")
    parser.add_argument("--base-url", help="Override the target API base URL")
    parser.add_argument(
        "--strict-known-bugs",
        action="store_true",
        help="Fail known product bug tests instead of marking them xfail",
    )
    parser.add_argument(
        "--markers",
        default=None,
        help="Optional pytest marker expression, for example: contract or 'not slow'",
    )
    args = parser.parse_args()

    command = [sys.executable, "-m", "pytest", "-v"]
    if args.base_url:
        command.extend(["--base-url", args.base_url])
    if args.strict_known_bugs:
        command.append("--strict-known-bugs")
    if args.markers:
        command.extend(["-m", args.markers])

    return subprocess.call(command)


if __name__ == "__main__":
    raise SystemExit(main())
