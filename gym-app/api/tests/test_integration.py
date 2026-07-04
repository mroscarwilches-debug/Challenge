"""Integration tests for full flow.

These use the real Flask app talking to a real Postgres database - no
faking anything. They walk through the same steps a real person
would: create a user, check it shows up in the list, and try to
create it again to see the database reject the duplicate.

You need the database container running first:

    cd gym-app
    docker-compose up -d db
"""
import psycopg2
import pytest

import app as app_module
from db import get_connection

# A weird, unlikely id so it won't clash with anything someone types
# in by hand while trying the API out.
TEST_USER_ID = 999_999_001


@pytest.fixture
def client():
    # Gives each test a way to call the API's endpoints directly.
    app_module.app.testing = True
    return app_module.app.test_client()


@pytest.fixture(autouse=True)
def _require_database():
    """Skip everything in this file if the database isn't running."""
    try:
        conn = get_connection()
        conn.close()
    except psycopg2.OperationalError:
        pytest.skip("database not reachable - run `docker-compose up -d db` first")


@pytest.fixture
def clean_test_user():
    """Delete our test user before the test starts and after it ends,
    so the test can run over and over without leftover data."""

    def _delete():
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id = %s", (TEST_USER_ID,))
            conn.commit()
        finally:
            conn.close()

    _delete()
    yield
    _delete()


def test_full_flow_create_list_and_reject_duplicate(client, clean_test_user):
    # Walks through the real flow: create a user, see it in the list,
    # then get blocked when trying to reuse the same id.
    # Step 1: create a user for real, through the API and into the
    # actual database.
    create_response = client.post(
        "/users",
        json={
            "id": TEST_USER_ID,
            "name": "Integration Test User",
            "weight": 100,
            "unit": "kg",
        },
    )
    assert create_response.status_code == 201
    created = create_response.get_json()
    assert created["id"] == TEST_USER_ID
    assert created["weight_kg"] == 100.0
    assert round(created["weight_lb"], 2) == 220.46

    # Step 2: that same user should now appear when we list everyone.
    list_response = client.get("/users")
    assert list_response.status_code == 200
    ids = [user["id"] for user in list_response.get_json()]
    assert TEST_USER_ID in ids

    # Step 3: trying to create the same id again should fail - and
    # this time it's the real database saying no, not a fake one.
    duplicate_response = client.post(
        "/users",
        json={"id": TEST_USER_ID, "name": "Duplicate", "weight": 50, "unit": "kg"},
    )
    assert duplicate_response.status_code == 409
