"""Local browser smoke check; creates a clearly named preview workspace, never fake market data."""
from pathlib import Path
from uuid import uuid4
import json
import os
import re
import secrets
import time
import urllib.request
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
artifacts = root / "artifacts"
artifacts.mkdir(exist_ok=True)
origin = os.environ.get("PREVIEW_ORIGIN", "http://localhost:3000")

def get_json(url):
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.load(response)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    context = browser.new_context(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
    page = context.new_page()
    page.set_default_timeout(45000)
    get_json("http://localhost:4000/api/health/ready")
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(origin, wait_until="networkidle", timeout=60000)
    page.get_by_role("heading", name=re.compile("See the landscape")).wait_for()
    page.screenshot(path=str(artifacts / "rivalscope-home.png"), full_page=True)
    page.goto(origin + "/register", wait_until="networkidle")
    suffix = uuid4().hex[:10]
    email = f"preview-{suffix}@rivalscope.local"
    password = secrets.token_urlsafe(24)
    page.get_by_label("Your name", exact=True).fill("Local Preview")
    page.get_by_label("Workspace name", exact=True).fill("Preview Workspace")
    page.get_by_label("Work email", exact=True).fill(email)
    page.get_by_label("Password", exact=True).fill(password)
    page.get_by_role("button", name="Create workspace").click()
    page.wait_for_url("**/workspace/overview", timeout=30000)
    page.get_by_role("heading", name="A clearer view of your market.").wait_for()
    page.get_by_role("heading", name="Your first insight starts here.").wait_for()
    page.wait_for_function("document.querySelector('.stat-card strong')?.textContent === '0'")
    page.screenshot(path=str(artifacts / "rivalscope-dashboard.png"), full_page=True)
    # Verify the real encrypted email outbox and worker delivery through local Mailpit.
    verify_url = None
    for _ in range(20):
        messages = get_json("http://localhost:8025/api/v1/messages")
        for message in messages.get("messages", []):
            if any(recipient.get("Address") == email for recipient in message.get("To", [])):
                details = get_json("http://localhost:8025/api/v1/message/" + message["ID"])
                match = re.search(r"https?://[^\s]+\?verify=[A-Za-z0-9_-]+", details.get("Text", ""))
                if match:
                    verify_url = match.group(0)
                    break
        if verify_url:
            break
        time.sleep(1)
    if not verify_url:
        raise RuntimeError("Verification email was not delivered by the worker")
    page.goto(verify_url, wait_until="networkidle")
    page.get_by_role("button", name="Continue", exact=True).click()
    page.get_by_text("Email verified. Open your workspace to start research.", exact=True).wait_for()
    page.goto(origin + "/workspace/projects", wait_until="networkidle")
    page.get_by_label("Project name", exact=True).fill("RivalScope product research")
    page.get_by_label("Industry", exact=True).fill("Competitive intelligence software")
    page.get_by_label("Business description", exact=True).fill("RivalScope AI helps teams research public competitor sources, trace factual evidence, and monitor market changes.")
    page.get_by_role("button", name="Create project", exact=True).click()
    page.wait_for_url("**/workspace/research?**", timeout=30000)
    try:
        page.get_by_role("heading", name="Ask a better market question.").wait_for()
    except Exception:
        page.screenshot(path=str(artifacts / "browser-failure.png"), full_page=True)
        print(json.dumps({"step":"research-page","errors":errors,"text":page.locator('main').inner_text()[:3000]}))
        raise
    page.screenshot(path=str(artifacts / "rivalscope-research.png"), full_page=True)
    # Check all primary routes for actual API and rendering failures.
    failures = []
    typography = []
    layout = []
    for section in ["competitors", "comparisons", "swot", "monitoring", "alerts", "copilot", "reports", "team", "billing", "integrations", "settings"]:
        page.goto(origin + "/workspace/" + section, wait_until="networkidle")
        page.get_by_role("main").wait_for()
        for width in [1440, 390]:
            page.set_viewport_size({"width": width, "height": 1000})
            page.wait_for_timeout(150)
            audit = page.evaluate("""() => {
                const small=[]; const fonts=new Set();
                for(const el of document.querySelectorAll('body *')) {
                    if(el.closest('nextjs-portal') || !el.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})) continue;
                    if(![...el.childNodes].some(n=>n.nodeType===Node.TEXT_NODE&&n.textContent.trim())) continue;
                    const cs=getComputedStyle(el); fonts.add(cs.fontFamily);
                    if(parseFloat(cs.fontSize)<14) small.push({tag:el.tagName,class:el.className?.baseVal??el.className,size:cs.fontSize});
                }
                return {small,fonts:[...fonts],overflow:document.documentElement.scrollWidth>innerWidth};
            }""")
            typography.append({"section":section,"width":width,"small":audit["small"],"fonts":audit["fonts"]})
            if audit["overflow"]: layout.append({"section":section,"width":width})
        page.set_viewport_size({"width":1440,"height":1000})
        if section in ["comparisons","settings","team","billing"]:
            page.screenshot(path=str(artifacts / ("rivalscope-"+section+".png")),full_page=True)
        alerts = [text.strip() for text in page.locator('[role="alert"]').all_text_contents() if text.strip()]
        if alerts:
            failures.append({"section": section, "alerts": alerts})
    page.goto(origin + "/workspace/overview", wait_until="networkidle")
    page.wait_for_function("document.querySelector('.stat-card strong')?.textContent === '1'")
    page.screenshot(path=str(artifacts / "rivalscope-dashboard.png"), full_page=True)
    page.set_viewport_size({"width": 390, "height": 844})
    page.screenshot(path=str(artifacts / "rivalscope-mobile.png"), full_page=True)
    overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
    (artifacts / "typography-audit.json").write_text(json.dumps({"screens":typography,"overflow":layout},indent=2))
    print(json.dumps({"fontViolations":sum(len(a["small"]) for a in typography),"overflowScreens":layout,"registration": "passed", "emailVerification": "passed", "projectCreation": "passed", "routesChecked": 11, "routeFailures": failures, "browserErrors": errors, "mobileOverflow": overflow, "screenshots": ["artifacts/rivalscope-home.png", "artifacts/rivalscope-dashboard.png", "artifacts/rivalscope-research.png", "artifacts/rivalscope-mobile.png"]}))
    browser.close()
