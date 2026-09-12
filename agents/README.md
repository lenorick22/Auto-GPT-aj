# Auto-GPT agent presets

## CreditFix-GPT (legal credit improvement)

A full credit-rebuild kit: rights research, report inventory, dispute/goodwill/validation letters, utilization & payoff math, and a 30/60/90 plan.

It is **not** a lawyer or guaranteed repair service. It refuses fraud and bad-faith disputes of accurate debts.

### Quick start

```bash
cp .env.template .env   # set OPENAI_API_KEY
pip install -r requirements.txt
./scripts/run_credit_repair.sh
```

Or without bootstrap:

```bash
python -m autogpt -C agents/credit_repair.yaml
```

### What you get

| Path | Purpose |
| --- | --- |
| `agents/credit_repair.yaml` | Agent brain (goals, constraints, operating rules) |
| `agents/credit_repair/seed/` | Files copied into the workspace on first run |
| `agents/credit_repair/templates/` | Bureau/furnisher dispute, goodwill, validation letters |
| `agents/credit_repair/tools/credit_math.py` | Utilization, target paydown, payoff, snowball/avalanche |

Runtime outputs land in `auto_gpt_workspace/creditfix/` (gitignored).

### Math tool examples

```bash
python agents/credit_repair/tools/credit_math.py utilization --cards 'visa:900:3000,amex:400:1000'
python agents/credit_repair/tools/credit_math.py target --balance 1200 --limit 4000 --target-pct 10
python agents/credit_repair/tools/credit_math.py payoff --balance 2500 --apr 22.9 --payment 200
python agents/credit_repair/tools/credit_math.py snowball --debts 'a:900:19,b:400:24' --budget 300 --method avalanche
```

### Recommended first session

1. Fill `QUESTIONS_FOR_USER.md` (seeded into the workspace).
2. Pull all three reports from AnnualCreditReport.com.
3. Let the agent classify tradelines and draft only **error-based** disputes.
4. Run `credit_math.py` to plan utilization and payoff.
