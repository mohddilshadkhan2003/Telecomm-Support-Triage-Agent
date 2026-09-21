from typing import List

from fastapi import FastAPI, HTTPException, status

from .database import db
from .models import DashboardResponse, QueryRequest, TicketResponse
from .triage_engine import TriageEngine

app = FastAPI(
    title="Telecom Support Triage Agent",
    description="AI-powered telecom support triage workflow for routing customer issues and prioritizing queue handling.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

engine = TriageEngine()


@app.get("/", summary="Service overview")
async def root():
    return {
        "service": "Telecom Support Triage Agent",
        "status": "online",
        "version": "2.0.0",
        "documentation_url": "/docs",
        "health_url": "/health",
    }


@app.get("/health", summary="Health check")
async def health_check():
    return {
        "status": "healthy",
        "service": "Telecom Support Triage Agent",
    }


@app.post(
    "/submit_query",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a new customer query",
)
async def submit_query(request: QueryRequest):
    if not request.query_text.strip():
        raise HTTPException(status_code=400, detail="Query text cannot be empty.")

    if not request.customer_id.strip():
        raise HTTPException(status_code=400, detail="Customer ID cannot be empty.")

    triage_results = engine.analyze_query(request.query_text)
    ticket = db.add_ticket(
        customer_id=request.customer_id,
        customer_name=request.customer_name,
        query_text=request.query_text,
        triage_data=triage_results,
    )
    return ticket


@app.get("/agent_dashboard", response_model=DashboardResponse, summary="Get prioritized support queue")
async def get_triage_queue():
    tickets = db.get_all_tickets_sorted()
    summary = db.get_dashboard_summary()
    return {
        "summary": summary,
        "tickets": tickets,
    }


@app.get("/tickets/{ticket_id}", response_model=TicketResponse, summary="Get a ticket by ID")
async def get_ticket(ticket_id: str):
    ticket = db.get_ticket_by_id(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    return ticket


@app.patch("/tickets/{ticket_id}/status", response_model=TicketResponse, summary="Update ticket status")
async def update_ticket_status(ticket_id: str, status_value: str):
    ticket = db.update_ticket_status(ticket_id, status_value)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    return ticket
