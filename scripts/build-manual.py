"""Render the Bengali manuals as offline, printable HTML; no application changes."""
from pathlib import Path
import html
import re
from markdown_it import MarkdownIt

root = Path(__file__).resolve().parents[1]
directory = root / 'docs' / 'manuals' / 'bn'
documents = [
    ('README.md', 'index.html', 'নির্দেশিকার সূচি'),
    ('USER_MANUAL.md', 'USER_MANUAL.html', 'সাধারণ ব্যবহারকারী'),
    ('BUSINESS_OWNER_MANUAL.md', 'BUSINESS_OWNER_MANUAL.html', 'ব্যবসার মালিক'),
    ('ADMIN_MANUAL.md', 'ADMIN_MANUAL.html', 'অ্যাডমিন ও পরিচালনা'),
]
style = '''
@font-face{font-family:ManualBengali;src:url(images/NotoSansBengali.ttf) format("truetype");font-weight:100 900;font-display:swap}:root{color-scheme:light;--ink:#203d36;--teal:#137d70;--line:#dbe7e1}
*{box-sizing:border-box}body{margin:0;background:#f3f7f4;color:#243c34;font-family:ManualBengali,"Nirmala UI","Noto Sans Bengali","Vrinda",system-ui,sans-serif;font-size:16px;line-height:1.95}
.top{background:#113b30;color:#e6f4e9;padding:30px max(22px,calc((100% - 1080px)/2));display:flex;align-items:center;justify-content:space-between;gap:20px}.top strong{font-size:25px}.top small{display:block;color:#adcfba;font-size:14px}.top button{border:1px solid #75ad92;border-radius:7px;color:white;background:transparent;padding:9px 17px;font:inherit;cursor:pointer}
nav{max-width:1080px;margin:20px auto;display:flex;gap:10px;flex-wrap:wrap;padding:0 24px}nav a{border:1px solid var(--line);background:white;border-radius:6px;padding:7px 13px;font-size:14px;color:var(--teal);text-decoration:none}
main{max-width:1080px;margin:20px auto 50px;padding:38px 44px;background:white;border:1px solid var(--line);border-radius:11px}h1,h2,h3{color:var(--ink);line-height:1.5}h1{font-size:31px;margin-top:0;border-bottom:2px solid #c7e2d4;padding-bottom:20px}h2{font-size:24px;margin-top:40px}h3{font-size:19px;margin-top:27px}p,li{overflow-wrap:anywhere}a{color:var(--teal);text-underline-offset:3px}img{display:block;max-width:100%;height:auto;border:1px solid var(--line);border-radius:8px;margin:24px auto}table{border-collapse:collapse;width:100%;font-size:14px;margin:20px 0;display:block;overflow-x:auto}th,td{padding:12px 14px;border:1px solid var(--line);vertical-align:top;text-align:left;min-width:100px}th{background:#edf5ef}tbody tr:nth-child(even){background:#fafcfb}blockquote{border-left:4px solid #8ebca3;background:#f2f8f4;padding:10px 22px;margin:22px 0}pre{padding:20px;background:#142f28;color:#e3f1e8;border-radius:8px;overflow:auto;line-height:1.65;font-size:14px}code{font-family:Consolas,monospace;font-size:1em}p code,td code,li code{background:#edf4ef;padding:2px 5px;border-radius:3px}.manual-part{margin-top:60px;padding-top:35px;border-top:3px solid #a5cdb6}.footer{color:#7b9081;text-align:center;font-size:14px;margin:20px}.toc{background:#eff6f1;border-radius:8px;padding:18px 24px;margin:25px 0}.toc strong{display:block;margin-bottom:8px}.toc a{display:block;font-size:14px;padding:3px 0}
@media(max-width:650px){main{padding:25px 19px;margin:14px 12px;border-radius:8px}.top{padding:20px}.top strong{font-size:20px}.top button{font-size:14px;white-space:nowrap}nav{padding:0 12px;gap:7px}nav a{font-size:14px}h1{font-size:26px}h2{font-size:21px}body{font-size:15px}}
@media print{body{background:white;font-size:11pt;line-height:1.65}.top,nav,.footer,.toc{display:none}main{max-width:none;margin:0;padding:0;border:0;box-shadow:none}h1{font-size:22pt}h2{font-size:16pt;break-after:avoid}h3{break-after:avoid}pre{background:#f4f4f4;color:black;white-space:pre-wrap;word-break:break-word}table{display:table;font-size:10.5pt}th,td{min-width:0;padding:7px}img{max-height:230mm;object-fit:contain}tr,blockquote{break-inside:avoid}.manual-part{break-before:page;border:0;margin:0;padding:0}a{color:inherit}@page{size:A4;margin:18mm}}
'''
parser = MarkdownIt('commonmark', {'html': False}).enable('table')
mapping = {source: destination for source, destination, _ in documents}

def render(source):
    text = (directory / source).read_text(encoding='utf-8-sig')
    result = parser.render(text)
    for old, new in mapping.items():
        result = result.replace(f'href="{old}"', f'href="{new}"')
    index = 0
    toc = []
    def heading(match):
        nonlocal index
        index += 1
        anchor = f'{Path(source).stem.lower()}-section-{index}'
        title = re.sub('<[^>]+>', '', match.group(2))
        if match.group(1) == '2':
            toc.append(f'<a href="#{anchor}">{title}</a>')
        return f'<h{match.group(1)} id="{anchor}">{match.group(2)}</h{match.group(1)}>'
    result = re.sub(r'<h([123])>(.*?)</h\1>', heading, result)
    if toc:
        end = result.find('</h1>') + len('</h1>')
        result = result[:end] + '<div class="toc"><strong>এই নির্দেশিকায়</strong>' + ''.join(toc) + '</div>' + result[end:]
    return result

def page(title, body):
    navigation = ''.join(f'<a href="{destination}">{label}</a>' for _, destination, label in documents)
    navigation += '<a href="RIVALSCOPE_MANUAL_BN.html">সম্পূর্ণ নির্দেশিকা</a>'
    return f'''<!doctype html>
<html lang="bn"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="RivalScope AI-এর বাংলা ব্যবহার, ব্যবসা ও পরিচালনা নির্দেশিকা"><title>{html.escape(title)} — RivalScope AI</title><style>{style}</style></head><body><header class="top"><div><strong>RivalScope AI</strong><small>বাংলা ব্যবহার ও পরিচালনা নির্দেশিকা · ২৯ অক্টোবর ২০২৬</small></div><button onclick="window.print()">প্রিন্ট / PDF</button></header><nav aria-label="নির্দেশিকা নির্বাচন">{navigation}</nav><main>{body}</main><footer class="footer">বর্তমান implementation-এর ভিত্তিতে তৈরি। বাস্তব API key বা password এই নথিতে নেই।</footer></body></html>'''

parts = []
for source, destination, title in documents:
    body = render(source)
    (directory / destination).write_text(page(title, body), encoding='utf-8')
    parts.append(f'<section class="manual-part">{body}</section>')
(directory / 'RIVALSCOPE_MANUAL_BN.html').write_text(page('সম্পূর্ণ বাংলা নির্দেশিকা', ''.join(parts)), encoding='utf-8')
print('Built 4 linked HTML guides and one combined printable manual.')
