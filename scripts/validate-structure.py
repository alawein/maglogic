#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_PATHS = [
    "AGENTS.md",
    "README.md",
    "SSOT.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "pyproject.toml",
    "python/maglogic/__init__.py",
    "python/tests/test_constants.py",
    "docs/README.md",
    "docs/architecture/STRUCTURE_DECISION.md",
    "oommf/",
    "mumax3/",
    "matlab/",
    "examples/",
    "docker/",
]


def main() -> int:
    failures: list[str] = []

    for relative_path in REQUIRED_PATHS:
        target = ROOT / relative_path
        if relative_path.endswith("/"):
            if not target.is_dir():
                failures.append(f"{relative_path}: missing required directory")
        elif not target.exists():
            failures.append(f"{relative_path}: missing required file")

    if (ROOT / "src").exists():
        failures.append(
            "src/: unexpected parallel package root; MagLogic uses python/maglogic/",
        )

    package_root = ROOT / "python" / "maglogic"
    if not package_root.is_dir():
        failures.append("python/maglogic/: missing canonical Python package directory")

    tests_root = ROOT / "python" / "tests"
    if not tests_root.is_dir():
        failures.append("python/tests/: missing canonical Python test directory")

    if failures:
        print("\n".join(failures))
        return 1

    print("structure: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
