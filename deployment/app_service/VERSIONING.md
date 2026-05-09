# Terraform Versioning Strategy

## Overview

Terraform modules are versioned via Git tags. Each environment pins to a specific version of the modules. No environment ever runs untagged or untested code.

---

## Environments

| Environment | State Backend | Who Runs It       | Purpose                          |
|-------------|---------------|-------------------|----------------------------------|
| sandbox     | Local file    | Developer, manual | Test new module code locally     |
| dev         | Azure Storage | GitHub Actions    | First shared environment         |
| qa          | Azure Storage | GitHub Actions    | Pre-production validation        |
| prod        | Azure Storage | GitHub Actions    | Live production, approval gated  |

---

## Folder Structure

```
deployment/app_service/terraform/
  modules/
    resource_group/       ← versioned, shared across all environments
    app_service/          ← (coming soon)
    database/             ← (coming soon)
    keyvault/             ← (coming soon)
  environments/
    sandbox/
      main.tf             ← module source = local path (../../modules/...)
      backend.tf          ← local backend
      providers.tf
      variables.tf
      terraform.tfvars
    dev/
      main.tf             ← module source = GitHub URL with ?ref=v0.1.0
      backend.tf          ← remote state: wings-dev.tfstate
      providers.tf
      variables.tf
      terraform.tfvars
    qa/
      main.tf             ← module source = GitHub URL with ?ref=v0.1.0 (after promotion)
      backend.tf          ← remote state: wings-qa.tfstate
      providers.tf
      variables.tf
      terraform.tfvars
    prod/
      main.tf             ← module source = GitHub URL with ?ref=v0.1.0 (after promotion)
      backend.tf          ← remote state: wings-prod.tfstate
      providers.tf
      variables.tf
      terraform.tfvars
```

---

## Module Source

**Sandbox (local development):**
```hcl
module "rg" {
  source = "../../modules/resource_group"
}
```

**Dev / QA / Prod (after tagging):**
```hcl
module "rg" {
  source = "git::https://github.com/AshishArora24/wings.git//deployment/app_service/terraform/modules/resource_group?ref=v0.1.0"
}
```

---

## Versioning Flow

```
1. Write / update module code
2. Test in sandbox (local apply → verify → destroy)
3. Commit and push to GitHub
4. Create Git tag: git tag v0.1.0 && git push origin v0.1.0
5. Update dev/main.tf → ref=v0.1.0 → pipeline deploys to dev
6. Verify dev → update qa/main.tf → ref=v0.1.0 → pipeline deploys to qa
7. Verify qa → update prod/main.tf → ref=v0.1.0 → pipeline deploys to prod (approval required)
```

---

## Git Tag Convention

| Tag      | Meaning                              |
|----------|--------------------------------------|
| v0.1.0   | Initial resource group module        |
| v0.2.0   | Added app service module             |
| v0.3.0   | Added database module                |
| v1.0.0   | All modules complete, production ready |

Format: `MAJOR.MINOR.PATCH`
- MAJOR — breaking change to module interface
- MINOR — new module added
- PATCH — bug fix or small change within a module

---

## State Files in Azure Blob Storage

| Environment | State File Key      |
|-------------|---------------------|
| dev         | wings-dev.tfstate   |
| qa          | wings-qa.tfstate    |
| prod        | wings-prod.tfstate  |
| sandbox     | local file only     |

All remote state stored in: `stwingstfstate` → container `tfstate`
