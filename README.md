# Order API

> Order API is a secure, headless, API-first e-commerce back office platform designed to empower small-to-medium businesses (SMBs) with flexibility, data sovereignty, and analytics-oriented features.
>
> Built with FastAPI, PostgreSQL, and Redis, it provides full lifecycle management for orders — from authentication, product catalog, and secure idempotent payments to automated invoicing and real-time monitoring.
>
> Order API helps business teams regain control over their operations through role-based access control (RBAC), self-service exports (CSV/Excel), observability tools, and integrated dashboards for operational decision-making.

[![CI](https://github.com/bmakedika/order-api/actions/workflows/ci.yml/badge.svg)](https://github.com/bmakedika/order-api/actions)
![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Overview

Order API follows production-inspired API design principles:

- **API-first & headless:** Connect any frontend or external tool through RESTful endpoints.
- **Layered architecture:** Clear separation of concerns (API → Middleware → Services → Repository).
- **Role-Based Access Control (RBAC):** Secure and fine-grained permissions for users and administrators.
- **Built-in observability:** Prometheus metrics and Grafana dashboards included by default.
- **Business-oriented analytics:** KPI monitoring, CSV/Excel exports, and operational dashboards.
- **Developer experience & reliability:** Automated tests, CI/CD pipeline, and Dockerized environment.
- **Scalable backend foundation:** Designed for monitoring, maintainability, and future extensibility.

**Interactive docs:** `http://localhost:8000/docs`  
**Metrics:** `http://localhost:8000/metrics`  
**Grafana:** `http://localhost:3001`  
**Prometheus:** `http://localhost:9090`

---

## Documentation

Additional project documentation is available in the `/docs` directory:

- `order-api-project-documentation.pdf` — Product backlog, user stories, sprint planning, architecture and roadmap
- `grafana-dashboard.png` — Monitoring dashboard (Latency p95, RPS, error rate)
- `prometheus-metrics.png` — Prometheus metrics overview and HTTP request histogram
- `soutenance-order-api.pdf` — Final project presentation slides

---

## Project Highlights

- Headless e-commerce backend
- Secure RBAC authorization model
- Observability with Prometheus & Grafana
- Dockerized architecture
- Monitoring-oriented KPIs
- Agile backlog & sprint planning
- Production-inspired API design

---

## Features

### Authentication & Security

- JWT Bearer — access token + refresh token with rotation
- Revoked token blacklist using Redis
- Role-based access control (`require_role()`) — user and admin
- Rate limiting by IP and route groups

### Product Catalog

- Full CRUD reserved for admins (POST / PATCH / DELETE)
- Public read-only access (GET) without authentication
- Pagination, filters, and sorting

### Orders

- Full lifecycle: draft → items → payment → delivery
- Filtering by authenticated user — users can only see their own orders
- Status updates restricted to admins

### Payments

- Idempotent payments via `Idempotency-Key` header (Redis cache 24h)
- Automatic invoicing on each successful payment
- Guaranteed no double charging

### Observability

- `/metrics` endpoint exposed for Prometheus
- HTTP metrics: `http_requests_total`, `http_request_duration_seconds`
- Grafana dashboard auto-provisioned at startup: p95 latency, RPS, error rate

### Quality & CI

- 25 pytest tests (auth, orders, products, invoices, RBAC)
- In-memory SQLite base for tests — full isolation
- GitHub Actions — CI pipeline on every push

---

## Tech Stack

| Technology         | Role                | Why this choice                                                       |
| ------------------ | ------------------- | --------------------------------------------------------------------- |
| **FastAPI**        | REST API framework  | Async performance, native Pydantic validation, auto-generated Swagger |
| **PostgreSQL 15**  | Relational database | Reliability, ACID transactions, native UUID support                   |
| **SQLAlchemy 2**   | ORM                 | Database abstraction, Repository pattern implementation               |
| **Alembic**        | Schema migrations   | Database versioning and rollback support                              |
| **Redis 7**        | Multi-purpose cache | Payment idempotency, JWT blacklist, rate limiting                     |
| **Prometheus**     | Metrics collection  | Real-time metrics scraping and monitoring                             |
| **Grafana 11**     | Dashboards          | KPI visualization and observability dashboards                        |
| **Docker Compose** | Local orchestration | Reproducible environments with one command                            |
| **pytest**         | Automated tests     | Isolated fixtures and API reliability                                 |
| **GitHub Actions** | CI/CD               | Automated pipeline on every push                                      |

---

## Architecture

```text
Client / Frontend
        │
        ▼
 ┌─────────────────────┐
 │     FastAPI API     │
 ├─────────────────────┤
 │ Routes & Middleware │
 │ Authentication JWT  │
 │ RBAC Authorization  │
 │ Rate Limiting       │
 └─────────────────────┘
        │
        ▼
 ┌─────────────────────┐
 │  Service Layer      │
 │ Business Logic      │
 └─────────────────────┘
        │
        ▼
 ┌─────────────────────┐
 │ Repository Layer    │
 │ SQLAlchemy ORM      │
 └─────────────────────┘
        │
        ├──────────────► PostgreSQL
        │
        ├──────────────► Redis
        │                 • JWT Blacklist
        │                 • Idempotency
        │                 • Rate Limiting
        │
        └──────────────► Prometheus
                              │
                              ▼
                           Grafana
```

---

## Quickstart

### Prerequisites

- Python 3.11+
- Docker Desktop
- Git

### 1. Clone the repository

```bash
git clone https://github.com/bmakedika/order-api.git
cd order-api-python
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your own values
```

> **Tip:** Use a password without special characters for `POSTGRES_PASSWORD` and `DATABASE_URL` to avoid URL encoding issues.

### 5. Start the infrastructure

```bash
docker compose up -d
```

### 6. Apply migrations

```bash
alembic upgrade head
```

> If migrations fail (Docker volume with old credentials):
>
> ```bash
> docker compose down -v
> docker compose up -d
> alembic upgrade head
> ```
>
> ⚠️ This will delete all existing data.

### 7. Run the API

```bash
uvicorn app.main:app --reload --env-file .env
```

The API will be available at `http://localhost:8000/docs`

---

## Monitoring (optional)

```bash
docker compose -f docker-compose.monitoring.yml up -d
```

| Service     | URL                             | Credentials   |
| ----------- | ------------------------------- | ------------- |
| Grafana     | `http://localhost:3001`         | admin / admin |
| Prometheus  | `http://localhost:9090`         | —             |
| API metrics | `http://localhost:8000/metrics` | —             |

The **Order API — Overview** dashboard is auto-loaded in Grafana (provisioning).

---

## Tests

```bash
# Run all tests
pytest -v

# With coverage
pytest --cov=app --cov-report=term-missing
```

The test suite uses an in-memory SQLite base and an isolated Redis (flushdb before each test). No dependency on Docker infrastructure.

---

## Useful commands

```bash
# Restart the infrastructure
docker compose down && docker compose up -d

# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Roll back a migration
alembic downgrade -1

# Run tests in verbose mode
pytest -v

# Check linting
ruff check app/
```

---

## Roadmap

| Timeline       | Features                                                                          |
| -------------- | --------------------------------------------------------------------------------- |
| **Short term** | Exports CSV/Excel · Grafana business dashboards · Automated KPI script            |
| **Mid term**   | Cloud deployment · Payment integration · Enhanced API documentation               |
| **Long term**  | Advanced analytics dashboards · Multi-tenant architecture · Open source evolution |

---

## License

MIT — see [LICENSE](LICENSE)

---

_Academic project — Pre-Master Digital · Bienvenu MAKEDIKA · 2026_  
_[github.com/bmakedika/order-api](https://github.com/bmakedika/order-api)_
