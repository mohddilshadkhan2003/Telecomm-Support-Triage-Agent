from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "Telecom Support Triage Agent"
    assert body["status"] == "online"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_submit_query_and_dashboard():
    response = client.post(
        "/submit_query",
        json={
            "customer_id": "CUST-12345",
            "customer_name": "John Doe",
            "query_text": "My internet is completely down and my business is losing money!",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["customer_id"] == "CUST-12345"
    assert data["customer_name"] == "John Doe"
    assert data["priority"] in {"critical", "high", "medium", "low"}
    assert data["status"] == "open"

    dashboard = client.get("/agent_dashboard")
    assert dashboard.status_code == 200
    dashboard_data = dashboard.json()
    assert dashboard_data["summary"]["total_tickets"] >= 1


def test_invalid_query_rejected():
    response = client.post(
        "/submit_query",
        json={
            "customer_id": "CUST-1",
            "customer_name": "Jane Doe",
            "query_text": "",
        },
    )
    assert response.status_code == 400
