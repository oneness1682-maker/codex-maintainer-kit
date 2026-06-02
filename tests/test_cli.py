from typer.testing import CliRunner

from codex_maintainer_kit.cli import app

runner = CliRunner()


def test_issue_command_file() -> None:
    result = runner.invoke(app, ["issue", "examples/issue-input.md"])
    assert result.exit_code == 0
    assert "Maintainer triage" in result.output


def test_pr_command_file() -> None:
    result = runner.invoke(app, ["pr", "examples/pr-diff.patch"])
    assert result.exit_code == 0
    assert "PR review brief" in result.output


def test_release_command_file() -> None:
    result = runner.invoke(app, ["release", "examples/release-log.txt"])
    assert result.exit_code == 0
    assert "Release notes draft" in result.output


def test_codex_task_command_json() -> None:
    result = runner.invoke(app, ["codex-task", "examples/issue-input.md", "--format", "json"])
    assert result.exit_code == 0
    assert "Codex task brief" in result.output


def test_visual_command_stdin() -> None:
    result = runner.invoke(
        app,
        ["visual", "-"],
        input="# Widget overflow\nScreenshot shows a broken mobile layout.",
    )
    assert result.exit_code == 0
    assert "Visual bug brief" in result.output
    assert "Screenshot QA checklist" in result.output


def test_issue_command_stdin_raw_markdown() -> None:
    result = runner.invoke(app, ["issue", "-"], input="# Bug: stdin crash\nTraceback")
    assert result.exit_code == 0
    assert result.output.startswith("# Maintainer triage")
    assert "## Classification" in result.output


def test_invalid_format_rejected() -> None:
    result = runner.invoke(app, ["issue", "examples/issue-input.md", "--format", "xml"])
    assert result.exit_code != 0


def test_invalid_mode_rejected() -> None:
    result = runner.invoke(app, ["codex-task", "examples/issue-input.md", "--mode", "unsafe"])
    assert result.exit_code != 0


def test_version_option_exits_without_command() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "codex-maintainer-kit" in result.output
    assert "0.1.1" in result.output
