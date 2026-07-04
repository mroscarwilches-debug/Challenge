"""API endpoint tests.

Tests for the Flask endpoints. None of these touch a real database -
`@patch("app.get_connection")` swaps it for a fake one, so the tests
run fast and don't need Docker at all. For tests against a real,
running database, see test_integration.py.
"""
from datetime import datetime
from unittest.mock import MagicMock, patch

import psycopg2

import app as app_module


def make_client():
    # Gives us a fake browser that can call the endpoints directly,
    # no real server needed.
    app_module.app.testing = True
    return app_module.app.test_client()


def test_health():
    # Checks the health endpoint replies with a simple "ok" status.
    client = make_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_convert_kg_to_lb():
    # Checks converting kilograms to pounds gives the right number.
    client = make_client()
    response = client.post("/convert", json={"value": 10, "unit": "kg"})
    assert response.status_code == 200
    body = response.get_json()
    assert body["converted_unit"] == "lb"
    assert body["converted_value"] == 22.05


def test_convert_lb_to_kg():
    # Checks converting pounds to kilograms gives the right number.
    client = make_client()
    response = client.post("/convert", json={"value": 10, "unit": "lb"})
    assert response.status_code == 200
    body = response.get_json()
    assert body["converted_unit"] == "kg"
    assert body["converted_value"] == 4.54


def test_convert_invalid_unit():
    # Checks an unknown unit gets rejected with a 400 error.
    client = make_client()
    response = client.post("/convert", json={"value": 10, "unit": "stone"})
    assert response.status_code == 400


def test_convert_invalid_value():
    # Checks a non-numeric value gets rejected with a 400 error.
    client = make_client()
    response = client.post("/convert", json={"value": "abc", "unit": "kg"})
    assert response.status_code == 400


@patch("app.get_connection")
def test_list_users(mock_get_connection):
    # Set up a fake connection that hands back one fake user row,
    # shaped just like a real one would be.
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        (1, "Oscar", 75.0, 165.35, datetime(2026, 1, 1))
    ]
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_connection.return_value = mock_conn

    client = make_client()
    response = client.get("/users")

    assert response.status_code == 200
    body = response.get_json()
    assert body[0]["name"] == "Oscar"
    assert body[0]["weight_lb"] == 165.35


@patch("app.get_connection")
def test_create_user(mock_get_connection):
    # Pretend the insert worked and the database gave back this row.
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (
        7,
        "Oscar",
        75.0,
        165.35,
        datetime(2026, 1, 1),
    )
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_connection.return_value = mock_conn

    client = make_client()
    response = client.post(
        "/users", json={"id": 7, "name": "Oscar", "weight": 75, "unit": "kg"}
    )

    assert response.status_code == 201
    body = response.get_json()
    assert body["id"] == 7
    assert body["name"] == "Oscar"


def test_create_user_missing_id():
    # No fake database needed - this should fail validation before the
    # code even tries to talk to a database.
    client = make_client()
    response = client.post(
        "/users", json={"name": "Oscar", "weight": 75, "unit": "kg"}
    )
    assert response.status_code == 400


def test_create_user_missing_name():
    # Checks creating a user without a name gets rejected.
    client = make_client()
    response = client.post("/users", json={"id": 1, "weight": 75, "unit": "kg"})
    assert response.status_code == 400


@patch("app.get_connection")
def test_create_user_duplicate_id(mock_get_connection):
    # Pretend the database rejected this because the id is already
    # taken (that's what a primary key clash looks like).
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = psycopg2.errors.UniqueViolation()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_connection.return_value = mock_conn

    client = make_client()
    response = client.post(
        "/users", json={"id": 1, "name": "Oscar", "weight": 75, "unit": "kg"}
    )

    assert response.status_code == 409
