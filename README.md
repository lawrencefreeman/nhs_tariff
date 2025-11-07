# 🚀 Snowflake Deployment Automation (GitHub Actions + Key Pair Auth) building Medallion Architecture with dbt

This repository demonstrates a **secure, automated Snowflake deployment pipeline** using **GitHub Actions** and **key pair authentication**.  
It is part of my professional portfolio, showcasing best practices in CI/CD, cloud security, and DevOps workflow design.

---

## 🏗️ Overview

The workflow provisions and configures Snowflake environments automatically, including:

- Database and schema creation  
- Storage integration setup (S3 → Snowflake)  
- Stage and file format management  
- Idempotent table creation and data loading  
- dbt transformations from Bronze to Silver / Gold layers
- Secure key pair–based authentication (no passwords in CI/CD)  

All steps run non-interactively via GitHub Actions on `ubuntu-latest`.

---

## ⚙️ Technology Stack

| Layer | Tools / Technologies |
|--------|----------------------|
| **Data Platform** | Snowflake |
| **Authentication** | Key Pair (JWT) |
| **CI/CD** | GitHub Actions |
| **Cloud Integration** | AWS S3 External Stage |
| **Scripting** | Bash + SQL |
| **Security Scanning** | Dependabot, CodeQL |
| **Version Control** | GitHub (protected main branch) |

---

## 🔒 Security Practices

This repository follows GitHub security best practices:

- Security disclosure policy ([`SECURITY.md`](./.github/SECURITY.md))
- Automated dependency and vulnerability scanning (Dependabot + CodeQL)
- Protected `main` branch with signed commits and required checks
- Minimal GitHub Actions permissions (least privilege)
- Secrets encrypted in GitHub and never echoed to logs
- No long-lived credentials — uses Snowflake JWT + short-lived keys

---

