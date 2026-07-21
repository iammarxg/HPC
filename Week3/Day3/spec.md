# Code Converter Web App — Specification

## 1. Objective
Build a web application that converts source code from one programming language to another, using **OpenRouter** as the sole LLM provider.

- **Default model:** the platform ships with a free OpenRouter model (prompt cost == 0 and completion cost == 0, per OpenRouter's model metadata) set as the system default.
- **User override:** logged-in users can change their personal default model in Settings via a searchable dropdown populated from the synced model list.
  - Users see **only the model's name**. Pricing, cost, and free/paid status are never shown to users — visible to admins only, in the admin dashboard (§13).
  - Models from restricted providers (Anthropic/Claude, OpenAI/ChatGPT, Google/Gemini) are selectable only by Tier 1 and Tier 2 accounts. Free-tier accounts see these models listed in the dropdown (not hidden), but:
    - The model name is visually grayed out.
    - A "PRO" (or "Paid") label appears next to the name.
    - Hovering the name/label shows a tooltip prompting the user to subscribe (e.g. "Upgrade to a paid plan to use this model").
    - Selection of a restricted model is blocked both client- and server-side for ineligible accounts.
- **Admin override:** an admin-set "forced model" takes precedence over every user's personal setting when active. Admin can also change the platform default independently of an emergency override.
- **Model list sync:** a scheduled background job calls OpenRouter's models endpoint every 24 hours, caches the result (id, label, provider, pricing/free flag), and powers every searchable model dropdown. Pricing, free/paid flag, and provider are exposed via `/api/admin/*` endpoints only — never via the end-user `/api/models` endpoint (§9).

## 2. Scope

### In scope
- OpenRouter API integration (sole LLM provider)
- Guest, free-tier, and paid-tier conversion flow with daily + monthly limits, plus purchasable usage/API-access add-ons for paid tiers
- Syntax-highlighted, copyable, and downloadable output
- Conversion history for free and paid registered accounts (not guests)
- Programmatic API access for Tier 2 subscribers by default, purchasable as an add-on for Tier 1
- A pluggable language registry, seeded with up to 20 popular languages, so new languages can be added without touching backend code
- A distinct LLM prompt template per directional language pair
- Tier 2 background AI-verification pass, fully hidden from the user until resolved
- A fully functional admin dashboard UI — every operational change (API keys, model settings, tier limits, language registry, alerts) is made through the dashboard, never by editing config files or redeploying (§13)
- Containerized deployment (Docker, multi-architecture) (§14)

### Out of scope
- Payment/billing provider integration (assume `subscription_tier` and add-on grants are already set on the user record by whatever billing system is used)
- Real-time collaborative editing
- Multi-provider LLM routing (OpenRouter only)
- Pulling code directly from external sources (e.g. GitHub import) — paste/upload only. If implemented in the future, this would be restricted to Tier 2 accounts only.

## 3. Assumptions
- Single provider: OpenRouter, for all models.
- Guest identification: IP + browser session, no persistent guest accounts.
- Daily limits reset at midnight in the user's local timezone, not UTC. Requires capturing an IANA timezone string (e.g. `Asia/Riyadh`) — from the browser for guests, stored on the user record for accounts — used server-side for all reset calculations.
- No offline/queued conversions; all requests are synchronous, single-shot.

## 4. Inputs

### 4.1 User-provided input (via UI)
| Field | Type | Constraints |
|---|---|---|
| `source_code` | string (textarea) | Required. Non-empty. Max 10,000 characters (see §11 for handling large inputs). |
| `source_language` | string (dropdown selection) | Required. Must match an entry in the language registry (§4.3). |
| `target_language` | string (dropdown selection) | Required. Must match an entry in the language registry. Must differ from `source_language`. |
| `context` *(Tier 2 only)* | string (short text input) | Optional. Max 500 characters. Silently ignored (not validated, never an error) for non-Tier-2 accounts — see §9. |

### 4.2 Model list (OpenRouter)
Synced every 24 hours from OpenRouter's models endpoint into a local cache (§10, `ModelRegistry`). Each cached entry stores: OpenRouter model ID, display label, provider, and free/paid pricing flag. Pricing, free/paid flag, and provider are admin-facing only (§13). The end-user `/api/models` endpoint returns only `id`, `label`, and a `restricted` boolean indicating whether the model requires a paid tier (§1) — never cost data.

### 4.3 Supported language list
Languages are defined in a **language registry** (config table, not application code) so adding a new language is a data change, not a deploy:

```json
{ "id": "python", "label": "Python", "file_extension": "py", "highlighter_alias": "python" }
```
The registry backs both language dropdowns (search-filterable on `label`) and the download feature (§5) via `file_extension`.

Seed the registry with up to 20 popular languages, including shell/scripting languages: Python, JavaScript, TypeScript, Java, C, C++, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, Scala, R, Perl, Lua, SQL, Bash, and Windows Batch.

### 4.4 System/session input
- Auth token (JWT or session cookie) if logged in — determines tier, saved model preference, and usage counters.
- IP address / anonymous session ID for guests — determines guest usage counter.
- User's IANA timezone string, for local-midnight reset calculations.

### 4.5 Conversion prompt templates
Each ordered language pair (source → target) uses its own distinct LLM prompt template — e.g. Bash → Batch and Batch → Bash are two separate templates, not one generic template reused with swapped variables. Templates may share structure, but the source/target-specific instructions and any language-specific conversion notes must be explicit in each template rather than inferred generically. Prompt content/wording is an implementation detail and is intentionally not specified here — only the requirement that a distinct, explicit template exists per directional pair (§10, `ConversionPromptTemplate`).

## 5. Outputs

### 5.1 Success response (to UI)
| Field | Type | Description |
|---|---|---|
| `conversion_id` | string | Identifier for this conversion (used to poll verification status, §6/§9). |
| `converted_code` | string, nullable | Output code in `target_language`. `null` while a Tier 2 verification pass is still pending (§6.9/§9). |
| `usage_remaining_today` | integer | Conversions left today. |
| `usage_remaining_month` | integer, nullable | Conversions left this month (paid tiers only; `null` for guest/free). |
| `usage_limit_today` | integer | Effective daily limit for this user's tier (base tier limit + any active add-on, §7). |
| `usage_limit_month` | integer, nullable | Effective monthly limit (paid tiers only). |

**Output display:**
- Read-only, syntax-highlighted code viewer. Use **Shiki** (TextMate grammars, VS Code-grade fidelity); **Prism.js** is an acceptable lighter alternative.
- **Copy button** — copies raw `converted_code` text, no formatting artifacts.
- **Download button** — downloads `converted_code` as `converted.<file_extension>`, extension pulled from the language registry entry for `target_language`.
- All rendered code is HTML-escaped/sanitized before display to prevent XSS via pasted or converted content (§12).

### 5.2 Error response (to UI)
| Field | Type | Description |
|---|---|---|
| `error_code` | string | Machine-readable code (§8). |
| `message` | string | Friendly, human-readable message — never a raw provider error. |

Errors are surfaced as a dismissible inline banner (not a full-page failure); the user's pasted code and selections are preserved for retry.

## 6. Functional Requirements

1. User can paste code and select source/target language without logging in.
2. Clicking **Convert**:
   - Client-side validation (non-empty code, both languages selected, languages differ, `context` length if present).
   - Sends request to the backend conversion endpoint.
   - Shows an animated loading state (skeleton/shimmer) until the response returns.
3. Backend always re-validates server-side; client-side checks are UX convenience only, never enforcement.
4. Backend checks the caller's remaining daily and monthly usage (§7) **before** calling OpenRouter, so a blocked request never costs an API call.
5. On success, backend increments usage counters and returns the converted code.
6. **Usage display:** an inline, non-modal counter (remaining/limit) is visible at all times. No upsell text or CTA is shown while usage remains. Once the user's usage reaches 0 (daily or monthly, whichever first):
   - Guests: upsell message ("Register for a free account to get 10 conversions a day.") with a **Register** button linking to the registration page.
   - Free-tier users: upsell message ("Upgrade to a paid plan for higher daily and monthly limits.") with an **Upgrade** button linking to the pricing/upgrade page.
7. **On limit exceeded (attempting to convert at 0 remaining):** a modal interrupts the flow, with the same CTA buttons as §6.6:
   - Guest → registration modal.
   - Free tier → subscription/upgrade modal.
   - Paid tiers hitting their own cap get the inline banner from §5.2, with an "add more usage" CTA where an active add-on path exists (§6.13).
8. **Tier 2 — context field:** optional `context` input (§4.1) sent alongside the system prompt to give the model background on the code's role/scope.
9. **Tier 2 — background verification pass:**
   - The initial (unverified) conversion is generated but never shown to the user.
   - The loading state (§6.2) remains active while an admin-configured verifier model reviews the original + converted code in the background.
   - Once verification resolves, the user is shown exactly one result:
     - Verification revised the output → the revised code, with a "Verified by {model name}" label and checkmark.
     - Verification failed, timed out, or made no changes → the original (unverified) conversion, with no badge.
   - The user never sees the unverified result first and then an update — only the single final state, in either case.
10. **Conversion history** (free & paid accounts only): every conversion is saved to the user's account and viewable from a history page/panel.
11. **Tier 2 API access:** authenticated REST access (API key scoped to the account) to the conversion endpoint, included by default for Tier 2, subject to the same usage limits as the web UI (see §6.13 for add-ons).
12. Output is copyable and downloadable in the target language's native file extension (§5.1) for all tiers.
13. **Usage add-ons:** Tier 2 accounts can purchase additional conversion usage on top of their plan limits. Tier 1 accounts (no API access by default) can purchase API access as an add-on. Add-on grants are recorded on the account (§10, `UserAddOn`) and factored into the usage-limit check (§7); payment processing itself remains out of scope (§2).

## 7. Business Rules — Usage Limits

| User Type | Daily Limit | Monthly Limit | Reset |
|---|---|---|---|
| Guest (no account) | 3 conversions/day | — | User's local midnight |
| Registered (free tier) | 10 conversions/day | — | User's local midnight |
| Paid — Tier 1 | 50 conversions/day | 750 conversions/month | Daily: local midnight · Monthly: 1st of calendar month, local time |
| Paid — Tier 2 | 150 conversions/day | 3,000 conversions/month | Daily: local midnight · Monthly: 1st of calendar month, local time |

All four numbers live in the `SubscriptionTier` table and are adjustable from the admin dashboard (§13).

Tier 1 accounts do not have API access by default; an active `api_access` add-on (§10) grants it. Tier 2 accounts have API access by default and may hold `extra_conversions` add-ons that increase their effective daily/monthly limits.

**Limit enforcement rules:**
- Effective limits = base tier limit + any active add-on grants.
- A conversion request must pass both the daily check and (for paid tiers) the monthly check — whichever would be exceeded first blocks the request. Counters increment together, atomically, on success.
- No stacking: an authenticated request always uses the account's counters exclusively; guest-session usage on that browser is irrelevant once authenticated.

## 8. Error Handling

OpenRouter mirrors standard HTTP status codes plus a `code`/`message` body. Internal error codes returned to the frontend:

| Trigger | OpenRouter status | Our `error_code` | UI message |
|---|---|---|---|
| Missing/empty code, missing language, source == target, or Tier 2 `context` exceeding 500 characters | — (pre-flight) | `invalid_input` | "Please check your code and language selection, then try again." |
| Language not in registry | — (pre-flight) | `unsupported_language` | "That language isn't supported yet." |
| Daily/monthly limit reached | — (pre-flight) | `limit_exceeded` | Contextual upsell message (§6.6) |
| Restricted model selected by an ineligible account | — (pre-flight) | `model_restricted` | "This model requires a paid plan." |
| Bad request to OpenRouter | 400 | `llm_provider_error` | "We couldn't process that request. Please try again." |
| OpenRouter API key invalid | 401 | `internal_error` | "Something went wrong on our end. Please try again shortly." — fires admin alert |
| OpenRouter credits exhausted | 402 | `llm_provider_error` | "Our conversion service is temporarily unavailable. We're on it — please try again soon." — fires admin alert |
| Content blocked by provider guardrails | 403 | `content_blocked` | "This code couldn't be processed by our content safety checks." |
| Requested model not found/deprecated | 404 | `internal_error` | "Something went wrong on our end. Please try again shortly." — fires admin alert |
| Provider request timeout | 408 | `timeout` | "The conversion is taking longer than expected. Please try again, or try a shorter snippet." |
| Input too large for the model | 413 | `input_too_large` | "Your code snippet is too large to convert. Please shorten it." |
| Malformed/unprocessable request | 422 | `invalid_input` | "Please check your code and language selection, then try again." |
| Rate limited (OpenRouter-level) | 429 | `llm_provider_error` | "Our conversion service is experiencing high demand. Please try again in a moment." |
| Provider/server error, all configured API keys exhausted | 500 / 502 / 503 | `llm_provider_error` | "The conversion service is temporarily unavailable. Please try again shortly." |
| Unhandled server error | — | `internal_error` | "Something went wrong on our end. Please try again shortly." |

A single failed OpenRouter key (§13.3) triggers a fallback to the next configured key, not a user-facing error — the rows above involving OpenRouter provider failures apply only once all configured keys have been exhausted. All error responses use the schema in §5.2 — raw OpenRouter error bodies and stack traces are never forwarded to the client, only logged server-side.

## 9. API Contract (backend)

### `POST /api/convert`
**Auth:** optional (guest allowed)
**Request body:**
```json
{
  "source_code": "def add(a, b):\n    return a + b",
  "source_language": "python",
  "target_language": "javascript",
  "context": "Standalone utility function, no external deps."
}
```
`context` is honored only for Tier 2 accounts. For non-Tier-2 accounts, if a `context` value is present it is silently stripped before constructing the prompt — it never triggers `invalid_input` and is never sent to OpenRouter.

**Response (200, non-Tier-2, or Tier 2 with verification disabled/unavailable):**
```json
{
  "conversion_id": "conv_8f2a1c",
  "converted_code": "function add(a, b) {\n    return a + b;\n}",
  "usage_remaining_today": 129,
  "usage_remaining_month": 2941,
  "usage_limit_today": 150,
  "usage_limit_month": 3000
}
```

**Response (200, Tier 2, verification pending):**
```json
{
  "conversion_id": "conv_8f2a1c",
  "converted_code": null,
  "verification_status": "pending",
  "usage_remaining_today": 129,
  "usage_remaining_month": 2941,
  "usage_limit_today": 150,
  "usage_limit_month": 3000
}
```
The client polls `GET /api/conversions/{conversion_id}` and does not render any code until `verification_status` resolves.

**Response (429 — internal limit):**
```json
{
  "error_code": "limit_exceeded",
  "message": "You've reached your daily conversion limit. Sign up for a free account to get more."
}
```

### `GET /api/conversions/{conversion_id}`
Polled by the client for Tier 2 conversions. Returns `verification_status` (`pending` | `verified` | `unchanged` | `failed`) and, once no longer `pending`, the final `converted_code` (revised if `verified`, original otherwise) and `verified_by_model` (set only when `verified`).

### `GET /api/usage`
Returns current usage counters for the caller without triggering a conversion — used to render the inline counter (§6.6).

### `GET /api/history`
**Auth:** required (free or paid account)
Returns the caller's saved conversion history, paginated.

### `GET /api/models`
Returns the cached, 24-hour-synced OpenRouter model list for populating searchable dropdowns. Response per model: `id`, `label`, `restricted` (bool). Never includes pricing, free/paid flag, or provider.

### `PATCH /api/settings/model`
**Auth:** required
Sets the caller's personal default model, chosen from `/api/models`. Rejects (`model_restricted`, §8) if the chosen model is `restricted` and the account isn't Tier 1/Tier 2.

### `POST /api/auth/register`, `POST /api/auth/login`, `POST /api/auth/logout`
Standard auth endpoints; issue/revoke the session token used across the above.

### Tier 2 programmatic access
`POST /api/v1/convert` — same contract as `/api/convert`, authenticated via a Tier-2-scoped API key (`Authorization: Bearer <key>`) instead of a session cookie, subject to the same usage limits.

### Admin-only endpoints
All require an authenticated session with the `admin` role (§10) and are logged to `AdminAuditLog` (§10).

**Models & AI**
- `PATCH /api/admin/default-model` — sets the platform default model.
- `PATCH /api/admin/model-override` — sets/clears the emergency forced model. Takes effect immediately (config read, not a deploy).
- `PATCH /api/admin/verifier-model` — sets the Tier 2 verification model. Applies within 10 seconds of the admin action.
- `POST /api/admin/models/resync` — forces an immediate model-list sync instead of waiting for the next 24h cycle.
- `GET /api/admin/models` — full model list including provider, pricing, and free/paid flag (admin-only view).
- `PATCH /api/admin/models/{id}` — override a model's `requires_paid_tier` flag beyond the automatic Anthropic/OpenAI/Google default.

**Credentials**
- `GET /api/admin/credentials/openrouter-keys` — lists all configured OpenRouter keys, masked, with `label`, `priority`, `status` (`active`|`failed`), `last_failure_at`, `last_failure_reason`.
- `POST /api/admin/credentials/openrouter-keys` — adds a new key (label + value), appended to the fallback order, encrypted at rest.
- `PATCH /api/admin/credentials/openrouter-keys/{id}` — edit label/priority, or reactivate a failed key.
- `DELETE /api/admin/credentials/openrouter-keys/{id}` — remove a key.
- `POST /api/admin/credentials/openrouter-keys/{id}/test` — sends a trivial test request against a specific key.

**Tiers & limits**
- `GET /api/admin/tiers`, `PATCH /api/admin/tiers/{tier_id}` — view/edit daily & monthly limits and feature flags per tier.
- `POST /api/admin/tiers` — create a new tier.

**Languages**
- `GET /api/admin/languages`, `POST /api/admin/languages`, `PATCH /api/admin/languages/{id}`, `DELETE /api/admin/languages/{id}` — full CRUD on the language registry (§4.3).

**Users**
- `GET /api/admin/users` — searchable/filterable user list.
- `PATCH /api/admin/users/{id}` — change a user's tier, reset their usage counters, suspend/reinstate their account.
- `PATCH /api/admin/users/{id}/addons` — grant/revoke add-ons (`extra_conversions`, `api_access`) manually (§10, `UserAddOn`).

**Analytics**
- `GET /api/admin/analytics` — aggregated usage metrics (conversions over time, by tier, by language pair, error-rate breakdown), date-range filter, CSV export.
- `GET /api/admin/analytics/model-usage` — most-selected models by user, sourced from `ModelSelectionLog`, independent of OpenRouter call success/failure.

**Alerts**
- `GET /api/admin/alerts`, `PATCH /api/admin/alerts` — configure notification channel(s) (`email` | `webhook` | `discord_webhook`) and trigger events (§8's admin-alert triggers, model sync failures, OpenRouter key failures, etc.).

**Audit**
- `GET /api/admin/audit-log` — paginated log of every admin action (who, what changed, old → new value, when).

## 10. Data Model

**User**
```
id, username, email, password_hash, subscription_tier_id,
timezone, default_model_id (nullable), role (enum: user | admin),
status (enum: active | suspended), created_at
```
`id` is the internal primary key; `username` is the user-facing handle used for login/display. `role` gates access to every `/api/admin/*` endpoint and the dashboard UI.

**SubscriptionTier**
```
id, name, daily_limit, monthly_limit (nullable),
allows_context_input (bool), allows_verification (bool), allows_api_access (bool)
```

**UserAddOn**
```
id, user_id, addon_type (enum: extra_conversions | api_access), quantity (nullable, for extra_conversions),
granted_at, expires_at (nullable), granted_by_admin_id (nullable), active (bool)
```
Represents purchased/granted add-ons layered on top of the base tier limits (§7). Payment processing that creates these records is out of scope (§2); the admin dashboard can also grant/revoke them manually (§13.6).

**UsageLog** *(daily)*
```
id, user_id (nullable), guest_identifier (nullable), local_date, count
```

**UsageLogMonthly** *(paid tiers only)*
```
id, user_id, year_month, count
```

**ConversionHistory** *(free & paid users only)*
```
id, user_id, source_language, target_language, source_code, converted_code,
verification_status (enum: not_applicable | verified | unchanged | failed),
verified_by_model (nullable), created_at
```

**LanguageRegistry**
```
id, label, file_extension, highlighter_alias
```

**ConversionPromptTemplate**
```
id, source_language_id, target_language_id, template_key, created_at, updated_at
```
One row per ordered (source, target) language pair (§4.5). Template content storage/location is an implementation detail.

**ModelRegistry** *(synced from OpenRouter every 24h)*
```
id, openrouter_model_id, label, provider, is_free, requires_paid_tier (bool), last_synced_at
```
`provider`, `is_free` are admin-facing only (§1, §4.2). `requires_paid_tier` drives the restricted/grayed-out UI treatment for Claude/ChatGPT/Gemini-family models and is auto-set by provider, admin-overridable.

**ModelSelectionLog**
```
id, user_id (nullable), guest_identifier (nullable), model_id, created_at
```
Logged at the point a model is selected for a conversion request, before the OpenRouter call — powers the "most used models" admin view (§13.7) independent of request success/failure.

**PlatformConfig** *(singleton, admin-editable)*
```
default_model_id, override_model_id (nullable), verifier_model_id
```

**OpenRouterApiKey**
```
id, label, encrypted_value, last_four, priority, status (enum: active | failed),
last_failure_at, last_failure_reason, last_tested_at, updated_by_admin_id, updated_at
```
Multiple keys are supported. Requests are attempted against the active key with the lowest `priority` value; on failure, the system falls back to the next active key in priority order without surfacing the failure to the end user (§13.3). A failing key is marked `status: failed` and flagged in the dashboard.

**ApiCredential**
```
id, service, encrypted_value, last_four, last_tested_at, last_test_result,
updated_by_admin_id, updated_at
```
Reserved for any non-OpenRouter service credentials; OpenRouter specifically uses `OpenRouterApiKey` above.

**AlertConfig**
```
id, channel (enum: email | webhook | discord_webhook), destination, event_types (array),
is_active
```

**AdminAuditLog**
```
id, admin_id, action, target (e.g. "tier:tier_2", "credential:openrouter"),
old_value, new_value, created_at
```
Every write from an `/api/admin/*` endpoint creates one row here.

## 11. Non-Functional Requirements

**Large inputs:**
- Inputs are capped at 10,000 characters (§4.1) — beyond that, reject upfront with `input_too_large` before calling OpenRouter.
- Within that ceiling, scale the request timeout with input size (base 30s, +10s per additional ~200 lines, capped around 90–120s).
- No chunking/sub-agent orchestration of large inputs across multiple model calls.

**Privacy:** guest-submitted source code is never persisted beyond serving the response. Registered users' code is persisted only as their own conversion history (§10).

**Usability:** language and model dropdowns remain filterable and keyboard-navigable regardless of list size.

## 12. Security Requirements
- Passwords hashed with bcrypt or argon2; never stored or logged in plaintext.
- Session tokens (JWT or equivalent) expire after a defined period (e.g. 7 days) with refresh; admin sessions expire sooner (e.g. 1 hour) given elevated privileges.
- All stored credentials (`ApiCredential`, `OpenRouterApiKey`, §10) are encrypted at rest, never logged, never returned unmasked by any endpoint.
- All user-submitted and converted code is HTML-escaped/sanitized before rendering in the syntax-highlighted viewer, to prevent XSS via pasted or generated content.
- `/api/auth/*` endpoints are rate-limited independently from conversion usage limits, to prevent credential brute-forcing.
- Every `/api/admin/*` endpoint re-checks the `admin` role on each request, not only at login, and is logged to `AdminAuditLog`.
- Destructive or high-impact admin actions (revoking/deleting an API key, setting/clearing the emergency model override, deleting a language) require an explicit confirmation step in the UI.

## 13. Admin Dashboard

A dedicated, role-gated (`role == admin`) area of the app. Every setting an admin needs to touch lives here — nothing is configured by editing files, env vars, or redeploying. Sidebar navigation; several sections have their own submenus.

### 13.1 Overview (landing page)
Conversions today/this month, error rate over the last 24h, active OpenRouter model in use, active emergency override (if any, as a persistent warning banner), any OpenRouter key currently in `failed` status, and the 5 most recent audit-log entries.

### 13.2 Models & AI
- **Default Model** — searchable dropdown (from `ModelRegistry`) to set the platform's normal default.
- **Emergency Override** — toggle: when on, every user is forced onto the selected model regardless of their personal setting, with a visible "Override active" state here and on Overview.
- **Verifier Model** — dropdown to set the Tier 2 background-verification model; saves and applies immediately.
- **Model Sync Status** — last successful sync timestamp, sync failure history, and a "Sync now" button.
- **Model list (admin view)** — each model's provider, free/paid pricing (§4.2, admin-only), and `requires_paid_tier` flag, with the ability to override the flag per model.

### 13.3 API & Credentials
- **OpenRouter API Keys** — list of all configured keys (masked, `label`, priority, status). **Add Key** (label + value, saved encrypted, appended to fallback order, tested on save). A key in `failed` status is flagged with a red exclamation icon and its failure reason. Admin can reorder priority, deactivate, delete, or re-test/reactivate a failed key. Failures never propagate to end users — the system silently falls back to the next active key (§8).
- **Tier 2 / Add-on API Keys** — list of all issued user-facing API keys with last-used timestamps and a **Revoke** action per key.

### 13.4 Tiers & Limits
Editable table, one row per tier: daily limit, monthly limit, feature flags (`allows_context_input`, `allows_verification`, `allows_api_access`). Inline edit, save per row. **Add Tier** button. Per-user add-on grants are managed under Users (§13.6), not here.

### 13.5 Language Registry
CRUD table: language label, id, file extension, syntax-highlighter alias. **Add Language** uses a guided form: Label → auto-suggested Language ID (editable) → File extension (with a live "converted.\<ext\>" preview) → Syntax-highlighter alias chosen from a searchable dropdown of supported grammars (not free text) → inline validation blocking duplicate IDs/extensions before save.

### 13.6 Users
Searchable/filterable table (by email, username, tier, status). Row actions: change tier, reset usage counters, suspend/reinstate account, grant/revoke add-ons (extra usage quantity, API access).

### 13.7 Analytics
Charts for conversions over time, breakdown by tier and language pair, error-rate by `error_code` (§8). **Model Usage** — table/chart of most-selected models (from `ModelSelectionLog`), by count and by tier, independent of OpenRouter call success/failure. Date-range filter, CSV export.

### 13.8 Alerts
Configure notification channel — email, generic webhook, or Discord webhook — and trigger events: at minimum OpenRouter 401/402 (§8), sustained 5xx/429 spike, model sync failure, an OpenRouter key entering `failed` status, and the emergency override being left on for an extended period.

### 13.9 Audit Log
Read-only, paginated view of `AdminAuditLog` — every change made elsewhere in the dashboard, who made it, and the before/after value.

## 14. Deployment

- Provide a `Dockerfile` for the application (multi-stage build: build stage + slim runtime stage).
- Provide a `docker-compose.yml` for local/dev orchestration, covering the app plus any required services (database, cache/queue if used).
- Container images must be built for both `linux/amd64` and `linux/arm64` using Docker Buildx multi-platform builds (e.g. `docker buildx build --platform linux/amd64,linux/arm64 -t <image>:<tag> --push .`).
- Secrets not stored in the database (e.g. initial admin bootstrap credentials, database connection string, JWT signing secret) are supplied via environment variables, never baked into the image.

## 15. Acceptance Criteria
- [ ] A guest can convert code 3 times in a day; the 4th attempt is blocked with `limit_exceeded` before any OpenRouter call, showing the registration modal.
- [ ] A registered free user can convert code 10 times in a day; on the 11th, the subscription/upgrade modal appears.
- [ ] Tier 1/Tier 2 users are blocked once either their daily or monthly limit (base + active add-ons) is hit, whichever comes first; both counters are visible in the UI.
- [ ] The usage counter is visible inline at all times; no upsell text or CTA appears until usage reaches 0, at which point the correct CTA button (Register / Upgrade) appears and links to the correct page.
- [ ] Source/target language dropdowns are search-filterable, driven entirely by the language registry, and seeded with the required language set including Bash and Batch.
- [ ] Every ordered language pair used in a conversion resolves to a distinct prompt template — no single generic template is reused across all pairs.
- [ ] The end-user model dropdown displays only model names; pricing, free/paid flag, and provider are never present in any end-user-facing response or UI element.
- [ ] Claude/ChatGPT/Gemini-family models are visible but grayed out and labeled "PRO" for free-tier accounts, show a subscribe-prompt tooltip on hover, and cannot be selected by non-paid accounts (client- and server-side).
- [ ] The model dropdown reflects the OpenRouter model cache and updates within 24 hours of any upstream model list change.
- [ ] An admin can set an emergency model override that immediately supersedes every user's personal model choice.
- [ ] An admin can change the Tier 2 verifier model and have it take effect in under 10 seconds, with no deploy required.
- [ ] For Tier 2 conversions, the user never sees the unverified conversion first — only a single final result, either the verified/revised version with its badge or the original if verification failed/timed out/made no changes.
- [ ] A `context` value submitted by a non-Tier-2 account is silently dropped from the request — it is never sent to OpenRouter and never produces an `invalid_input` error.
- [ ] Output is rendered syntax-highlighted, is copyable via one click, and is downloadable with the correct file extension for `target_language`.
- [ ] Conversion history is saved and retrievable for free/paid accounts, and is never created for guest sessions.
- [ ] Tier 2 API access works against `/api/v1/convert` with a scoped API key by default; a Tier 1 account can be granted API access via an `api_access` add-on and then also succeeds against the same endpoint.
- [ ] A Tier 2 account with an active `extra_conversions` add-on shows an increased effective daily/monthly limit reflecting the base tier plus the add-on.
- [ ] All error states in §8 are reproducible and return the documented `error_code` with a friendly (non-raw) message.
- [ ] Daily counters reset at the user's local midnight; monthly counters reset on the 1st of the calendar month, user's local time.
- [ ] An admin can add multiple OpenRouter API keys, and a request that fails against one key transparently falls back to the next active key with no failure shown to the end user; the failed key shows a red exclamation icon and failure reason in the dashboard.
- [ ] The admin dashboard displays a most-used-models table/chart sourced from `ModelSelectionLog`, populated at selection time regardless of downstream OpenRouter success/failure.
- [ ] Admin alerts can be configured to a Discord webhook in addition to email and generic webhook.
- [ ] The "Add Language" form guides the admin through label, ID, extension, and highlighter alias with live preview and duplicate validation, without requiring any code change.
- [ ] Every admin action listed in §9's admin endpoints produces a corresponding entry in the Audit Log with old and new values.
- [ ] Non-admin users cannot reach any `/api/admin/*` endpoint or dashboard route, even with a valid session.
- [ ] All user-submitted and converted code is escaped before rendering; pasting code containing HTML/script tags does not execute in the browser.
- [ ] A Dockerfile and docker-compose.yml exist and produce a working local deployment; images build successfully for both `linux/amd64` and `linux/arm64`.