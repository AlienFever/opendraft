#!/usr/bin/env python3
"""
ABOUTME: Regression test for #26 — packaging config must include all subpackages and prompt files
ABOUTME: Guards against re-introducing `packages = ["engine"]` (which silently drops subpackages)
"""

import os
import re
import sys
import tomllib
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = REPO_ROOT / "pyproject.toml"


def _load_pyproject() -> dict:
    with open(PYPROJECT, "rb") as f:
        return tomllib.load(f)


def test_pyproject_uses_find_or_lists_all_subpackages():
    """pyproject.toml must discover all subpackages, not just the top-level 'engine'.

    Bug: `packages = ["engine"]` shipped only engine/__init__.py and top-level
    modules — `engine.concurrency`, `engine.opendraft`, `engine.phases`,
    `engine.utils`, and the `prompts/*.md` data files were silently dropped
    from the wheel, causing FileNotFoundError at runtime (see issue #26).
    """
    cfg = _load_pyproject()
    setuptools = cfg.get("tool", {}).get("setuptools", {})

    has_find = "find" in setuptools.get("packages", {})
    explicit = setuptools.get("packages")
    if isinstance(explicit, list):
        explicit_set = set(explicit)
    else:
        explicit_set = set()

    if not has_find:
        # If not using find:, the explicit list must include every subpackage
        # we know about in this repo.
        required = {
            "engine",
            "engine.concurrency",
            "engine.opendraft",
            "engine.phases",
            "engine.utils",
            "engine.utils.api_citations",
            "engine.utils.pdf_engines",
        }
        missing = required - explicit_set
        assert not missing, (
            f"pyproject.toml packages list is missing subpackages: {sorted(missing)}. "
            f"Either use [tool.setuptools.packages.find] (recommended) or list every "
            f"subpackage explicitly. See https://github.com/federicodeponte/opendraft/issues/26"
        )


def test_prompt_files_present_on_disk():
    """The prompt files referenced by the package must exist in the repo.

    Catches a different failure mode: even with packages.find working, a
    renamed/relocated prompt file should be caught here before it ships.
    """
    prompts_dir = REPO_ROOT / "engine" / "prompts"
    assert prompts_dir.is_dir(), f"Prompts directory missing: {prompts_dir}"

    # The specific file the user reported as missing in issue #26.
    scribe = prompts_dir / "01_research" / "scribe.md"
    assert scribe.is_file(), (
        f"Prompt file missing: {scribe}. This is the exact file from issue #26."
    )

    # Sanity check: at least the top-level prompt subdirs should have content.
    for sub in ("01_research", "02_structure", "03_compose", "04_validate"):
        sub_dir = prompts_dir / sub
        assert sub_dir.is_dir(), f"Prompt subdir missing: {sub_dir}"
        assert any(sub_dir.glob("*.md")), f"No .md files in {sub_dir}"


def test_prompt_files_declared_in_package_data():
    """package-data must include prompt files so they end up in the wheel."""
    cfg = _load_pyproject()
    pkg_data = cfg.get("tool", {}).get("setuptools", {}).get("package-data", {})

    assert "engine" in pkg_data, (
        "[tool.setuptools.package-data] is missing the 'engine' key — "
        "prompt .md files will not be shipped in the wheel."
    )

    globs = pkg_data["engine"]
    assert any("prompts" in g and g.endswith(".md") for g in globs), (
        f"package-data for 'engine' should include prompts/**/*.md, got: {globs}"
    )
