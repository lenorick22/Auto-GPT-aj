# Reading credit reports

## Three bureaus
Equifax, Experian, TransUnion can each show different data. Always compare all three when possible (AnnualCreditReport.com).

## Sections to inventory
1. **Personal info** — names, addresses, employers (mixed files often start here).
2. **Accounts / tradelines** — revolving, installment, open, closed, authorized user.
3. **Collections** — original creditor, collector, amount, status.
4. **Public records** — bankruptcies (tax liens/judgments reporting rules have changed over time — verify current bureau practice).
5. **Inquiries** — hard vs soft.
6. **Consumer statements** — optional notes.

## For each tradeline capture
- Bureau, creditor, account mask, dates opened/reported, status, balance, limit, past due
- Payment pattern codes if shown
- Whether it is yours, accurate, duplicate, obsolete, or unverifiable

## Classification labels (CreditFix standard)
- `keep` — accurate, leave alone while rebuilding
- `dispute-error` — wrong facts / wrong person / duplicate / not verifiable
- `investigate` — unclear; need statements or validation
- `not-mine` — possible mixed file or fraud
- `identity-theft` — confirmed or strongly suspected theft

## Red flags
- Accounts you never opened
- Wrong late dates or “current” vs “charged off” mismatch
- Same debt listed twice (original + collection without correct status)
- Closed account still showing incorrect past-due
- Address/name you’ve never used (possible mixed file)
