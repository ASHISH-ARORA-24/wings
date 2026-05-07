# Wings – Claude Instructions

## Scope discipline

Do exactly what is asked. If the user says "do task A", do task A only.
Do not create task B or C alongside it, even if it seems helpful or related.
If something adjacent seems worth doing, mention it — but do not do it without being asked.

## On every commit

1. Write unit tests for any new or changed code in `tests/unit/<app_name>/`
2. Run tests and confirm all pass before committing
3. Bump the patch version in `pyproject.toml` (e.g. `0.1.1` → `0.1.2`)
4. Update `CHANGELOG.md` with the changes
5. Update `doc/architecture.md` if any architectural decision changed
6. After committing, create a git tag matching the new version: `git tag v<version>`
