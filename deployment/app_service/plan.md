# App Service Deployment — End to End Plan

## Overview
Deploy the Wings Django application to Azure App Service across three environments (dev, qa, prod) using Terraform for infrastructure, GitHub Actions for CI/CD, Azure Key Vault for secrets, and Managed Identity for secure service-to-service communication. Nothing is done manually — everything goes through code and pipelines.

---

## Status Legend
- [ ] Not started
- [~] In progress
- [x] Done

---

## Phase 1 — Azure Account & Local Setup

- [x] 1.1 Verify Azure subscription is active
- [x] 1.2 Install Azure CLI on local machine
- [x] 1.3 Install Terraform on local machine
- [x] 1.4 Install GitHub CLI on local machine
- [x] 1.5 Login to Azure CLI (`az login`)
- [x] 1.6 Set the correct subscription (`az account set`)

---

## Phase 2 — Azure Foundation (Manual, One Time Only)

> These are the only steps done manually. Everything after this is IaC and pipelines.

- [x] 2.1 Create a Resource Group for Terraform remote state (`rg-wings-tfstate`, Central India)
- [x] 2.2 Create an Azure Storage Account for Terraform state (`stwingstfstate`, Central India, LRS)
- [x] 2.3 Create a Storage Container inside it (`tfstate`)
- [x] 2.4 Create a Service Principal for GitHub Actions
- [x] 2.5 Assign the Service Principal the correct RBAC role (Contributor on subscription or resource group)
- [x] 2.6 Store Service Principal credentials as GitHub Secrets
  - `AZURE_CLIENT_ID`
  - `AZURE_CLIENT_SECRET`
  - `AZURE_TENANT_ID`
  - `AZURE_SUBSCRIPTION_ID`

---

## Phase 3 — Terraform Infrastructure

> Versioned module strategy: modules are tagged in Git and each environment pins to a specific version. Sandbox runs locally; dev/qa/prod run via pipeline only.

- [ ] 3.1 Restructure Terraform folder into versioned layout:
  - `modules/` — shared reusable modules (resource_group, app_service, database, etc.)
  - `environments/sandbox/` — local state, run manually from laptop
  - `environments/dev/` — remote state, pipeline only
  - `environments/qa/` — remote state, pipeline only
  - `environments/prod/` — remote state, pipeline only
- [ ] 3.2 Write Terraform modules:
  - [ ] Resource Group
  - [ ] App Service Plan
  - [ ] App Service (Web App)
  - [ ] Azure Database for PostgreSQL — one per environment
    - sandbox/dev: smallest SKU, cheapest tier
    - qa: mirrors prod sizing for accurate testing
    - prod: production grade, backup enabled, high availability
  - [ ] Azure Key Vault
  - [ ] App Insights + Log Analytics Workspace
  - [ ] Managed Identity for the App Service
- [x] 3.3 Build and test sandbox environment locally (full cycle: init → plan → apply → destroy)
- [x] 3.4 Tag module version in Git (`tf/v1.0.0`) and push to GitHub
- [ ] 3.5 Update dev/qa/prod environments to reference module via GitHub tag (`ref=tf/v1.0.0`)
- [ ] 3.6 Create GitHub environments (dev, qa, prod) with protection rules
  - qa and prod: require manual approval before apply
  - dev: no approval needed
- [ ] 3.7 Write GitHub Actions pipeline for Terraform (`.github/workflows/infra-deploy.yml`)

  **Pipeline design decisions (agreed):**
  - Single pipeline file handles dev, qa, prod — not 3 separate files
  - Sandbox is never in the pipeline — developer runs it locally only
  - Path-based triggers — only the environment whose files changed will run
    - `environments/dev/**` changed → dev job runs
    - `environments/qa/**` changed → qa job runs
    - `environments/prod/**` changed → prod job runs
  - On PR opened/updated → `terraform plan` only, no apply
  - On PR merged to main → `terraform apply`
  - After each apply → smoke tests (verify Azure resources exist and respond)
  - Version promotion is always manual — developer creates a branch, updates `ref=` in environment's `main.tf`, opens PR
  - Rollback: create branch, revert `ref=` to old version, merge → pipeline restores old version
  - Approval gates: qa and prod use GitHub Environment protection rules (required reviewers)
  - Sequence per environment: init → plan → apply → smoke test

---

## Phase 4 — Key Vault & Secrets

- [ ] 4.1 Store all secrets in Azure Key Vault (one Key Vault per environment, secrets never shared across envs):
  - Django `SECRET_KEY`
  - PostgreSQL host, port, database name, username, password
  - Google OAuth `CLIENT_ID` and `CLIENT_SECRET`
- [ ] 4.2 Assign Managed Identity of App Service access to Key Vault (`Key Vault Secrets User` role)
- [ ] 4.3 Update Django `settings.py` to read secrets from Key Vault via Managed Identity (no `.env` file in Azure)

---

## Phase 5 — Django Production Readiness

- [ ] 5.1 Switch database from SQLite to PostgreSQL
- [ ] 5.2 Configure `ALLOWED_HOSTS` and `DEBUG=False` for non-dev environments
- [ ] 5.3 Configure Django to serve static files via Azure Blob Storage or WhiteNoise
- [ ] 5.4 Add `gunicorn` as the production WSGI server
- [ ] 5.5 Create `startup.sh` — the App Service startup command
- [ ] 5.6 Add `requirements.txt` (or ensure `pyproject.toml` works for Azure)

---

## Phase 6 — GitHub Actions App Pipeline

- [ ] 6.1 Write `app-deploy.yml` pipeline:
  - Trigger: push to any branch → deploy to dev
  - Trigger: merge to `main` → deploy to qa (with approval gate for prod)
- [ ] 6.2 Pipeline steps:
  - [ ] Run unit tests (`uv run pytest tests/unit/ -v`)
  - [ ] Run security scan (Trivy / Checkov)
  - [ ] Run code quality check (SonarQube or ruff)
  - [ ] Build the app
  - [ ] Run database migrations on App Service
  - [ ] Deploy to App Service
- [ ] 6.3 Add environment protection rules in GitHub (require approval for qa and prod)

---

## Phase 7 — Networking & Security

- [ ] 7.1 Restrict App Service to HTTPS only
- [ ] 7.2 Enable Azure Managed SSL certificate (free, auto-renewing)
- [ ] 7.3 Configure App Service to only accept traffic (no direct DB access from internet)
- [ ] 7.4 Enable Azure Defender / Security Centre on the resource group

---

## Phase 8 — Monitoring & Alerting

- [ ] 8.1 Connect App Service to Application Insights
- [ ] 8.2 Set up Log Analytics Workspace
- [ ] 8.3 Create alerts for:
  - App errors / exceptions
  - High response time
  - App Service restarts
- [ ] 8.4 Verify logs are flowing (requests, errors, dependencies)

---

## Phase 9 — Validation

- [ ] 9.1 Deploy to dev end to end via pipeline
- [ ] 9.2 Run smoke tests on dev
- [ ] 9.3 Merge to main — confirm qa deploys automatically with approval gate
- [ ] 9.4 Approve and deploy to prod
- [ ] 9.5 Verify Google login works in all environments
- [ ] 9.6 Verify secrets are loaded from Key Vault (no .env on server)
- [ ] 9.7 Verify HTTPS is enforced
- [ ] 9.8 Verify logs appear in App Insights

---

## Key Concepts Covered

| Concept | Where |
|---|---|
| Service Principal | Phase 2 |
| RBAC / IAM | Phase 2, 4 |
| Terraform remote state | Phase 3 |
| Terraform versioned modules | Phase 3 |
| Sandbox environment | Phase 3 |
| Managed Identity | Phase 4 |
| Azure Key Vault | Phase 4 |
| Production Django setup | Phase 5 |
| CI/CD pipeline | Phase 6 |
| Approval gates | Phase 6 |
| HTTPS / SSL | Phase 7 |
| Monitoring & alerting | Phase 8 |
