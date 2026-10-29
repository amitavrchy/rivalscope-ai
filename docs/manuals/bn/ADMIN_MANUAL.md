# অ্যাডমিন ও পরিচালনা নির্দেশিকা

**RivalScope AI · বাংলা · ২৯ অক্টোবর ২০২৬**

এই নির্দেশিকা workspace admin, platform administrator এবং deployment operator-এর দায়িত্ব আলাদা করে দেখায়। এটি বর্তমান implementation-এর manual; production readiness-এর সনদ নয়। এখানে থাকা পরিবর্তনের উদাহরণগুলো নির্দেশনা মাত্র—manual তৈরির সময় কোনো role, plan, credit বা live payment বদলানো হয়নি।

## ১. আগে আপনার দায়িত্ব বুঝুন

| দায়িত্ব | অনুমতি | কোথা থেকে কাজ করবেন |
| --- | --- | --- |
| Workspace ADMIN | নির্দিষ্ট প্রতিষ্ঠানের research, team, workspace preferences ও integrations; billing নয় | সাধারণ sidebar-এর Team, Settings, Integrations ইত্যাদি |
| Workspace OWNER | নিজের workspace-এর billing-সহ সব workspace permission | সাধারণ workspace UI |
| Platform Administrator | আলাদা `platformAdmin` অনুমতিসহ verified account; platform-level API access | Sidebar → Administration; প্রয়োজনে অনুমোদিত admin API |
| Deployment Operator | Hosting, environment, Docker, database, worker, logs পরিচালনার infrastructure access | Server/terminal ও deployment tooling |

Platform administrator হওয়া মাত্র সব customer workspace-এর research পড়ার membership পাওয়া যায় না। Customer research-এর সাধারণ endpoint-গুলো membership ও tenant policy মানে।

Workspace admin-এর দৈনন্দিন কাজের জন্য [ব্যবসার মালিকের নির্দেশিকা](BUSINESS_OWNER_MANUAL.md)-র role/team অংশ অনুসরণ করুন। `ADMIN` billing permission পান না এবং owner-এর মতো অন্য admin পরিচালনা করতে পারেন না।

## ২. Platform administrator হিসেবে প্রবেশ

১. নিজের account দিয়ে sign in করুন ও email verification শেষ করুন।

২. অনুমোদিত deploy maintainer আপনার account-এর platform privilege provision করেছেন কি না নিশ্চিত করুন। বর্তমান register বা Team role selector দিয়ে নিজেকে platform admin করা যায় না। Default shared admin/password নেই।

৩. Sidebar-এ **Administration** দেখালে খুলুন। সরাসরি স্থানীয় পথ: `http://localhost:3000/workspace/admin`।

৪. **Administration**-এ Overview, Organizations, Users, Plans, Credit packs, Subscriptions, Jobs, Provider usage, Audit, Flags, Settings ও Diagnostics tab দেখুন। Record-গুলো সর্বশেষ সীমিত ফল; পুরো database export নয়।

৫. নিচের form থেকে credit adjustment, plan/Stripe mapping, credit pack, feature flag, operational setting এবং platform role পরিবর্তন করুন। Job record-এর **Request cancellation** বা failed/cancelled run-এর **Restart as new run** ব্যবহার করুন; নতুন run নতুন credit reservation করে। Users record-এ **Revoke sessions** আছে। Privilege change-এ নিজের password/MFA লাগে এবং নিজের platform role বদলানো যায় না।

`Platform access is restricted` বা 403 এলে verified platform-admin permission যাচাই করুন। Workspace role বদলে সমস্যাটি সমাধান হবে না। প্রথম admin provisioning-এর জন্য অনুমোদিত operator backend থেকে `node --import tsx src/admin-cli.ts grant <verified-email>` চালাতে পারেন; compiled container-এ `node dist/admin-cli.js grant <verified-email>`। Revoke-এর জন্য `revoke` ব্যবহার করুন। এটি audit করে এবং শেষ admin revoke আটকায়। Shared default admin account নেই।

## ৩. Admin API-তে কী আছে

API reference স্থানীয়ভাবে [http://localhost:4000/api/docs](http://localhost:4000/api/docs)-এ। নিচের endpoint-গুলোতে signed-in verified platform administrator প্রয়োজন।

| Endpoint | কাজ | UI-তে বর্তমান অবস্থা |
| --- | --- | --- |
| `GET /api/admin/overview` | Organization/user count, run summary, research/monitor queue counts, recent audit | Overview tab |
| `GET /api/admin/organizations` | সর্বোচ্চ ১০০ organization-এর পরিচয়, credit ও subscription summary | Organizations tab |
| `POST /api/admin/organizations/{id}/credits` | Credit adjustment এবং immutable ledger/audit entry | Credit adjustment form |
| `PATCH /api/admin/plans/{id}` | Database-backed plan field, trial days ও Stripe price ID | Plan configuration form |

**Provider usage**-এ provider/model, token counts, duration ও configured rate থাকলে estimated cost পাওয়া যায়। Rate না থাকলে cost unavailable; token count দিয়ে আয় বা profit অনুমান করবেন না। **Feature flags** research, monitoring, copilot ও public sharing চালু/বন্ধ করে। **Operational settings**-এ announcement, support email এবং daily AI token cap সেট করা যায়। Telemetry exporter/DSN configured হলে বাইরের collector/Sentry-তে যাচাই করতে হবে।

### সঠিক origin থেকে API ব্যবহার

অ্যাপের mutation-এ configured app origin ও JSON content type প্রয়োজন। স্থানীয় API docs-এর port `4000`, কিন্তু app origin `3000`; তাই Swagger page থেকে mutation চালালে Origin-এর কারণে 403 হতে পারে। Origin protection বন্ধ করবেন না।

সাধারণ কাজ UI দিয়েই করুন। API-only admin operation-এর জন্য signed-in অবস্থায় app-এর `http://localhost:3000` tab-এ browser developer console খুলে নিচের মতো same-origin request ব্যবহার করা যায়। সব `{...}` placeholder আগে বাস্তব ID দিয়ে বদলাতে হবে। Account permission server-এ যাচাই হয়। কোনো cookie/token কপি করার প্রয়োজন নেই।

শুধু overview পড়ার উদাহরণ:

```javascript
const response = await fetch('/api/admin/overview');
const result = await response.json();
console.log(response.status, result);
```

এই manual কোনো script paste করার মাধ্যমে admin privilege তৈরি করতে বলে না; অনুমোদিত account ছাড়া request প্রত্যাখ্যাত হবে।

## ৪. Credit adjustment

**ব্যবহার করুন:** অনুমোদিত support correction বা commercial decision বাস্তবায়নে। Owner-এর সাধারণ research budget-এর জন্য platform credit adjustment প্রয়োজন নেই।

১. `GET /api/admin/organizations` থেকে সঠিক organization-এর **ID, name, credits ও reservedCredits** মিলিয়ে নিন। একই রকম নাম হলে ID-ই চূড়ান্ত পরিচয়।

২. Adjustment-এর reason ও কত unit যোগ/বিয়োগ হবে অনুমোদিত support record-এ লিখুন।

৩. App tab-এর console থেকে একবার request পাঠান:

```javascript
const organizationId = 'REPLACE_WITH_ORGANIZATION_UUID';
const response = await fetch(`/api/admin/organizations/${organizationId}/credits`, {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({
    amount: 50,
    reason: 'Approved correction for support case RS-EXAMPLE'
  })
});
console.log(response.status, await response.json());
```

৪. সফল হলে organization balance এবং owner-এর **Billing & usage → Credit activity**-তে `ADJUST` মিলিয়ে নিন।

`amount` শূন্য হতে পারে না; বর্তমান গ্রহণযোগ্য সীমা −১০০০০০ থেকে ১০০০০০। Negative adjustment মোট credit-কে reserved credit-এর নিচে নামাতে পারবে না। Reason অন্তত ১০ অক্ষর। প্রতিবার আলাদা request নতুন adjustment হতে পারে—response অস্পষ্ট হলে balance/ledger না দেখে আবার পাঠাবেন না। Ledger entry edit/delete করে correction করবেন না; আলাদা adjustment করুন।

## ৫. Plan পরিবর্তন ও Stripe mapping

Plan ID বর্তমানে `free`, `starter`, `pro`, `agency`, `enterprise`। Public `GET /api/billing/plans` enabled plan দেখায়।

| Field | অর্থ |
| --- | --- |
| monthlyPriceCents / annualPriceCents | UI-তে ব্যবহৃত price amount; বর্তমানে UI dollar চিহ্ন দেখায় |
| monthlyCredits | Plan-এর credit policy |
| projectLimit / seatLimit / monitorLimit | সংশ্লিষ্ট resource limit |
| stripeMonthlyPriceId / stripeAnnualPriceId | Stripe-এ আগে তৈরি করা সঠিক price ID |
| enabled | Plan listing-এর সক্রিয় অবস্থা |

১. ব্যবসার মালিকের কাছ থেকে price/limit/policy পরিবর্তন নিশ্চিত করুন।

২. Stripe dashboard-এ সঠিক account, currency ও billing interval-এর product/price মিলিয়ে নিন। App থেকে Stripe product/price তৈরি হয় না।

৩. বর্তমান plan listing সংরক্ষণ করে প্রয়োজনীয় field-ই update করুন:

```javascript
const response = await fetch('/api/admin/plans/starter', {
  method: 'PATCH',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ projectLimit: 10, seatLimit: 3, monitorLimit: 5 })
});
console.log(response.status, await response.json());
```

৪. Public plan listing ও customer **Billing & usage**-এ ফল যাচাই করুন। Commercial price বদলালে Stripe mapping ও checkout-এর amount/interval আলাদাভাবে যাচাই করুন। Database display price বদলানো নিজে থেকে Stripe price বদলায় না।

Plan update platform audit record রাখে; admin-এর owned workspace লাগবে না। সাধারণ seed বিদ্যমান field overwrite করে না। Monthly credit field বদলালেই existing organization-এ সঙ্গে সঙ্গে নতুন credit যোগ হয় না। Monitor limit কমলে সীমার বাইরে monitor execution বন্ধ হয়; আগের research data মুছে যায় না।

## ৬. Provider ও external service setup

Workspace owner/admin **Integrations**-এ setup status দেখতে পারেন। Provider secret সেই UI-তে লেখা বা দেখা যায় না; operator backend environment/secret store-এ দেন।

| প্রয়োজন | Server configuration | কোথায় যাচাই করবেন |
| --- | --- | --- |
| Gemini research | `AI_PROVIDER`, `GEMINI_API_KEY`, `GEMINI_MODEL` | Integrations; ছোট provider check; research error |
| Automatic discovery | `TAVILY_API_KEY` | Integrations; discovery-enabled run |
| Optional OpenAI adapter | `OPENAI_API_KEY`, `OPENAI_MODEL`; provider/fallback policy | নির্দিষ্ট adapter test; token/model configuration |
| Production email | `SMTP_URL`, `MAIL_FROM` | Outbox delivery, নিজের verification email |
| Credential encryption | ৩২ random byte-এর hex `ENCRYPTION_KEY` | Startup/configuration ও encrypted credential workflow |
| Stripe | `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, plan price IDs | Sandbox checkout, verified webhook, subscription ও ledger |

কোনো বাস্তব credential এই manual-এ অন্তর্ভুক্ত নেই। `.env` commit করবেন না এবং secret frontend-এর `NEXT_PUBLIC_*` variable-এ দেবেন না। Encryption key হারালে পুরোনো encrypted outbox/webhook secret খুলতে সমস্যা হবে; অনুমোদিত secret management-এ এটি সংরক্ষণ করুন। Key বদলালেই পুরোনো data re-encrypt হয় না।

বর্তমান Gemini model configuration `gemini-3.5-flash-lite`; আগের live smoke check-এ structured output সফল হয়েছে। Provider availability/quota সময়ের সঙ্গে বদলাতে পারে। আবার পরীক্ষা দরকার হলে backend folder-এ `npm run check:provider` চালান; এটি একটি ছোট live request করে। **Configured** label-কে live health check বলবেন না।

## ৭. Billing সমস্যা সামলানো

Stripe webhook endpoint: `POST /api/billing/webhook`। এটি payment provider-এর signature দিয়ে যাচাই হয়; browser app-origin rule থেকে এর নির্দিষ্ট exemption আছে। Checkout success URL দেখে plan বা credit হাতে পরিবর্তন করবেন না।

| সমস্যা | যাচাই করুন |
| --- | --- |
| Choose plan-এ setup error | Stripe key, selected plan-এর monthly/annual price ID |
| Checkout শেষ, status বদলায়নি | Stripe event delivery, signature secret, customer/organization mapping |
| Invoice paid, credit নেই | Invoice type, subscription mapping, ledger-এর invoice reference, handler error |
| Credit দুইবার grant হয়েছে সন্দেহ | একই invoice-এর ledger reference; event ID ও invoice ID; repeated manual adjustment আছে কি না |
| Portal খুলছে না | ঐ organization-এর Stripe customer তৈরি আছে কি না; portal account configuration |

বর্তমানে signed webhook verification ও idempotent invoice grant automated test-এ যাচাই হয়েছে; Stripe transport সেখানে mocked। Live sandbox end-to-end subscription lifecycle verification এখনও বাকি। Automatic trial, add-on বা refund lifecycle সম্পূর্ণ হয়েছে বলে customer-কে জানাবেন না।

## ৮. Local service চালু ও অবস্থা দেখা

**শুধু স্থানীয় প্রস্তুত workspace-এর জন্য।** Docker Desktop চালু করুন। Project root থেকে:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start-local.ps1
```

Script backend build করে PostgreSQL/Redis/Mailpit এবং API/web/worker চালু করার চেষ্টা করে। এটি execution policy-র current script invocation-এর বিকল্প; প্রতিষ্ঠানের policy মেনে চালাবেন। `ExecutionPolicy Bypass` ব্যবহার করতে না চাইলে অনুমোদিত PowerShell execution policy-তে script চালান, অথবা repository README-র আলাদা terminal command ব্যবহার করুন।

| সেবা | স্থানীয় ঠিকানা/পথ | সফলতার লক্ষণ |
| --- | --- | --- |
| Web | `http://localhost:3000` | Home/login/workspace render হয় |
| API | `http://localhost:4000/api/health/ready` | `status: ready` |
| PostgreSQL | loopback port 5433 | `docker compose ps`-এ healthy |
| Redis | loopback port 6380 | `docker compose ps`-এ healthy |
| Mailpit | `http://localhost:8025` | Verification/reset/invitation email আসে |
| Worker | Background process | Run queued থেকে এগোয়; outbox email যায় |
| Logs | `artifacts/api.log`, `worker.log`, `web.log` এবং `*-error.log` | নতুন failure আছে কি না; আগে manually চালানো web-এর log `frontend.log`-এও থাকতে পারে |

Web খোলা যাচ্ছে বলেই worker চলছে বোঝায় না। API readiness বর্তমান implementation-এ database পরীক্ষা করে; Redis, worker বা সব provider-এর health প্রমাণ করে না।

প্রাথমিক infra check:

```powershell
docker compose ps
Invoke-RestMethod http://localhost:4000/api/health/ready
```

একই port-এ আগে অন্য process চললে start script listener reuse করতে পারে। অনুমান না করে process/service পরিচয় যাচাই করুন। Script current environment-এর migration/seed স্বয়ংক্রিয়ভাবে চালায় না; নতুন setup হলে repository README অনুযায়ী এগুলো আগে করুন।

## ৯. Research বা email আটকে গেলে

| লক্ষণ | সম্ভাব্য জায়গা | করণীয় |
| --- | --- | --- |
| queued থেকে এগোয় না | Worker/Redis/queue submission | Worker process ও Redis দেখুন; durable queued run worker reconcile করতে পারে |
| plan/analyze failed | AI key/model/quota/schema | Run/stage error দেখুন; configured model ও provider check মিলিয়ে নিন |
| extract failed | Public source/robots/DNS/content policy | Canonical public URL দিন; access control বা private-network restriction বন্ধ করবেন না |
| অনেকক্ষণ running | Network timeout/stage budget/worker interruption | Run-এর সময়, stage ও worker log মিলিয়ে দেখুন; customer-কে repeated new run দিতে বলবেন না |
| Verification email আসে না | Worker/SMTP/encryption/outbox retry | Worker log ও local Mailpit/production mail delivery পরীক্ষা করুন; rate limit মেনে resend করুন |
| Monitor enabled কিন্তু check নেই | Subscription/credits/scheduler | Plan/credit, worker ও monitoring scheduler দেখুন |

Research worker-এর নিজস্ব bounded attempts এবং BullMQ retry আছে। **FAILED** terminal run-কে queue-তে আবার দিলেই নতুনভাবে চলবে—এমন নয়; executor terminal run skip করে। কারণ ঠিক করার পর নতুন run শুরু করলে নতুন reservation হবে। User **Cancel run** দিয়ে চলমান কাজ থামানোর অনুরোধ করতে পারেন।

এখন raw failed job recovery, queue cancellation management ও সব dead-letter-এর জন্য পূর্ণ admin UI নেই। Database row হাতে বদলে recovery শুরু করার আগে checkpoint, idempotency ও credit settlement-এর সঙ্গে মিল রেখে developer-reviewed procedure প্রয়োজন।

## ১০. Customer API key ও webhook সহায়তা

Workspace **Integrations**-এ API key একবার দেখানো হয়। হারালে পুরোনোটি উদ্ধার করা যায় না; নতুন key দিন ও পুরোনোটি revoke করুন। Account member remove করা আলাদা; organization-owned API key প্রয়োজন হলে আলাদা revoke করতে হবে। Key-এর scope, expiry ও tenant boundary server-এ যাচাই হয়। বর্তমান read-only public endpoints `/api/v1/projects` ও `/api/v1/reports`।

Webhook management বর্তমানে API-only, workspace integration permission প্রয়োজন:

| Endpoint | কাজ |
| --- | --- |
| `GET /api/organizations/{orgId}/webhooks` | Endpoint ও সাম্প্রতিক delivery status |
| `POST /api/organizations/{orgId}/webhooks` | HTTPS receiver URL ও subscribed events দিয়ে endpoint তৈরি; signing secret একবার ফেরত দেয় |
| `DELETE /api/organizations/{orgId}/webhooks/{id}` | Endpoint disable |
| `POST /api/organizations/{orgId}/webhooks/{id}/retry/{deliveryId}` | Dead-letter delivery আবার pending করা |

বর্তমান events: `research.completed` ও `monitor.changed`। Delivery-তে event ID ও timestamped HMAC signature header থাকে। Receiver-কে signature যাচাই ও event ID দিয়ে duplicate handling করতে হবে। ব্যর্থ delivery-তে bounded backoff চলে; ৬ attempt শেষে `dead_letter` হতে পারে। Delivery/receiver problem না বুঝে বারবার manual retry করবেন না। Private-network receiver বা redirect দিয়ে restriction bypass করা যাবে না। Slack/Discord adapter এখনও নেই।

## ১১. দৈনন্দিন দায়িত্বের তালিকা

১. Web ও API readiness; database/cache health পরীক্ষা।

২. Research/monitor queue-তে waiting, active ও failed count অস্বাভাবিক কি না দেখুন।

৩. Email delivery ও pending/dead-letter webhook সমস্যা দেখুন।

৪. Provider quota/model/setup এবং billing event error পরীক্ষা করুন।

৫. Credit adjustment বা plan পরিবর্তনের কারণ ও audit record মিলিয়ে নিন।

৬. Customer issue-তে organization ID ও run/project context নিশ্চিত করুন; প্রয়োজন ছাড়া private research সংগ্রহ করবেন না।

৭. `docs/OPERATIONS.md`-এর backup/restore runbook অনুসরণ করুন। `npm run db:backup` dump ও checksum তৈরি করে; `npm run db:restore-check -- <dump-path>` আলাদা restore-check database-এ পরীক্ষা করে। স্থানীয় restore drill করা হয়েছে; production encrypted backup storage ও scheduled drill operator-কে configure করতে হবে।

## ১২. Production চালুর আগে অবশিষ্ট gate

Production Compose/Dockerfile আছে। Local image build/restore-এর evidence `docs/IMPLEMENTATION_STATUS.md`-এ রাখা হয়। বাস্তব hosting-এ launch করার আগে:

- HTTPS ingress, production secret management, বাস্তব SMTP, সঠিক origin ও database/cache networking।
- সর্বশেষ database migration/seed এবং production backup/restore drill।
- Google OAuth account/redirect URL দিয়ে real browser callback; Tavily দিয়ে discovery; SMTP দিয়ে বাস্তব inbox delivery।
- Stripe sandbox lifecycle ও price/credit policy acceptance।
- Redis-backed abuse protection, per-key metering এবং isolated security regression suite চালানো।
- Telemetry collector/Sentry-তে sanitized event পৌঁছানো, worker failure/recovery এবং deployed smoke check।

বিস্তারিত সত্যতা যাচাইয়ের নথি: repository-এর `docs/IMPLEMENTATION_STATUS.md`। Audit ও credit ledger immutable; log ঢেকে বা ledger edit করে সমস্যা মেটানোর নির্দেশনা এই manual দেয় না।

[সব নির্দেশিকায় ফিরে যান](README.md) · [সাধারণ ব্যবহারকারী](USER_MANUAL.md) · [ব্যবসার মালিক](BUSINESS_OWNER_MANUAL.md)
