# Codex Maintainer Kit

Turn issues, PR diffs, and git history into **Codex-ready maintainer workflows**.

`codex-maintainer-kit` is a small MIT-licensed CLI for open-source maintainers who want cleaner issue triage, PR review checklists, release-note drafts, and safe task briefs for Codex.

> It does not replace maintainer judgment. It creates local heuristic drafts so humans and Codex can work from the same checklist. The MVP does not call AI APIs unless future optional integrations are enabled.

## Why this exists

Open-source maintainers repeatedly do the same translation work:

- rough issue report → reproducibility checklist and task scope
- large PR diff → review risks and test checklist
- git log → release notes and pre-tag checklist
- maintainer request → Codex-ready task brief with guardrails

Codex is more useful when it receives concrete context, files to inspect, tests to run, and a definition of done. This kit generates that structure locally.

## Install

```bash
python -m pip install git+https://github.com/oneness1682-maker/codex-maintainer-kit.git
```

For local development:

```bash
git clone https://github.com/oneness1682-maker/codex-maintainer-kit.git
cd codex-maintainer-kit
python -m pip install -e '.[dev]'
```

## CLI

```bash
cmtk issue examples/issue-input.md
cmtk pr examples/pr-diff.patch
cmtk release examples/release-log.txt
cmtk codex-task examples/issue-input.md --mode implementation
```

All commands also accept stdin:

```bash
git diff main...HEAD | cmtk pr -
git log --oneline v0.1.0..HEAD | cmtk release -
```

## Commands

### `cmtk issue`

Classifies an issue as bug/docs/feature/question, estimates priority, and creates:

- reproducibility checklist
- Codex-ready task seed
- maintainer reply draft

### `cmtk pr`

Reads a unified diff and creates:

- changed-file summary
- risk estimate
- review checklist
- Codex review prompt

### `cmtk release`

Reads git log text and creates:

- feature/fix/docs sections
- other changes
- pre-tag maintainer checklist

### `cmtk codex-task`

Turns a maintainer request into a safer Codex task brief:

- goal
- context
- step-by-step Codex instructions
- definition of done
- suggested Codex CLI command

## Example output

```markdown
# Codex task brief: CLI crashes when issue text is piped from stdin

## Goal
Prepare a safe implementation workflow...

## Instructions for Codex
1. Inspect the repository before changing files.
2. Identify the smallest set of files needed for the task.
3. If this is a bug, write or update a regression test first.
...
```

## Project fit for Codex for Open Source

This project is intentionally aligned with maintainer workflows: issue triage, pull-request review, release workflows, and maintainer automation. It is small, local-first, and designed to prepare better work packets for Codex rather than hiding decisions behind opaque automation.

Suggested application summary, under 500 characters:

```text
Codex Maintainer Kit is a small MIT-licensed CLI that helps open-source maintainers turn common repository inputs—issues, PR diffs, and git history—into structured, Codex-ready workflows. It focuses on practical maintainer tasks: issue triage, PR review briefs, release-note drafts, and bounded implementation prompts. The project is a good fit because it directly improves how maintainers prepare work for Codex while keeping humans in control of review, edits, and merge decisions.
```

## Development

```bash
python -m pip install -e '.[dev]'
pytest -q
ruff check src tests
```

## Roadmap

- GitHub issue/PR URL ingestion through `gh`
- Configurable templates
- JSON schema output for automation
- Optional OpenAI/Codex SDK integration
- Release-note grouping by conventional commits

## License

MIT
