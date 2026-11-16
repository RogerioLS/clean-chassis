"""Integration tests for Kaggle flavor automation scripts and template hygiene."""

import os
import subprocess
import sys
import zipfile
from pathlib import Path

from scripts.kaggle_utils import find_kaggle_credentials
from scripts.submit_kaggle import resolve_default_submission_path, validate_submission_package
from scripts.sync_kaggle_dataset import KaggleDatasetSync

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def test_env_example_exists_with_required_keys() -> None:
    """Verifies .env.example exists and declares standard Kaggle configuration keys."""
    env_example = REPO_ROOT / ".env.example"
    assert env_example.is_file()
    content = env_example.read_text(encoding="utf-8")
    for key in (
        "KAGGLE_USERNAME=",
        "KAGGLE_API_TOKEN=",
        "KAGGLE_KEY=",
        "KAGGLE_COMPETITION=",
        "KAGGLE_DATASET_SLUG=",
        "REQUESTS_CA_BUNDLE=",
    ):
        assert key in content


def test_no_hardcoded_personal_or_legacy_project_defaults() -> None:
    """Verifies Kaggle template scripts avoid hardcoded personal or legacy slugs."""
    for rel_path in (
        "scripts/kaggle_utils.py",
        "scripts/submit_kaggle.py",
        "scripts/sync_kaggle_dataset.py",
    ):
        text = (REPO_ROOT / rel_path).read_text(encoding="utf-8")
        assert "rogeriolopesdasilva" not in text
        assert "gemma-agent-code" not in text


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


def test_submit_kaggle_validates_csv_and_parquet(tmp_path: Path, monkeypatch) -> None:
    """Verifies submit_kaggle validates valid/invalid CSV and Parquet submissions."""
    valid_csv = tmp_path / "submission.csv"
    valid_csv.write_text("id,target\n1,0.5\n", encoding="utf-8")
    ok_csv, errs_csv = validate_submission_package(valid_csv)
    assert ok_csv is True
    assert errs_csv == []

    header_only_csv = tmp_path / "empty_rows.csv"
    header_only_csv.write_text("id,target\n", encoding="utf-8")
    bad_csv, errs_bad_csv = validate_submission_package(header_only_csv)
    assert bad_csv is False
    assert any("no data rows" in err for err in errs_bad_csv)

    # Verify hermetic Parquet magic-byte check when pandas is not installed
    monkeypatch.setitem(sys.modules, "pandas", None)
    valid_parquet = tmp_path / "submission.parquet"
    valid_parquet.write_bytes(b"PAR1" + b"\x00" * 16 + b"PAR1")
    ok_pq, errs_pq = validate_submission_package(valid_parquet)
    assert ok_pq is True
    assert errs_pq == []

    corrupt_parquet = tmp_path / "corrupt.parquet"
    corrupt_parquet.write_bytes(b"NOTPARQUET_DATA")
    bad_pq, errs_bad_pq = validate_submission_package(corrupt_parquet)
    assert bad_pq is False
    assert any("Parquet magic" in err for err in errs_bad_pq)


def test_resolve_default_submission_path_priority(tmp_path: Path) -> None:
    """Verifies default submission discovery prefers artifacts/submission.parquet over zip."""
    artifacts = tmp_path / "artifacts"
    artifacts.mkdir()
    zip_path = artifacts / "submission.zip"
    zip_path.write_bytes(b"zip")
    assert resolve_default_submission_path(tmp_path) == zip_path

    parquet_path = artifacts / "submission.parquet"
    parquet_path.write_bytes(b"PAR1")
    assert resolve_default_submission_path(tmp_path) == parquet_path


def test_find_kaggle_credentials_uses_kaggle_json_fallback(tmp_path: Path, monkeypatch) -> None:
    """Verifies find_kaggle_credentials avoids hardcoded usernames via home kaggle.json."""
    for var in ("KAGGLE_API_TOKEN", "KAGGLE_USERNAME", "KAGGLE_KEY"):
        monkeypatch.delenv(var, raising=False)

    kaggle_dir = tmp_path / ".kaggle"
    kaggle_dir.mkdir()
    (kaggle_dir / "kaggle.json").write_text(
        '{"username": "alice_competitor", "key": "secret_key_123"}',
        encoding="utf-8",
    )

    creds = find_kaggle_credentials(home_dir=tmp_path)
    assert creds == ("alice_competitor", "secret_key_123")


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


def test_sync_kaggle_dataset_includes_notebooks_and_excludes_secrets(tmp_path: Path) -> None:
    """Verifies KaggleDatasetSync stages notebooks/src/scripts while excluding secrets."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "pipeline.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "notebooks" / "exp1").mkdir(parents=True)
    (tmp_path / "notebooks" / "exp1" / "train.ipynb").write_text("{}", encoding="utf-8")
    (tmp_path / "notebooks" / "exp1" / "output").mkdir()
    (tmp_path / "notebooks" / "exp1" / "output" / "model.bin").write_bytes(b"weights")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / ".env").write_text("KAGGLE_KEY=leak\n", encoding="utf-8")
    (tmp_path / "scripts" / "api_token.txt").write_text("secret\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")

    staging = tmp_path / "artifacts" / "staging"
    syncer = KaggleDatasetSync(
        repo_root=tmp_path,
        dataset_slug="alice/demo-comp",
        title="Demo Comp",
        staging_dir=staging,
        dry_run=True,
    )
    exit_code = syncer.sync(message="test sync")
    assert exit_code == 0
    assert (staging / "src" / "pipeline.py").is_file()
    assert (staging / "notebooks" / "exp1" / "train.ipynb").is_file()
    assert (staging / "dataset-metadata.json").is_file()
    assert not (staging / "notebooks" / "exp1" / "output" / "model.bin").exists()
    assert not (staging / "scripts" / ".env").exists()
    assert not (staging / "scripts" / "api_token.txt").exists()
    assert os.path.exists(staging / "README.md")
