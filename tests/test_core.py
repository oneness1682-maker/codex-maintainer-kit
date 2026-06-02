from codex_maintainer_kit.core import (
    changed_files_from_diff,
    detect_issue_type,
    detect_priority,
    render_codex_task,
    render_issue,
    render_pr,
    render_release,
)


def test_issue_triage_detects_bug_and_priority() -> None:
    text = "# Crash in production\nTraceback when saving settings"
    output = render_issue(text)
    assert "Type: bug" in output
    assert "Priority: high" in output
    assert "Codex-ready task brief" in output


def test_issue_type_docs() -> None:
    assert detect_issue_type("README documentation typo") == "docs"


def test_priority_medium_for_blocking() -> None:
    assert detect_priority("cannot install package") == "medium"


def test_pr_diff_summary_extracts_files() -> None:
    diff = """diff --git a/src/a.py b/src/a.py
--- a/src/a.py
+++ b/src/a.py
@@ -1 +1,2 @@
-a
+b
+c
"""
    assert changed_files_from_diff(diff) == ["src/a.py"]
    output = render_pr(diff)
    assert "Files changed: 1" in output
    assert "Additions: 2" in output
    assert "Deletions: 1" in output


def test_release_groups_changes() -> None:
    output = render_release("feat: add issue command\nfix: stdin crash\ndocs: update readme")
    assert "feat: add issue command" in output
    assert "fix: stdin crash" in output
    assert "docs: update readme" in output


def test_codex_task_contains_guardrails() -> None:
    output = render_codex_task("# Fix stdin crash")
    assert "Do not touch secrets" in output
    assert "Definition of done" in output
    assert "codex exec" in output
