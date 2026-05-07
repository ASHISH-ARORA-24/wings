# Changelog

All notable changes to this project will be documented here.

## [Unreleased]

### Added
- `accounts` app with `UserExtraInfo` model — extends the built-in User with `phone` and `role` (family/vendor) fields
- `UserExtraInfo` shown as an inline on the User admin page
- `SITE_NAME` setting in `settings.py` as a single source of truth for the display name ("Wing Man", temporary)
- `wings/context_processors.py` — injects `{{ site_name }}` into every template automatically
- Login button in homepage navbar

### Changed
- Homepage updated to use `{{ site_name }}` throughout (title, nav logo, hero, footer)
