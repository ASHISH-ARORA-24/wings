# Deployment – Common Instructions

## Philosophy

This project is deployed and managed like an enterprise application.
- **Nothing is done manually** — no clicking in the Azure portal to create or change infrastructure
- **Everything is code** — infrastructure (Terraform), configuration (Ansible), and pipelines (GitHub Actions)
- **Everything is reviewed** — all changes go through pull requests and pipelines before reaching any environment
- **Security first** — least privilege, managed identities, Key Vault for secrets, no hardcoded credentials anywhere

---

## Environments

| Environment | Trigger | Purpose |
|---|---|---|
| `dev` | Any branch push | Development and feature testing |
| `qa` | Merge to `main` | QA validation before production |
| `prod` | Manual approval after QA | Live production environment |

---

## Branching and Deployment Rules

- Any branch can trigger a deployment to **dev**
- Only **`main`** branch can deploy to **qa**
- **`prod`** deployments require a manual approval gate after QA passes
- Infrastructure changes (Terraform) also go through pipelines — never applied locally or manually

---

## Infrastructure as Code (IaC)

- **Terraform** — all Azure resources are defined and managed via Terraform
- Terraform state is stored remotely in **Azure Storage** (not locally)
- Infrastructure versioning is managed via Git tags and Terraform workspaces per environment
- No `terraform apply` from a local machine — only pipelines can apply infrastructure changes

---

## Application Deployment

- Application is deployed via **GitHub Actions** pipelines
- Each deployment is versioned and traceable back to a Git commit and tag
- Rollback is done by redeploying a previous Git tag — no manual intervention

---

## Azure Security Standards

- **Service Principal** — pipelines authenticate to Azure using a Service Principal with the minimum required permissions
- **Managed Identity** — Azure services talk to each other using Managed Identities, not passwords or connection strings
- **Azure Key Vault** — all secrets (DB passwords, API keys, OAuth credentials) are stored in Key Vault, never in code or env files
- **IAM (Role-Based Access Control)** — every service and principal has only the permissions it needs, nothing more
- **No public database access** — databases are on private networks only
- **HTTPS everywhere** — no plain HTTP in any environment

---

## Tooling

| Area | Tool | Why |
|---|---|---|
| Infrastructure provisioning | **Terraform** | Cloud agnostic, huge industry adoption, best for Azure resources |
| Configuration management | **Ansible** | Agentless, simple, industry standard for configuring servers and apps |
| Secrets management | **Azure Key Vault** | Native Azure, integrates with Managed Identity, no passwords in code |
| CI/CD pipelines | **GitHub Actions** | Already on GitHub, YAML based, huge ecosystem |
| Container registry | **Azure Container Registry (ACR)** | Native Azure, integrates cleanly with AKS and App Service |
| Container orchestration | **Kubernetes (AKS)** | Industry standard, mandatory interview topic |
| Monitoring & alerting | **Azure Monitor + App Insights** | Native, deep integration with all Azure services |
| Log management | **Azure Log Analytics** | Centralised logs across all services |
| Policy & compliance | **Azure Policy** | Enforce security rules at the org level |
| Cost management | **Azure Cost Management** | Track and alert on spend |
| Kubernetes packaging | **Helm** | Package and version Kubernetes deployments |
| Security scanning | **Trivy / Checkov** | Scan containers and IaC for vulnerabilities in the pipeline |
| Code quality | **SonarQube** | Code quality and security analysis in the pipeline |
| Metrics & dashboards | **Prometheus + Grafana** | Metrics and visualisation on Kubernetes |

---

## What We Will Learn and Cover

- Azure IAM — service principals, managed identities, RBAC roles
- Azure Key Vault — storing and accessing secrets securely
- Terraform — writing, planning, and applying infrastructure
- Ansible — configuration management for servers and apps
- GitHub Actions — building CI/CD pipelines for both infra and app
- Helm — packaging and versioning Kubernetes deployments
- Infrastructure versioning — how to manage and roll back infra changes
- Application versioning — how to manage and roll back app deployments
- Network security — VNets, subnets, private endpoints, NSGs
- Monitoring and logging — Azure Monitor, Application Insights, Log Analytics
- Security scanning — Trivy, Checkov in the pipeline
- Code quality — SonarQube in the pipeline
- Cost management — budgets, alerts, tagging strategy
