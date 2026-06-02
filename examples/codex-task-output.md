# Codex task brief: CLI crashes when issue text is piped from stdin

## Goal
Fix stdin handling for issue triage.

## Instructions for Codex
1. Reproduce with `cat examples/issue-input.md | cmtk issue -`.
2. Add a regression test for stdin-style input if possible.
3. Make the smallest implementation change.
4. Run `pytest -q` and a CLI smoke command.
5. Report changed files and commands run.
