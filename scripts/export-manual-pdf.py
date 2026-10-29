"""Export and visually check the generated offline Bengali manual using installed Edge."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from pypdf import PdfReader

root = Path(__file__).resolve().parents[1]
directory = root / 'docs' / 'manuals' / 'bn'
with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page(viewport={'width': 1280, 'height': 1000})
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto((directory / 'RIVALSCOPE_MANUAL_BN.html').as_uri(), wait_until='load')
    page.evaluate('document.fonts.ready')
    broken = page.locator('img').evaluate_all('(images) => images.filter(i => !i.complete || i.naturalWidth === 0).map(i => i.src)')
    if broken or errors:
        raise RuntimeError(json.dumps({'brokenImages': broken, 'pageErrors': errors}))
    page.pdf(path=str(directory / 'RIVALSCOPE_MANUAL_BN.pdf'), format='A4', print_background=True, prefer_css_page_size=True, display_header_footer=True, header_template='<span></span>', footer_template='<div style="font-family:Arial;font-size:14px;width:100%;text-align:center;color:#758779">RivalScope AI · <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
    (root / 'artifacts').mkdir(exist_ok=True)
    page.screenshot(path=str(root / 'artifacts' / 'bengali-manual-preview.png'))
    page.set_viewport_size({'width': 390, 'height': 844})
    overflow = page.evaluate('document.documentElement.scrollWidth > innerWidth')
    browser.close()
pdf = PdfReader(directory / 'RIVALSCOPE_MANUAL_BN.pdf')
print(json.dumps({'pdfPages': len(pdf.pages), 'brokenImages': broken, 'browserErrors': errors, 'mobileOverflow': overflow, 'pdfPath': str(directory / 'RIVALSCOPE_MANUAL_BN.pdf')}))
