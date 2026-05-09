# App Service Deployment — Execution Log

A sequential record of every step performed, the command used, and why it was done.

---

## Phase 1 — Local Setup

### Step 1.1 — Verify Azure CLI is installed

**Command:**
```bash
az --version
```

**Result:** Azure CLI 2.83.0 installed and working.

**Why:** Before doing anything in Azure, we need the CLI tool that lets us talk to Azure from the terminal. Without it we can't create resources, login, or run any Azure commands.

---

### Step 1.2 — Upgrade Azure CLI

**Command:**
```bash
az upgrade
```

**Why:** Always work on the latest version. Azure CLI updates bring bug fixes, new commands, and security patches. In an enterprise setup you never work on an outdated toolchain.

**Result:** Upgrade completed successfully.

---

### Step 1.3 — Verify Terraform is installed

**Command:**
```bash
terraform --version
```

**Result:** Terraform v1.14.4 installed, out of date.

**Why:** Terraform is our IaC tool — it creates and manages all Azure resources. We need it on the latest version to avoid bugs and get the latest provider support.

---

### Step 1.4 — Upgrade Terraform

**Command:**
```bash
sudo apt-get update && sudo apt-get install --only-upgrade terraform
```

**Result:** Terraform upgraded to v1.15.2.

**Why:** Always run the latest stable version in enterprise work. Terraform provider updates often include fixes for Azure resource handling.

---

### Step 1.5 — Verify GitHub CLI is installed

**Command:**
```bash
gh --version
```

**Result:** gh version 2.86.0 installed and working.

**Why:** GitHub CLI is needed to manage GitHub secrets (Service Principal credentials) from the terminal without going through the UI.

---

### Step 1.6 — Login to Azure CLI

**Command:**
```bash
az login
```

**Result:** Logged in successfully. Subscription `wings` selected.

**Why:** Before running any Azure CLI command, we must authenticate. This is done once with a personal account to set up the foundation. After this, all automation uses a Service Principal.

---

### Step 1.7 — Create new Azure subscription

**Done via:** Azure Portal → Subscriptions → Add

**Result:**
- Subscription Name: `wings`
- Subscription ID: `50e0c5b9-6745-44de-be51-ed9ece141ff5`
- Tenant ID: `8b574092-a70d-49ac-89dc-d754d40b400d`

**Why:** A dedicated subscription for this project keeps costs, resources, and permissions isolated from any other work. Enterprise projects always have their own subscription.

---

### Step 1.8 — Set active subscription in Azure CLI

**Command:**
```bash
az account set --subscription "50e0c5b9-6745-44de-be51-ed9ece141ff5"
az account show
```

**Result:** Subscription `wings` confirmed as default.

**Why:** Setting the default subscription ensures every CLI command targets the correct subscription. Avoids accidental changes to other subscriptions.

---

### Step 1.9 — Create azure_details.md (local only)

**Done via:** File created at `deployment/azure_details.md` and added to `.gitignore`.

**Why:** A local reference file to store subscription ID, tenant ID, and Service Principal credentials. Never committed to git — contains sensitive information.

---

## Phase 2 — Azure Foundation

### Step 2.1 — Create App Registration (Service Principal)

**Done via:** Portal → App registrations → New registration

**Result:**
- Name: `wings-github-actions-sp`
- Application (Client) ID: `22391b6c-2af1-4662-b25e-f414488b9300`
- Directory (Tenant) ID: `8b574092-a70d-49ac-89dc-d754d40b400d`
- Object ID: `a4496194-9677-496b-a35d-372245ee35a5`

**CLI equivalent:**
```bash
az ad app create --display-name "wings-github-actions-sp"
```

**Why:** A Service Principal is a non-human identity used by GitHub Actions to authenticate to Azure. Using a Service Principal instead of a personal account follows the least privilege principle — the pipeline gets only the access it needs, nothing more.

---

### Step 2.2 — Create Client Secret

**Done via:** Portal → App registrations → wings-github-actions-sp → Certificates & secrets → New client secret

**Result:**
- Description: `wings-github-actions-secret`
- Expires: 24 months
- Secret Value and Secret ID saved in `azure_details.md`

**CLI equivalent:**
```bash
az ad app credential reset \
  --id 22391b6c-2af1-4662-b25e-f414488b9300 \
  --append
```

**Why:** The client secret is the password for the Service Principal. GitHub Actions uses the Client ID + Secret to authenticate to Azure. Secret is only shown once in the portal — must be saved immediately.

---

### Step 2.5 — Create Resource Group for Terraform state

**Done via:** Portal → Resource groups → Create

**Result:** `rg-wings-tfstate` created in `Central India`

**CLI equivalent:**
```bash
az group create --name rg-wings-tfstate --location centralindia
```

**Why:** All Azure resources must live inside a Resource Group. We create a dedicated one for Terraform state — separate from application resources — so it's never accidentally deleted when environments are torn down.

---

### Step 2.6 — Create Storage Account for Terraform state

**Done via:** Portal → Storage accounts → Create

**Result:** `stwingstfstate` created in `rg-wings-tfstate`, Central India, LRS, HTTPS only, TLS 1.2

**CLI equivalent:**
```bash
az storage account create \
  --name stwingstfstate \
  --resource-group rg-wings-tfstate \
  --location centralindia \
  --sku Standard_LRS \
  --min-tls-version TLS1_2
```

**Why:** Terraform state must be stored remotely so GitHub Actions pipelines can access it. Azure Blob Storage is the standard backend for Azure-based Terraform setups. LRS is sufficient for state files — we don't need geo-redundancy here.

---

### Step 2.7 — Create Storage Container for Terraform state

**Done via:** Portal → stwingstfstate → Containers → Create

**Result:** `tfstate` container created with private access

**CLI equivalent:**
```bash
az storage container create \
  --name tfstate \
  --account-name stwingstfstate \
  --auth-mode login
```

**Why:** The container is the folder inside the storage account where Terraform saves its `.tfstate` files. Private access ensures no anonymous access — only authenticated identities can read or write state.

---

### Step 2.4 — Store Service Principal credentials as GitHub Secrets

**Done via:** GitHub CLI from inside the project directory

**Commands:**
```bash
gh secret set AZURE_CLIENT_ID --body "22391b6c-2af1-4662-b25e-f414488b9300"
gh secret set AZURE_CLIENT_SECRET --body "REDACTED"
gh secret set AZURE_TENANT_ID --body "8b574092-a70d-49ac-89dc-d754d40b400d"
gh secret set AZURE_SUBSCRIPTION_ID --body "50e0c5b9-6745-44de-be51-ed9ece141ff5"
```

**Result:** All 4 secrets set on `ASHISH-ARORA-24/wings` repository.

**Why:** GitHub Actions pipelines need these 4 values to authenticate to Azure as the Service Principal. Storing them as GitHub Secrets means they are encrypted at rest, never visible in logs, and only accessible to pipeline runs — not exposed in code.

---

### Step 2.3 — Assign Contributor Role to Service Principal

**Done via:** Portal → Subscriptions → wings → Access control (IAM) → Add role assignment → Contributor → wings-github-actions-sp

**CLI equivalent:**
```bash
az role assignment create \
  --assignee 22391b6c-2af1-4662-b25e-f414488b9300 \
  --role Contributor \
  --scope /subscriptions/50e0c5b9-6745-44de-be51-ed9ece141ff5
```

**Why:** Registering an app in Azure AD only creates the identity — it gives no permissions by default. Assigning Contributor on the subscription allows the Service Principal to create and manage all resources needed for deployment. Contributor was chosen over Owner because it cannot modify IAM permissions — least privilege.

---
