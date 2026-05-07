# Wings – Claude Instructions

## Scope discipline

Do exactly what is asked. If the user says "do task A", do task A only.
Do not create task B or C alongside it, even if it seems helpful or related.
If something adjacent seems worth doing, mention it — but do not do it without being asked.

## On every commit

1. Bump the patch version in `pyproject.toml` (e.g. `0.1.1` → `0.1.2`)
2. Update `CHANGELOG.md` with the changes
3. Update `doc/architecture.md` if any architectural decision changed
4. After committing, create a git tag matching the new version: `git tag v<version>`
