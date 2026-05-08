# Wings – Claude Instructions

## Scope discipline

Do exactly what is asked. If the user says "do task A", do task A only.
Do not create task B or C alongside it, even if it seems helpful or related.
If something adjacent seems worth doing, mention it — but do not do it without being asked.

## Pre-commit checklist

Follow these steps in order before every commit — no exceptions.

### 1. Unit tests
- Write unit tests for all new and changed code under `tests/unit/<app_name>/`
- Cover as many cases as reasonably possible (happy path, edge cases, failure cases)
- Run the full suite and confirm everything passes:
  ```
  uv run pytest tests/unit/ -v
  ```
- Do not commit if any test is failing

### 2. Version bump
- Increment the patch version in `pyproject.toml`
- Format: `MAJOR.MINOR.PATCH` — only the patch number increases per commit
- Example: `0.1.2` → `0.1.3`

### 3. Changelog
- Add a new version entry to `CHANGELOG.md` using the bumped version number
- Format:
  ```
  ## [0.1.3] - YYYY-MM-DD
  ### Added / Changed / Fixed
  - ...
  ```
- Do not use `[Unreleased]` — always use the actual version

### 4. Commit and tag
- Commit all changes including tests, version bump, and changelog
- Immediately after, create a git tag:
  ```
  git tag v<version>
  ```

> **Important:** Only follow this checklist when explicitly asked to commit. Do not run any of these steps automatically during normal development work.

## Code conventions

### Views
- All views must be **function-based only**. No class-based views under any circumstances.

### Commands
- Always use `uv run` to execute project commands:
  ```
  uv run manage.py runserver
  uv run manage.py migrate
  uv run pytest tests/unit/ -v
  ```

### Security
- Never commit `.env` — it contains credentials. It is already in `.gitignore` and must stay there.
