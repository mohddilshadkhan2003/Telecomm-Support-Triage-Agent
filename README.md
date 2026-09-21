# Telecom Support Triage Agent

A secure, database-backed telecom support operations platform with automated triage, a live web dashboard, authentication, analytics, and containerized deployment.

## Product capabilities

| Capability | Included |
|---|---:|
| Rule-based query classification | Yes |
| Priority scoring and escalation | Yes |
| SQLite persistence | Yes |
| Authenticated agent dashboard | Yes |
| Admin JWT authentication | Yes |
| Queue and status management | Yes |
| Database-backed analytics | Yes |
| Docker production runtime | Yes |
| CRM integration boundary | Webhook-ready |

## Architecture

```text
Customer / CRM webhook
        |
        v
FastAPI service ── JWT authentication ── Agent dashboard
        |
        +── TriageEngine (config/settings.yaml)
        +── TicketDatabase (SQLite)
        +── Analytics API
        +── CRM integration boundary
```

## Run locally

```bash
cd finalproject
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ..
cp .env.example .env
# Set TRIAGE_SECRET_KEY and ADMIN_PASSWORD in .env
cd finalproject
python run.py
```

Open `/dashboard` for the web control center, `/docs` for the API explorer, and `/redoc` for reference documentation.

## Run with Docker

```bash
cp .env.example .env
# Set secure values in .env
docker compose up -d --build
docker compose logs -f telecom-triage
```

The container exposes port `8000` and persists SQLite data in the `triage-data` Docker volume.

## Authentication

The dashboard uses an administrator JWT. Configure credentials through environment variables:

- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `TRIAGE_SECRET_KEY`
- `TOKEN_EXPIRE_MINUTES`

Never commit `.env` or production secrets. The default values are development placeholders and must be changed before deployment.

Get a token through `POST /auth/token`, then send it as `Authorization: Bearer <token>` to protected endpoints.

## API surface

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `/health` | No | Container health check |
| POST | `/auth/token` | No | Issue an access token |
| POST | `/submit_query` | No | Create and triage a ticket |
| GET | `/agent_dashboard` | Yes | Queue and summary metrics |
| GET | `/analytics` | Yes | Category, priority, and status analytics |
| GET | `/tickets/{ticket_id}` | Yes | Retrieve a ticket |
| PATCH | `/tickets/{ticket_id}/status` | Yes | Update `open`, `in_progress`, `resolved`, or `closed` |

## CRM and ticketing integration

The service is intentionally integration-friendly: external CRM systems can submit tickets to `/submit_query`, and can consume the returned `ticket_id`, priority, category, and automated response. For a production connector, place a small adapter in `finalproject/app/integrations/` that maps CRM webhooks to `QueryRequest` and sends status changes back to the provider. Keep provider credentials in environment variables and make outbound calls asynchronous with retries and idempotency keys.

## Operations

```bash
make up       # build and start
make logs     # follow logs
make stop     # stop services
make backup   # export a SQLite SQL backup
```

For production, place a TLS reverse proxy in front of the service, restrict network access to `/docs`, rotate the JWT secret, use PostgreSQL for multi-instance deployments, and add centralized logs/metrics.

## Testing

```bash
cd finalproject
pytest -q
```

## Repository layout

```text
finalproject/app/       API, authentication, persistence, triage engine, dashboard assets
finalproject/config/    Configurable categories, priorities, and responses
finalproject/tests/     API regression tests
Dockerfile              Production container image
docker-compose.yml      Persistent local/production-style deployment
Makefile                Operational shortcuts
```
