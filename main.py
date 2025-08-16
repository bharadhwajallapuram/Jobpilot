import os, json, pathlib
from job_agent.config import load_config
from job_agent.adapters.greenhouse import fetch_greenhouse
from job_agent.adapters.lever import fetch_lever
from job_agent.adapters.ashby import fetch_ashby
from job_agent.adapters.smartrecruiters import fetch_smartrecruiters
from job_agent.sheets import open_sheet, append_jobs
from job_agent.llm.generate import generate_cover_letter, tailor_resume

def fetch_all(cfg):
    targets = cfg.get("targets", {})
    jobs = []
    for slug in targets.get("greenhouse", []):
        jobs += fetch_greenhouse(slug)
    for slug in targets.get("lever", []):
        jobs += fetch_lever(slug)
    for slug in targets.get("ashby", []):
        jobs += fetch_ashby(slug)
    for slug in targets.get("smartrecruiters", []):
        jobs += fetch_smartrecruiters(slug)
    # de-dup by (source, req_id) or (company, title, location)
    seen = set()
    deduped = []
    for j in jobs:
        key = (j.source, j.req_id or f"{j.company}|{j.title}|{j.location}")
        if key in seen:
            continue
        seen.add(key)
        deduped.append(j)
    return deduped

def main():
    cfg = load_config()
    outdir = pathlib.Path(cfg["agent"]["output_dir"])
    outdir.mkdir(parents=True, exist_ok=True)

    # 1) Fetch jobs
    jobs = fetch_all(cfg)

    # 2) Write to Google Sheet
    ws = open_sheet(cfg["google"]["sheet_id"])
    append_jobs(ws, jobs)

    # 3) Prepare artifacts for first N jobs
    n = int(cfg["agent"].get("max_jobs_per_run", 5))
    candidate_bio = json.load(open("data/candidate_bio.json", encoding="utf-8"))
    prepared = 0

    for j in jobs:
        if prepared >= n:
            break
        cover = generate_cover_letter(candidate_bio, j.model_dump())
        cover_path = outdir / f"cover_{j.company}_{j.req_id or 'x'}.txt"
        cover_path.write_text(cover, encoding="utf-8")

        resume_path = outdir / f"resume_{j.company}_{j.req_id or 'x'}.docx"
        tailor_resume(cfg["agent"]["master_resume_json"], j.model_dump(), str(resume_path))

        print(f"Prepared: {j.title} @ {j.company}\n  Cover: {cover_path}\n  Resume: {resume_path}\n  Apply: {j.apply_url}\n")
        prepared += 1

if __name__ == "__main__":
    main()