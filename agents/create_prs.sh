#!/usr/bin/env bash
set -euo pipefail

REPO="RoseTechCyber/Agentic-Cybersecurity-Framework"
REVIEWER="RoseTechCyber"

# Make a temp directory for PR body files
TMPDIR="$(mktemp -d)"
echo "Using temp dir: $TMPDIR"

# PR bodies
cat > "$TMPDIR/data-integration.md" <<'EOF'
Adds a data-integration scaffold for local development.

Includes:
- docker-compose.yml (Cosmos DB emulator, Chroma, Redis)
- connectors/ingest_cosmos.py (example ingestion to Cosmos emulator + Chroma)
- fabric_adapter/README.md (local Fabric simulation guidance)

How to test (quick):
1. cd data-integration && docker-compose up -d
2. Wait for Cosmos emulator to initialize, create sample JSON files in sample_data/
3. python connectors/ingest_cosmos.py --path sample_data

Security notes:
- Uses Cosmos emulator dev key for convenience; do not use this key in production.

PR checklist:
- [ ] ruff/flake8 linting passes
- [ ] pytest smoke (if any tests) passes
- [ ] No secrets or model files committed (.env.example only)
- [ ] docker-compose smoke-start verified
EOF

cat > "$TMPDIR/foundry-windows-local.md" <<'EOF'
Adds native-Windows LLaMA quickstart and install instructions for local experimentation.

Includes:
- README.md
- install/README.md (Windows install + model placement instructions)
- examples/llama_cpp_example.py (llama-cpp-python quickstart)

How to test (quick):
1. On Windows: create venv, pip install llama-cpp-python
2. Place a GGML quantized model (not committed) and set LLAMA_MODEL_PATH or place at C:\models\
3. python examples/llama_cpp_example.py

Security notes:
- Do not commit model binaries or large files.
- Follow licensing for model downloads.

PR checklist:
- [ ] Lint
- [ ] Example verified locally (no model binaries in repo)
- [ ] No secrets or large files committed
EOF

cat > "$TMPDIR/agents.md" <<'EOF'
Adds a minimal reasoning agent scaffold and unit tests.

Includes:
- agents/reasoning_agent/core.py
- agents/orchestrator/runner.py (example plugin)
- agents/tests/test_agent_basic.py
- agents/requirements.txt

How to test (quick):
1. python -m venv .venv && source .venv/bin/activate
2. pip install -r agents/requirements.txt
3. pytest agents/tests/test_agent_basic.py

PR checklist:
- [ ] ruff/flake8 linting passes
- [ ] pytest unit test(s) pass
- [ ] Requirements minimal and safe (no secrets)
EOF

cat > "$TMPDIR/web-app.md" <<'EOF'
Adds a FastAPI backend skeleton (RAG & agent endpoints) and a local-first inference client with optional hybrid fallback.

Includes:
- web-app/backend/app/main.py (endpoints: /health, /agents/run, /rag/query)
- web-app/backend/clients/inference_client.py (local-first, optional hybrid fallback to Azure/OpenAI)
- web-app/backend/requirements.txt
- web-app/README.md

How to test (quick):
1. python -m venv .venv && source .venv/bin/activate
2. pip install -r web-app/backend/requirements.txt
3. uvicorn web-app.backend.app.main:app --reload --host 0.0.0.0 --port 8080
4. Test endpoints: GET /health, POST /agents/run, POST /rag/query
5. To test hybrid fallback: set USE_HYBRID=true and configure AZURE_OPENAI_ENDPOINT & AZURE_OPENAI_KEY

Security notes:
- Hybrid is off by default and requires environment variables for Azure/OpenAI.
- Do not commit credential files; use .env.example.

PR checklist:
- [ ] Lint
- [ ] Unit-test smoke
- [ ] Hybrid fallback documented and off-by-default (USE_HYBRID env)
- [ ] No secrets in repo
EOF

cat > "$TMPDIR/infra.md" <<'EOF'
Adds infra scaffolding including CI workflow, developer setup scripts, and GPU run guidance.

Includes:
- .github/workflows/ci.yml (lint, test, docker-smoke)
- scripts/dev_setup.sh (Linux)
- scripts/dev_setup.ps1 (Windows)
- infra/gpu/README.md (GPU notes + vLLM/TGI guidance)

How to test (quick):
1. Run the CI on this PR to validate workflow triggers
2. Optionally run scripts/dev_setup.sh in a safe dev environment to verify dev env steps
3. Review infra/gpu/README.md for recommended GPU stacks

PR checklist:
- [ ] CI workflow triggered and ran on PR
- [ ] ruff/flake8 linting step included
- [ ] No credentials or secrets added
- [ ] Documentation for GPU run validated
EOF

# Branches and titles
declare -A BRANCH_TITLE=(
  ["data-integration"]="scaffold: data-integration (Cosmos emulator, Chroma, ingestion example)"
  ["foundry-windows-local"]="feat(foundry-windows-local): native Windows LLaMA quickstart"
  ["agents"]="scaffold: agents (reasoning agent core, orchestrator, tests)"
  ["web-app"]="scaffold: web-app backend skeleton + inference client (local-first + hybrid)"
  ["infra"]="scaffold(infra): CI workflow, dev setup scripts, GPU guidance"
)

declare -A BRANCH_BODYFILE=(
  ["data-integration"]="$TMPDIR/data-integration.md"
  ["foundry-windows-local"]="$TMPDIR/foundry-windows-local.md"
  ["agents"]="$TMPDIR/agents.md"
  ["web-app"]="$TMPDIR/web-app.md"
  ["infra"]="$TMPDIR/infra.md"
)

# Create PRs
for branch in "${!BRANCH_TITLE[@]}"; do
  echo "Creating PR for branch: $branch"
  # Check that remote branch exists
  if gh api repos/"$REPO"/branches/"$branch" > /dev/null 2>&1; then
    gh pr create --repo "$REPO" --base main --head "$branch" --title "${BRANCH_TITLE[$branch]}" --body-file "${BRANCH_BODYFILE[$branch]}" --add-reviewer "$REVIEWER" || {
      echo "gh pr create failed for $branch"
    }
  else
    echo "Remote branch $branch does not exist. Skipping."
  fi
done

echo "Done. Temp files are in $TMPDIR (remove when done)."
