# Changelog

All notable changes to this project will be documented here.

## [0.1.3] - 2026-05-07

### Changed
- CLAUDE.md: redrafted pre-commit checklist — unit tests, version bump, dated changelog entry, commit, tag

### Added
- `accounts` app with `UserExtraInfo` model — extends the built-in User with `phone` and `role` (family/vendor) fields
- `UserExtraInfo` shown as an inline on the User admin page
- `SITE_NAME` setting in `settings.py` as a single source of truth for the display name ("Wing Man", temporary)
- `wings/context_processors.py` — injects `{{ site_name }}` into every template automatically
- Login button in homepage navbar

### Changed
- Homepage updated to use `{{ site_name }}` throughout (title, nav logo, hero, footer)
- Dev dependencies: added `pytest-django`, `model-bakery`, `faker`
- `pyproject.toml` updated with `[tool.pytest.ini_options]` config

### Tests
- Unit test structure: `tests/unit/<app_name>/`
- `tests/conftest.py` with shared fixtures (`user`, `family_user`, `vendor_user`)
- `tests/unit/accounts/test_models.py` — 9 tests for `UserExtraInfo`
- `tests/unit/wings/test_context_processors.py` — 3 tests for `site_name` processor
- `tests/unit/wings/test_views.py` — 3 tests for home view
