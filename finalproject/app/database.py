from __future__ import annotations

import os
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import List

from .models import TicketResponse


class TicketDatabase:
    def __init__(self, db_path: str | None = None):
        default_path = Path(__file__).resolve().parents[1] / "data" / "triage.db"
        self.db_path = Path(db_path or os.getenv("DATABASE_PATH", default_path))
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_db()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize_db(self):
        with self._connect() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT, ticket_id TEXT UNIQUE NOT NULL,
                customer_id TEXT NOT NULL, customer_name TEXT NOT NULL, query_text TEXT NOT NULL,
                category TEXT NOT NULL, priority TEXT NOT NULL, priority_score INTEGER NOT NULL,
                automated_response TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'open',
                created_at TEXT NOT NULL, updated_at TEXT NOT NULL)""")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tickets_priority ON tickets(priority_score DESC)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status)")

    @staticmethod
    def _ticket(row) -> TicketResponse:
        return TicketResponse(**{**dict(row), "created_at": datetime.fromisoformat(row["created_at"]), "updated_at": datetime.fromisoformat(row["updated_at"]), "id": None})

    def add_ticket(self, customer_id: str, customer_name: str, query_text: str, triage_data: dict) -> TicketResponse:
        now = datetime.now().isoformat()
        ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
        with self._connect() as conn:
            conn.execute("""INSERT INTO tickets(ticket_id,customer_id,customer_name,query_text,category,priority,priority_score,automated_response,status,created_at,updated_at)
                VALUES(?,?,?,?,?,?,?,?,?,?,?)""", (ticket_id, customer_id.strip(), customer_name.strip(), query_text.strip(), triage_data["category"], triage_data["priority"], triage_data["priority_score"], triage_data["automated_response"], "open", now, now))
        return self.get_ticket_by_id(ticket_id)

    def get_all_tickets_sorted(self) -> List[TicketResponse]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM tickets ORDER BY priority_score DESC, created_at ASC").fetchall()
        return [self._ticket(row) for row in rows]

    def get_dashboard_summary(self) -> dict:
        with self._connect() as conn:
            row = conn.execute("""SELECT COUNT(*) total_tickets,
                COALESCE(SUM(status='open'),0) open_tickets,
                COALESCE(SUM(priority='critical'),0) critical_tickets,
                COALESCE(SUM(priority='high'),0) high_tickets,
                COALESCE(SUM(priority='medium'),0) medium_tickets,
                COALESCE(SUM(priority='low'),0) low_tickets FROM tickets""").fetchone()
        return dict(row)

    def get_ticket_by_id(self, ticket_id: str) -> TicketResponse | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,)).fetchone()
        return self._ticket(row) if row else None

    def update_ticket_status(self, ticket_id: str, ticket_status: str) -> TicketResponse | None:
        if ticket_status not in {"open", "in_progress", "resolved", "closed"}:
            raise ValueError("Invalid ticket status")
        with self._connect() as conn:
            conn.execute("UPDATE tickets SET status=?, updated_at=? WHERE ticket_id=?", (ticket_status, datetime.now().isoformat(), ticket_id))
        return self.get_ticket_by_id(ticket_id)

    def analytics(self) -> dict:
        with self._connect() as conn:
            categories = [dict(row) for row in conn.execute("SELECT category, COUNT(*) count FROM tickets GROUP BY category ORDER BY count DESC")]
            priorities = [dict(row) for row in conn.execute("SELECT priority, COUNT(*) count FROM tickets GROUP BY priority ORDER BY count DESC")]
            statuses = [dict(row) for row in conn.execute("SELECT status, COUNT(*) count FROM tickets GROUP BY status ORDER BY count DESC")]
        return {"categories": categories, "priorities": priorities, "statuses": statuses}


db = TicketDatabase()
