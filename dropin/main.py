import os, json, pathlib
from job_agent.config import load_config
from job_agent.adapters.greenhouse import fetch_greenhouse
from job_agent.adapters.lever import fetch_lever
from job_agent.adapters.ashby import fetch_ashby
from job_agent.adapters.smartrecruiters import fetch_smartrecruiters
from job_agent.adapters.monster_rss import fetch_monster_rss
from job_agent.adapters.dice_api import fetch_dice
from job_agent.adapters.indeed_linkedin_playwright import fetch_from_signed_in_search
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
    # de-dup
    seen = set()
    deduped = []
    for j in jobs:
        key = (j.source, j.req_id or f"{j.company}|{j.title}|{j.location}")
        if key not in seen:
            seen.add(key)
            deduped.append(j)
    return deduped

def main():
    cfg = load_config()
    outdir = pathlib.Path(cfg["agent"]["output_dir"])
    outdir.mkdir(parents=True, exist_ok=True)

    # 1) Fetch jobs
    jobs = fetch_all(cfg)

    # 2a) Extra sources (Monster RSS, Dice API, LinkedIn/Indeed via Playwright review)
    extra = cfg.get("targets_extra", {})
    try:
        jobs += fetch_monster_rss(extra.get("monster_query",""), extra.get("monster_location",""))
    except Exception:
        pass
    try:
        jobs += fetch_dice(extra.get("dice_query",""), extra.get("dice_location",""))
    except Exception:
        pass
    # Human-in-the-loop flows (uncomment to use)
    # try:
    #     jobs += fetch_from_signed_in_search(extra.get("linkedin_search_url",""))
    # except Exception:
    #     pass
    # try:
    #     jobs += fetch_from_signed_in_search(extra.get("indeed_search_url",""))
    # except Exception:
    #     pass

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
