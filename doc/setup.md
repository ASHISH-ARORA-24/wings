# Wings – Project Setup & Developer Notes

## Running the project

```bash
# Start the dev server
.venv/bin/python manage.py runserver
```

App is available at `http://127.0.0.1:8000/`

---

## Admin portal

URL: `http://127.0.0.1:8000/admin/`  
Superuser: `admin` / `admin` *(local dev only)*

---

## Site name

The display name shown across all pages is **temporary** and controlled from a single place:

```python
# wings/settings.py
SITE_NAME = 'Wing Man'
```

All templates receive this automatically via `wings/context_processors.py` — no view code needed. Use it in any template as:

```html
{{ site_name }}
```

**When the final name is decided, update only `SITE_NAME` in `settings.py` and it reflects everywhere.**

---

## Templates

- Templates live in the root-level `templates/` directory.
- Registered in `settings.py` as `BASE_DIR / 'templates'`.
- Homepage: `templates/home.html`, served at `/` by `wings/views.py::home`.

---

## Key files

| File | Purpose |
|---|---|
| `wings/settings.py` | All config including `SITE_NAME` |
| `wings/urls.py` | URL routing |
| `wings/views.py` | Project-level views (homepage etc.) |
| `wings/context_processors.py` | Injects `site_name` into every template |
| `templates/home.html` | Homepage template |
| `doc/family_onboarding.md` | Family onboarding flow diagram |
