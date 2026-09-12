# CreditFix-GPT — executive brief

**Date:** [DATE]  
**Client:** [FULL LEGAL NAME]  
**Goal:** Raise creditworthiness through **lawful** report cleanup + fundamentals (payments, utilization, inquiries).

## Snapshot
| Item | Value |
| --- | --- |
| Scores (E / X / T) | [ ] / [ ] / [ ] |
| Overall revolving utilization | [ ]% |
| Open collections / charge-offs | [ ] |
| Hard inquiries (12 mo) | [ ] |
| Identity-theft suspected? | Yes / No |

## 5-phase operating system
0. **Setup** — workspace, questions, freezes if needed  
1. **Rights** — FCRA/CFPB timelines, freeze/alert options, official links  
2. **Inventory** — every tradeline/inquiry/public record classified  
3. **Letters** — error disputes, validation, goodwill (accurate lates only)  
4. **Rebuild** — on-time automation, utilization targeting, inquiry hygiene  
5. **Close-out** — ranked next actions + follow-up calendar  

## First 48 hours
1. Answer `QUESTIONS_FOR_USER.md` (no full SSN in chat if avoidable).  
2. Pull Equifax + Experian + TransUnion via AnnualCreditReport.com.  
3. Place security freezes if fraud risk.  
4. Fill `trackers/report_inventory.csv` (one row per item).  
5. Run utilization math:
   `python agents/credit_repair/tools/credit_math.py utilization --cards 'name:bal:limit,...'`

## Success metrics
- Utilization trending under 30% (stretch: under 10% before statement close)  
- Growing on-time streak  
- Every dispute logged with dates/outcomes  
- No surprise hard pulls  

## Hard rules
- Dispute **errors** and unverifiable items — not accurate debts to stall collectors.  
- Never invent identifiers or account numbers.  
- Not legal advice; accurate negatives may remain until they age off.
