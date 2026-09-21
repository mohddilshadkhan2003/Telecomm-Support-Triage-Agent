from typing import Annotated

from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .auth import ADMIN_USERNAME, TOKEN_MINUTES, authenticate, create_access_token, current_user, require_admin
from .database import db
from .models import DashboardResponse, LoginRequest, QueryRequest, TicketResponse, TokenResponse
from .triage_engine import TriageEngine

app = FastAPI(title="Telecom Support Triage Agent", description="Secure telecom support triage and operations platform.", version="3.0.0")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
engine = TriageEngine()


@app.get("/", summary="Service overview")
async def root():
    return {"service": "Telecom Support Triage Agent", "status": "online", "version": "3.0.0", "documentation_url": "/docs", "dashboard_url": "/dashboard"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Telecom Support Triage Agent", "database": str(db.db_path)}


@app.post("/auth/token", response_model=TokenResponse, summary="Create an admin access token")
async def login(form: Annotated[LoginRequest, Depends()]):
    role = authenticate(form.username, form.password)
    if role is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return TokenResponse(access_token=create_access_token(form.username, role), expires_in_minutes=TOKEN_MINUTES)


@app.post("/submit_query", response_model=TicketResponse, status_code=201)
async def submit_query(request: QueryRequest):
    triage = engine.analyze_query(request.query_text)
    return db.add_ticket(request.customer_id, request.customer_name, request.query_text, triage)


@app.get("/agent_dashboard", response_model=DashboardResponse)
async def get_triage_queue(user: Annotated[dict, Depends(current_user)]):
    return {"summary": db.get_dashboard_summary(), "tickets": db.get_all_tickets_sorted()}


@app.get("/analytics")
async def analytics(user: Annotated[dict, Depends(current_user)]):
    return db.analytics()


@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: str, user: Annotated[dict, Depends(current_user)]):
    ticket = db.get_ticket_by_id(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@app.patch("/tickets/{ticket_id}/status", response_model=TicketResponse)
async def update_ticket_status(ticket_id: str, status_value: str, user: Annotated[dict, Depends(current_user)]):
    try:
        ticket = db.update_ticket_status(ticket_id, status_value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@app.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
async def dashboard(request: Request):
    return HTMLResponse((request.app.state.dashboard_html if hasattr(request.app.state, "dashboard_html") else open("app/static/dashboard.html", encoding="utf-8").read()))
