# Credit repair playbook outline (for CreditFix-GPT)

The agent should expand this into `auto_gpt_workspace/credit_repair_playbook.md`.

## 1. Pull your reports
- Get free reports from AnnualCreditReport.com (all three bureaus).
- Save PDFs; never share full SSN in chat logs if avoidable.

## 2. Inventory every line item
- Accounts, balances, payment status, dates opened/closed
- Hard inquiries and public records
- Mark: accurate / inaccurate / unsure / not mine

## 3. Fix errors the legal way
- Dispute inaccurate items with the bureau and the furnisher
- Use templates in `agents/credit_repair/templates/`
- Keep copies and dates of everything sent

## 4. Improve the score fundamentals
- On-time payments (largest factor)
- Keep credit card utilization under ~30% (lower is better)
- Avoid unnecessary new hard inquiries
- Do not close old accounts solely for "optimization" without understanding average age of accounts

## 5. Identity theft (if applicable)
- Place fraud alerts or freezes
- File FTC IdentityTheft.gov report and police report when needed
- Follow official recovery steps only

## 6. What this agent will not do
- Fake identities, synthetic IDs, or fabricated employment/address history
- "Credit washing" or advising you to dispute accurate debts as a delay tactic
- Guaranteeing a specific score increase
