# Wings – Architecture

## Stack

- **Framework:** Django 6, Python 3.12
- **Database:** SQLite (dev); intended to swap for Postgres in production
- **Package manager:** uv

---

## Apps

### `accounts`
Extends Django's built-in `User` model without replacing it.

- `UserExtraInfo` — `OneToOneField` to `User`; holds extra fields that don't belong on the auth model
  - `phone` — contact number
  - `role` — either `family` or `vendor`; determines what the user can access

**Why not a custom User model?** Project started with the default User; a `OneToOneField` profile keeps things simple and avoids a DB reset. If more user fields are added, they go here first.

---

## Site name

`SITE_NAME` in `settings.py` is the single source of truth for the product display name. It is injected into every template via `wings/context_processors.py` as `{{ site_name }}`. Changing one value updates the entire UI.

---

## Templates

- Root-level `templates/` directory, registered in `DIRS`
- Project-level views (homepage etc.) live in `wings/views.py`
- App-level views and templates will live inside their respective app directories

---

## URL structure (current)

| URL | View | Notes |
|---|---|---|
| `/` | `wings.views.home` | Homepage |
| `/admin/` | Django admin | Superuser only |
| `/login/` | TBD | Login page (not yet built) |

---

## User roles

| Role | Value | Description |
|---|---|---|
| Family | `family` | A family looking for matches |
| Vendor | `vendor` | A service provider |

Role is stored on `UserExtraInfo.role` and checked in code via `UserExtraInfo.FAMILY` / `UserExtraInfo.VENDOR` constants.
