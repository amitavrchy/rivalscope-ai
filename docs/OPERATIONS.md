# Operations and recovery

## Secrets and integrations

Production must use a verified TLS ingress, an HTTPS APP_ORIGIN, database/cache credentials, persistent volumes and a secret store. Keep the database migration identity separate from ordinary application access where the hosting platform supports it. The tenant-reader role intentionally has no write privileges; customer API reads and semantic retrieval use it with a transaction-local organization context. Other application services retain explicit tenant filters and authorization. This is scoped defense in depth, not a claim that all privileged service queries are covered by RLS.

Google login uses authorization code + PKCE + state cookie + nonce verification. Register the exact APP_ORIGIN/api/auth/google/callback redirect URI and set GOOGLE_OAUTH_CLIENT_ID/SECRET. Existing password accounts must explicitly connect Google after reauthentication. MFA uses encrypted TOTP secrets, one-use recovery hashes and expiring login challenges.

Google/Tavily/Stripe live credentials are not part of the repository. The user requested implementation and sandbox testing until these credentials become available. Mock billing requires BILLING_PROVIDER=mock and MOCK_BILLING_WEBHOOK_SECRET and is rejected in production. It never activates a plan merely because a browser follows a success URL. Production uses signed Stripe events.

## Telemetry and diagnostics

Set OTEL_EXPORTER_OTLP_ENDPOINT to an authorized collector to enable OTLP HTTP trace export. Set SENTRY_DSN to enable sanitized error reports; no external telemetry export is enabled by default. Request logs contain request ID, route template, method, status and duration, not cookies, provider bodies or arbitrary query parameters. Admin diagnostics expose worker heartbeat, failed outbox counts and authenticated Prometheus metrics at /api/admin/diagnostics/metrics.

Provider usage records report model, token counts, duration and prompt version. Cost remains unknown unless the operator configures AI_INPUT_USD_PER_MILLION and AI_OUTPUT_USD_PER_MILLION for the selected provider/model. Failure records explicitly mark usage as unknown. Redis token reservations enforce a conservative daily organization budget; unknown failed-request consumption retains its reservation. The token-budget day is UTC. Product credits are a separate ledger.

## Backups and isolated restore

From rivalscope-backend:

```
node scripts/backup.mjs
node scripts/restore-check.mjs /absolute/path/to/backup.dump unique_name_restore_check
```

On Windows, use a quoted absolute Windows file path. Pass --production to select production Compose. The backup helper uses pg_dump custom format, restricted local file creation and a SHA256 sidecar. It never places a password on the command line. The restore helper verifies the checksum, creates a new database whose name must end in _restore_check, never overwrites an existing database, restores with stop-on-error and prints aggregate verification counts. A successful restore check leaves the isolated database available for inspection.

Development backups are local files under ignored backups/. Production operators must put backups in encrypted, access-restricted storage with managed retention, protect the encryption-key backup separately and schedule the helper through their deployment scheduler. A persistent Docker volume alone is not a backup. Do not delete or overwrite a production database to run a restore drill.

## Research and queue recovery

Queued database runs reconcile into BullMQ after a queue submission outage. Stage outputs/checkpoints and attempts are durable. Finished runs are idempotent; cancellation and failures settle only completed stages and release unused holds. Platform administrators can request cancellation or restart a failed/cancelled run as a new run from Administration → Jobs. A restart reserves new credits; do not repeat it without inspecting the resulting run.

Email, notification and webhook delivery use durable idempotent outboxes with bounded retry. Webhooks and channel notifications become dead-letter records after exhaustion. Workspace webhook UI permits explicit retry. The mail outbox is inspectable without exposing encrypted message bodies. Repair the receiver/SMTP problem before requeueing failed deliveries.

## Platform administrator provisioning

An authorized operator can run this from the backend directory:

```
node --import tsx src/admin-cli.ts grant verified-account@example.com
node --import tsx src/admin-cli.ts revoke verified-account@example.com
```

This requires database operator access, an existing verified account, and records a platform audit entry. It refuses to revoke the final administrator. The application UI permits verified administrators to change another verified user's platform role after password/MFA reauthentication.

## Production acceptance

Before exposing the service: run migrations, seed configurable plans, build images, test HTTPS/session cookies and intended origins, configure live integration accounts, run a Stripe sandbox lifecycle with real account credentials, perform a restore drill, verify worker/queue/outbox health, and review the implementation status against the complete product scope. Local deterministic transport fixtures do not prove third-party account activation or production hosting behavior.
