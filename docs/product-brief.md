# Product brief: Codex Maintainer Kit

## Problem
Open-source maintainers spend repetitive time turning rough issues, PR diffs, and git logs into actionable maintenance work. Codex can help, but it works best with structured context, explicit safety constraints, and clear definitions of done.

## MVP
`codex-maintainer-kit` is a small CLI that converts maintainer inputs into Codex-ready workflows:

- `cmtk issue`: classify an issue and draft a reproducibility checklist.
- `cmtk pr`: summarize a diff and draft a PR review checklist.
- `cmtk release`: turn git log text into release notes.
- `cmtk codex-task`: produce a safe task brief for Codex CLI/SDK.

## Non-goals
- It does not replace maintainer judgment.
- It does not call private APIs by default.
- It does not require repository secrets.
- It does not claim project popularity; usefulness should be proven by examples and adoption.

## OpenAI Codex for OSS fit
The project directly supports issue triage, PR review, release workflows, and maintainer automation—the same workflows highlighted by the Codex for Open Source program.
