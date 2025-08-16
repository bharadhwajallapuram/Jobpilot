import requests, xml.etree.ElementTree as ET
from typing import List
from ..models import Job

def fetch_monster_rss(query: str, location: str = "", days: int = 1) -> List[Job]:
    """Fetch recent postings via Monster RSS (typically ~24h). Build from a saved search.
    Example pattern: https://www.monster.com/jobs/search/rss/?q=DATA+ANALYST&where=New+York
    """
    base = "https://www.monster.com/jobs/search/rss/"
    params = []
    if query:
        params.append(f"q={query.replace(' ', '+')}")
    if location:
        params.append(f"where={location.replace(' ', '+')}")
    url = base + ("?" + "&".join(params) if params else "")

    r = requests.get(url, timeout=20)
    r.raise_for_status()
    try:
        root = ET.fromstring(r.content)
    except ET.ParseError:
        return []

    jobs: List[Job] = []
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        desc = (item.findtext("description") or "").strip()
        jobs.append(Job(
            source="monster_rss",
            company="Monster",
            title=title,
            location=None,
            apply_url=link,
            jd_text=desc,
            req_id=None
        ))
    return jobs
