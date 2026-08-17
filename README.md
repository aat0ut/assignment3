# Task API — Containerized with Postgres

A CRUD task API built with **FastAPI** and **PostgreSQL**, fully containerized with **Docker Compose**. This is the third storage swap for this project — in-memory (A1) → SQLite (A2) → containerized Postgres (this assignment) — with the API surface staying identical the whole way through.

## What this is

- FastAPI app exposing 5 CRUD endpoints for managing tasks
- PostgreSQL database running in its own container
- Both services started together with a single `docker compose up`
- Data persists across restarts via a named Docker volume
- Secrets (DB password, connection string) kept out of source control via `.env`

## Run it

Requires [Docker](https://www.docker.com/products/docker-desktop/) (or Podman) installed and running.

```bash
git clone https://github.com/aat0ut/assignment3
cp .env.example .env
docker compose up
```

The API will be available at **http://localhost:8000**.

To stop everything:
```bash
docker compose down
```

To stop everything **and** wipe stored data:
```bash
docker compose down -v
```

## Environment variables

Copy `.env.example` to `.env` before running. No values need to be changed for local use — the compose file overrides `DATABASE_URL` internally to point the API at the `db` service.

| Variable | Description |
|---|---|
| `DATABASE_URL` | Postgres connection string, e.g. `postgres://postgres:dev@localhost:5433/tasks` (used for running the API outside Docker, e.g. during local development) |

## Endpoints

| Method | Path | Description | Success | Errors |
|---|---|---|---|---|
| `GET` | `/tasks` | List all tasks | `200` | — |
| `GET` | `/tasks/{id}` | Get a single task by id | `200` | `404` if not found |
| `POST` | `/tasks/` | Create a new task | `201` | `400` if `title` is missing/empty |
| `PUT` | `/tasks/{id}` | Update a task's title/done status | `200` | `404` if not found |
| `DELETE` | `/tasks/{id}` | Delete a task | `204` | `404` if not found |

### Example request

```bash
curl -i http://localhost:8000/tasks/999
```

```
HTTP/1.1 404 Not Found
content-type: application/json

{"detail":"Task not found"}
```

## Data persistence

Tasks are stored in a `tasks` table in Postgres, created automatically on first run, and seeded with 3 example tasks only if the table is empty. The table lives in a named Docker volume (`taskdata`), so data survives `docker compose down` / `up` — it's only wiped with `docker compose down -v`.

## Notes

- The plain `postgres` image now defaults to Postgres 18, which changed its expected data directory layout and will fail to start against a volume created by an older version. This project pins `postgres:16` explicitly in both the one-off `docker run` command and `compose.yaml` to avoid that.
- Locally (outside Docker Compose), Postgres runs on host port `5433` instead of the default `5432`, to avoid clashing with a Postgres 17 install already running on this machine via the system service. Inside the Compose network, the API reaches the database at `db:5432` — the internal port is unaffected by the host-side remap.

## Tech stack

- Python 3.9 + FastAPI
- PostgreSQL 16
- `psycopg` (raw driver)
- Docker & Docker Compose
- `uv` for Python dependency management
