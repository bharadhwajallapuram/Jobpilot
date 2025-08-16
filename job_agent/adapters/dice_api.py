import os
import requests
from typing import List
from ..models import Job

DICE_API_BASE = os.getenv("DICE_API_BASE", "").rstrip("/")  # Provided by Dice/partner program
DICE_API_KEY = os.getenv("DICE_API_KEY", "")                # Your Dice API key/token

def fetch_dice(query: str, location: str = "") -> List[Job]:
    """Use Dice's official endpoints if you have partner access.
    Set DICE_API_BASE and DICE_API_KEY via environment or compose.
    """
    if not DICE_API_BASE or not DICE_API_KEY:
        return []
    params = {"q": query, "location": location}
    headers = {"Authorization": f"Bearer {DICE_API_KEY}"}
    url = f"{DICE_API_BASE}/jobs/search"
    r = requests.get(url, params=params, headers=headers, timeout=25)
    r.raise_for_status()
    data = r.json()
    jobs: List[Job] = []
    for j in data.get("results", []):
        jobs.append(Job(
            source="dice_api",
            company=j.get("company","Dice"),
            title=j.get("title",""),
            location=j.get("location"),
            apply_url=j.get("url") or j.get("applyUrl",""),
            jd_text=j.get("description","") or "",
            req_id=str(j.get("id")) if j.get("id") else None
        ))
    return jobs
