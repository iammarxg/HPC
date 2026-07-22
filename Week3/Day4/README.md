# Code Converter

A web application that converts source code from one programming language to another using an LLM backend (via [OpenRouter](https://openrouter.ai)). Supports guest usage, free accounts, and paid tiers with daily and monthly usage limits, an optional AI-verification pass on conversions, and a full admin dashboard for runtime configuration.

## Features

- Paste code, pick a source and target language, convert — no account required
- Searchable source/target language dropdowns, seeded with 20 popular languages including Bash and Batch
- Guest, free, and two paid tiers, each with daily and monthly conversion limits
- Purchasable usage add-ons (extra conversions for Tier 2, API access for Tier 1)
- Syntax-highlighted, copyable, and downloadable output (correct file extension per language)
- Conversion history for registered accounts
- Tier 2: optional context field for the model, plus a background AI-verification pass that reviews the conversion before showing it
- Tier 2 programmatic API access
- Admin dashboard: model configuration, multiple OpenRouter API keys with automatic failover, tier/limit management, language registry, usage analytics, alerting (email, webhook, Discord), and a full audit log — no config files or redeploys required for day-to-day operation

## Documentation

| File | Purpose |
|---|---|
| [`spec.md`](../Day3/spec.md) | Full functional, API, data-model, security, and deployment specification. Source of truth for behavior. |
| [`system-prompt.md`](./system-prompt.md) | Guidance for AI coding assistants continuing this project. |

Read `spec.md` before making functional changes — it is the authoritative reference for this project's behavior.

## Tech Stack

| Layer | Choice |
|---|---|
| Language | TypeScript (frontend & backend) |
| Frontend | Next.js (React) — public conversion UI, Settings, and the admin dashboard |
| Backend | Node.js — Next.js API routes, or a separate Express/Fastify service |
| Database | PostgreSQL |
| ORM | Prisma or Drizzle |
| Background jobs | BullMQ + Redis (or equivalent cron-triggered worker) — powers the 24h OpenRouter model sync (§4.2) and the Tier 2 verification pass (§6.9) |
| Syntax highlighting | [Shiki](https://shiki.style) |

A single TypeScript codebase keeps the frontend, backend, and admin dashboard in sync with the API contract and data model in `spec.md`, and Shiki (the recommended highlighter, §5) is JS-native with no cross-language bridge required.

## Getting Started

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/)

### Run locally
```bash
docker compose up --build
```
This starts the application and its supporting services as defined in `docker-compose.yml`. See `spec.md` §14 for deployment requirements.

### Environment Variables
Bootstrap-level secrets (not managed via the admin dashboard) are supplied through environment variables — for example, the database connection string and the session/JWT signing secret. The OpenRouter API key itself is configured **after** startup, from the admin dashboard, and supports multiple keys with automatic failover (`spec.md` §13.3).

| Variable | Description |
|---|---|
| `DATABASE_URL` | Connection string for the application database |
| `JWT_SECRET` | Signing secret for session tokens |
| `ADMIN_BOOTSTRAP_EMAIL` | Initial admin account email, created on first run |
| `ADMIN_BOOTSTRAP_PASSWORD` | Initial admin account password, created on first run |

*(Adjust this table to match the actual implementation as it's built.)*

## Admin Dashboard

Available to accounts with the `admin` role. Covers model defaults and emergency overrides, OpenRouter API key management (multiple keys, automatic fallback on failure), subscription tier and limit configuration, the language registry, user management, usage analytics, and alert configuration. See `spec.md` §13 for the full feature map.

## Multi-Architecture Builds

Container images are built for both `linux/amd64` and `linux/arm64`:
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t <image>:<tag> --push .
```

## Contributing

This project follows the behavior defined in `spec.md`. Changes that alter user-facing behavior, limits, or the data model should be reflected there first.
