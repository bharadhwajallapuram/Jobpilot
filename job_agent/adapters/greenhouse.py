import requests
from typing import List
from ..models import Job
from .utils import strip_html

def fetch_greenhouse(company_slug: str) -> List[Job]:
    # JSON endpoint: https://boards-api.greenhouse.io/v1/boards/{slug}/jobs
    url = f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs?content=true"
    try:
        r = requests.get(url, timeout=25)
        r.raise_for_status()
        data = r.json()
        jobs = []
        for j in data.get("jobs", []):
            jobs.append(Job(
                source="greenhouse",
                company=company_slug,
                title=j.get("title",""),
                location=(j.get("location") or {}).get("name"),
                apply_url=j.get("absolute_url"),
                jd_text=strip_html(j.get("content","")),
                req_id=str(j.get("id")) if j.get("id") else None
            ))
        return jobs
    except Exception:
        return []