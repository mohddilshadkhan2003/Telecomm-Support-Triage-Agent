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


def test_submit_query_and_dashboard_without_auth_should_fail():
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
    assert dashboard.status_code == 401


def test_auth_token_and_dashboard_access():
    token = client.post(
        "/auth/token",
        json={"username": "admin", "password": "change-me"},
    )
    assert token.status_code == 200
    token_value = token.json()["access_token"]

    dashboard = client.get("/agent_dashboard", headers={"Authorization": f"Bearer {token_value}"})
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
    assert response.status_code == 422


def test_dashboard_html_served():
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "Telecom Triage Control Center" in response.text
