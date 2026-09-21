# Telecom Support Triage Agent

A production-style support triage API for telecom customer support teams.

## Overview

This service accepts customer queries, identifies the likely support category, evaluates urgency, generates a response, and creates a ticket for resolution tracking. It is built with FastAPI and is designed to be quick to run, easy to extend, and useful in operational support environments.

## Features

- Query classification for network, billing, device, and service issues
- Automatic priority scoring
- Ticket creation and dashboard retrieval
- Health and service status endpoints
- YAML-driven configuration for triage rules
- Swagger documentation

## Project structure

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
├── tests/
│   └── test_api.py
├── requirements.txt
├── run.py
└── README.md
```

## Installation

```bash
cd finalproject
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Usage

Open the API docs at:

- http://localhost:8000/docs

Example request:

```bash
curl -X POST "http://localhost:8000/submit_query" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST-12345",
    "customer_name": "John Doe",
    "query_text": "My internet is completely down and my business is losing money!"
  }'
```

## Testing

```bash
pytest -q
```

## Notes

The logic is intentionally simple and configurable so it can be expanded for enterprise telecom operations, CRM integrations, and agent dashboards.
