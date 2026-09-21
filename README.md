# Telecom Support Triage Agent

A production-grade telecom support triage platform built with FastAPI to classify customer issues, rank priorities, and streamline support operations.

## Overview

This project helps telecom teams reduce manual triage effort by automatically analyzing incoming support queries, classifying them into meaningful categories, and identifying their urgency level. It can be used as a modern support queue foundation for internal operations or a prototype for a larger customer support platform.

## Key capabilities

- Automated support query categorization
- Urgency detection for critical and high-impact incidents
- Ticket generation with human-readable responses
- Support dashboard with queue summary metrics
- Persistent storage using SQLite
- Docker-ready deployment setup
- API documentation through FastAPI

## Tech stack

- Python 3.11+
- FastAPI
- Pydantic
- SQLite
- Uvicorn
- Pytest
- Docker and Docker Compose

## Project structure

```text
.
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
├── finalproject/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── triage_engine.py
│   ├── config/
│   │   └── settings.yaml
│   ├── data/
│   │   └── .gitkeep
│   ├── tests/
│   │   └── test_api.py
│   ├── requirements.txt
│   ├── run.py
│   └── README.md
├── TELECOMM LLD.pdf
├── TELECOMM Project HLD.pdf
├── Telecomm Support Triage Report.pdf
└── .gitignore
```

## Quick start

### Local development

```bash
cd finalproject
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

### Docker

```bash
docker-compose up --build
```

Then visit:

- http://localhost:8000
- http://localhost:8000/docs
- http://localhost:8000/redoc

## Configuration

The triage rules and responses are controlled in:

`finalproject/config/settings.yaml`

This file defines:

- category mappings
- priority keywords
- automated support responses

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | / | Service overview |
| GET | /health | Health status |
| POST | /submit_query | Submit triage request |
| GET | /agent_dashboard | View ticket queue and summary |
| GET | /tickets/{ticket_id} | Fetch one ticket |
| PATCH | /tickets/{ticket_id}/status | Update ticket status |

## Example request

```bash
curl -X POST "http://localhost:8000/submit_query" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST-12345",
    "customer_name": "John Doe",
    "query_text": "My internet is completely down and my business is losing money!"
  }'
```

## Example response

```json
{
  "ticket_id": "TKT-A1B2C3D4",
  "customer_id": "CUST-12345",
  "customer_name": "John Doe",
  "query_text": "My internet is completely down and my business is losing money!",
  "category": "network_issue",
  "priority": "critical",
  "priority_score": 100,
  "automated_response": "Your case has been escalated to the emergency support team. A specialist will contact you within 5 minutes.",
  "status": "open",
  "created_at": "2026-09-21T12:00:00",
  "updated_at": "2026-09-21T12:00:00"
}
```

## Testing

```bash
cd finalproject
pytest -q
```

## Production roadmap

This solution is designed to evolve into a stronger telecom operations platform with:

- SQLite/PostgreSQL persistence for enterprise workloads
- authentication and role-based access
- customer and agent dashboards
- CRM or ticketing system integrations
- analytics and SLA monitoring
- alerting and escalation workflows

## Summary

This repo is now structured as a more professional, maintainable, and deployable telecom triage service that models real operational support workflows while staying lightweight and developer-friendly.
