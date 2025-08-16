import requests
from typing import List
from ..models import Job
from .utils import strip_html

def fetch_ashby(org_slug: str) -> List[Job]:
    # Public Ashby postings API (v2) sample endpoint:
    # https://api.ashbyhq.com/posting-api/job-board/{org_slug}
    url = f"https://api.ashbyhq.com/posting-api/job-board/{org_slug}"
    try:
        r = requests.get(url, timeout=25)
        r.raise_for_status()
        data = r.json()
        jobs = []
        for board in data.get("jobBoard", {}).get("jobPostings", []):
            jobs.append(Job(
                source="ashby",
                company=org_slug,
                title=board.get("title",""),
                location=", ".join(board.get("locations", []) or []),
                apply_url=board.get("jobUrl"),
                jd_text=strip_html(board.get("description","")),
                req_id=board.get("id")
            ))
        return jobs
    except Exception:
        return []