# Implementation Guide

Purpose

This document describes concrete implementation details and step-by-step guidance for applying the scaffolding across repository branches. It is intended for maintainers who will: finish branch artifacts, open PRs, validate CI, run local smoke tests, and prepare the project for iterative development.

Branches covered
- data-integration
- agents
- foundry-windows-local
- web-app
- infra
- docs
- tooling
- integrations

Quick note about permissions
- Automated pushes, PR creation, and GitHub Actions that write require a collaborator/service account with Write access and Actions workflow permissions set to "Read and write". If you plan to let automation push or merge, ensure the account accepts the invite and that branch protections allow the automation to act (or permit PRs from forks).

1. General PR and CI checklist (apply to every branch)
- Linting: ruff/flake8 configured; add a CI job that fails the PR on lint errors.
- Tests: include at least a smoke pytest job (pytest -q) to catch obvious issues.
- Secrets: do not commit secrets. Include .env.example with placeholder values.
- Model files: do NOT commit model binaries. Use .gitignore and README instructions to download models externally.
- Docker-compose smoke (if branch adds services): confirm docker-compose up -d works in CI or as a manual step.
- PR description must include run/test steps, security notes, and a checklist with the items above.

2. Branch-by-branch implementation details

A. data-integration
- Purpose: Local dev stack for ingestion (Cosmos DB emulator, Chroma vector DB, Redis). Contains sample connectors and example ingestion scripts.
- Key files (expected): data-integration/docker-compose.yml, data-integration/connectors/ingest_cosmos.py, data-integration/fabric_adapter/README.md
- Local run steps:
  1. cd data-integration
  2. docker-compose up -d
  3. Wait for Cosmos emulator to initialize (first run may take >30s)
  4. Place sample JSON docs in sample_data/ and run ingestion: python connectors/ingest_cosmos.py --path sample_data
- CI checks:
  - docker-smoke job in CI should attempt docker-compose up -d and report the container statuses.
  - Alternatively, mark the docker smoke step as optional in CI if running Docker-in-GitHub Actions is undesirable.
- Security:
  - Cosmos emulator uses a development key. Document the need to replace before production.

B. agents
- Purpose: Agent orchestrator, plugin API, tests and minimal examples.
- Key files: agents/reasoning_agent/core.py, agents/orchestrator/runner.py, agents/tests/test_agent_basic.py, agents/requirements.txt
- Implementation notes:
  - Keep the AgentPlugin API minimal and well-documented to avoid coupling.
  - Plugins should be pure functions (stateless) or clearly declare stateful behavior.
- Local run steps:
  1. python -m venv .venv && source .venv/bin/activate
  2. pip install -r agents/requirements.txt
  3. pytest agents/tests/test_agent_basic.py
- CI checks:
  - Run pytest, fail on failures.
  - Lint the agents folder.

C. foundry-windows-local
- Purpose: Native Windows examples using llama-cpp-python and GGML quantized models for CPU workflows.
- Key files: foundry-windows-local/README.md, foundry-windows-local/install/README.md, foundry-windows-local/examples/llama_cpp_example.py
- Implementation notes:
  - Provide explicit instructions for LLAMA_MODEL_PATH and where to place model files (C:\models by default in example).
  - Add a short section on DirectML/CUDA paths and WSL alternatives.
- Local run steps (Windows):
  1. Create and activate venv
  2. pip install llama-cpp-python
  3. Place GGML model and run the example

D. web-app
- Purpose: FastAPI backend for agent orchestration and RAG endpoints; includes a local-first inference client with optional hybrid fallback to Azure/OpenAI.
- Key files: web-app/backend/app/main.py, web-app/backend/clients/inference_client.py, web-app/backend/requirements.txt, web-app/README.md
- Implementation notes:
  - Keep hybrid fallback disabled by default via USE_HYBRID=false. Require env vars AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY to enable.
  - Keep inference client retries and timeouts conservative to avoid cascading costs with cloud endpoints.
- Local run steps:
  1. python -m venv .venv && source .venv/bin/activate
  2. pip install -r web-app/backend/requirements.txt
  3. uvicorn web-app.backend.app.main:app --reload --host 0.0.0.0 --port 8080
- CI checks:
  - Lint the web-app folder; include a smoke test that the /health endpoint returns status: ok (can be a simple pytest/requests test or a lightweight HTTP check in CI).

E. infra
- Purpose: CI skeleton, developer setup scripts, GPU guidance and examples (vLLM/TGI notes). Contains .github workflows and scripts.
- Key files: .github/workflows/ci.yml, scripts/dev_setup.sh, scripts/dev_setup.ps1, infra/gpu/README.md
- Implementation notes:
  - Set Actions workflow permissions to Read & write to allow automation to create/update branches if desired.
  - If branch protection rules exist, add the automation account to the allowed list or require PRs from forks.
- CI checks:
  - Lint, test and docker-smoke jobs as included in the workflow.

F. docs
- Purpose: central place for architecture, runbooks, contributing guidelines, CODEOWNERS
- Key files: docs/ARCHITECTURE.md, docs/RUNNING_LOCAL_GPU.md, docs/ROADMAP.md, docs/BRANCHES.md, docs/CONTRIBUTING.md, .github/CODEOWNERS
- Implementation notes:
  - Keep runbooks simple and reproducible; include exact commands and required env variables.
  - Use docs to capture any security or governance constraints for ingestion and modeling.

G. tooling & integrations
- Purpose: Placeholders for forensic wrappers (YARA/osquery), and integration stubs (GitHub MCP, M365 Graph)
- Implementation notes:
  - These should be small examples that do not include credentials; provide sample config and .env.example files.

3. Applying changes & PR guidance (step-by-step)

A. Create local branches and push (if you do this manually)
1. git fetch origin
2. git checkout -b <branch> origin/<branch>  # e.g. origin/web-app
3. Make further edits, add files, then:
   git add <files>
   git commit -m "scaffold: <branch> - <short description>"
   git push origin HEAD

B. Create PRs (recommended using GH CLI)
- Example (web-app):
  gh pr create --repo RoseTechCyber/Agentic-Cybersecurity-Framework --base main --head web-app --title "scaffold: web-app backend skeleton + inference client" --body-file web-app_pr_body.md

C. PR body template (copy for each PR)
- Title: <brief title>
- Body: include 1) what is added, 2) how to test (exact commands), 3) security notes, 4) PR checklist
- Add reviewers and labels (e.g., scaffolding, infra, web-app)

D. PR checklist (copy into body)
- [ ] Linting passes (ruff/flake8)
- [ ] Unit test smoke (pytest)
- [ ] No secrets or model binaries committed
- [ ] Docker smoke-start for branches that add services

4. Hybrid fallback (web-app) implementation notes
- Default: USE_HYBRID=false
- To enable hybrid mode:
  - Set USE_HYBRID=true in environment where web-app runs
  - Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY (or equivalent variables for other cloud providers)
- Cost & privacy: Document the expected cost per request and required data handling for sending content to cloud providers.

5. Enabling automated pushes / PRs and Action workflows
- Invite automation/service account as a collaborator with Write access and confirm the invite is accepted.
- Settings → Actions → Workflow permissions: set to Read & write and optionally enable PR creation by Actions.
- If you need the agent to push to protected branches, add the automation to the branch protection allowlist.

6. GPU inference deployment notes
- Linux GPU (recommended for prod testing): prefer vLLM or TGI running in a GPU-enabled container behind an HTTP endpoint. Document the docker-compose snippet and required host drivers.
- Windows GPU: prefer WSL2 + CUDA or build DirectML-enabled binaries; include a short note in foundry-windows-local on alternatives.

7. Troubleshooting
- Permission errors pushing/creating PRs: check pending invites, Actions workflow permissions, and branch protection rules.
- Docker errors in CI: ensure the CI runner has privileged Docker-in-Docker support (or skip docker-smoke in PR CI and run manually).
- Model errors: verify model path env var (LLAMA_MODEL_PATH) and that the model binary is present on the host (not in repo).

8. Next steps & milestones
- Add GPU server examples (vLLM/TGI) as runnable docker-compose in infra/gpu with a minimal model demonstration (use small HF models for testing).
- Expand agent plugin examples and add E2E tests that run ingestion → retrieval → response using the emulator + small local model.
- Add security hardening: secrets scanning, pre-commit hooks, and CI gating for large files.

9. Contact & maintainers
- Repository owner: @RoseTechCyber
- For infra & CI: @RoseTechCyber (or replace with your infra team)


