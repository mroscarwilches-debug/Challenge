# Gym App API

Flask service for managing gym users and converting weights between
kilograms and pounds.

## Endpoints

### GET /health
Health check. Returns `{"status": "ok"}`.

### GET /users
Returns all users.

```json
[
  {
    "id": 1,
    "name": "Oscar",
    "weight_kg": 75.0,
    "weight_lb": 165.35,
    "created_at": "2026-01-01T00:00:00"
  }
]
```

### POST /users
Creates a user. The `id` is assigned by the client and must be unique.

Request body:
```json
{"id": 1, "name": "Oscar", "weight": 75, "unit": "kg"}
```

- `unit` must be `"kg"` or `"lb"`.
- Returns `201` with the created user.
- Returns `400` if `id`, `name`, `weight`, or `unit` are missing/invalid.
- Returns `409` if a user with the same `id` already exists.
- Returns `503` if the database is unreachable.

### POST /convert
Converts a weight value.

Request body:
```json
{"value": 75, "unit": "kg"}
```

Response:
```json
{"input_value": 75.0, "input_unit": "kg", "converted_value": 165.35, "converted_unit": "lb"}
```

## Configuration

The service reads these environment variables (see `../.env`):

- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- `DB_HOST` (default `db`), `DB_PORT` (default `5432`)
- `API_PORT` (default `5000`)

## Error handling

- Bad input (missing/invalid fields) -> `400` with a JSON `error` message.
- Duplicate `id` on `POST /users` -> `409`.
- Database unreachable -> `503` instead of a raw connection traceback.
- Anything else unexpected -> `500` with a generic JSON message (the
  real error is logged server-side, not sent to the client).

## Health checks

Both containers in `docker-compose.yml` declare a `healthcheck`:

- `db` uses `pg_isready` to confirm Postgres accepts connections.
- `api` calls its own `GET /health` endpoint from inside the container.

The `api` service's `depends_on` waits for `db`'s healthcheck to pass
(`condition: service_healthy`), not just for the container to start.

## Testing

Matches the three testing requirements from the challenge:

- **Unit tests for weight conversion functions** - `tests/test_conversions.py`
- **API endpoint tests** - `tests/test_api_endpoints.py` (mocked database)
- **Integration tests for full flow** - `tests/test_integration.py` (real database)

```bash
pip install -r requirements-dev.txt

# Unit tests + API endpoint tests (no database needed)
pytest tests/test_conversions.py tests/test_api_endpoints.py

# Integration tests (needs the database container running)
docker-compose up -d db
pytest tests/test_integration.py

# Everything at once
pytest
```

## Notes: what was built and why

This section explains, in plain language, what was added in the
`feature/api-service` branch and why, so it's easy to follow later.

This phase adds the second layer of the gym app: a small web service
(API) that sits between the database and whatever will call it later
(a frontend, or just curl/Postman for now). It lives in `gym-app/api/`.

### The files, in plain words

- **`app.py`** - the actual web service. It defines three things you
  can call over HTTP:
  - `GET /health` - just says "I'm alive", useful to check the
    container is running.
  - `GET /users` - lists every user stored in the database.
  - `POST /users` - adds a new user. You send a JSON body with an
    `id`, `name`, `weight`, and `unit` (`"kg"` or `"lb"`), and it
    saves both the kg and lb values in the database.
  - `POST /convert` - just converts a number from kg to lb or lb to
    kg, without touching the database at all.

- **`conversions.py`** - the small math functions (`kg_to_lb`,
  `lb_to_kg`) used by the API. Kept separate from `app.py` so they're
  easy to test on their own, without needing a database or a running
  server.

- **`db.py`** - one function, `get_connection()`, that opens a
  connection to the PostgreSQL database using the same environment
  variables from `gym-app/.env` (user, password, db name, host, port).

- **`requirements.txt`** / **`requirements-dev.txt`** - the Python
  packages needed to run the API (Flask, psycopg2) and, separately,
  the extra package needed only for running tests (pytest).

- **`Dockerfile`** - instructions to package this service into its own
  container, the same way the database already has one.

- **`tests/test_conversions.py`** - checks the math functions give the
  right numbers.

- **`tests/test_api_endpoints.py`** - checks the API endpoints behave
  correctly (right status codes, right error messages) without needing
  a real database - it fakes ("mocks") the database connection.

- **`tests/test_integration.py`** - runs the same endpoints against a
  real, live database to confirm the full flow actually works end to
  end.

- **`docker-compose.yml`** - updated to add the new `api` service
  next to the existing `db` service, so both can eventually run
  together with `docker-compose up -d`.

### Important decision: how `id` works

Originally the plan was to auto-generate the `id` for each user.
That was changed on purpose: **the `id` is provided by whoever calls
the API**, not generated automatically. Because of that:

- If you try to create a user with an `id` that already exists, the
  API replies with `409 Conflict` instead of creating a duplicate or
  silently overwriting anything.

### What's still missing

- The frontend (simple web page) - next branch, `feature/frontend-ui`.
- Combining everything into one final `docker-compose.yml` run -
  planned for the `feature/docker-compose` branch.
