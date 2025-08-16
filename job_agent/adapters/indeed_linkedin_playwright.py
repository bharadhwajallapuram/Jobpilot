from playwright.sync_api import sync_playwright
from ..models import Job

def fetch_from_signed_in_search(start_url: str, max_items: int = 30) -> list[Job]:
    """Open a signed-in search (LinkedIn/Indeed), pause for manual login/CAPTCHA,
    then collect visible job card links for review. Use only if permitted by site terms.
    """
    jobs: list[Job] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx = browser.new_context()
        page = ctx.new_page()
        page.goto(start_url, timeout=60000)

        # Let the user log in/solve challenges and confirm selectors
        page.pause()

        # NOTE: Update selectors after inspecting the page you are allowed to automate.
        selectors = ["a.job-card-container__link", "a.tapItem"]
        for sel in selectors:
            try:
                cards = page.locator(sel)
                count = cards.count()
                for i in range(min(count, max_items)):
                    href = cards.nth(i).get_attribute("href")
                    title = (cards.nth(i).inner_text() or "").strip()
                    if href:
                        jobs.append(Job(
                            source="browser_review",
                            company="(review)",
                            title=title[:200],
                            location=None,
                            apply_url=href if href.startswith("http") else page.url,
                            jd_text="Open detail to view full JD",
                            req_id=None
                        ))
            except Exception:
                continue
        browser.close()
    return jobs
