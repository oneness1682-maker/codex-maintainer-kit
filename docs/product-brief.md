# Product brief: Codex Maintainer Kit

## Problem
Open-source maintainers spend repetitive time turning rough issues, PR diffs, and git logs into actionable maintenance work. Codex can help, but it works best with structured context, explicit safety constraints, and clear definitions of done.

## Product direction
`codex-maintainer-kit` is a local-first, MIT-licensed CLI that helps open-source maintainers turn common repository inputs into structured workflows that are ready for Codex-assisted work.

The tool is intentionally narrow: it prepares better task packets, review briefs, and release drafts without requiring network access, API tokens, repository secrets, or private project context. A human maintainer remains responsible for review, edits, merge decisions, and public communication.

## MVP scope
The MVP is defined around four CLI commands:

- `cmtk issue`: classify an issue and draft a reproducibility checklist.
- `cmtk pr`: summarize a diff and draft a PR review checklist.
- `cmtk release`: turn git log text into release notes.
- `cmtk codex-task`: produce a safe task brief for Codex CLI/SDK.

These commands cover the core maintainer flow:

- issue triage
- PR review briefs
- release-note drafts
- Codex-ready implementation prompts

## Non-goals
- It does not replace maintainer judgment.
- It does not call private APIs by default.
- It does not require repository secrets.
- It does not claim project popularity; usefulness should be proven by examples and adoption.

## OpenAI Codex for OSS fit
The project directly supports issue triage, PR review, release workflows, and maintainer automation—the same workflows highlighted by the Codex for Open Source program.

## Application blurb, under 500 characters
Codex Maintainer Kit is a small MIT-licensed CLI that helps open-source maintainers turn common repository inputs—issues, PR diffs, and git history—into structured, Codex-ready workflows. It focuses on practical maintainer tasks: issue triage, PR review briefs, release-note drafts, and bounded implementation prompts. The project is a good fit because it directly improves how maintainers prepare work for Codex while keeping humans in control of review, edits, and merge decisions.
