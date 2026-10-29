"""Populated UI acceptance against rivalscope_test only; no invented production market data."""
from pathlib import Path
from uuid import uuid4
import json
import secrets
import time
import urllib.request
import psycopg
from psycopg.types.json import Jsonb
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
artifacts=root/'artifacts'
test_api='http://127.0.0.1:4001'
origin='http://localhost:3000'
for attempt in range(60):
    try:
        with urllib.request.urlopen(test_api+'/api/health/ready',timeout=2) as ready:
            if ready.status==200: break
    except OSError:
        time.sleep(1)
else:
    raise RuntimeError('Start the isolated test API on port 4001 before this browser check')
audit_js="""() => {
  const small=[];const fonts=new Set();
  for(const el of document.querySelectorAll('body *')) {
    if(el.closest('nextjs-portal')||!el.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}))continue;
    if(![...el.childNodes].some(n=>n.nodeType===Node.TEXT_NODE&&n.textContent.trim()))continue;
    const cs=getComputedStyle(el);fonts.add(cs.fontFamily);
    if(parseFloat(cs.fontSize)<14)small.push({tag:el.tagName,class:el.className?.baseVal??el.className,size:cs.fontSize});
  }
  return {small,fonts:[...fonts],overflow:document.documentElement.scrollWidth>innerWidth};
}"""
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    context=browser.new_context(viewport={'width':1440,'height':1000})
    page=context.new_page();page.set_default_timeout(30000)
    errors=[];http_failures=[];screens=[]
    page.on('pageerror',lambda e: errors.append(str(e)))
    page.on('response',lambda r:http_failures.append({'path':r.url.split('/api/')[-1],'status':r.status}) if '/api/' in r.url and r.status>=400 else None)
    def proxy(route):
        try:
            response=route.fetch(url=test_api+'/api/'+route.request.url.split('/api/',1)[1],headers={**route.request.headers,'connection':'close'},max_retries=2 if route.request.method=='GET' else 0,timeout=15000)
            route.fulfill(response=response)
        except Exception:
            http_failures.append({'path':route.request.url.split('/api/',1)[1],'status':'transport failure'})
            route.abort()
    page.route('**/api/**',proxy)
    suffix=uuid4().hex[:12];password=secrets.token_urlsafe(24)
    response=context.request.post(test_api+'/api/auth/register',headers={'Origin':origin},data={'name':'Isolated browser tester','email':f'browser-{suffix}@example.test','password':password,'organizationName':'Isolated browser acceptance'})
    assert response.status==201,response.status
    from http.cookies import SimpleCookie
    jar=SimpleCookie();jar.load(response.headers['set-cookie'])
    context.add_cookies([{'name':'rs_session','value':jar['rs_session'].value,'domain':'localhost','path':'/','httpOnly':True,'sameSite':'Lax'}])
    me=context.request.get(test_api+'/api/auth/me').json();user_id=me['id'];org_id=me['memberships'][0]['organization']['id']
    project_id=str(uuid4());run_id=str(uuid4());source_id=str(uuid4());competitor_id=str(uuid4());feature_id=str(uuid4());price_id=str(uuid4());report_id=str(uuid4())
    quote='Test fixture only: Starter costs USD 19 per month and includes shared research and team collaboration.'
    content={'executiveSummary':'Isolated acceptance fixture, not live market research.','competitors':[],'findings':[{'category':'PRICING','claim':'The fixture Starter plan costs USD 19 per month.','kind':'FACT','citations':[{'sourceId':source_id,'quotation':quote}]}],'limitations':['Deterministic test fixture. No external market assertions.'],'methodology':{'verification':'Fixture quotation matched against saved fixture text.','failures':[]}}
    with psycopg.connect('postgresql://rivalscope:rivalscope_local@localhost:5433/rivalscope_test') as db:
        assert db.info.dbname=='rivalscope_test'
        db.execute('UPDATE "User" SET "emailVerifiedAt"=NOW(),"platformAdmin"=true WHERE id=%s',(user_id,))
        db.execute('INSERT INTO "Project" (id,"organizationId",name,description,"updatedAt") VALUES (%s,%s,%s,%s,NOW())',(project_id,org_id,'Browser fixture project','A clearly labeled isolated acceptance project for populated UI checks.'))
        db.execute('INSERT INTO "ResearchRun" (id,"organizationId","projectId","idempotencyKey",status,options,"reservedCredits") VALUES (%s,%s,%s,%s,\'COMPLETED\',%s,21)',(run_id,org_id,project_id,str(uuid4()),Jsonb({})))
        db.execute('INSERT INTO "Source" (id,"organizationId","projectId","runId",url,title,"contentHash",text) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(source_id,org_id,project_id,run_id,'https://fixture.example/pricing','Isolated fixture pricing','a'*64,quote))
        db.execute('INSERT INTO "Competitor" (id,"organizationId","projectId",name,domain,classification,"updatedAt") VALUES (%s,%s,%s,%s,%s,\'DIRECT\',NOW())',(competitor_id,org_id,project_id,'Fixture competitor','fixture.example'))
        db.execute('INSERT INTO "Feature" (id,"organizationId",name,"normalizedName") VALUES (%s,%s,%s,%s)',(feature_id,org_id,'Shared research','shared research'))
        db.execute('INSERT INTO "CompetitorFeature" (id,"organizationId","competitorId","featureId","sourceId",quotation) VALUES (%s,%s,%s,%s,%s,%s)',(str(uuid4()),org_id,competitor_id,feature_id,source_id,quote))
        db.execute('INSERT INTO "PricingPlan" (id,"organizationId","competitorId",name,amount,currency,interval,"sourceUrl") VALUES (%s,%s,%s,\'Starter\',19,\'USD\',\'MONTH\',%s)',(price_id,org_id,competitor_id,'https://fixture.example/pricing'))
        db.execute('INSERT INTO "Report" (id,"organizationId","projectId","runId",title,content) VALUES (%s,%s,%s,%s,%s,%s)',(report_id,org_id,project_id,run_id,'Isolated fixture report',Jsonb(content)))
    for section in ['overview','projects','research','competitors','comparisons','swot','monitoring','alerts','copilot','reports','team','billing','integrations','settings','admin']:
        print(json.dumps({'checking':section}),flush=True)
        page.goto(f'{origin}/workspace/{section}?org={org_id}&project={project_id}',wait_until='networkidle')
        try:
            page.locator('.workspace-main').wait_for()
        except Exception:
            page.screenshot(path=str(artifacts/'isolated-browser-failure.png'),full_page=True)
            print(json.dumps({'section':section,'errors':errors,'httpFailures':http_failures,'body':page.locator('body').inner_text()[:2000]}))
            raise
        for width in [1440,390]:
            page.set_viewport_size({'width':width,'height':1000});page.wait_for_timeout(150)
            screens.append({'section':section,'width':width,**page.evaluate(audit_js)})
        page.set_viewport_size({'width':1440,'height':1000})
        if section in ['comparisons','reports','admin']:
            page.screenshot(path=str(artifacts/f'isolated-{section}.png'),full_page=True)
        if section=='comparisons':
            page.get_by_label('Save this competitor selection').fill('Browser saved comparison')
            page.get_by_role('button',name='Save comparison',exact=True).click()
            page.get_by_text('Comparison saved',exact=True).wait_for()
        if section=='research':
            page.get_by_label('Team note',exact=True).fill('Evidence review note from the isolated browser test.')
            page.get_by_role('button',name='Add team note',exact=True).click()
            page.get_by_text('Evidence review note from the isolated browser test.',exact=True).wait_for()
        if section=='reports':
            page.get_by_text('Share this report',exact=True).click()
            page.get_by_role('button',name='Create expiring link',exact=True).click()
            page.get_by_text('Link created. Copy it now.',exact=True).wait_for()
        if section=='billing':
            page.once('dialog',lambda d:d.accept())
            page.get_by_role('button',name='Buy credits',exact=True).click()
            page.wait_for_url('**/workspace/billing?**sandboxPurchase=**')
            page.get_by_role('button',name='Complete sandbox credit purchase',exact=True).click()
            page.get_by_text('Development sandbox credits granted. No real payment was made.',exact=True).wait_for()
        if section=='admin':
            for tab in ['organizations','users','plans','credit-packs','subscriptions','jobs','provider-usage','audit','flags','settings','diagnostics']:
                button=page.get_by_role('button',name=tab.replace('-',' '),exact=True)
                button.click();page.wait_for_timeout(200)
    # The same account as VIEWER must see read-only collaboration and no sharing operation.
    with psycopg.connect('postgresql://rivalscope:rivalscope_local@localhost:5433/rivalscope_test') as db:
        db.execute('UPDATE "Membership" SET role=\'VIEWER\' WHERE "organizationId"=%s AND "userId"=%s',(org_id,user_id))
    page.goto(f'{origin}/workspace/research?org={org_id}&project={project_id}',wait_until='networkidle')
    assert page.get_by_role('button',name='Estimate & start research',exact=True).is_disabled()
    assert page.get_by_role('button',name='Add team note',exact=True).is_disabled()
    assert page.get_by_text('Share this report',exact=True).count()==0
    result={'isolatedDatabase':'rivalscope_test','screens':screens,'browserErrors':errors,'httpFailures':http_failures,'workflowChecks':['comparison saved','team note saved','expiring report link created','sandbox credit add-on completed','viewer controls restricted']}
    (artifacts/'populated-ui-audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'screens':len(screens),'fontViolations':sum(len(x['small']) for x in screens),'overflowScreens':[{'section':x['section'],'width':x['width']} for x in screens if x['overflow']],'browserErrors':errors,'httpFailures':http_failures,'workflowChecks':result['workflowChecks']}))
    browser.close()
