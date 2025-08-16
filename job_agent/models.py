from pydantic import BaseModel
from typing import List, Optional

class Job(BaseModel):
    source: str
    company: str
    title: str
    location: Optional[str] = None
    remote: Optional[bool] = None
    posted_date: Optional[str] = None
    apply_url: str
    req_id: Optional[str] = None
    recruiter_name: Optional[str] = None
    recruiter_email: Optional[str] = None
    recruiter_link: Optional[str] = None
    skills: List[str] = []
    jd_text: str

class Candidate(BaseModel):
    name: str
    email: str
    phone: str
    links: List[str] = []
    summary: str = ""
    skills: List[str] = []
    bullets: List[str] = []