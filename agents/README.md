# Agents

Specialized Auto-GPT personas for this repo.

## Nations Light — Meta Growth Agent

Ethical Meta (Facebook/Instagram) content and growth coach for a page celebrating Native American / Indigenous Nations cultures.

- Config: `agents/native_nations_meta_growth.yaml`
- Playbook: `docs/playbooks/native-nations-meta-page-playbook.md`

### Run

```bash
python -m autogpt --ai-settings agents/native_nations_meta_growth.yaml
```

Uses official Meta Business Suite / Ads Manager workflows only. Drafts require human approval before publishing.

## Credit File Error Analyst

Analyzes **your own** credit report text or screenshot OCR for possible errors and drafts official FCRA disputes. No bureau logins, no guaranteed deletions, no scrubbing accurate negatives.

- Config: `agents/credit_file_error_analyst.yaml`
- Playbook: `docs/playbooks/credit-file-error-analyst-playbook.md`

### Run

```bash
python -m autogpt --ai-settings agents/credit_file_error_analyst.yaml
```
