import re
from bs4 import BeautifulSoup

def strip_html(html: str) -> str:
    if not html:
        return ""
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text).strip()
    return text