import requests
from typing import List
from ..models import Job
from .utils import strip_html

def fetch_lever(company_slug: str) -> List[Job]:
    url = f"https://api.lever.co/v0/postings/{company_slug}?mode=json"
    try:
        r = requests.get(url, timeout=25)
        r.raise_for_status()
        data = r.json()
        jobs = []
        for j in data:
            jobs.append(Job(
                source="lever",
                company=company_slug,
                title=j.get("text",""),
                location=(j.get("categories") or {}).get("location"),
                apply_url=j.get("hostedUrl"),
                jd_text=strip_html(j.get("description","")),
                req_id=j.get("id")
            ))
        return jobs
    except Exception:
        return []