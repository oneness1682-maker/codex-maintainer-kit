# CLI specification

`cmtk` is a local-first command line tool for turning common maintainer inputs into Codex-ready workflows.

## Global behavior

- Input is read from a file path, `-`, or stdin when the path is omitted.
- Output defaults to Markdown.
- `--format json` wraps the Markdown output in a JSON object for scripts.
- `--format rich` renders Markdown in terminals that support Rich formatting.
- No network calls, API tokens, repository secrets, or private platform credentials are required for the MVP.

## Commands

### `cmtk issue [PATH]`

Purpose: triage an issue report into a maintainer checklist and Codex task seed.

Example:

```bash
cmtk issue examples/issue-input.md
```

Output includes:

- issue type estimate
- priority estimate
- reproducibility checklist
- Codex-ready task brief
- maintainer reply draft

### `cmtk pr [PATH]`

Purpose: summarize a unified PR diff into review risks and a Codex review prompt.

Example:

```bash
git diff main...HEAD | cmtk pr -
```

Output includes:

- changed file summary
- additions/deletions count
- initial risk estimate
- review checklist
- Codex review prompt

### `cmtk release [PATH]`

Purpose: turn git log text into draft release notes and a pre-tag checklist.

Example:

```bash
git log --oneline v0.1.0..HEAD | cmtk release -
```

Output includes:

- features
- fixes
- docs
- other changes
- maintainer release checklist

### `cmtk codex-task [PATH] --mode implementation|review|docs|release`

Purpose: convert maintainer context into a bounded Codex task brief.

Example:

```bash
cmtk codex-task examples/issue-input.md --mode implementation
```

Output includes:

- goal
- context excerpt
- step-by-step Codex instructions
- definition of done
- suggested Codex CLI command

## MVP limits

- Heuristic parsing only.
- No GitHub API integration in the MVP.
- No automatic posting, merging, or release publishing.
- Human maintainers review, edit, and approve all outputs.
