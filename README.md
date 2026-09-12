# Auto-GPT-aj

Autonomous GPT agent fork with a production-ready **CreditFix-GPT** preset.

> Upstream Chinese docs: https://github.com/kaqijiang/Auto-GPT-ZH

## CreditFix-GPT — rebuild credit the legal way

Not a vague chatbot prompt — a full operating kit:

- 5-phase agent goals + hard compliance constraints (English output, no invented IDs)
- Seed workspace: inventory CSV, dispute log, 30/60/90 plan, bureau contacts
- Letter pack: bureau dispute, furnisher dispute, goodwill, debt validation
- `credit_math.py` for utilization targets and snowball/avalanche previews
- Trained **knowledge corpus** (15+ modules) on scores, FCRA rights, disputes, collections, rebuilding, scams

```bash
cp .env.template .env   # add OPENAI_API_KEY
pip install -r requirements.txt
./scripts/train_credit_repair.sh   # install knowledge
./scripts/run_credit_repair.sh
```

Docs: [`agents/README.md`](agents/README.md)

**Disclaimer:** Educational automation only — not a licensed credit counselor or attorney. Accurate negatives may remain until they age off. No fraud, fake identities, or bad-faith disputes.
