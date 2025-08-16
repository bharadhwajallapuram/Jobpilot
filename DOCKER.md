# Docker & Compose Usage

## Build
```bash
docker compose build
```

## Configure
1. Copy `.env.example` -> `.env` and set `OPENAI_API_KEY`.
2. Put your Google Sheets `service_account.json` at project root (or remove the volume if not using Sheets).
3. If you want to send emails, place your Gmail OAuth `token.json` at project root.
4. Update `config.toml` with your targets and sheet id.

## Run
```bash
docker compose up --build
```

Artifacts (cover letters and tailored resumes) appear in `./outputs` on your host.
