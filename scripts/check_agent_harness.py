#!/usr/bin/env python3
"""Agent Harness Integrity & Governance Checker.

Validates `.agents/` protocol completeness (AGENTS.md, rules, skills),
canonical `docs/` structure (no README.md inside docs/), git hooks, and
`.github/issues/` task-to-issue linkage.

Usage:
    python3 scripts/check_agent_harness.py
    python3 scripts/check_agent_harness.py --strict-issue
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.kaggle_utils import Colors  # noqa: E402

EXPECTED_RULES = (
    "00_clean_chassis_governance.md",
    "01_clean_architecture.md",
    "02_security_and_anti_cheating.md",
    "03_git_workflow_and_commits.md",
    "04_testing_and_benchmarking.md",
    "05_agent_operating_guidelines.md",
    "06_documentation_and_summary.md",
    "07_terminal_and_minimalism.md",
    "08_pragmatic_minimalism_and_experiments.md",
)

EXPECTED_SKILLS = (
    "audit-enforcer",
    "competition-orchestrator",
    "documentation-steward",
    "git-governance",
    "kaggle-submission-guard",
    "kanban-task-tracker",
)

CANONICAL_DOCS = (
    "docs/status/PROJECT_STATUS.md",
    "docs/status/HANDOFF_RESUME.md",
    "docs/architecture/SYSTEM_DESIGN.md",
    "docs/research/BENCHMARK_ANALYSIS.md",
    "docs/research/DATASET_EDA.md",
    "docs/notes/MASTER_MEMORY_COMPILATION.md",
)


def _check_agents_layer(repo_root: Path) -> List[str]:
    """Validates AGENTS.md, rules, and skill frontmatter definitions."""
    errors: List[str] = []
    agents_md = repo_root / ".agents" / "AGENTS.md"
    if not agents_md.is_file() or agents_md.stat().st_size == 0:
        errors.append("Missing or empty .agents/AGENTS.md")

    rules_dir = repo_root / ".agents" / "rules"
    for rule_name in EXPECTED_RULES:
        rule_path = rules_dir / rule_name
        if not rule_path.is_file() or rule_path.stat().st_size == 0:
            errors.append(f"Missing or empty rule: .agents/rules/{rule_name}")

    skills_dir = repo_root / ".agents" / "skills"
    for skill_name in EXPECTED_SKILLS:
        skill_file = skills_dir / skill_name / "SKILL.md"
        if not skill_file.is_file() or skill_file.stat().st_size == 0:
            errors.append(f"Missing or empty skill: .agents/skills/{skill_name}/SKILL.md")
            continue
        content = skill_file.read_text(encoding="utf-8")
        if f"name: {skill_name}" not in content or "description:" not in content:
            errors.append(f"Invalid frontmatter in .agents/skills/{skill_name}/SKILL.md")

    return errors


def _check_docs_layer(repo_root: Path) -> List[str]:
    """Validates canonical docs files and ensures no README.md lives inside docs/."""
    errors: List[str] = []
    for rel_doc in CANONICAL_DOCS:
        target = repo_root / rel_doc
        if not target.is_file() or target.stat().st_size == 0:
            errors.append(f"Missing or empty canonical doc: {rel_doc}")

    docs_dir = repo_root / "docs"
    if docs_dir.is_dir():
        for readme in sorted(docs_dir.rglob("README.md")):
            errors.append(f"Forbidden README.md inside docs/: {readme.relative_to(repo_root)}")

    return errors


def _check_hooks_and_issues(
    repo_root: Path,
    strict_issue: bool = False,
    branch_name: str | None = None,
) -> Tuple[List[str], List[str]]:
    """Validates git hooks, task files in .github/issues/, and branch-to-task linkage."""
    errors: List[str] = []
    warnings: List[str] = []

    for hook in (".githooks/pre-commit", ".githooks/commit-msg"):
        if not (repo_root / hook).is_file():
            errors.append(f"Missing required git hook: {hook}")

    issues_dir = repo_root / ".github" / "issues"
    task_files = sorted(issues_dir.glob("*.md")) if issues_dir.is_dir() else []

    for task_file in task_files:
        text = task_file.read_text(encoding="utf-8")
        if not re.search(r"^id:\s*[A-Za-z0-9_-]+", text, re.MULTILINE):
            errors.append(f"Task file missing frontmatter 'id:': {task_file.name}")
        has_unchecked = "- [ ]" in text
        has_issue_num = bool(re.search(r"^github_issue:\s*\d+", text, re.MULTILINE))
        if has_unchecked and not has_issue_num:
            msg = f"Open task '{task_file.name}' has no 'github_issue: <NUM>' bound yet."
            if strict_issue:
                errors.append(msg)
            else:
                warnings.append(msg)

    active_branch = branch_name if branch_name is not None else _detect_git_branch(repo_root)
    if active_branch:
        match = re.search(r"^(?:feat|fix|docs|refactor|test|chore)/(task-\d+)", active_branch)
        if match:
            task_prefix = match.group(1).lower()
            if not any(task_prefix in tf.name.lower() for tf in task_files):
                errors.append(
                    f"Active branch '{active_branch}' references '{task_prefix}' "
                    "without a matching file in .github/issues/."
                )

    return errors, warnings


def _detect_git_branch(repo_root: Path) -> str:
    """Returns current git branch name or empty string if unavailable."""
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=False,
        )
        return proc.stdout.strip() if proc.returncode == 0 else ""
    except OSError:
        return ""


def verify_agent_harness(
    repo_root: Path = REPO_ROOT,
    strict_issue: bool = False,
    branch_name: str | None = None,
) -> Tuple[bool, List[str], List[str]]:
    """Runs all agent harness checks and returns `(passed, errors, warnings)`."""
    errors: List[str] = []
    errors.extend(_check_agents_layer(repo_root))
    errors.extend(_check_docs_layer(repo_root))
    hook_errors, warnings = _check_hooks_and_issues(
        repo_root, strict_issue=strict_issue, branch_name=branch_name
    )
    errors.extend(hook_errors)
    return len(errors) == 0, errors, warnings


def main() -> int:
    """CLI entrypoint for agent harness verification."""
    parser = argparse.ArgumentParser(description="Verify Clean Chassis agent harness integrity.")
    parser.add_argument(
        "--strict-issue",
        action="store_true",
        help="Fail if any open task in .github/issues/ lacks 'github_issue: <NUM>'.",
    )
    args = parser.parse_args()

    passed, errors, warnings = verify_agent_harness(REPO_ROOT, strict_issue=args.strict_issue)

    print(
        f"{Colors.BOLD}{Colors.BLUE}🛡️  [HARNESS] Validating .agents/, docs/, and "
        f"governance...{Colors.RESET}"
    )
    for warn in warnings:
        print(f"{Colors.YELLOW}  ⚠ {warn}{Colors.RESET}")

    if not passed:
        print(f"{Colors.RED}❌ Agent harness check failed:{Colors.RESET}")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(
        f"{Colors.GREEN}✔ Agent harness verified ({len(EXPECTED_RULES)} rules, "
        f"{len(EXPECTED_SKILLS)} skills, {len(CANONICAL_DOCS)} canonical docs).{Colors.RESET}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
