# Bug: CLI crashes when issue text is piped from stdin

When I run:

```bash
cat issue.md | cmtk issue -
```

I expected a triage brief, but the command exits with an error on Python 3.11.

Environment:
- OS: Ubuntu 24.04
- Python: 3.11
- codex-maintainer-kit: 0.1.0
