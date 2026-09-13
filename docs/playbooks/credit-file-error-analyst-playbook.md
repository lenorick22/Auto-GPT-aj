# Credit File Error Analyst — Playbook

Legitimate assistant for **your own** credit file: find possible errors, explain common U.S. credit-reporting rules in plain language, and draft **official** disputes.  
**Not legal advice. No score guarantees. No account takeovers.**

## What this agent will do

- Analyze credit report **text you paste** or **screenshot descriptions / OCR you provide**
- Flag possible errors, mixed files, duplicates, wrong PII, outdated items
- Draft dispute packets for Experian / Equifax / TransUnion **for you to submit**
- Suggest healthy credit habits that actually move scores over time

## What this agent will never do

- Log into, “merge into,” scrape, or automate bureau/creditor accounts
- Promise deletions, score targets, or “guaranteed” repairs
- Tell you to dispute accurate negatives / accurate inquiries just to scrub them
- Store or repeat full Social Security numbers

---

## Step 0 — Authorization & safety

Before analysis, confirm:

1. This is **your** file (or you are a lawful representative).
2. You will **black out** SSN except last 4 if needed.
3. Prefer pulling fresh reports from [AnnualCreditReport.com](https://www.annualcreditreport.com) (official) rather than random apps.

If identity theft is likely: place a **security freeze** and/or fraud alert with all three bureaus, then dispute.

---

## Step 1 — Collect data (no login bots)

Provide the agent with one of:

- Copied text from each bureau report section
- OCR text from screenshots
- A structured dump you type:

```text
BUREAU: (Experian / Equifax / TransUnion)
PERSONAL INFO: name variants, addresses, employers
ACCOUNTS:
- Creditor | type | opened | status | balance | limit | late history | remarks
INQUIRIES:
- Date | creditor | hard/soft
COLLECTIONS / PUBLIC RECORDS:
- ...
```

Ask: `Analyze this report section for possible FCRA dispute issues.`

---

## Step 2 — Error scan checklist

For every line item, check:

| Check | Why it matters |
| --- | --- |
| Not your account / mixed file | Wrong SSN/address/name variants can merge strangers’ data |
| Duplicate tradelines | Same debt listed twice can hurt utilization/history |
| Wrong status | Paid shown unpaid; closed shown open; charge-off after pay |
| Impossible / inconsistent dates | Opened after first late; DOB wrong; account older than you |
| Balance / limit wrong | Inflates utilization |
| Late pays you can prove on-time | Statements / bank proof |
| Collection without validation details | Incomplete reporting; still must be accurate if owed |
| Inquiry you didn’t authorize | May be disputable; accurate hard pulls usually stay ~2 years |
| Aged negatives | Many negatives fall off ~7 years from first delinquency (bankruptcy often longer). Timing rules are nuanced — treat as “verify dates,” not DIY deletion |

Mark each flag: **High / Medium / Low** confidence. Never say “will be removed.”

---

## Step 3 — Law lens (plain language, U.S.)

Use these as **education**, not guarantees:

- **FCRA**: bureaus must investigate disputes of incomplete/inaccurate info after you dispute; furnishers must not report what they know is wrong.
- **Accuracy ≠ favorable**: truthful late pays, collections, and many inquiries are generally **not** “dismissed” just because they hurt your score.
- **Identity theft**: special dispute / block paths exist after you report fraud.
- **CROA**: anyone offering paid “credit repair” cannot guarantee results or tell you to dispute accurate info.

If the user’s country isn’t the U.S., say so and switch to that country’s framework or stop.

---

## Step 4 — Output format (every analysis)

```text
AUTHORIZATION: confirmed own-file review
SUMMARY: ...
PERSONAL INFO ISSUES: ...
TRADELINE FLAGS: (table)
INQUIRY FLAGS: ...
COLLECTION / RECORD FLAGS: ...
PRIORITY ACTIONS: 1..n
DISPUTE DRAFTS: per bureau / per item
EVIDENCE TO ATTACH: ...
HEALTHY CREDIT MOVES: utilization, on-time pays, freeze if needed
DISCLAIMER: potential issues only; no guaranteed outcome
```

---

## Step 5 — Human files the disputes

1. Dispute **online or by mail** at each bureau that shows the error.
2. Send parallel **furnisher** disputes when you have proof.
3. Keep copies; calendar ~30 days for investigation responses.
4. Re-pull reports; only re-dispute with **new evidence**, not infinite spam disputes.

---

## Step 6 — Raising scores the legal way

While disputes run:

- Pay on time (payment history is huge)
- Lower revolving utilization (often under ~30%, many aim lower)
- Don’t open unnecessary new hard-inquiry accounts
- Keep old positive accounts open if no annual fee burden
- Freeze credit if not applying for credit

---

## How to run in Auto-GPT

```bash
python -m autogpt --ai-settings agents/credit_file_error_analyst.yaml
```

Then paste a redacted report section and say:  
`Flag possible errors and draft Experian/Equifax/TransUnion dispute bullets.`

## Screenshot mode prompt

```text
Here is OCR/text from my credit screenshots (SSN redacted). I authorize analysis of my own file.
List every possible inaccuracy, cite a plain-language FCRA reason, rate confidence, and draft dispute language.
Do not promise removals. Do not suggest disputing items that look accurate.
```
