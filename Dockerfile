# Telecom Support Triage Agent

A production-grade telecom support triage platform built with FastAPI to classify customer issues, rank their urgency, and streamline support operations for telecom teams.

## Overview

This project helps support teams handle a high volume of customer queries by automatically identifying the likely issue category, assigning a priority level, generating a useful response, and storing the issue as a ticket for resolution.

## Why it matters

In telecom operations, delays in issue triage can negatively affect customer experience and service continuity. This app provides a practical first layer of automation to reduce manual sorting, speed response handling, and improve visibility into critical cases.

## Core features

- Query classification for network, billing, device, and service issues
- Priority scoring using rule-based matching
- Ticket creation and retrieval
- Queue summary dashboard
- SQLite-backed persistence
- Optional Docker deployment
- Swagger API documentation

## Quick start

```bash
cd finalproject
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

Then open:

- http://localhost:8000/docs
- http://localhost:8000/redoc

## Docker deployment

```bash
docker-compose up --build
```

## API overview

- POST /submit_query — create a triaged support ticket
- GET /agent_dashboard — fetch queue summary and tickets
- GET /tickets/{ticket_id} — retrieve a specific ticket
- PATCH /tickets/{ticket_id}/status — update the ticket state
- GET /health — health check

## Repository structure

```text
.
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── README.md
├── finalproject/
│   ├── app/
│   ├── config/
│   ├── data/
│   ├── tests/
│   ├── requirements.txt
│   ├── run.py
│   └── README.md
├── TELECOMM LLD.pdf
├── TELECOMM Project HLD.pdf
├── Telecomm Support Triage Report.pdf
└── .gitignore
```

## Testing

```bash
cd finalproject
pytest -q
```

## Summary

The project now represents a more professional and operationally meaningful telecom triage system, with improved structure, persistence, and deployment readiness.
