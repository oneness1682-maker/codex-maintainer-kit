from __future__ import annotations

from enum import Enum
import json
from typing import Optional

import typer
from rich.console import Console
from rich.markdown import Markdown

from . import __version__
from .core import read_input, render_codex_task, render_issue, render_pr, render_release

app = typer.Typer(
    help="Turn issues, PR diffs, and git history into Codex-ready maintainer workflows.",
    no_args_is_help=True,
)
console = Console()


class OutputFormat(str, Enum):
    markdown = "markdown"
    json = "json"
    rich = "rich"


class TaskMode(str, Enum):
    implementation = "implementation"
    review = "review"
    docs = "docs"
    release = "release"


def emit(markdown: str, fmt: OutputFormat) -> None:
    if fmt is OutputFormat.json:
        console.print_json(json.dumps({"markdown": markdown}, ensure_ascii=False))
        return
    if fmt is OutputFormat.rich:
        console.print(Markdown(markdown))
        return
    typer.echo(markdown)


@app.callback()
def main(
    version: bool = typer.Option(False, "--version", help="Show version and exit."),
) -> None:
    if version:
        console.print(f"codex-maintainer-kit {__version__}")
        raise typer.Exit()


@app.command()
def issue(
    path: Optional[str] = typer.Argument(None, help="Issue markdown/text path, or '-' / omitted for stdin."),
    format: OutputFormat = typer.Option(OutputFormat.markdown, "--format", "-f"),
) -> None:
    """Triage an issue report into a maintainer checklist and Codex task seed."""
    emit(render_issue(read_input(path)), format)


@app.command()
def pr(
    path: Optional[str] = typer.Argument(None, help="Unified diff path, or '-' / omitted for stdin."),
    format: OutputFormat = typer.Option(OutputFormat.markdown, "--format", "-f"),
) -> None:
    """Summarize a PR diff into review risks and a Codex review prompt."""
    emit(render_pr(read_input(path)), format)


@app.command("release")
def release_notes(
    path: Optional[str] = typer.Argument(None, help="git log text path, or '-' / omitted for stdin."),
    format: OutputFormat = typer.Option(OutputFormat.markdown, "--format", "-f"),
) -> None:
    """Draft release notes and a pre-tag maintainer checklist from git log text."""
    emit(render_release(read_input(path)), format)


@app.command("codex-task")
def codex_task(
    path: Optional[str] = typer.Argument(None, help="Issue/task text path, or '-' / omitted for stdin."),
    mode: TaskMode = typer.Option(TaskMode.implementation, "--mode"),
    format: OutputFormat = typer.Option(OutputFormat.markdown, "--format", "-f"),
) -> None:
    """Convert maintainer context into a Codex-ready task brief."""
    emit(render_codex_task(read_input(path), mode=mode.value), format)


if __name__ == "__main__":
    app()
