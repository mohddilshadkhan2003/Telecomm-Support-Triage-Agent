# Telecom Support Triage Agent

A FastAPI-based support triage system for telecom customer care teams. It classifies incoming customer messages into categories, ranks urgency, generates a response, and creates a support ticket for agents.

## Features
- Automatic query classification
- Priority scoring
- Support queue dashboard
- Ticket tracking and status updates
- Config-driven triage rules
- FastAPI Swagger documentation

## Tech stack
- Python 3.10+
- FastAPI
- Pydantic
- YAML-based configuration
- Uvicorn

## Repository structure
```text
finalproject/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── triage_engine.py
├── config/
│   └── settings.yaml
├── requirements.txt
├── run.py
├── README.md
└── tests/
    └── test_api.py
```

## Setup
```bash
cd finalproject
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

## API endpoints
- GET / — service overview
- GET /health — health check
- POST /submit_query — submit a support query
- GET /agent_dashboard — view triaged queue
- GET /tickets/{ticket_id} — fetch a ticket
- PATCH /tickets/{ticket_id}/status — update ticket status

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
