#!/usr/bin/env python3
"""Shared Kaggle Environment, SSL, and Credential Helpers.

Centralizes `.env` loading, corporate proxy CA bundle discovery, ANSI terminal
colors, and Kaggle API credential resolution across Kaggle automation scripts.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Optional, Tuple


class Colors:
    """ANSI color codes for formatted terminal output."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"


def load_local_env(repo_root: Path) -> None:
    """Loads `.env` defaults and SSL CA bundle configuration if present.

    Args:
        repo_root: Root directory of the repository containing optional `.env`.
    """
    env_file = repo_root / ".env"
    if env_file.is_file():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and "=" in stripped:
                key, value = stripped.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())

    ca_bundle = Path("/etc/ssl/certs/ca-certificates.crt")
    if ca_bundle.exists():
        os.environ.setdefault("REQUESTS_CA_BUNDLE", str(ca_bundle))
        os.environ.setdefault("CURL_CA_BUNDLE", str(ca_bundle))


def _read_kaggle_json(kaggle_json_path: Path) -> Optional[Tuple[str, str]]:
    """Reads `(username, key)` from a `kaggle.json` file if valid."""
    if not kaggle_json_path.is_file():
        return None
    try:
        data = json.loads(kaggle_json_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    username = str(data.get("username", "")).strip()
    key = str(data.get("key", "")).strip()
    if username and key:
        return username, key
    return None


def find_kaggle_credentials(home_dir: Optional[Path] = None) -> Optional[Tuple[str, str]]:
    """Discovers Kaggle credentials from environment variables or `~/.kaggle/`.

    Args:
        home_dir: Optional home directory override for testing. Defaults to `Path.home()`.

    Returns:
        Tuple of `(username, token_or_key)` or `None` if unconfigured.
    """
    kaggle_dir = (home_dir or Path.home()) / ".kaggle"
    json_creds = _read_kaggle_json(kaggle_dir / "kaggle.json")
    fallback_user = json_creds[0] if json_creds else "kaggle_user"

    # 1. Environment variables (highest priority)
    api_token = os.environ.get("KAGGLE_API_TOKEN", "").strip()
    if api_token:
        username = os.environ.get("KAGGLE_USERNAME", "").strip() or fallback_user
        return username, api_token

    user_env = os.environ.get("KAGGLE_USERNAME", "").strip()
    key_env = os.environ.get("KAGGLE_KEY", "").strip()
    if user_env and key_env:
        return user_env, key_env

    # 2. Configuration files in ~/.kaggle (fallback)
    token_file = kaggle_dir / "access_token"
    if token_file.is_file():
        try:
            token = token_file.read_text(encoding="utf-8").strip()
        except OSError:
            return json_creds
        if token:
            username = os.environ.get("KAGGLE_USERNAME", "").strip() or fallback_user
            return username, token

    return json_creds


def build_kaggle_env(creds: Tuple[str, str]) -> Dict[str, str]:
    """Builds a subprocess environment dictionary populated with Kaggle credentials.

    Args:
        creds: Tuple of `(username, key_or_token)`.

    Returns:
        Environment mapping safe to pass to `subprocess.run`.
    """
    env = os.environ.copy()
    env["KAGGLE_USERNAME"] = creds[0]
    env["KAGGLE_KEY"] = creds[1]
    return env
