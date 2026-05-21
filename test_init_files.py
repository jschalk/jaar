"""
test_init_files.py — Linter that confirms every non-test, non-ref directory
inside a given set of root directories contains an __init__.py file.

Usage:
    pytest test_init_files.py -v

Configure ROOT_DIRS below to match your project layout.
"""

import pytest
from pathlib import Path

# ── Configure these ────────────────────────────────────────────────────────────
ROOT_DIRS = [
    "src",
]

EXCLUDE_DIR_NAMES = {
    "_ref",
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "env",
    ".mypy_cache",
    ".pytest_cache",
    "dist",
    "build",
    ".eggs",
    "node_modules",
}

EXCLUDE_PREFIXES = ("test", "tests", "testing", ".")
# ──────────────────────────────────────────────────────────────────────────────


def _is_excluded(directory: Path) -> bool:
    name = directory.name
    return name in EXCLUDE_DIR_NAMES or name.startswith(EXCLUDE_PREFIXES)


def _collect_dirs_missing_init(root: Path) -> list[Path]:
    missing = []
    for directory in sorted(root.rglob("*")):
        if not directory.is_dir():
            continue
        if any(_is_excluded(part) for part in [directory, *directory.parents]):
            continue
        if not (directory / "__init__.py").exists():
            missing.append(directory)
    return missing


def _all_missing() -> list[tuple[str, Path]]:
    results = []
    for root_str in ROOT_DIRS:
        root = Path(root_str)
        if not root.exists():
            continue
        results.extend(
            (root_str, missing_dir) for missing_dir in _collect_dirs_missing_init(root)
        )
    return results


@pytest.mark.parametrize(
    "root,directory",
    _all_missing(),
    ids=lambda p: str(p) if isinstance(p, Path) else p,
)
def test_has_init_py(root: str, directory: Path):
    """Every non-test, non-ref package directory must contain an __init__.py."""
    assert (directory / "__init__.py").exists(), (
        f"Missing __init__.py in '{directory}'\n"
        f"  Fix: touch {directory / '__init__.py'}"
    )


def test_root_dirs_exist():
    """All configured ROOT_DIRS must exist so the linter is actually running."""
    missing_roots = [r for r in ROOT_DIRS if not Path(r).exists()]
    assert not missing_roots, (
        f"ROOT_DIRS configured in test_init_files.py not found on disk: "
        f"{missing_roots}\nRun pytest from the project root."
    )
