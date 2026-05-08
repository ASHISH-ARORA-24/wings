# Changelog

All notable changes to this project will be documented here.

## [0.1.4] - 2026-05-08

### Added
- `family` and `vendor` Django apps with protected dashboards
- Google OAuth login via `django-allauth`
- Login modal on homepage with email/phone input, Get OTP button, Login with Google and Login with Microsoft buttons
- Role selector (Family / Vendor) in login modal — mandatory before any login action
- `wings/adapters.py` — custom allauth adapter redirects to correct dashboard based on session role
- `wings/views.py` — `google_login_with_role` view stores role in session before Google redirect
- `.env` support via `python-dotenv` — Google credentials stored securely, never committed
- `CLAUDE.md` — code conventions: function-based views only, `uv run` for all commands, never commit `.env`

### Changed
- Logout now skips confirmation page and redirects directly to homepage

### Tests
- 41 unit tests across all apps — all passing
- `tests/unit/family/test_views.py` — 7 tests
- `tests/unit/vendor/test_views.py` — 7 tests
- `tests/unit/wings/test_adapters.py` — 5 tests for role-based redirect logic
- `tests/unit/wings/test_views.py` — expanded to 9 tests including `google_login_with_role`

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
