#!/usr/bin/env bash
# Bootstrap + start CreditFix-GPT (legal credit improvement only).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PYTHON_BIN="${PYTHON_BIN:-}"
if [[ -z "$PYTHON_BIN" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN=python3
  elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN=python
  else
    echo "Python not found. Install Python 3 or set PYTHON_BIN."
    exit 1
  fi
fi

if [[ ! -f .env ]]; then
  echo "Missing .env — copy .env.template to .env and set OPENAI_API_KEY."
  exit 1
fi

SEED_DIR="$ROOT/agents/credit_repair/seed"
DEST_DIR="$ROOT/auto_gpt_workspace/creditfix"
mkdir -p "$DEST_DIR"/{letters,trackers}

shopt -s nullglob
for src in "$SEED_DIR"/* "$SEED_DIR"/letters/* "$SEED_DIR"/trackers/*; do
  [[ -f "$src" ]] || continue
  rel="${src#$SEED_DIR/}"
  dest="$DEST_DIR/$rel"
  mkdir -p "$(dirname "$dest")"
  if [[ ! -f "$dest" ]]; then
    cp "$src" "$dest"
    echo "Seeded $rel"
  fi
done

echo "CreditFix workspace: $DEST_DIR"
echo "Starting CreditFix-GPT..."
exec "$PYTHON_BIN" -m autogpt -C agents/credit_repair.yaml "$@"
