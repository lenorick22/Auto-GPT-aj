# Auto-GPT agent presets

## CreditFix-GPT (legal credit improvement)

Helps you research consumer rights, spot report errors, draft dispute/goodwill letters, and build a payment/utilization plan. It is **not** a lawyer or guaranteed credit-repair service, and it refuses illegal tactics.

### Run

1. Copy `.env.template` to `.env` and set a valid `OPENAI_API_KEY`.
2. Install deps: `pip install -r requirements.txt`
3. Start the agent:

```bash
python -m autogpt -C agents/credit_repair.yaml
```

Or:

```bash
./scripts/run_credit_repair.sh
```

### What it creates

Under `auto_gpt_workspace/` (gitignored runtime folder), the agent should produce:

- `credit_repair_playbook.md` — step-by-step plan
- Dispute / goodwill letter drafts personalized from your notes
- A simple progress tracker

Starter templates live in `agents/credit_repair/templates/`.
