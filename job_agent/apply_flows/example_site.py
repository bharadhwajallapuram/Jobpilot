from playwright.sync_api import sync_playwright

def apply_example(url, candidate):
    # Demo only: replace selectors with the target site's selectors (if permitted by ToS)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx = browser.new_context()
        page = ctx.new_page()
        page.goto(url, timeout=60000)
        # Example selectors - replace with real ones after inspecting the page
        # page.fill("#name", candidate["name"])
        # page.fill("#email", candidate["email"])
        # page.set_input_files("input[type=file]", candidate["resume_path"])
        # page.click("button[type=submit]")
        page.wait_for_timeout(2000)
        browser.close()