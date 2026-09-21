from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class QueryRequest(BaseModel):
    customer_id: str = Field(..., min_length=3, max_length=80)
    customer_name: str = Field(..., min_length=2, max_length=120)
    query_text: str = Field(..., min_length=5, max_length=4000)


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    ticket_id: str
    customer_id: str
    customer_name: str
    query_text: str
    category: str
    priority: str
    priority_score: int
    automated_response: str
    status: str = "open"
    created_at: datetime
    updated_at: datetime


class DashboardSummary(BaseModel):
    total_tickets: int
    open_tickets: int
    critical_tickets: int
    high_tickets: int
    medium_tickets: int
    low_tickets: int


class DashboardResponse(BaseModel):
    summary: DashboardSummary
    tickets: List[TicketResponse]
