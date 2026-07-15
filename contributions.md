# Contribution Guidelines

Thanks for helping improve StakeHabit API.

## Before you start

- Make sure you are working from a clean branch.
- Review the current setup in [README.md](README.md) and [DEVELOPMENT.md](DEVELOPMENT.md).
- If you are changing the API contract, update the relevant schemas, routes, and docs together.

## Development workflow

1. Create a feature branch.
2. Make the smallest change that solves the problem.
3. Add or update tests when you change behavior.
4. Run the relevant test suite before opening a pull request.
5. Update documentation when the API surface changes.

## Coding expectations

- Keep route handlers thin and move domain logic into service modules.
- Use Pydantic schemas for request and response validation.
- Keep model and database changes paired with Alembic migrations.
- Prefer clear error messages that are useful to API consumers.

## Testing checklist

Run:

```bash
.venv/bin/python -m pytest tests/ -q
```

For focused work, run a smaller suite such as:

```bash
.venv/bin/python -m pytest tests/test_pools.py -q
```

## Pull request expectations

A good pull request should include:
- a short summary of the change
- any API contract changes
- relevant test evidence
- any documentation updates needed for frontend or agent integration
