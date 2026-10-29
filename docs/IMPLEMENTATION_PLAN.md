# RivalScope AI implementation plan

The existing workspace contains independent NestJS 12 and Next.js 16 applications with npm lockfiles, installed dependencies, starter tests, and an unused Python environment. Preserve these applications and npm lockfiles. A new monorepo would discard the existing foundation without benefit. Node 24 is available. PostgreSQL, Redis, and object storage will run through Docker Compose.

## Dependency order and acceptance gates

1. Foundation: validate installed tooling, align Prisma CLI/client versions, document architecture, configure validated server environment and local infrastructure. Gate: schema validation, compilation, health endpoint.
2. Identity and organizations: Argon2 passwords, opaque hashed sessions, origin checks, rate limits, organizations, RBAC, invitations, account lifecycle. Gate: authentication and permission integration tests.
3. Persistence and tenant boundaries: normalized Prisma models, migrations, composite tenant foreign keys, credit ledger. Gate: fresh database migration and cross-tenant regression tests. Evaluate RLS; do not claim it is enabled if relying on application policies.
4. Projects and research configuration: CRUD, validated inputs, estimates, run lifecycle. Gate: persisted project and run API tests.
5. Providers: Gemini structured output, explicitly configured fallback, Tavily, bounded safe extraction, no production mocks. Gate: deterministic provider tests and separately reported live checks.
6. Orchestration: BullMQ, durable stage checkpoints, cancellation, source evidence, citations, reservations and refunds. Gate: retry, accounting, citation and cancellation tests.
7. Intelligence: evidence-backed competitor profiles, comparison, SWOT and opportunities; preserve unavailable values. Gate: schema and evidence constraints.
8. Reports: source-backed viewing and JSON/Markdown exports, real-data visualizations. Gate: API/UI build and export verification.
9. Monitoring: scheduler APIs, history, deduplicated changes, durable alerts. Gate: scheduler and change detection tests.
10. Copilot: tenant-filtered evidence retrieval and persisted conversations. Gate: context isolation and citation tests. Vector retrieval remains separately gated on embeddings and index tests.
11. Collaboration: invites, role changes, comments, scoped sharing and activity. Gate: escalation and expiry tests.
12. Billing: configurable database plans, Stripe verified webhook lifecycle, idempotency, seats and entitlements. Gate: signed event and concurrency tests.
13. Integrations: hashed scoped API keys, encrypted credentials, signed durable webhooks with retry/dead letter. Gate: key scope and delivery security tests.
14. Admin: separate platform role, audited mutations, diagnostics without secrets. Gate: privilege boundary tests.
15. Security/quality: audit, retention/privacy, telemetry, meaningful E2E and regression tests. Gate: checks on a fresh database and CI.
16. Deployment: distinct development/production Compose, API/worker/frontend images, reverse proxy, migrations, backups and restore instructions. Gate: container builds and smoke test where infrastructure permits.

All phases remain in scope. Status must distinguish working code, tested behavior, configuration-only foundations, and pending work. External accounts, delivery, OAuth, billing and production infrastructure cannot be reported as connected without credentials and verification. Never substitute demonstration data for unavailable services.
