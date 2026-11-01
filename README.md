# RivalScope AI

[Web app](https://rivalscope-132.netlify.app) · [API](https://rivalscope-api.onrender.com)

Evidence-backed competitive intelligence for teams that research public sources, compare competitors, and watch the market from one workspace.

## Overview

RivalScope turns public competitor information into source-backed findings. This repository is the workspace for that product. The web application and the API live in Git submodules, `rivalscope-frontend` and `rivalscope-backend`, which are the repositories behind the deployments above. A retained Python project in `rivalscope-ai` supports browser checks and the Bengali manuals. It does not run a second API. Research executes in the NestJS worker.

The browser talks only to the Next.js app. A same-origin `/api` rewrite, aimed at `API_INTERNAL_URL`, forwards to the NestJS API. Sessions are HttpOnly cookies. Provider credentials stay in the API environment. PostgreSQL is the system of record, with pgvector for copilot retrieval. Redis and BullMQ run background research, schedules, and rate limits.

## Key features

- Accounts with Argon2id passwords, email verification, hashed expiring sessions, TOTP multi-factor authentication, recovery codes, and optional Google sign-in.
- Workspaces with six roles (owner, admin, analyst, editor, viewer, billing manager), invitations, and project collaboration.
- Research runs with seven bounded stages: plan, search, extract, analyze, catalog, verify, and report. Citations must match text fetched for that run.
- Competitor catalogs, published pricing, SWOT records, and comparison matrices that leave missing evidence unknown.
- Website monitoring, literal phrase watch rules, and email, Slack, or Discord notifications.
- A project copilot that retrieves saved research with pgvector embeddings, with a lexical fallback.
- PDF and DOCX reports, plus expiring shared links.
- Stripe checkout, credit balances, scoped customer API keys, and signed webhooks.
- Platform administration, usage history, and account or workspace export and deletion.

## Tech stack

![Next.js](https://img.shields.io/badge/Next.js-16-000000?logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/React-19-149ECA?logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![NestJS](https://img.shields.io/badge/NestJS-12-E0234E?logo=nestjs&logoColor=white)
![Prisma](https://img.shields.io/badge/Prisma-7-2D3748?logo=prisma&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17%20%2B%20pgvector-4169E1?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7%20%2B%20BullMQ-DC382D?logo=redis&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-4-06B6D4?logo=tailwindcss&logoColor=white)

| Layer | Stack |
| --- | --- |
| Web | Next.js 16 App Router, React 19, TanStack Query, Tailwind CSS 4, Zod |
| API | NestJS 12, Prisma 7, BullMQ, Zod, OpenAPI |
| Data | PostgreSQL 17 with pgvector, Redis 7 |
| AI and search | Gemini by default (`AI_PROVIDER`), optional OpenAI, optional Tavily discovery |
| Billing and mail | Stripe, SMTP via `SMTP_URL` |

## Project structure

```
rivalscope-frontend/          Next.js web app (submodule)
rivalscope-backend/           NestJS API, worker, and Prisma schema (submodule)
rivalscope-ai/                Python tooling for checks and manuals
docs/manuals/bn/              Bengali user, owner, and admin manuals
deployment/nginx.conf         Reverse proxy for the container stack
docker-compose.yml            Local Postgres, Redis, and Mailpit
docker-compose.production.yml API, worker, web, database, and proxy
scripts/                      Workspace checks and the local start helper
package.json                  dev, database, and check scripts
```

## Getting started

Use Node.js 24. Docker is required for PostgreSQL (pgvector) and Redis.

```bash
git clone --recurse-submodules https://github.com/amitavrchy/rivalscope-ai.git
cd rivalscope-ai
docker compose up -d --wait
```

Copy `rivalscope-backend/.env.example` to `rivalscope-backend/.env`, and `rivalscope-frontend/.env.example` to `rivalscope-frontend/.env`.

On the API, set `DATABASE_URL`, `REDIS_URL`, and `ENCRYPTION_KEY` (32 random bytes as hex). Set `APP_ORIGIN` to the web origin; production requires `https`. `PORT` is the API listen port. Account mail needs `SMTP_URL` and `MAIL_FROM`. Optional integrations use `GEMINI_API_KEY`, `OPENAI_API_KEY`, `AI_FALLBACK_PROVIDER`, `TAVILY_API_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `GOOGLE_OAUTH_CLIENT_ID`, and `GOOGLE_OAUTH_CLIENT_SECRET`.

On the web app, set `API_INTERNAL_URL` to the API origin. Do not put provider secrets in frontend variables.

```bash
npm --prefix rivalscope-backend ci
npm --prefix rivalscope-frontend ci
npm run db:generate
npm run db:migrate
npm run db:seed
```

Run the API, worker, and web app in separate terminals:

```bash
npm run dev:api
npm run dev:worker
npm run dev:web
```

OpenAPI is served at `/api/docs`. Readiness is `GET /api/health/ready`.

`docker-compose.production.yml` builds the API, worker, and web images, runs migrations, and places Nginx (`deployment/nginx.conf`) in front. Production secrets belong in `rivalscope-backend/.env.production`, including `APP_ORIGIN`, `DATABASE_URL`, `REDIS_URL`, `ENCRYPTION_KEY`, `SMTP_URL`, and provider keys. `BILLING_PROVIDER=mock` is rejected when `NODE_ENV` is production.

Check each app:

```bash
npm --prefix rivalscope-backend run typecheck
npm --prefix rivalscope-backend run lint
npm --prefix rivalscope-backend run build
npm --prefix rivalscope-frontend run lint
npm --prefix rivalscope-frontend run build
```

`npm run check` runs those steps plus the backend unit and integration tests. Point integration tests at an isolated database with `DATABASE_URL` or `TEST_DATABASE_URL`, and `REDIS_URL` or `TEST_REDIS_URL`.

## Author

Amitav Roy Chowdhury — [github.com/amitavrchy](https://github.com/amitavrchy)
