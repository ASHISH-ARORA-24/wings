# Terraform Changelog

All infrastructure changes are documented here.

## Versioning Convention

- Tag format: `tf/v1.x.x` — starts at v1 to avoid overlap with app version (`v0.x.x`)
- MAJOR — breaking change to module interface (variable renamed, removed, type changed)
- MINOR — new module added
- PATCH — bug fix or small change within an existing module

---

## [tf/v1.0.0] - 2026-05-09

### Added
- Initial Terraform structure with versioned environment layout
- `modules/resource_group/` — reusable module that creates `rg-{project}-{environment}` with standard tags
- `environments/sandbox/` — local backend, runs manually from developer machine
- `environments/dev/` — Azure remote state (`wings-dev.tfstate`), pipeline only
- `environments/qa/` — Azure remote state (`wings-qa.tfstate`), pipeline only
- `environments/prod/` — Azure remote state (`wings-prod.tfstate`), pipeline only
- `VERSIONING.md` — documents versioning strategy, folder structure, promotion flow, and git tag convention
