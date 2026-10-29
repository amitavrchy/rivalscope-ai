# Product completion gates

The user's scope is the full production product, with a 14px minimum font size throughout. A gate is complete only when implemented and meaningfully verified. Provider credentials, third-party account setup and production operational validation remain distinct from implementation.

| Gate | Work | Acceptance |
| --- | --- | --- |
| Readable UI | Shared font family/type scale, minimum 14px, mobile reflow | Computed-style audit, desktop/mobile browser checks, production build |
| Identity | MFA/recovery codes, Google OIDC, profile/session management | Single-use challenge/recovery, OAuth state/nonce/linking, revoked-session tests |
| Privacy | Account/workspace exports and controlled deletion | Reauthentication, ownership/active-job/retention handling, tenant tests |
| Collaboration | Project access, comments, bookmarks, sharing, ownership/invitations | UI + APIs, private access and expiry tests |
| Intelligence | Comparison matrices, positioning, vector retrieval, PDF/DOCX | Source-backed data only, embeddings compatibility, real exports |
| Billing | Trials, proration/add-ons, sandbox adapter, lifecycle | Signature/idempotency tests; separate live sandbox acceptance |
| Integrations | Credential management/rotation, webhooks, per-key metering | Encryption/redaction, expiry/scope/rate and delivery tests |
| Admin | Organizations/users/plans/jobs/flags/settings/credits | Separate admin privilege, audited mutations and working UI |
| Security/reliability | Tenant defense, distributed limits, stage recovery/accounting | Tenant suite, crash/cancellation/duplicate tests |
| Operations | Observability, builds, backups/restore, deployment | Image build, restore drill, health/metrics, deployed smoke checks |

No scope item is removed merely to label the product complete. Track evidence and unresolved prerequisites in IMPLEMENTATION_STATUS.md.

The source delivery now includes 38 passing unit/security checks and 45 passing PostgreSQL integration checks. Typography/populated UI acceptance covered 30 desktop/mobile views; see IMPLEMENTATION_STATUS.md for the remaining production and architecture boundaries.
