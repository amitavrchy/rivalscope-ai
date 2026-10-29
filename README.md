# RivalScope AI

Next.js frontend, NestJS API and BullMQ worker with PostgreSQL/pgvector and Redis. See [implementation status](docs/IMPLEMENTATION_STATUS.md) for feature coverage, verification and external service activation requirements.

This is the shared workspace repository. The API and web application are independent Git submodules; the retained Python tooling lives in `rivalscope-ai/`. AI research currently executes in the NestJS worker.

```bash
git clone --recurse-submodules https://github.com/amitavrchy/rivalscope-ai.git rivalscope
cd rivalscope
```

## বাংলা ব্যবহার নির্দেশিকা

[নির্দেশিকার সূচি](docs/manuals/bn/README.md) · [সাধারণ ব্যবহারকারী](docs/manuals/bn/USER_MANUAL.md) · [ব্যবসার মালিক](docs/manuals/bn/BUSINESS_OWNER_MANUAL.md) · [অ্যাডমিন](docs/manuals/bn/ADMIN_MANUAL.md)

Browser/print সংস্করণের জন্য [সম্পূর্ণ বাংলা manual](docs/manuals/bn/RIVALSCOPE_MANUAL_BN.html) খুলুন। সরাসরি পড়া বা শেয়ার করার জন্য [বাংলা PDF](docs/manuals/bn/RIVALSCOPE_MANUAL_BN.pdf) আছে।

## Local development (Windows / PowerShell)

Node 24 and Docker Desktop are required. Existing npm lockfiles are retained.

```powershell
docker compose up -d --wait
npm --prefix rivalscope-backend ci
npm --prefix rivalscope-frontend ci
# Copy .env.example to .env only when no local environment already exists.
# Configure a random 32-byte hex ENCRYPTION_KEY and server provider credentials.
npm run db:generate
npm run db:migrate
npm run db:seed
```

Run these in three terminals:

```powershell
npm run dev:api
npm run dev:worker
npm run dev:web
```

For this prepared workspace, `powershell -ExecutionPolicy Bypass -File scripts/start-local.ps1` builds the API and starts all three applications in the background with logs under ignored `artifacts/`. It reuses existing listeners on ports 3000/4000 and an existing registered worker process. Start Docker Desktop first.

- App: http://localhost:3000
- API docs: http://localhost:4000/api/docs
- Readiness: http://localhost:4000/api/health/ready
- Verification/password-reset email inbox: http://localhost:8025

Register, open the local inbox, verify your email and create a project. Research works from known public source URLs with discovery disabled. Automatic discovery requires `TAVILY_API_KEY`. Checkout requires Stripe keys, a webhook secret and database-backed plan price IDs. Provider credentials must never appear in frontend or `NEXT_PUBLIC_*` environment variables.

On Windows networks requiring the OS certificate store, use Node's `--use-system-ca` or set `NODE_USE_SYSTEM_CA=1` before launching Node. Keep TLS certificate verification enabled.

## Checks

Unit tests use deterministic fixtures and do not call live providers. Integration tests require a separate `rivalscope_test` database and Redis database 1:

```powershell
docker compose exec postgres createdb -U rivalscope rivalscope_test
$env:DATABASE_URL='postgresql://rivalscope:rivalscope_local@localhost:5433/rivalscope_test'
npm run db:migrate
npm run db:seed
npm run check
```

Use `TEST_DATABASE_URL` and `TEST_REDIS_URL` to override integration infrastructure. Integration tests append uniquely named test records to the dedicated test database; they never truncate user data. `scripts/smoke-preview.py` uses the retained Python Playwright environment and installed Edge to verify the running local UI. It creates a clearly labeled preview workspace, verifies real local email delivery and saves ignored desktop/mobile screenshots. `npm --prefix rivalscope-backend run check:provider` makes a small live Gemini request and prints no secret.

## Deployment

`docker-compose.production.yml`, app Dockerfiles and `deployment/nginx.conf` define the container topology. Production requires `rivalscope-backend/.env.production` with container database/Redis hostnames, a strong database password, HTTPS `APP_ORIGIN`, SMTP, encryption and provider secrets. Bind the loopback reverse proxy behind your TLS ingress. Migrations/plan seeding precede API and worker startup. API and web image builds have succeeded locally; rebuild for the published commits and verify the deployed stack before launch. No production deployment or live payment acceptance has been performed.

No external service is silently replaced with mock data. S3-compatible storage is an optional Compose profile and is not yet used by report exports. The Python dependency environment is retained but is not a running service.
