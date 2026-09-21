# Telecom Support Triage Agent

A professional FastAPI-based telecom support triage platform designed to classify incoming customer queries, prioritize issues, and route them into an efficient support workflow.

## Overview

Telecom support teams often receive large volumes of customer messages spanning billing, connectivity, service requests, and device issues. This application helps automate the first layer of triage by:

- identifying the likely issue category,
- assigning business urgency based on keywords,
- generating an automated support response,
- storing tickets for human follow-up and team operations.

The result is a cleaner support queue, faster response times, and better visibility for service agents.

## Why this project matters

This solution helps telecom organizations reduce manual ticket sorting and improves operational efficiency by:

- shortening the time to first response,
- ensuring critical incidents are identified early,
- organizing support work by priority,
- creating a reusable triage workflow that can evolve into a larger customer support system.

## Architecture at a glance

```text
Customer Query
      |
      v
FastAPI API
      |
      +--> Triage Engine
      |       - category detection
      |       - priority analysis
      |       - automated response selection
      |
      +--> Ticket Database
              - stores ticket data
              - supports dashboard reporting
```

## Core features

- Automatic ticket categorization
- Priority scoring for critical and high-impact incidents
- Automated response generation
- Support queue dashboard
- Ticket status tracking
- Config-driven triage rules via YAML
- FastAPI Swagger and ReDoc documentation
- Clean, extensible Python service structure

## Tech stack

- Python 3.10+
- FastAPI
- Pydantic
- Uvicorn
- YAML configuration
- Pytest for verification

## Repository structure

```text
.
├── finalproject/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── triage_engine.py
│   ├── config/
│   │   └── settings.yaml
│   ├── tests/
│   │   └── test_api.py
│   ├── requirements.txt
│   ├── run.py
│   └── README.md
├── README.md
├── TELECOMM LLD.pdf
├── TELECOMM Project HLD.pdf
├── Telecomm Support Triage Report.pdf
└── .gitignore
```

## Quick start

```bash
cd finalproject
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

Once running, the service is available at:

- http://localhost:8000
- http://localhost:8000/docs
- http://localhost:8000/redoc

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | / | Service overview |
| GET | /health | Health check |
| POST | /submit_query | Submit a customer query for triage |
| GET | /agent_dashboard | View the priority queue |
| GET | /tickets/{ticket_id} | Fetch a specific ticket |
| PATCH | /tickets/{ticket_id}/status | Update ticket status |

## Example: submit a query

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

## Dashboard behavior

The dashboard returns a summary alongside the ticket list, including:

- total tickets
- open tickets
- critical ticket count
- high priority count
- medium priority count
- low priority count

This gives team leads a fast operational picture of current support pressure.

## Configuration

The triage behavior is driven by `finalproject/config/settings.yaml`. This allows you to adjust:

- keyword categories,
- priority rules,
- automated response messages.

This makes the system easy to customize for different telecom operations or brand requirements.

## Testing

```bash
cd finalproject
pytest -q
```

## Future enhancements

This project is already a strong foundation for further growth, including:

- SQLite or PostgreSQL persistence,
- authentication and role-based agent access,
- a frontend dashboard using React or Streamlit,
- analytics and SLA monitoring,
- integration with CRM and ticketing systems.

## License

This project is intended for educational and operational prototyping use. If you plan to deploy it in production, review your organization’s security, data handling, and compliance requirements first.

## Summary

The Telecom Support Triage Agent combines automated issue classification, prioritization, and ticketing into a compact and professional support workflow. It is designed to help telecom teams act faster, reduce manual routing effort, and make support operations more structured and efficient.


""" 
    },
    {
      "content": "# Telecom Support Triage Agent\n\nA production-style support triage API for telecom customer support teams.\n\n## Overview\n\nThis service accepts customer queries, identifies the likely support category, evaluates urgency, generates a response, and creates a ticket for resolution tracking. It is built with FastAPI and is designed to be quick to run, easy to extend, and useful in operational support environments.\n\n## Features\n\n- Query classification for network, billing, device, and service issues\n- Automatic priority scoring\n- Ticket creation and dashboard retrieval\n- Health and service status endpoints\n- YAML-driven configuration for triage rules\n- Swagger documentation\n\n## Project structure\n\n```text\nfinalproject/\n├── app/\n│   ├── __init__.py\n│   ├── database.py\n│   ├── main.py\n│   ├── models.py\n│   └── triage_engine.py\n├── config/\n│   └── settings.yaml\n├── tests/\n│   └── test_api.py\n├── requirements.txt\n├── run.py\n└── README.md\n```\n\n## Installation\n\n```bash\ncd finalproject\npython -m venv venv\nsource venv/bin/activate\npip install -r requirements.txt\npython run.py\n```\n\n## Usage\n\nOpen the API docs at:\n\n- http://localhost:8000/docs\n\nExample request:\n\n```bash\ncurl -X POST \"http://localhost:8000/submit_query\" \\\n  -H \"Content-Type: application/json\" \\\n  -d '{\n    \"customer_id\": \"CUST-12345\",\n    \"customer_name\": \"John Doe\",\n    \"query_text\": \"My internet is completely down and my business is losing money!\"\n  }'\n```\n\n## Testing\n\n```bash\npytest -q\n```\n\n## Notes\n\nThe logic is intentionally simple and configurable so it can be expanded for enterprise telecom operations, CRM integrations, and agent dashboards.\n"