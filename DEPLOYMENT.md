# DevOps Configuration for tmpfu9n40cc

This repository has been configured automatically by the **AI DevOps Agent**.

## Architecture Summary

- **Repository Type:** Single Service
- **Service `tmpfu9n40cc`:**
  - Framework: `python_generic`
  - Language: `python`
  - Package Manager: `uv`
  - Exposed Port: `8000`
  - Recommended Deployment Target: **Render**

## Running Locally with Docker Compose

```bash
# Build and start all services locally
docker compose up --build
```

## CI/CD & Cloud Sandbox Testing

- `.github/workflows/ci.yml`: Standard pull request test & build workflow.
- `.github/workflows/ai-devops-verify.yml`: Cloud sandbox workflow for automated container verification.
