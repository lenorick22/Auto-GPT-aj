#!/usr/bin/env bash
# Install CreditFix knowledge corpus into the workspace (and optionally into Auto-GPT memory).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PYTHON_BIN="${PYTHON_BIN:-}"
if [[ -z "$PYTHON_BIN" ]]; then
  if command -v python3 >/dev/null 2>&1; then PYTHON_BIN=python3
  elif command -v python >/dev/null 2>&1; then PYTHON_BIN=python
  else echo "Python not found"; exit 1; fi
fi

KB_SRC="$ROOT/agents/credit_repair/knowledge"
SEED_SRC="$ROOT/agents/credit_repair/seed"
DEST="$ROOT/auto_gpt_workspace/creditfix"
mkdir -p "$DEST/knowledge" "$DEST/letters" "$DEST/trackers"

copy_tree() {
  local src="$1" dest="$2"
  shopt -s nullglob
  for f in "$src"/*; do
    [[ -f "$f" ]] || continue
    local base="$(basename "$f")"
    if [[ ! -f "$dest/$base" ]]; then
      cp "$f" "$dest/$base"
      echo "Installed $base"
    else
      # Knowledge corpus should stay fresh — overwrite knowledge docs
      if [[ "$dest" == *"/knowledge" ]]; then
        cp "$f" "$dest/$base"
        echo "Updated $base"
      fi
    fi
  done
}

echo "=== CreditFix training: knowledge corpus ==="
copy_tree "$KB_SRC" "$DEST/knowledge"

echo "=== CreditFix training: seed templates/trackers ==="
for f in "$SEED_SRC"/*; do
  [[ -f "$f" ]] || continue
  base="$(basename "$f")"
  if [[ ! -f "$DEST/$base" ]]; then cp "$f" "$DEST/$base"; echo "Seeded $base"; fi
done
for sub in letters trackers; do
  mkdir -p "$DEST/$sub"
  for f in "$SEED_SRC/$sub"/*; do
    [[ -f "$f" ]] || continue
    base="$(basename "$f")"
    if [[ ! -f "$DEST/$sub/$base" ]]; then cp "$f" "$DEST/$sub/$base"; echo "Seeded $sub/$base"; fi
  done
done

# Manifest of trained modules
"$PYTHON_BIN" - <<PY
from pathlib import Path
kb = Path("auto_gpt_workspace/creditfix/knowledge")
mods = sorted(p.name for p in kb.glob("*.md"))
manifest = kb / "TRAINED_MANIFEST.md"
manifest.write_text(
    "# CreditFix trained modules\\n\\n"
    + "\\n".join(f"- {m}" for m in mods)
    + "\\n\\nCreditFix-GPT should read INDEX.md then these modules as needed.\\n"
)
print(f"Manifest written ({len(mods)} modules)")
PY

if [[ "${INGEST_MEMORY:-0}" == "1" ]]; then
  if [[ ! -f .env ]]; then
    echo "INGEST_MEMORY=1 requires .env with OPENAI_API_KEY for embeddings."
    exit 1
  fi
  echo "=== Ingesting knowledge into Auto-GPT memory ==="
  "$PYTHON_BIN" -m autogpt.data_ingestion --dir "$DEST/knowledge" --init
  echo "Memory ingest complete."
else
  echo "Knowledge files installed to $DEST/knowledge"
  echo "Tip: INGEST_MEMORY=1 ./scripts/train_credit_repair.sh  # also embed into Auto-GPT memory (needs API key)"
fi

echo "Training complete. Start with: ./scripts/run_credit_repair.sh"
