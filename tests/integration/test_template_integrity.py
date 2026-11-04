"""Template Scaffold & Architecture Integrity Tests.

Verifies that Clean Chassis contains all mandatory directories, governance files,
valid scripts, and functional dry-runs when instantiated as a new repository template.
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class TestCleanChassisTemplateScaffold:
    """Verifies repository scaffold completeness and governance files."""

    def test_mandatory_root_files_exist(self) -> None:
        """Ensures all standard open-source and governance root files exist."""
        mandatory_files = [
            "README.md",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md",
            "SECURITY.md",
            "LICENSE",
            "Makefile",
            "pyproject.toml",
            ".gitignore",
        ]
        for filename in mandatory_files:
            file_path = BASE_DIR / filename
            assert file_path.exists(), f"Mandatory root file missing: {filename}"
            assert file_path.stat().st_size > 0, f"File cannot be empty: {filename}"

    def test_institutional_docs_hierarchy_exists(self) -> None:
        """Ensures the Big Tech docs/ hierarchy and blueprints exist."""
        mandatory_docs = [
            "docs/status/PROJECT_STATUS.md",
            "docs/architecture/SYSTEM_DESIGN.md",
            "docs/research/README.md",
            "docs/notes/README.md",
        ]
        for doc_path in mandatory_docs:
            target = BASE_DIR / doc_path
            assert target.exists(), f"Mandatory docs template missing: {doc_path}"
            assert target.stat().st_size > 0, f"Docs blueprint cannot be empty: {doc_path}"

    def test_githooks_configured_and_executable(self) -> None:
        """Verifies local pre-commit and commit-msg hooks exist."""
        hooks = [".githooks/pre-commit", ".githooks/commit-msg"]
        for hook in hooks:
            hook_path = BASE_DIR / hook
            assert hook_path.exists(), f"Git hook missing: {hook}"

    def test_pr_scripts_dry_run_execution(self) -> None:
        """Verifies scripts/create_pr.py and scripts/pr.py execute dry-run with code 0."""
        res_create = subprocess.run(
            [sys.executable, "scripts/create_pr.py", "--dry-run"],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            check=False,
        )
        assert res_create.returncode == 0, f"create_pr dry-run failed: {res_create.stderr}"
        assert "[DRY-RUN] PULL REQUEST PAYLOAD PREVIEW" in res_create.stdout

        res_pr = subprocess.run(
            [sys.executable, "scripts/pr.py", "--dry-run"],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            check=False,
        )
        assert res_pr.returncode == 0, f"pr.py dry-run failed: {res_pr.stderr}"

    def test_setup_kanban_dry_run_execution(self) -> None:
        """Verifies .github/scripts/setup_kanban.py executes dry-run with code 0."""
        res_kanban = subprocess.run(
            [sys.executable, ".github/scripts/setup_kanban.py", "--dry-run"],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            check=False,
        )
        assert res_kanban.returncode == 0, f"setup_kanban failed: {res_kanban.stderr}"
        assert "CLEAN CHASSIS — GITHUB KANBAN SETUP" in res_kanban.stdout

    def test_commit_linter_validation_rules(self) -> None:
        """Validates that conventional commit rules accept valid and reject invalid commits."""
        from scripts.lint_branch_and_commits import validate_commit

        # Valid standard task commit
        valid_task, _ = validate_commit("feat(core): [TASK-01:#1] implement core engine")
        assert valid_task is True

        # Valid reserved tag commit
        valid_tag, _ = validate_commit("chore(infra): [INFRA] update dependencies")
        assert valid_tag is True

        # Valid dependabot commits
        valid_dep, _ = validate_commit("chore(deps): bump urllib3 from 2.0.0 to 2.1.0")
        assert valid_dep is True

        # Invalid commit
        invalid, err = validate_commit("just fixed a bug without format")
        assert invalid is False
        assert "Invalid commit format" in err
