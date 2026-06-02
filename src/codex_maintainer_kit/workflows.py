from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable, Literal

OutputFormat = Literal["markdown", "json"]


@dataclass(frozen=True)
class Finding:
    label: str
    value: str


def read_input(path: str | None) -> str:
    if path in (None, "-"):
        import sys

        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def first_nonempty_line(text: str, default: str = "Untitled") -> str:
    for line in text.splitlines():
        line = line.strip().lstrip("# ").strip()
        if line:
            return line[:120]
    return default


def bulletize(items: Iterable[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


VISUAL_BUG_TOKENS = (
    "visual bug",
    "layout broken",
    "broken layout",
    "overflow",
    "clipped",
    "clipping",
    "protrude",
    "protrudes",
    "screenshot",
    "mobile layout",
    "desktop layout",
    "responsive",
    "widget",
)

UI_FILE_PATTERNS = (
    ".css",
    ".scss",
    ".sass",
    ".tsx",
    ".jsx",
    "components/",
    "app/",
    "pages/",
)


def looks_like_visual_bug(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in VISUAL_BUG_TOKENS)


def touches_ui_files(files: Iterable[str]) -> bool:
    return any(
        file.endswith(UI_FILE_PATTERNS) or file.startswith(UI_FILE_PATTERNS)
        for file in files
    )


def detect_issue_type(text: str) -> str:
    lowered = text.lower()
    if looks_like_visual_bug(text):
        return "visual bug"
    if any(token in lowered for token in ["traceback", "error", "bug", "crash", "regression", "fail"]):
        return "bug"
    if any(token in lowered for token in ["docs", "readme", "documentation"]):
        return "docs"
    if any(token in lowered for token in ["feature", "request", "support", "add"]):
        return "feature"
    return "question/triage"


def detect_priority(text: str) -> str:
    lowered = text.lower()
    if any(token in lowered for token in ["security", "data loss", "production", "urgent", "critical"]):
        return "high"
    if any(token in lowered for token in ["regression", "broken", "blocking", "cannot", "crash", "traceback"]):
        return "medium"
    return "low"


def changed_files_from_diff(diff: str) -> list[str]:
    files: list[str] = []
    for match in re.finditer(r"^\+\+\+ b/(.+)$", diff, re.MULTILINE):
        name = match.group(1).strip()
        if name != "/dev/null":
            files.append(name)
    return sorted(set(files))


def summarize_diff(diff: str) -> tuple[int, int, list[str]]:
    additions = sum(1 for line in diff.splitlines() if line.startswith("+") and not line.startswith("+++"))
    deletions = sum(1 for line in diff.splitlines() if line.startswith("-") and not line.startswith("---"))
    return additions, deletions, changed_files_from_diff(diff)


def render_issue(text: str) -> str:
    title = first_nonempty_line(text, "Issue")
    issue_type = detect_issue_type(text)
    priority = detect_priority(text)
    return f"""# Maintainer triage: {title}

## Classification
- Type: {issue_type}
- Priority: {priority}
- Confidence: heuristic draft; maintainer should confirm

## Reproducibility checklist
- [ ] Confirm expected behavior
- [ ] Confirm actual behavior
- [ ] Capture environment/version
- [ ] Add or identify a regression test
- [ ] Decide whether Codex can safely attempt a fix

## Codex-ready task brief
Goal: Resolve or clarify `{title}`.

Context to inspect:
- Read the issue report and linked files.
- Search for tests covering the reported behavior.
- Prefer a minimal regression test before implementation.

Definition of done:
- The root cause is explained in the PR or issue comment.
- Relevant tests pass locally.
- User-facing docs are updated if behavior changed.

## Maintainer reply draft
Thanks for the report. I will verify the reproduction path, check whether this is a regression, and prepare a focused fix or follow-up question.
"""


def render_pr(diff: str) -> str:
    additions, deletions, files = summarize_diff(diff)
    file_lines = bulletize(files) if files else "- No changed files detected from unified diff headers"
    risk = "high" if any(f.startswith(("auth", "security", "api", "src/auth")) for f in files) else "medium" if additions + deletions > 250 else "low"
    visual_section = """

## Visual QA checklist
- [ ] Mobile and desktop visual check completed
- [ ] Overflow/clipping verified
- [ ] No unrelated layout shift observed
- [ ] Before/after screenshot or browser check captured
""" if touches_ui_files(files) else ""
    return f"""# PR review brief

## Diff summary
- Files changed: {len(files)}
- Additions: {additions}
- Deletions: {deletions}
- Initial risk: {risk}

## Files to inspect
{file_lines}

## Review checklist
- [ ] Does the change match the stated PR goal?
- [ ] Are edge cases covered by tests?
- [ ] Are security-sensitive paths affected?
- [ ] Are errors handled clearly?
- [ ] Are docs or examples needed?
{visual_section}

## Codex review prompt
Review this diff as an open-source maintainer. Focus on correctness, tests, regressions, security-sensitive behavior, and whether the implementation is smaller than the problem requires. Return blocking issues first, then non-blocking suggestions.
"""


def render_release(log_text: str) -> str:
    lines = [line.strip() for line in log_text.splitlines() if line.strip()]
    features = [line for line in lines if re.search(r"\b(feat|add|introduce)\b", line, re.I)]
    fixes = [line for line in lines if re.search(r"\b(fix|bug|patch|resolve)\b", line, re.I)]
    docs = [line for line in lines if re.search(r"\b(doc|readme|example)\b", line, re.I)]
    other = [line for line in lines if line not in features + fixes + docs]

    def section(title: str, items: list[str]) -> str:
        return f"## {title}\n" + (bulletize(items) if items else "- None")

    return "\n\n".join(
        [
            "# Release notes draft",
            section("Features", features),
            section("Fixes", fixes),
            section("Docs", docs),
            section("Other changes", other[:12]),
            "## Maintainer checklist\n- [ ] Confirm version number\n- [ ] Confirm breaking changes\n- [ ] Confirm migration notes\n- [ ] Confirm CI passed before tagging",
        ]
    )


def render_codex_task(text: str, mode: str = "implementation") -> str:
    title = first_nonempty_line(text, "Maintainer task")
    return f"""# Codex task brief: {title}

## Goal
Prepare a safe {mode} workflow for: {title}

## Context
{text.strip()[:2000]}

## Instructions for Codex
1. Inspect the repository before changing files.
2. Identify the smallest set of files needed for the task.
3. If this is a bug, write or update a regression test first.
4. Make the minimal implementation change.
5. Run the relevant tests and report exact commands/results.
6. Do not touch secrets, credentials, unrelated formatting, or generated files unless required.

## Definition of done
- [ ] Behavior matches the issue or maintainer request
- [ ] Tests or documented verification are included
- [ ] Risky assumptions are listed
- [ ] Final response includes changed files and commands run

## Suggested Codex CLI command
```bash
codex exec --sandbox workspace-write --ask-for-approval on-request "$(cat codex-task.md)"
```
"""


def render_visual(text: str) -> str:
    title = first_nonempty_line(text, "Visual issue")
    return f"""# Visual bug brief: {title}

## Goal
Fix the reported visual issue with the smallest safe UI/layout change.

## Context
{text.strip()[:2000]}

## Likely inspection targets
- Component or template that renders the affected surface
- CSS/Tailwind classes controlling size, overflow, position, z-index, and breakpoints
- Any embedded media/canvas/iframe/SVG that may escape its container

## Screenshot QA checklist
- [ ] Confirm expected visual state from the report or design intent
- [ ] Compare before/after screenshots
- [ ] Check mobile and desktop breakpoints
- [ ] Verify overflow, clipping, z-index, and sticky/fixed positioning
- [ ] Confirm no unrelated layout shift on nearby content

## Browser verification
- Open the exact URL or route where the screenshot was taken
- Inspect the affected element's bounding rectangle and computed overflow/position styles
- Re-check after deploy or cache-busted production load if this is a live-site fix

## Codex implementation guardrails
1. Inspect the relevant UI files before editing.
2. Prefer the smallest visual containment/layout fix.
3. Do not change APIs, credentials, business copy, or unrelated data flows.
4. Run the project's typecheck/build and any UI/source-contract checks.
5. Report changed files, commands run, and visual verification evidence.
"""
