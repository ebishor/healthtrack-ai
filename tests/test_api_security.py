from fastapi.testclient import TestClient
from app.auth.user_store import _users
from app.main import app

import jwt
from app.auth.token import create_access_token
from app.core.config import JWT_SECRET_KEY

from unittest.mock import AsyncMock, patch

client = TestClient(app)


def test_health_endpoint_returns_ok():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_assessment_requires_authentication():
    response = client.post(
        "/api/assess",
        json={
            "patient_age": 35,
            "symptoms": "Fever and dry cough for two days",
        },
    )

    assert response.status_code == 401


def test_assessment_rejects_missing_symptoms():
    # Register a test user.
    register_response = client.post(
        "/api/auth/register",
        json={
            "username": "validationtester",
            "password": "TestPassword123!",
        },
    )

    assert register_response.status_code == 201

    # Log in to obtain an access token.
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": "validationtester",
            "password": "TestPassword123!",
        },
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Send an authenticated request with symptoms missing.
    response = client.post(
        "/api/assess",
        headers={"Authorization": f"Bearer {token}"},
        json={"patient_age": 35},
    )

    assert response.status_code == 422
def test_password_is_not_stored_in_plain_text():
    username = "passwordsecuritytester"
    password = "TestPassword123!"

    response = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 201
    assert _users[username]["password_hash"] != password
    assert "password" not in _users[username]


def test_login_rejects_incorrect_password():
    username = "loginsecuritytester"

    register_response = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "password": "CorrectPassword123!",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        data={
            "username": username,
            "password": "WrongPassword123!",
        },
    )

    assert login_response.status_code == 401

def test_assessment_rejects_unauthorized_role():
    token = create_access_token(
        username="unauthorizedtester",
        role="viewer",
    )

    response = client.post(
        "/api/assess",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "patient_age": 35,
            "symptoms": "Fever and dry cough for two days",
        },
    )

    assert response.status_code == 403

def test_assessment_handles_llm_failure():
    # Register a test user and obtain a token.
    username = "llmfailuretester"
    password = "TestPassword123!"

    register_response = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "password": password,
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Simulate an unavailable LLM service.
    with patch(
        "app.api.routes.generate_assessment",
        new_callable=AsyncMock,
    ) as mock_assessment:
        from app.services.llm_service import LLMServiceError

        mock_assessment.side_effect = LLMServiceError(
            "The AI assessment service is temporarily unavailable."
        )

        response = client.post(
            "/api/assess",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "patient_age": 35,
                "symptoms": "Fever and dry cough for two days",
            },
        )

    assert response.status_code == 502
    assert response.json() == {
        "detail": "The AI assessment service is temporarily unavailable."
    }

def test_request_id_is_returned_and_logged(caplog):
    import json
    import logging
    import uuid

    with caplog.at_level(logging.INFO):
        response = client.get("/api/health")

    assert response.status_code == 200

    request_id = response.headers.get("X-Request-ID")
    assert request_id is not None

    # Verify the request ID is a valid UUID.
    uuid.UUID(request_id)

    # Verify the structured log contains the same request ID.
    matching_records = [
        record
        for record in caplog.records
        if getattr(record, "event", None) == "request_completed"
        and getattr(record, "request_id", None) == request_id
    ]

    assert matching_records, "Request completion log was not found"

    # Verify the request ID is present in the formatted JSON log.
    log_entry = json.loads(
        __import__("app.core.logging_config", fromlist=["JsonFormatter"])
        .JsonFormatter()
        .format(matching_records[0])
    )

    assert log_entry["request_id"] == request_id
    assert log_entry["http_status"] == 200

def test_assessment_logs_do_not_contain_symptoms_or_credentials(caplog):
    import logging

    username = "privacytestuser"
    password = "PrivacyTestPassword123!"
    symptoms = "UniquePrivateSymptomPhrase98765"

    client.post(
        "/api/auth/register",
        json={"username": username, "password": password},
    )

    login_response = client.post(
        "/api/auth/login",
        data={"username": username, "password": password},
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    with caplog.at_level(logging.INFO):
        with patch(
            "app.api.routes.generate_assessment",
            new_callable=AsyncMock,
        ) as mock_assessment:
            from app.schemas.response import ClinicalAssessment

            mock_assessment.return_value = ClinicalAssessment(
                summary="Test summary",
                potential_diagnoses=[],
                further_evaluation=[],
                management_considerations=[],
                red_flags=[],
                disclaimer="Test disclaimer",
            )

            response = client.post(
                "/api/assess",
                headers={"Authorization": f"Bearer {token}"},
                json={"patient_age": 35, "symptoms": symptoms},
            )

    assert response.status_code == 200

    captured_logs = "\n".join(
        record.getMessage() for record in caplog.records
    )

    assert symptoms not in captured_logs
    assert password not in captured_logs
    assert token not in captured_logs