# Implementation and verification status

Updated 2026-10-29. This is a code and local sandbox delivery. Live Google OAuth, Tavily and Stripe acceptance is deferred at the user's request because credentials are unavailable. Do not treat this as a production launch approval.

## Implemented

- Identity: Argon2 passwords, email verification/reset, hashed expiring sessions, profile/session management, TOTP MFA, replay prevention, single-use recovery codes, Google OIDC with PKCE/state/nonce and explicit account linking.
- Privacy: account/workspace JSON export, password/MFA reauthentication, ownership and active-job checks, controlled deletion and pseudonymous immutable accounting/audit retention.
- Workspaces: six server-enforced roles, normalized permission records, memberships, invitations/revocation, ownership transfer, workspace settings, team audit and plan/seat checks.
- Projects/collaboration: create/edit/archive/restore, project participants, team notes, personal bookmarks, expiring password-protected report links, explicit public-sharing confirmation and revocation.
- Research: seven bounded stages (plan/search/extract/analyze/catalog/verify/report), durable checkpoints and attempt budgets, cancellation, reservations/settlement/releases, source-backed findings and separate AI evidence review. Strategic content remains inference; automatic facts are PARTIALLY_VERIFIED.
- Providers: Gemini and optional OpenAI adapters, structured schema validation, bounded retry/explicit fallback, token/optional configured-rate cost records, per-organization daily budgets and validated response cache. Tavily has a search-adapter interface, normalized deduplication and cache.
- Sources: DNS-pinned public fetching, private/reserved address and unsafe redirect rejection, size/time/content limits, robots checks, source hashes, retrieval times, failed-source reporting and a tenant-scoped 15-minute source cache. Cache reuse rechecks robots and preserves retrieval time; live-fetch preference bypasses reuse.
- Intelligence: persisted product/feature catalogs, published pricing/history, SWOT/opportunity records, comparison selections, source-backed matrices and compatible-currency monthly-price/feature-evidence positioning. Unavailable information stays unavailable.
- Copilot: project/tenant-filtered semantic retrieval with compatible 768-dimensional pgvector/HNSW indexes, explicit lexical fallback, saved chat history, quotation validation and credit consumption.
- Monitoring/alerts: current BullMQ schedulers, source snapshots and change history, duplicate suppression, plan/grace/credit checks, pause/resume, literal phrase appearance/disappearance rules and user-selected severity. Generic page changes are not asserted to be confirmed price/feature changes.
- Notifications: per-user read state, instant/daily/weekly email preferences, encrypted durable email outbox, Slack/Discord incoming-webhook adapters, retries and delivery records.
- Billing: configurable plans/normalized entitlements, monthly/annual checkout, first eligible trial attempt, Stripe portal/invoice APIs, signed idempotent webhooks, invoice persistence, bounded past-due grace, prorated plan-change submission, credit add-ons and explicit development-only sandbox billing. No browser redirect grants a paid entitlement.
- Accounting: immutable ledger and usage events, concurrent reservation/settlement safety, per-activity consumption and persisted daily usage metrics. Annual cycle credit allowances are granted upfront for twelve months; plan-change invoices do not grant another full cycle allowance.
- Integrations: encrypted credentials, hashed scoped API keys, atomic key rotation/revocation, Redis per-key limits/usage history, signed webhook deliveries, secret rotation, disable/enable, retries/dead letter and audited recovery.
- Administration: separate verified platform privilege, organizations/users/plans/subscriptions/jobs/provider usage/audit/flags/settings/diagnostics, audited credit/plan/configuration mutations, session revocation and reauthenticated platform-role changes. Operator provisioning CLI refuses to remove the last administrator.
- Operations: structured request IDs/logs, authenticated metrics/worker diagnostics, opt-in OpenTelemetry/Sentry, Docker/Compose/Nginx, environment templates, CI and backup/isolated restore scripts.
- UI/documentation: shared local licensed fonts with 14px minimum, responsive layouts, role-aware controls and Bengali user/business-owner/admin manuals in Markdown, HTML and PDF.

## Verification evidence

- Strict backend typechecking and frontend lint/production build have passed; the frontend generates 24 routes.
- Unit/security/evidence-quality suite: 38 tests passed. PostgreSQL integration suite: 45 tests passed across four files.
- Integration coverage includes MFA/OIDC boundaries, privacy, cross-tenant access and foreign keys, RLS, accounting, research, real PDF/DOCX files, sharing, monitor expiry/downgrade, billing signatures/add-ons, provider caching/budgets/fallback, API-key limits/rotation, durable webhook/digest delivery, watch rules, usage metrics and source-cache freshness/isolation.
- Eleven migrations are present. Main and isolated test databases have applied the schema. An incorrect immutable-trigger function reference in the final migration was corrected after PostgreSQL rolled the failed application back; no database reset or user-data deletion was performed.
- Real browser registration, local worker email verification and project creation passed. Eleven primary workspace screens passed desktop/mobile smoke checks.
- A separate populated browser run against `rivalscope_test` passed 15 screens at two widths (30 views), zero visible fonts below 14px, no document overflow, no page errors and no failing API responses. Comparison save, notes, expiring sharing, sandbox credit purchase and viewer restrictions passed. Later watch-rule/usage UI additions require the final rerun.
- Live Gemini structured-output smoke check and a small 768-dimensional embedding request succeeded. This does not verify other provider accounts or quotas.
- API/web Docker images built locally earlier in the implementation. Rebuild images for the published commits before deployment.
- A real custom-format PostgreSQL dump and SHA-256 verification restored successfully to an isolated restore-check database. Dumps and local artifacts are ignored and not published.
- Backend and frontend dependency audits reached zero known vulnerabilities after unused CLI dependencies were removed; licensed shadcn CSS is vendored separately.

## Boundaries and remaining acceptance

1. Supply Google OAuth client credentials/redirect configuration, Tavily credentials, Stripe test keys/webhook/price IDs, production SMTP and any Slack/Discord/telemetry destinations. Run the real-account lifecycle checks; deterministic fixtures do not prove third-party acceptance.
2. Review annual credit/trial/grace/proration/refund commercial policy before charging customers. No regional payment provider is currently configured; only Stripe and the explicit local mock adapter run.
3. S3-compatible storage exists as optional Compose infrastructure; exports currently stream from the authenticated API and record export metadata rather than storing files in S3.
4. Lists intentionally have bounded latest-record limits. Full cursor pagination across every list, additional provider/model quality evaluations and broader operational load/failure testing remain part of the original full-production brief.
5. Research stages share one bounded research queue; notifications/webhooks/email use durable transactional outboxes. There is not a dedicated BullMQ queue for every category named in the original architecture brief.
6. RLS is a read-only defense layer for scoped tenant queries. Privileged application services still require explicit tenant authorization/filters; this is not a claim that every application transaction runs under an unprivileged tenant role.
7. Configure production TLS, secret/egress policies, encrypted off-host backups, deployment monitoring and real restore/recovery drills. No production deployment or external customer notification has been performed.

The full production brief is not represented as 100% complete while these boundaries remain. Repository publication is a source delivery, separate from provider activation and deployment.
