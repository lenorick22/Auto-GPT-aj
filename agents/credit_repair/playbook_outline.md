# CreditFix master playbook

Expand into `auto_gpt_workspace/creditfix/` during a run. Prefer official sources.

## Score levers (typical FICO-style emphasis)
1. **Payment history** — never miss due dates; autopay at least the minimum  
2. **Utilization** — under 30%; many target under 10% before statement close  
3. **Age of history** — don’t casually close oldest cards  
4. **Mix** — long-term; don’t open junk accounts just for “mix”  
5. **New credit** — minimize unnecessary hard inquiries  

## Error vs accurate negative
| Situation | Move |
| --- | --- |
| Not your account / mixed file | Bureau + furnisher dispute; freeze if theft |
| Wrong balance/status/dates | Dispute with evidence |
| Duplicate collection | Dispute duplicates |
| Accurate late payment | Goodwill after sustained on-time; else wait for aging |
| Unfamiliar collection | Debt validation |

## Evidence standards
- Government ID + proof of address  
- Statements showing correct balance/status  
- FTC IdentityTheft.gov affidavit / police report for theft  
- Mail copies only — never originals  

## Cadence
- Weekly: utilization check + payment calendar  
- ~30 days: dispute follow-ups  
- 90 days: full re-inventory + refresh `NEXT_ACTIONS.md`
