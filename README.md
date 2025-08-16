# Jobpilot
Job Pilot – An open-source, AI-powered job-hunting copilot. It automatically searches and aggregates job postings from multiple sources – including Greenhouse, Lever, Ashby, SmartRecruiters, Monster (RSS), Dice (API), LinkedIn, and Indeed – then logs them into Google Sheets for tracking.

An end-to-end *job-hunt copilot* that:
1) searches job boards (Greenhouse, Lever, Ashby, SmartRecruiters),
2) extracts job + recruiter info,
3) logs to Google Sheets,
4) (optionally) auto-applies via Playwright (site-specific, ToS permitting),
5) writes a tailored cover letter,
6) customizes your resume, and
7) emails the recruiter (or drafts an email) via Gmail API.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install  # needed only if you plan to use auto-apply flows
cp config.example.toml config.toml
# Put your Google service account JSON at service_account.json (Sheets)
# Put your Gmail OAuth token at token.json (after running a quick OAuth flow)
python main.py
```

## Google Setup
- **Sheets**: Create a Service Account in Google Cloud Console. Download JSON as `service_account.json` at project root. Share your target Google Sheet with the service account email.
- **Gmail**: Enable Gmail API for your Google account. Use OAuth flow to create `token.json` (this repo expects it). You can also choose to create drafts only instead of sending email.

## Configuration
See `config.example.toml`. Copy to `config.toml` and fill:
- `google.sheet_id` - Your Google Sheet ID.
- `openai.api_key` - Your OpenAI API key.
- `agent.master_resume_json` - Path to the resume data source JSON.
- Update `TARGETS` in `main.py` with your companies (by platform).

## Legal & ToS Notes
- Respect websites’ Terms of Service. Use automation only for sites you are permitted to automate.
- Some job boards use CAPTCHAs/anti-bot; prefer semi-automated review + one-click assist.
- This is a reference implementation provided as-is.

## Structure
```
job_agent/
  adapters/       # job board fetchers
  apply_flows/    # site-specific Playwright flows (optional)
  llm/            # cover letter + resume tailoring
  data/           # sample data (resume, bio)
  mail/           # Gmail send/draft
  sheets.py       # Google Sheets append & update
  models.py       # Pydantic models
  config.py       # config loader
main.py           # orchestrator
```

## Typical Run
- Fetch jobs from configured boards → append to Google Sheet.
- For each job (demo: first 5), generate a cover letter and tailored resume (saved under `outputs/`).
- (Optional) Kick an apply flow or compose an email draft.

Enjoy and customize!

