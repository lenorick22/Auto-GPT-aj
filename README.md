# Auto-GPT-aj

Autonomous GPT agent fork with ready-to-run presets.

> Upstream Chinese docs redirect: https://github.com/kaqijiang/Auto-GPT-ZH

## CreditFix-GPT — fix your credit (legally)

This repo includes a preset agent that helps you improve credit through **lawful** steps: pull reports, find errors, draft FCRA-style dispute and goodwill letters, and build a payment/utilization plan.

```bash
cp .env.template .env   # add your OPENAI_API_KEY
pip install -r requirements.txt
python -m autogpt -C agents/credit_repair.yaml
# or: ./scripts/run_credit_repair.sh
```

Details and letter templates: [`agents/README.md`](agents/README.md).

**Important:** CreditFix-GPT is educational automation, not a licensed credit counselor or attorney. It will not help with fraud, fake identities, or disputing accurate debts in bad faith.
