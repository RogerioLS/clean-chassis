"""Integration tests for Kaggle flavor automation scripts."""

import subprocess
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def test_submit_kaggle_help() -> None:
    """Verifies submit_kaggle.py responds to --help."""
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "submit_kaggle.py"), "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Kaggle Competition Submission Utility" in result.stdout


def test_submit_kaggle_dry_run_status() -> None:
    """Verifies submit_kaggle.py simulates status query with --dry-run."""
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "submit_kaggle.py"),
            "--status",
            "--dry-run",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "[DRY-RUN] Status query simulated successfully" in result.stdout


def test_submit_kaggle_dry_run_with_dummy_archive(tmp_path: Path) -> None:
    """Verifies submit_kaggle.py validates zip package and dry-runs submission."""
    dummy_zip = tmp_path / "submission.zip"
    with zipfile.ZipFile(dummy_zip, "w") as zf:
        zf.writestr("model.py", "# dummy model\n")

    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "submit_kaggle.py"),
            "--file",
            str(dummy_zip),
            "--dry-run",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "[DRY-RUN] Package verified and formatted successfully!" in result.stdout


def test_sync_kaggle_dataset_help() -> None:
    """Verifies sync_kaggle_dataset.py responds to --help."""
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "sync_kaggle_dataset.py"), "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Sync codebase components to a Kaggle Dataset" in result.stdout


def test_sync_kaggle_dataset_dry_run() -> None:
    """Verifies sync_kaggle_dataset.py packages codebase in dry-run mode."""
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "sync_kaggle_dataset.py"),
            "--dry-run",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "[DRY-RUN] Staging area prepared and validated successfully!" in result.stdout
