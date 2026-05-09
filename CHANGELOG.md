# Changelog

All notable changes to this project will be documented here.

## Versioning Convention

| Version type | Tag format | Tracks |
|---|---|---|
| App | `v0.x.x` | Django code, templates, tests, config |
| Terraform | `tf/v0.x.x` | Terraform modules and environment config |

Both versions live in `pyproject.toml` — `version` for app, `tool.wings.terraform_version` for Terraform.
Bump only the one that changed. If both changed, bump both and create both tags.

Terraform changes are tracked separately in `CHANGELOG_TF.md`.

## [0.1.7] - 2026-05-09

### Fixed
- Added Terraform-specific entries to `.gitignore` — `.terraform/` directories, `terraform.tfstate`, and `terraform.tfstate.backup` were accidentally committed and have been removed from tracking
- Added `deployment/.env` to `.gitignore`

## [0.1.6] - 2026-05-09

### Changed
- Restructured Terraform into versioned environment layout (sandbox, dev, qa, prod)
- sandbox environment uses local backend — runs manually from laptop
- dev, qa, prod environments use Azure remote state — pipeline only
- Each environment is self-contained with its own backend, providers, variables, and outputs
- Updated `plan.md` Phase 3 to reflect versioned module strategy over workspaces

### Added
- `deployment/app_service/VERSIONING.md` — documents versioning strategy, folder structure, git tag convention, and promotion flow

## [0.1.5] - 2026-05-09

### Added
- `deployment/` folder structure with `app_service/`, `common_instructions.md`
- `deployment/app_service/plan.md` — end to end App Service deployment plan
- `deployment/app_service/execution_log.md` — sequential log of all steps performed
- `deployment/azure_details.md` — local only, git-ignored, stores Azure credentials reference
- `.gitignore` updated to exclude `deployment/azure_details.md` and `.env`
- Phase 1 complete: Azure CLI, Terraform, GitHub CLI verified and updated
- Phase 2 complete: Service Principal created, Contributor role assigned, GitHub secrets set, Terraform remote state storage created (rg-wings-tfstate, stwingstfstate, tfstate container)

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
