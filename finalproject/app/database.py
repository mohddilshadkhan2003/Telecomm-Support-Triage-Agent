import uuid
from datetime import datetime
from typing import List

from .models import TicketResponse


class TicketDatabase:
    def __init__(self):
        self.tickets: List[TicketResponse] = []

    def add_ticket(self, customer_id: str, customer_name: str, query_text: str, triage_data: dict) -> TicketResponse:
        now = datetime.now()
        ticket = TicketResponse(
            ticket_id=f"TKT-{uuid.uuid4().hex[:8].upper()}",
            customer_id=customer_id,
            customer_name=customer_name,
            query_text=query_text.strip(),
            category=triage_data["category"],
            priority=triage_data["priority"],
            priority_score=triage_data["priority_score"],
            automated_response=triage_data["automated_response"],
            status="open",
            created_at=now,
            updated_at=now,
        )
        self.tickets.append(ticket)
        return ticket

    def get_all_tickets_sorted(self) -> List[TicketResponse]:
        return sorted(self.tickets, key=lambda x: (-x.priority_score, x.created_at))

    def get_dashboard_summary(self) -> dict:
        tickets = self.get_all_tickets_sorted()
        return {
            "total_tickets": len(tickets),
            "open_tickets": sum(1 for ticket in tickets if ticket.status == "open"),
            "critical_tickets": sum(1 for ticket in tickets if ticket.priority == "critical"),
            "high_tickets": sum(1 for ticket in tickets if ticket.priority == "high"),
            "medium_tickets": sum(1 for ticket in tickets if ticket.priority == "medium"),
            "low_tickets": sum(1 for ticket in tickets if ticket.priority == "low"),
        }

    def get_ticket_by_id(self, ticket_id: str) -> TicketResponse | None:
        for ticket in self.tickets:
            if ticket.ticket_id == ticket_id:
                return ticket
        return None

    def update_ticket_status(self, ticket_id: str, status: str) -> TicketResponse | None:
        ticket = self.get_ticket_by_id(ticket_id)
        if ticket is None:
            return None
        ticket.status = status
        ticket.updated_at = datetime.now()
        return ticket


db = TicketDatabase()
