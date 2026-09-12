#!/usr/bin/env bash
# Start the CreditFix-GPT Auto-GPT agent (legal credit improvement only).
set -euo pipefail
cd "$(dirname "$0")/.."

if [[ ! -f .env ]]; then
  echo "Missing .env — copy .env.template to .env and set OPENAI_API_KEY."
  exit 1
fi

exec python -m autogpt -C agents/credit_repair.yaml "$@"
