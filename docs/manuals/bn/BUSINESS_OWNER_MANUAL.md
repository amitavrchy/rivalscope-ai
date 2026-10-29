# ব্যবসার মালিকের নির্দেশিকা

**RivalScope AI · বাংলা · ২৯ অক্টোবর ২০২৬**

এটি নিজের প্রতিষ্ঠানের competitor research, দল ও research credit পরিচালনাকারীর জন্য। এখানে ব্যবসার মালিক বলতে সাধারণত workspace-এর `OWNER` বোঝানো হয়েছে। RivalScope SaaS-এর নিজস্ব ব্যবসা পরিচালনা করলে শেষের আলাদা অংশটিও পড়ুন।

## ১. Workspace সাজিয়ে নিন

১. [সাধারণ ব্যবহারকারীর নির্দেশিকা](USER_MANUAL.md) অনুসারে register ও email verify করুন।

২. **Settings → Workspace preferences** খুলুন।

৩. Workspace name, Industry, Website ও Timezone দিন → **Save preferences**। বাংলাদেশের জন্য timezone লিখতে পারেন `Asia/Dhaka`।

৪. **Projects** থেকে প্রত্যেক ব্যবসা/পণ্য/গবেষণা প্রশ্নের জন্য project তৈরি করুন। সব competitor-কে আলাদা workspace করার প্রয়োজন নেই; একই গবেষণার competitors একই project-এ রাখুন।

৫. একাধিক আলাদা প্রতিষ্ঠান থাকলে **Settings → Create another workspace** ব্যবহার করুন। Sidebar-এর উপরের selector দিয়ে প্রতিষ্ঠান বদলান। নতুন workspace-এর permission ও data আলাদা।

Workspace timezone setting সংরক্ষিত হয়, তবে বর্তমানে UI-এর অধিকাংশ date/time ব্রাউজারের local timezone অনুযায়ী দেখায়। Scheduling interval ঘণ্টা হিসেবে চলে।

## ২. আগে সিদ্ধান্তের প্রশ্ন ঠিক করুন

একটি project শুরু করার আগে লিখুন: কোন সিদ্ধান্ত নিতে হবে, কার সঙ্গে তুলনা হবে, কোন বাজারে, কোন তথ্য দরকার, এবং কোন তারিখের মধ্যে ফল দরকার।

| সিদ্ধান্তের লক্ষ্য | গবেষণার উপযুক্ত প্রশ্ন | কোথায় ফল দেখবেন |
| --- | --- | --- |
| পণ্যের পার্থক্য বুঝতে | প্রতিযোগীরা কোন feature প্রকাশ করেছে; আমাদের প্রস্তাব কোথায় আলাদা হতে পারে? | Comparisons → FEATURE/POSITIONING |
| Pricing পর্যালোচনা | Public pricing-এর currency, billing interval ও সীমা কী? | Comparisons → PRICING; supporting sources |
| সুযোগ খুঁজতে | পাওয়া evidence থেকে সম্ভাব্য unmet need কী বোঝা যায়? | SWOT & opportunities → OPPORTUNITY |
| পরিবর্তন নজরে রাখতে | নির্দিষ্ট public pricing/features page বদলেছে কি? | Monitoring → snapshot; Alerts |
| ব্যবস্থাপনার brief তৈরি | সবচেয়ে গুরুত্বপূর্ণ findings ও evidence limitation কী? | Research → Latest report; Reports |

এগুলো গবেষণার প্রশ্নের উদাহরণ; platform আপনার ব্যবসার revenue, market share বা ROI মেপে দেয় না।

## ৩. প্রথম গবেষণার বাস্তব কাজের তালিকা

১. **Projects**-এ আপনার পণ্যের বিবরণসহ project তৈরি করুন।

২. দুই–চারটি competitor-এর আসল public pricing/features URL সংগ্রহ করুন।

৩. **Research**-এ project বেছে সুনির্দিষ্ট objective দিন।

৪. প্রথমে **Standard** দিয়ে ছোট গবেষণা করুন। বর্তমান পরিবেশে Tavily ছাড়া কাজ করতে **Discover sources with web search বন্ধ** রাখুন।

৫. **Estimate & start research**-এ reserve amount দেখুন এবং budget-এর মধ্যে হলে শুরু করুন।

৬. শেষ হলে source quotation ও retrieval time মিলিয়ে findings যাচাই করুন।

৭. দরকারি তথ্য না থাকলে ফলকে জোর করে পূর্ণ মনে করবেন না; ভালো source ও ছোট objective দিয়ে follow-up run পরিকল্পনা করুন।

৮. একটি report export করে সংশ্লিষ্ট দলের সঙ্গে সিদ্ধান্ত নিন।

## ৪. দল ও দায়িত্ব বণ্টন

### কে কী করতে পারেন

| কাজ | OWNER | ADMIN | ANALYST | EDITOR | VIEWER | BILLING_MANAGER |
| --- | --- | --- | --- | --- | --- | --- |
| Research/project/report দেখা | হ্যাঁ | হ্যাঁ | হ্যাঁ | হ্যাঁ | হ্যাঁ | না |
| Project তৈরি; research/copilot/monitor চালু | হ্যাঁ | হ্যাঁ | হ্যাঁ | না | না | না |
| Project edit/archive; comment API | হ্যাঁ | হ্যাঁ | না | হ্যাঁ | না | না |
| Team ও workspace preferences পরিচালনা | হ্যাঁ | হ্যাঁ | না | না | না | না |
| Billing, usage ledger, checkout/portal | হ্যাঁ | না | না | না | না | হ্যাঁ |
| Integrations/API key/webhook পরিচালনা | হ্যাঁ | হ্যাঁ | না | না | না | না |
| Platform administration | আলাদা অনুমতি | আলাদা অনুমতি | আলাদা অনুমতি | আলাদা অনুমতি | আলাদা অনুমতি | আলাদা অনুমতি |

এটি backend-এর বর্তমান permission policy। বিশেষ করে `ADMIN` billing দেখতে পারেন না এবং `ANALYST` project তৈরি করতে পারলেও edit/archive করতে পারেন না। Team notes ও ব্যক্তিগত bookmarks **Research → Project collaboration**-এ পাওয়া যায়।

### Member আমন্ত্রণ

১. নিজের email verified কি না দেখুন।

২. **Team** খুলুন → teammate-এর **Email address** লিখুন।

৩. **Role** নির্বাচন করুন → **Send invitation**।

৪. সদস্যকে ওই ইমেইল দিয়ে account তৈরি/sign in ও email verify করতে বলুন।

৫. সদস্য invitation link খুলে **Continue** চাপবেন। Sign in করতে অন্য পাতায় গেলে পরে invitation link আবার খুলবেন।

৬. গ্রহণের পর **Team**-এ সদস্যের নাম ও role মিলিয়ে নিন। Invitation সাধারণত সাত দিন কার্যকর।

চলমান valid invitation-ও seat count-এ ধরা হয়। Free plan-এর প্রাথমিক seed-এ ১টি seat আছে; আপনার **Billing & usage**-এ যে seat limit দেখায় সেটিই অনুসরণ করুন। Seat পূর্ণ থাকলে invitation যাবে না। Paid upgrade বর্তমানে Stripe setup ছাড়া করা যায় না।

### Role বদলানো বা সদস্য সরানো

**Team → সদস্যের Role selector** দিয়ে role বদলান। **Remove → confirmation** দিয়ে workspace থেকে সরান। `ADMIN` তৈরি/পরিচালনা করার বিশেষ সীমা আছে: owner-ই admin invite করতে বা admin role নিয়ন্ত্রণ করতে পারেন। **Invitations**-এ pending invitation revoke করুন। **Transfer ownership**-এ verified existing member বেছে নিজের password ও MFA code দিন; transfer শেষে আপনার role হবে `ADMIN`।

Member সরালে তার অন্য workspace/account মুছে যায় না। তিনি যে গবেষণা আগে চালিয়েছেন সেটিও নিজে থেকে বাতিল হয় না; কাজ বন্ধ দরকার হলে সংশ্লিষ্ট run আলাদা করে cancel করুন।

## ৫. Research budget ও credits

**কোথায় যাবেন:** **Billing & usage**

| সংখ্যা/লেনদেন | অর্থ |
| --- | --- |
| Available credits | নতুন কাজের জন্য ব্যবহারযোগ্য credit; মোট credit থেকে reservation বাদ দেওয়া |
| Credits reserved | চলমান/সারিতে থাকা কাজের জন্য ধরে রাখা credit |
| GRANT | Signup, অনুমোদিত billing event বা credit grant |
| RESERVE | Research-এর জন্য hold; একই মুহূর্তে চূড়ান্ত খরচ নয় |
| SETTLE | Run-এর completed stage অনুযায়ী চূড়ান্ত charge |
| RELEASE | Reservation-এর অব্যবহৃত অংশ ছাড়া; নতুন ক্রয় করা credit নয় |
| CONSUME | Copilot বা monitor-এর সরাসরি credit খরচ |
| ADJUST | অনুমোদিত platform admin-এর adjustment |

উদাহরণ: ১০০ credit থাকলে Standard research-এ ২১ reserve করার পর available ৭৯ হবে। কাজ শেষে ২১ charge হলে reserved শূন্য ও balance ৭৯। আংশিক কাজের পর failure হলে completed stage-এর charge থাকতে পারে; পুরো reserve-ই অবশ্যই ফেরত পাবেন—এমন নয়।

**বর্তমান unit:** Standard ২১ / Deep ২৭; discovery থাকলে আরও ৩। সফল source-backed copilot response ২; monitor-এর প্রতিটি সফল check ১। Credit টাকা বা Gemini usage bill নয়। Credit history-র row-গুলো সরল যোগ করলে balance নাও মিলতে পারে, কারণ reserve/release hold-ও দেখায়।

Daily budget alert বা workspace-level custom spend cap-এর UI বর্তমানে নেই। Owner-কে available/reserved credit ও চলমান run দেখে budget নিয়ন্ত্রণ করতে হবে। Free credit মাসে নিজে থেকেই refill হয়—এমন ধরে নেবেন না; বর্তমান free grant signup/workspace creation-এর সময় দেওয়া হয়।

## ৬. Plan ও payment

১. **Billing & usage**-এ current plan, status, seat ও credit দেখুন।

২. **Annual billing** চালু/বন্ধ করে plan-এর displayed price দেখুন।

৩. **Choose [plan]** চাপলে Stripe setup থাকলে checkout খুলবে। Setup না থাকলে descriptive error দেখাবে।

৪. আগে থেকেই paid subscription থাকলে নতুন subscription তৈরির বদলে billing portal-এ পাঠাতে পারে।

৫. **Billing portal** থেকে Stripe account-এর portal configuration অনুযায়ী subscription/payment management হবে।

Checkout থেকে ফিরে এলেই account paid হয়েছে ধরে নেবেন না; server-side verified billing event দিয়ে status বদলায়। Plan-এর দাম ও limit database-backed; manual-এর কোনো উদাহরণকে চূড়ান্ত commercial offer মনে করবেন না। বর্তমান implementation-এ annual invoice থেকে বারো মাসের credit একসঙ্গে grant হয়; monthly release নয়। এই নীতি production rollout-এর আগে অনুমোদন করা দরকার।

বর্তমান স্থানীয় setup-এ Stripe credentials ও price ID configured নয়। **Credit add-ons → Buy credits** একবারের credit purchase; verified payment event না আসা পর্যন্ত credits যোগ হয় না। **Change an existing plan**-এ নতুন plan/interval বেছে confirmation দিলে Stripe prorated invoice তৈরি করে; payment/webhook activation নির্ধারণ করে। Plan change-এর জন্য আরেকটি পূর্ণ credit allowance দেওয়া হয় না; paid billing cycle-এ allowance আসে। Annual cycle-এর allowance ১২ মাসের জন্য একসঙ্গে দেওয়া হয়।

Trial days operator plan অনুযায়ী সেট করেন; একই workspace-এর প্রথম eligible checkout attempt-এ trial পাওয়া যায়। Payment failure-এর grace period operator নির্ধারণ করেন—default ৩ দিন। Grace/period শেষ হলে নতুন research ও monitor check বন্ধ হয়; saved data পড়া যায়। Subscription, invoice ও credits reconcile করে সিদ্ধান্ত নিন।

Development billing sandbox আলাদা করে enabled থাকলে স্পষ্ট sandbox panel দেখা যাবে। **Complete sandbox payment** অথবা **Complete sandbox credit purchase** বাস্তব টাকা কাটে না। Sandbox production-এ ব্যবহার করা যায় না। Live Stripe sandbox account-এ পুরো lifecycle acceptance credentials পাওয়ার পরে করতে হবে।

## ৭. সাপ্তাহিক ব্যবসায়িক review

| কখন | কী দেখবেন | কী সিদ্ধান্ত নেবেন |
| --- | --- | --- |
| সপ্তাহের শুরুতে | Overview; active research; available/reserved credit | কোন গবেষণায় অগ্রাধিকার দেবেন |
| নতুন report এলে | Source, quotation, retrieval date, limitations | কোন findings ব্যবহারযোগ্য; কোথায় আরও evidence দরকার |
| Website change alert এলে | Previous/Current snapshot; মূল public page | আসল business change কি না; follow-up research দরকার কি না |
| সপ্তাহের শেষে | Exported report ও নিজের decision note | কী সিদ্ধান্ত নেওয়া হলো; কে কাজ করবেন; পুনরায় কবে দেখবেন |
| সদস্য যোগ/বিদায় হলে | Team role ও Integrations API key | প্রবেশাধিকার ঠিক আছে কি না |

Decision note **Research → Project collaboration**-এ team note অথবা personal bookmark হিসেবে রাখুন। Reports-এর **Share this report** থেকে অনুমোদিত audience, expiry ও প্রয়োজনে password বেছে share করুন। Public link তৈরির confirmation দেওয়ার আগে report-এর তথ্য দেখে নিন।

## ৮. Report দেখে সিদ্ধান্ত নেওয়ার নিয়ম

প্রতিটি বড় সিদ্ধান্তের আগে তিনটি প্রশ্ন করুন: **দাবিটির source কী? Source কতটা নতুন? দাবিটি fact, নাকি inference?**

Pricing-এ currency, monthly/annual interval, plan limit ও special offer দেখুন। Website-এর wording বদলানোকে নিশ্চিত price change ভাববেন না। গবেষণায় কোনো তথ্য না পাওয়া মানে বাস্তবে সেই feature বা প্রতিষ্ঠান নেই—এমন নয়।

**PARTIALLY_VERIFIED** quote matching বোঝায়; পুরো semantic claim independently verified নয়। SWOT, opportunity, positioning ও recommendation-কে পর্যালোচনার ভিত্তি হিসেবে ব্যবহার করুন।

## ৯. API access ও তথ্যের নিয়ন্ত্রণ

**Integrations → Workspace API keys → Key name → Create API key** দিয়ে read-only project/report key তৈরি হয়। Key একবার দেখানো হয়; নিরাপদে রাখুন। **Rotate key** দিলে পুরোনোটি সঙ্গে সঙ্গে বন্ধ হয়ে একই scope/expiry-র নতুন key পাওয়া যায়। **Revoke** স্থায়ীভাবে key বন্ধ করে। **Customer API usage**-এ সর্বশেষ authorized requests দেখা যায়।

এই key দিয়ে backend-এর `/api/v1/projects` ও `/api/v1/reports` endpoint পড়া যায়; UI-তে তৈরি key-তে দুই read scope দেওয়া হয়। এটি Gemini/Tavily provider key নয়।

**Settings → Data exports** থেকে নিজের account এবং owner হলে workspace JSON export করুন। **Deletion controls**-এ password/MFA এবং নির্দিষ্ট confirmation phrase দিয়ে deletion করতে হয়। Active research আগে cancel করে শেষ হতে দিন। Workspace delete-এ research/team/integrations সরানো এবং paid subscription cancellation হয়; প্রয়োজনীয় pseudonymous ledger/audit references থাকে। Account delete-এর আগে সব owned workspace-এর ownership মেটাতে হবে।

## ১০. আপনি যদি RivalScope SaaS-এর ব্যবসার মালিক হন

Customer workspace-এর `OWNER` হওয়া এবং RivalScope কোম্পানির commercial owner হওয়া আলাদা দায়িত্ব। Commercial launch-এর আগে operator-এর সঙ্গে নিশ্চিত করুন:

- Package price, seat, project, monitor ও credit policy অনুমোদিত এবং Stripe price-এর সঙ্গে মিলেছে।
- Live payment, refund/cancellation expectations, email delivery ও support workflow যাচাই হয়েছে।
- Privacy/export/deletion, production security, backup/restore ও observability-এর বাকি কাজের গ্রহণযোগ্য পরিকল্পনা আছে।
- Marketing-এ অসম্পূর্ণ feature-কে available বলা হচ্ছে না।
- Revenue/MRR/churn/provider-cost dashboard বর্তমানে নেই; plan price বা token count-কে বাস্তব revenue/margin ধরে নেওয়া হচ্ছে না।

প্রযুক্তিগত checklist-এর জন্য [অ্যাডমিন নির্দেশিকা](ADMIN_MANUAL.md) ও repository-এর `docs/IMPLEMENTATION_STATUS.md` দেখুন।

[সব নির্দেশিকায় ফিরে যান](README.md) · [সাধারণ ব্যবহারকারী](USER_MANUAL.md) · [অ্যাডমিন](ADMIN_MANUAL.md)
