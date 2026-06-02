"""Backward-compatible exports for the workflow renderers.

The MVP implementation lives in :mod:`codex_maintainer_kit.workflows`.
This module keeps older imports working while the public API settles.
"""

from .workflows import (  # noqa: F401
    changed_files_from_diff,
    detect_issue_type,
    detect_priority,
    first_nonempty_line,
    read_input,
    render_codex_task,
    render_issue,
    render_pr,
    render_release,
    summarize_diff,
)
