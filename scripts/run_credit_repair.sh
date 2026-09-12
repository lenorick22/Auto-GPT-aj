#!/usr/bin/env bash
# Install knowledge corpus then start CreditFix-GPT.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
"$ROOT/scripts/train_credit_repair.sh"

PYTHON_BIN="${PYTHON_BIN:-}"
if [[ -z "$PYTHON_BIN" ]]; then
  if command -v python3 >/dev/null 2>&1; then PYTHON_BIN=python3
  elif command -v python >/dev/null 2>&1; then PYTHON_BIN=python
  else echo "Python not found"; exit 1; fi
fi
if [[ ! -f .env ]]; then
  echo "Missing .env — copy .env.template to .env and set OPENAI_API_KEY."
  exit 1
fi
echo "Starting CreditFix-GPT with trained knowledge corpus..."
exec "$PYTHON_BIN" -m autogpt -C agents/credit_repair.yaml "$@"
