import requests
from typing import List
from ..models import Job

def fetch_smartrecruiters(company_slug: str) -> List[Job]:
    # Public endpoint pattern (varies by org). This one lists postings:
    # https://api.smartrecruiters.com/v1/companies/{slug}/postings
    url = f"https://api.smartrecruiters.com/v1/companies/{company_slug}/postings"
    try:
        r = requests.get(url, timeout=25)
        r.raise_for_status()
        data = r.json()
        jobs = []
        for j in data.get("content", []):
            jobs.append(Job(
                source="smartrecruiters",
                company=company_slug,
                title=j.get("name",""),
                location=(j.get("location") or {}).get("city"),
                apply_url=(j.get("applyUrl") or j.get("ref") or ""),
                jd_text="",
                req_id=j.get("id")
            ))
        return jobs
    except Exception:
        return []