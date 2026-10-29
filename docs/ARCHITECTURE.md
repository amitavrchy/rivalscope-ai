# Architecture

Next.js App Router serves the workspace UI. A same-origin `/api` rewrite forwards to the NestJS REST API on port 4000. The browser receives only an HttpOnly opaque session cookie; provider credentials stay in the backend environment. Swagger documents the API. Zod validates configuration, request bodies and model outputs. NestJS services isolate identity, tenancy, projects, accounting, providers, research orchestration and reporting.

PostgreSQL is the system of record through Prisma and the pg driver adapter. Organization-owned records carry `organizationId`; lookups always include authorized membership. Composite foreign keys prevent a child from referencing another tenant's project. Redis/BullMQ executes background research in a separate worker process. Research runs and stages persist progress; the API streams tenant-authorized progress using SSE. Database transactions reserve credits and append immutable ledger entries. Queued work is reconciled from durable pending runs to cover crashes between transaction commit and queue submission.

Research follows bounded planning, search, extraction, analysis and report stages. Search results are untrusted suggestions, never evidence until safely fetched. DNS addresses are validated and pinned for each request; redirects are revalidated. Extraction limits time, body size, pages and text. AI receives isolated source data and returns validated structured claims. Citation IDs must belong to the current run; quotations must occur in extracted source text. Model interpretation is labeled inference. Unsupported quantitative claims remain unavailable. Missing credentials fail explicitly. Provider fallback must be explicitly configured.

The Python environment is retained but is not yet a service. Avoid adding a second orchestration/database stack until a measured workload needs it. The required Next.js/NestJS/PostgreSQL/Redis architecture uses container hosting, not a Cloudflare Worker rewrite.

## Security boundaries

- Session tokens and invitations are random, hashed at rest and expire. Passwords use Argon2id.
- Mutations require an allowed Origin plus JSON content type; cookies are SameSite Lax and Secure in production.
- Backend membership and role checks precede resource access. Platform administrators use a separate user attribute.
- Source fetching never uses caller-controlled network credentials. Internal/private addresses, unsafe schemes, redirects and oversized responses are rejected.
- Secrets live only in ignored local environment files or deployment secret stores; error responses do not include provider response bodies or secrets.
- Credit updates serialize on the organization row and use unique idempotency keys.
- PostgreSQL RLS is a future defense-in-depth gate, not a replacement for application authorization. The initial migration does not claim RLS protection.

## Operational boundaries

Development containers bind database/cache/storage ports to loopback. Production requires HTTPS, restricted ingress, restricted worker egress, database backups, external secret management and configured third-party providers. Read IMPLEMENTATION_STATUS.md before treating a module as complete.
