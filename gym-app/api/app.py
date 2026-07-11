"""Flask API for the gym-app: manage users and convert weights.

Endpoints:
    GET  /health   -> service health check
    GET  /users    -> list all users
    POST /users    -> create a user {id, name, weight, unit}
    POST /convert  -> convert a weight {value, unit}
"""

import os
from decimal import Decimal, InvalidOperation

import psycopg2
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from conversions import kg_to_lb, lb_to_kg
from db import get_connection

app = Flask(__name__)

# The two units this API knows about. Anything else is a 400 error.
VALID_UNITS = {"kg", "lb"}

# No real person weighs this much - this catches obvious typos (like
# entering grams in a kg field) before they hit the database. Both
# limits represent the same cutoff (250 kg), just in each unit.
MAX_WEIGHT_KG = Decimal("250")
MAX_WEIGHT_LB = Decimal("551.16")


@app.errorhandler(psycopg2.OperationalError)
def handle_database_unavailable(error):
    # Runs when the database can't be reached - sends a clean error
    # instead of a scary raw connection failure.
    app.logger.error("Database connection failed: %s", error)
    return jsonify(error="database is unavailable"), 503


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    # Catches any other surprise error, so the client always gets JSON
    # back instead of Flask's default HTML error page.
    if isinstance(error, HTTPException):
        return error
    app.logger.exception("Unexpected error")
    return jsonify(error="internal server error"), 500


def _user_to_dict(row):
    # Turns a raw database row into the JSON shape we send back.
    return {
        "id": row[0],
        "name": row[1],
        "weight_kg": float(row[2]),
        "weight_lb": float(row[3]),
        "created_at": row[4].isoformat(),
    }


@app.get("/health")
def health():
    # Just says "I'm alive" - Docker uses this to check the container.
    return jsonify(status="ok"), 200


@app.get("/users")
def list_users():
    # Reads every user from the database and sends them back as JSON.
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, weight_kg, weight_lb, created_at "
                "FROM users ORDER BY id"
            )
            rows = cur.fetchall()
    finally:
        conn.close()
    return jsonify([_user_to_dict(row) for row in rows]), 200


@app.post("/users")
def create_user():
    # Adds a new user: checks the input, works out both units, and
    # saves the user in the database.
    data = request.get_json(silent=True) or {}
    user_id = data.get("id")
    name = data.get("name")
    weight = data.get("weight")
    unit = data.get("unit")

    # Check everything looks right before we go near the database.
    # Note: the client picks the id themselves, we don't generate it.
    if not isinstance(user_id, int):
        return jsonify(error="'id' is required and must be an integer"), 400
    if not name or not isinstance(name, str):
        return jsonify(error="'name' is required and must be a string"), 400
    if unit not in VALID_UNITS:
        return jsonify(error="'unit' must be 'kg' or 'lb'"), 400
    try:
        # Using Decimal (not float) here so the number stays exact
        # when we save it in the database.
        weight_value = Decimal(str(weight))
    except (InvalidOperation, TypeError):
        return jsonify(error="'weight' must be a number"), 400
    if weight_value <= 0:
        return jsonify(error="'weight' must be greater than zero"), 400
    if unit == "kg" and weight_value > MAX_WEIGHT_KG:
        return jsonify(error=f"'weight' must be at most {MAX_WEIGHT_KG} kg"), 400
    if unit == "lb" and weight_value > MAX_WEIGHT_LB:
        return jsonify(error=f"'weight' must be at most {MAX_WEIGHT_LB} lb"), 400

    # We always save both units, so figure out the one that's missing.
    if unit == "kg":
        weight_kg = weight_value
        weight_lb = Decimal(str(kg_to_lb(float(weight_value))))
    else:
        weight_lb = weight_value
        weight_kg = Decimal(str(lb_to_kg(float(weight_value))))

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            try:
                # RETURNING lets us get the saved row straight back,
                # including created_at, without asking the database
                # again in a second query.
                cur.execute(
                    """
                    INSERT INTO users (id, name, weight_kg, weight_lb)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, name, weight_kg, weight_lb, created_at
                    """,
                    (user_id, name, weight_kg, weight_lb),
                )
                row = cur.fetchone()
            except psycopg2.errors.UniqueViolation:
                # This id is already taken (it's the primary key).
                # Undo the failed insert and tell the client why,
                # instead of letting a confusing error bubble up.
                conn.rollback()
                return jsonify(error=f"user with id {user_id} already exists"), 409
        conn.commit()
    finally:
        conn.close()

    return jsonify(_user_to_dict(row)), 201


@app.post("/convert")
def convert_weight():
    # Converts a weight from kg to lb or lb to kg - no database here.
    data = request.get_json(silent=True) or {}
    value = data.get("value")
    unit = data.get("unit")

    if unit not in VALID_UNITS:
        return jsonify(error="'unit' must be 'kg' or 'lb'"), 400
    try:
        value = float(value)
    except (TypeError, ValueError):
        return jsonify(error="'value' must be a number"), 400

    # Whatever unit came in, we convert to the other one.
    if unit == "kg":
        converted_value = kg_to_lb(value)
        converted_unit = "lb"
    else:
        converted_value = lb_to_kg(value)
        converted_unit = "kg"

    return (
        jsonify(
            input_value=value,
            input_unit=unit,
            converted_value=round(converted_value, 2),
            converted_unit=converted_unit,
        ),
        200,
    )


if __name__ == "__main__":
    # 0.0.0.0 means "listen on every network interface", which is what
    # lets other containers (and our own machine) reach this one.
    app.run(host="0.0.0.0", port=int(os.environ.get("API_PORT", 5000)))
