
"""Capture real Django browser screenshots for the final project evidence."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

with open("/tmp/onlinecourse-demo-credentials.json", encoding="utf-8") as file:
    demo = json.load(file)

Path("evidence").mkdir(exist_ok=True)
base = "http://127.0.0.1:8000"

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(
        viewport={"width": 1440, "height": 1000},
        device_scale_factor=1
    )

    # Actual Django admin home with Authentication and OnlineCourse sections.
    page.goto(f"{base}/admin/", wait_until="domcontentloaded")
    page.locator("input[name='username']").fill(demo["username"])
    page.locator("input[name='password']").fill(demo["password"])
    page.locator("input[type='submit']").click()
    page.wait_for_url(f"{base}/admin/", timeout=20000)
    page.get_by_text("Authentication and Authorization").wait_for()
    page.get_by_text("OnlineCourse").wait_for()
    page.screenshot(path="evidence/03-admin-site.png", full_page=True)

    # Login through the course site's actual login form and complete the exam.
    page.goto(f"{base}/onlinecourse/login/", wait_until="domcontentloaded")
    page.locator("#username").fill(demo["username"])
    page.locator("#psw").fill(demo["password"])
    page.locator("form").last.locator("button[type='submit']").click()

    page.goto(
        f"{base}/onlinecourse/{demo['course_id']}/",
        wait_until="domcontentloaded"
    )

    page.get_by_role("button", name="Start Exam").click()

    # Wait for the exam section to become visible before selecting an answer.
    page.locator("#exam").wait_for(state="visible")

    # Select the correct answer without forcing the click.
    page.locator(
        f"input[name='choice_{demo['correct_choice_id']}']"
    ).check()

    page.locator("input[type='submit'][value='Submit']").click()

    page.get_by_text("Congratulations", exact=False).wait_for()
    page.get_by_text("100/100", exact=False).wait_for()
    page.screenshot(path="evidence/07-final.png", full_page=True)

    browser.close()

print("Saved evidence/03-admin-site.png and evidence/07-final.png")
