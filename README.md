# Order API

> Order API is a secure, headless, API-first e-commerce back office platform designed to empower small-to-medium businesses (SMBs) with maximum flexibility, data sovereignty, and future-ready analytics features.
>
> Built with FastAPI, PostgreSQL, and Redis, it offers full lifecycle management for orders — from authentication, product catalog, and secure idempotent payments to automated invoicing and real-time monitoring.
>
> Order API puts control back in the hands of business teams by providing robust role-based access (RBAC), self-service data exports (CSV/Excel), and integrated dashboards for real-time decision-making — all in a scalable, open architecture.

[![CI](https://github.com/bmakedika/order-api/actions/workflows/tests.yml/badge.svg)](https://github.com/bmakedika/order-api/actions)
![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Overview

Order API is designed with production-grade API principles:

- **API-first & headless:** Seamlessly connect any frontend or tool, benefit from RESTful, well-documented endpoints.
- **Layered architecture:** (API → Middleware → Services → Repository) for clear separation of concerns and maintainability.
- **Role-Based Access Control (RBAC):** Fine-grained, secure permissions for users and admins.
- **Built-in observability:** Exported Prometheus metrics and ready-to-use Grafana dashboards.
- **Business-centric analytics:** Automated reporting, KPI calculation, data exports (CSV/Excel) and support for operational dashboards (see roadmap).
- **Developer experience & reliability:** 25+ automated tests, in-memory test stack, and CI on every push.
- **Ready for scaling and real-time monitoring.**

**Interactive docs:** `http://localhost:8000/docs`  
**Metrics:** `http://localhost:8000/metrics`  
**Grafana:** `http://localhost:3001`  
**Prometheus:** `http://localhost:9090`

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

## Tech stack

| Technology         | Role                | Why this choice                                                       |
| ------------------ | ------------------- | --------------------------------------------------------------------- |
| **FastAPI**        | REST API framework  | Async performance, native Pydantic validation, auto-generated Swagger |
| **PostgreSQL 15**  | Relational database | Reliability, ACID transactions, native UUID support                   |
| **SQLAlchemy 2**   | ORM                 | Database abstraction, easy Repository pattern                         |
| **Alembic**        | Schema migrations   | Versioning of DB changes, possible rollback                           |
| **Redis 7**        | Multi-purpose cache | Idempotency for payment, JWT blacklist, rate limiting                 |
| **Prometheus**     | Metrics collection  | Industry standard, scrapes every 5s                                   |
| **Grafana 11**     | Dashboards          | Automatic provisioning via JSON files                                 |
| **Docker Compose** | Local orchestration | Environment reproducibility with one command                          |
| **pytest**         | Automated tests     | Isolated fixtures, strict asyncio mode                                |
| **GitHub Actions** | CI/CD               | Auto pipeline on every push to `main`                                 |

---

## Architecture

```
order-api-python/
├── app/
│   ├── api/                  # REST endpoints (auth, products, orders, invoices, users)
│   ├── core/
│   │   ├── auth.py           # JWT, require_role(), backward-compatible aliases
│   │   ├── config.py         # Environment variables (pydantic-settings)
│   │   ├── database.py       # SQLAlchemy engine, SessionLocal
│   │   ├── redis_client.py   # Shared Redis client
│   │   ├── token_blacklist.py
│   │   ├── metrics/
│   │   │   └── prometheus.py # Middleware + /metrics endpoint
│   │   └── middlewares/
│   │       ├── audit.py      # CSV log for each request
│   │       ├── cors.py       # CORS middleware
│   │       └── rate_limit.py # IP-based rate limiting
│   ├── models/               # SQLAlchemy models
│   ├── repos/                # Repository layer — db queries
│   ├── schemas/              # Pydantic schemas (request / response)
│   └── services/             # Business logic
├── monitoring/
│   ├── prometheus.yml        # Prometheus scrape config
│   └── grafana/
│       ├── provisioning/     # Datasource + dashboard provider
│       └── dashboards/       # Order API dashboard (JSON)
├── tests/                    # Pytest tests suite
├── docker-compose.yml        # PostgreSQL + Redis
├── docker-compose.monitoring.yml  # Prometheus + Grafana
└── alembic/                  # Schema migrations
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

## Endpoints

### Authentication

| Method | Endpoint         | Description          | Auth           |
| ------ | ---------------- | -------------------- | -------------- |
| POST   | `/auth/register` | Create an account    | —              |
| POST   | `/auth/login`    | Obtain JWT tokens    | —              |
| POST   | `/auth/refresh`  | Refresh access token | Cookie refresh |
| POST   | `/auth/logout`   | Revoke tokens        | Bearer         |

### Products

| Method | Endpoint         | Description      | Auth  |
| ------ | ---------------- | ---------------- | ----- |
| GET    | `/products`      | List products    | —     |
| GET    | `/products/{id}` | Product details  | —     |
| POST   | `/products`      | Create a product | admin |
| PATCH  | `/products/{id}` | Update a product | admin |
| DELETE | `/products/{id}` | Delete a product | admin |

### Orders

| Method | Endpoint                       | Description             | Auth         |
| ------ | ------------------------------ | ----------------------- | ------------ |
| POST   | `/orders`                      | Create an order (draft) | user         |
| GET    | `/orders/{id}`                 | Order details           | user (owner) |
| POST   | `/orders/{id}/items`           | Add an item             | user         |
| DELETE | `/orders/{id}/items/{item_id}` | Remove an item          | user         |
| POST   | `/orders/{id}/pay`             | Pay (idempotent)        | user         |
| PATCH  | `/orders/{id}/status`          | Update order status     | admin        |

### Invoices

| Method | Endpoint                | Description           | Auth         |
| ------ | ----------------------- | --------------------- | ------------ |
| GET    | `/invoices/{id}`        | Invoice details       | user (owner) |
| GET    | `/orders/{id}/invoices` | Invoices for an order | user (owner) |

### User

| Method | Endpoint    | Description                       | Auth |
| ------ | ----------- | --------------------------------- | ---- |
| GET    | `/users/me` | Profile of the authenticated user | user |

---

## Authentication — curl examples

```bash
# 1. Create an account
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "secret123"}'

# 2. Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "secret123"}'

# 3. Use the token
curl http://localhost:8000/orders \
  -H "Authorization: Bearer <access_token>"
```

---

## Idempotent Payment — curl example

```bash
curl -X POST http://localhost:8000/orders/{id}/pay \
  -H "Authorization: Bearer <access_token>" \
  -H "Idempotency-Key: order-001-attempt-1"
```

Calling `/pay` multiple times with the same key always returns the same response without double charging.

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
| **Short term** | Exports CSV/Excel (admin) · Grafana business dashboards · Automated KPI script    |
| **Mid term**   | Cloud deployment · Payment integration · Enhanced API docs                        |
| **Long term**  | Advanced business analytics dashboards and reporting · Multi-tenant · Open source |

---

## License

MIT — see [LICENSE](LICENSE)

---

_Academic project — Pre-Master Digital · Bienvenu MAKEDIKA · 2026_  
_[github.com/bmakedika/order-api](https://github.com/bmakedika/order-api)_
