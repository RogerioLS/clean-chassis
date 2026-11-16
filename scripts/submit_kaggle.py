#!/usr/bin/env python3
"""Kaggle Competition Submission Utility.

Provides pre-submission package validation (`.zip`, `.parquet`, `.csv`, or
competition-specific hooks), credential discovery, Kaggle CLI dispatch, and
leaderboard submission status querying.

Usage:
    python3 scripts/submit_kaggle.py --dry-run
    python3 scripts/submit_kaggle.py --message "Submission v1.0"
    python3 scripts/submit_kaggle.py --status
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.kaggle_utils import (  # noqa: E402
    Colors,
    build_kaggle_env,
    find_kaggle_credentials,
    load_local_env,
)

load_local_env(REPO_ROOT)

DEFAULT_COMPETITION = os.environ.get("KAGGLE_COMPETITION", "").strip() or "kaggle-competition-slug"

_CANDIDATE_SUBMISSIONS = (
    Path("artifacts") / "submission.parquet",
    Path("artifacts") / "submission.csv",
    Path("artifacts") / "submission.zip",
    Path("submission") / "submission.parquet",
    Path("submission") / "submission.csv",
    Path("submission") / "submission.zip",
)


def resolve_default_submission_path(repo_root: Path = REPO_ROOT) -> Path:
    """Resolves the default submission artifact across standard output locations.

    Args:
        repo_root: Repository root directory.

    Returns:
        First existing candidate submission path, or `artifacts/submission.zip`.
    """
    for rel_path in _CANDIDATE_SUBMISSIONS:
        candidate = repo_root / rel_path
        if candidate.is_file():
            return candidate
    return repo_root / "artifacts" / "submission.zip"


DEFAULT_SUBMISSION_PATH = resolve_default_submission_path()


def compute_file_sha256(filepath: Path) -> str:
    """Computes hexadecimal SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as file_handle:
        while chunk := file_handle.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def _run_custom_validator(package_path: Path) -> Tuple[bool, bool, List[str]]:
    """Attempts dynamic import of a competition-specific `SubmissionValidator`.

    Returns:
        Tuple of `(handled, is_valid, errors)`.
    """
    validator_modules = (
        "competitions.submission.validator",
        "src.submission.validator",
    )
    for module_name in validator_modules:
        try:
            val_mod = importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue
        except Exception as exc:
            return True, False, [f"Competition validator import error ({module_name}): {exc}"]

        validator_cls = getattr(val_mod, "SubmissionValidator", None)
        if validator_cls is not None:
            try:
                result = validator_cls(package_path).validate()
                return True, bool(result.passed), list(result.errors)
            except Exception as exc:
                return True, False, [f"Competition validator check encountered error: {exc}"]

    return False, True, []


def _validate_zip(package_path: Path) -> List[str]:
    """Validates zip archive integrity and ensures it contains at least one entry."""
    errors: List[str] = []
    try:
        with zipfile.ZipFile(package_path, "r") as zf:
            bad_file = zf.testzip()
            if bad_file:
                errors.append(f"Corrupted file inside archive: {bad_file}")
            if not zf.infolist():
                errors.append("Submission archive is empty.")
    except zipfile.BadZipFile:
        errors.append(f"File is not a valid zip archive: {package_path}")
    return errors


def _validate_parquet(package_path: Path) -> List[str]:
    """Validates Parquet magic bytes and delegates to repo/pandas validator if present."""
    errors: List[str] = []
    size = package_path.stat().st_size
    if size < 12:
        return [f"Parquet submission file is too small ({size} bytes): {package_path}"]

    with open(package_path, "rb") as file_handle:
        header = file_handle.read(4)
        file_handle.seek(-4, os.SEEK_END)
        footer = file_handle.read(4)

    if header != b"PAR1" or footer != b"PAR1":
        return [f"File does not have valid Parquet magic header/footer: {package_path}"]

    try:
        import pandas as pd  # type: ignore[import-not-found]
    except ModuleNotFoundError:
        return errors

    try:
        df = pd.read_parquet(package_path)
        if df.empty:
            errors.append("Parquet submission dataframe is empty.")
            return errors
        try:
            exporter = importlib.import_module("src.submission.parquet_exporter")
            validator_fn = getattr(exporter, "validate_submission_dataframe", None)
            if callable(validator_fn):
                validator_fn(df)
        except ModuleNotFoundError:
            pass
    except Exception as exc:
        errors.append(f"Parquet submission validation failed: {exc}")

    return errors


def _validate_csv(package_path: Path) -> List[str]:
    """Validates that a CSV submission has a valid header and at least one data row."""
    try:
        with open(package_path, "r", encoding="utf-8", newline="") as file_handle:
            reader = csv.reader(file_handle)
            header = next(reader, None)
            if not header or not any(cell.strip() for cell in header):
                return ["CSV submission is missing a header row."]
            first_row = next(reader, None)
            if first_row is None:
                return ["CSV submission contains no data rows."]
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        return [f"CSV submission validation failed: {exc}"]
    return []


def validate_submission_package(package_path: Path) -> Tuple[bool, List[str]]:
    """Validates structure, non-emptiness, and format compliance of a submission file.

    Supports custom competition validators (`SubmissionValidator`), `.zip`,
    `.parquet`, and `.csv` submission artifacts.

    Args:
        package_path: Path to the submission artifact.

    Returns:
        Tuple of `(is_valid, error_list)`.
    """
    if not package_path.is_file():
        return False, [f"Submission file not found at: {package_path}"]

    if package_path.stat().st_size == 0:
        return False, [f"Submission file is empty: {package_path}"]

    handled, custom_valid, custom_errors = _run_custom_validator(package_path)
    if handled:
        return custom_valid, custom_errors

    suffix = package_path.suffix.lower()
    validators = {
        ".zip": _validate_zip,
        ".parquet": _validate_parquet,
        ".csv": _validate_csv,
    }
    validator_fn = validators.get(suffix)
    errors = validator_fn(package_path) if validator_fn else []
    return len(errors) == 0, errors


def execute_kaggle_submission(
    competition: str,
    package_path: Path,
    message: str,
    dry_run: bool = False,
) -> int:
    """Dispatches submission artifact to Kaggle competition via CLI or dry-run simulation.

    Args:
        competition: Kaggle competition slug.
        package_path: Path to the validated submission artifact.
        message: Descriptive submission message.
        dry_run: When True, simulates submission without invoking external networks.

    Returns:
        Exit code (0 on success, non-zero on failure).
    """
    sha256 = compute_file_sha256(package_path)
    size_bytes = package_path.stat().st_size
    creds = find_kaggle_credentials()

    print(f"{Colors.BOLD}{Colors.BLUE}==================================================")
    print(f" 🚀 KAGGLE SUBMISSION DISPATCH: {competition.upper()}")
    print(f"=================================================={Colors.RESET}")
    print(f"  Archive   : {package_path}")
    print(f"  Size      : {size_bytes:,} bytes")
    print(f"  SHA-256   : {sha256}")
    print(f'  Message   : "{message}"')
    print(f"  Auth User : {creds[0] if creds else 'None (Unconfigured)'}")
    print(f"{Colors.BLUE}--------------------------------------------------{Colors.RESET}")

    if dry_run:
        print(f"{Colors.GREEN}✔ [DRY-RUN] Package verified and formatted successfully!")
        print(f"✔ [DRY-RUN] Ready to submit to competition: '{competition}'{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}To submit live, run:{Colors.RESET}")
        print(f'  kaggle competitions submit -c {competition} -f {package_path} -m "{message}"\n')
        return 0

    if not creds:
        print(f"{Colors.RED}❌ Error: Kaggle API credentials not found.{Colors.RESET}")
        print("Please configure credentials via .env, ~/.kaggle/kaggle.json, or environment:")
        print('  export KAGGLE_USERNAME="your_username"')
        print('  export KAGGLE_KEY="your_api_key"')
        return 1

    kaggle_bin = shutil.which("kaggle")
    if not kaggle_bin:
        print(f"{Colors.RED}❌ Error: 'kaggle' CLI not installed in environment.{Colors.RESET}")
        print("Install via: pip install kaggle")
        return 1

    cmd = [
        kaggle_bin,
        "competitions",
        "submit",
        "-c",
        competition,
        "-f",
        str(package_path),
        "-m",
        message,
    ]

    print(f"{Colors.CYAN}📡 Submitting artifact to Kaggle...{Colors.RESET}")
    env = build_kaggle_env(creds)

    try:
        proc = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
        print(f"{Colors.GREEN}✔ Submission successfully submitted!{Colors.RESET}")
        if proc.stdout:
            print(proc.stdout)
        return 0
    except subprocess.CalledProcessError as exc:
        print(f"{Colors.RED}❌ Submission failed with error code {exc.returncode}:{Colors.RESET}")
        if exc.stderr:
            print(exc.stderr)
        return exc.returncode


def query_submission_status(competition: str, dry_run: bool = False) -> int:
    """Queries and displays recent submissions for the competition."""
    print(
        f"{Colors.BOLD}{Colors.BLUE}📊 Querying recent submissions for: "
        f"{competition}{Colors.RESET}"
    )
    if dry_run:
        print(f"{Colors.GREEN}✔ [DRY-RUN] Status query simulated successfully.{Colors.RESET}")
        return 0

    kaggle_bin = shutil.which("kaggle")
    creds = find_kaggle_credentials()

    if not creds:
        print(f"{Colors.RED}❌ Error: Kaggle credentials not configured.{Colors.RESET}")
        return 1

    if not kaggle_bin:
        print(f"{Colors.RED}❌ Error: 'kaggle' CLI not installed.{Colors.RESET}")
        return 1

    cmd = [kaggle_bin, "competitions", "submissions", "-c", competition]
    env = build_kaggle_env(creds)

    try:
        proc = subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
        if proc.stdout:
            print(proc.stdout)
        return 0
    except subprocess.CalledProcessError as exc:
        print(f"{Colors.RED}❌ Query failed: {exc.stderr}{Colors.RESET}")
        return exc.returncode


def main() -> int:
    """CLI entrypoint for Kaggle submission automation."""
    default_path = resolve_default_submission_path()
    parser = argparse.ArgumentParser(description="Kaggle Competition Submission Utility")
    parser.add_argument(
        "--file",
        type=str,
        default=str(default_path),
        help=f"Path to submission file (default: {default_path})",
    )
    parser.add_argument(
        "--competition",
        type=str,
        default=DEFAULT_COMPETITION,
        help=f"Kaggle competition slug (default: {DEFAULT_COMPETITION})",
    )
    parser.add_argument(
        "--message",
        type=str,
        default="Kaggle automated submission",
        help="Submission description message",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate validation and submission without network calls",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Query status of recent submissions instead of submitting",
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip pre-submission validator check",
    )

    args = parser.parse_args()

    if args.status:
        return query_submission_status(args.competition, dry_run=args.dry_run)

    package_path = Path(args.file).resolve()
    if not args.skip_validation:
        print(f"{Colors.CYAN}🔍 Validating submission package before dispatch...{Colors.RESET}")
        is_valid, errors = validate_submission_package(package_path)
        if not is_valid:
            print(f"{Colors.RED}❌ Pre-submission validation failed:{Colors.RESET}")
            for err in errors:
                print(f"  - {err}")
            return 1
        print(f"{Colors.GREEN}✔ Pre-submission package validation passed!{Colors.RESET}\n")

    return execute_kaggle_submission(
        competition=args.competition,
        package_path=package_path,
        message=args.message,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    sys.exit(main())
