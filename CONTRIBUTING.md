# Contributing

Thanks for considering a contribution to Codex Maintainer Kit.

## Development setup

```bash
git clone https://github.com/oneness1682-maker/codex-maintainer-kit.git
cd codex-maintainer-kit
python -m pip install -e '.[dev]'
pytest -q
```

## Contribution types

Good first contributions:

- improve output templates
- add examples from real maintainer workflows
- add tests for issue/PR/release parsing
- improve README clarity
- add GitHub CLI ingestion behind safe flags

## Pull request checklist

- [ ] Keep changes focused and small.
- [ ] Add or update tests.
- [ ] Do not commit secrets, tokens, private issue data, or private repository content.
- [ ] Run `pytest -q`.
- [ ] Run `ruff check src tests` if available.
- [ ] Explain why the change helps maintainers or Codex task preparation.

## Security

Do not include private repository data in issues or examples. If you find a security-sensitive issue, open a minimal report without secrets and ask for a private contact path.
