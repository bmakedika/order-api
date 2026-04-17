# Order API (FastAPI)

A production-like REST API built with **FastAPI**, **PostgreSQL**, and **Redis**.  
Designed as a portfolio project showcasing **clean architecture**, **JWT authentication**, and **idempotent payments**.

- Interactive docs: `http://127.0.0.1:8000/docs`
- OpenAPI schema: `http://127.0.0.1:8000/openapi.json`

---

## Features

- JWT Bearer authentication (admin/user roles)
- Products CRUD (admin) + list & detail (public)
- Orders lifecycle: create draft, add/remove items, pay
- Idempotent payments via `Idempotency-Key` (Redis-backed)
- Database migrations with Alembic
- Automated tests with pytest

---

## Tech Stack

- **FastAPI** — REST API framework
- **PostgreSQL** — persistent database
- **SQLAlchemy** — ORM
- **Alembic** — database migrations
- **Redis** — idempotency key storage
- **Docker / Docker Compose** — containerized services
- **pytest** — automated tests

---

## Project Structure

```text
app/
├── api/          # endpoints (products, orders, auth)
├── core/         # config, auth, security, database, redis
├── models/       # SQLAlchemy models
├── repos/        # database queries (repository pattern)
├── schemas/      # Pydantic schemas
├── services/     # business logic
└── storage/      # legacy fake DB (replaced by PostgreSQL)
```

---

## Getting Started (Local Dev)

### 1) Clone the repository

```bash
git clone https://github.com/bmakedika/order-api-python.git
cd order-api-python
```

### 2) Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/Mac
```

### 3) Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4) Configure environment variables

```bash
cp .env.example .env
# Edit .env with your values
```

Notes:

- **Tip:** Use a simple password without special characters (e.g. `secret`) in `POSTGRES_PASSWORD` and `DATABASE_URL` to avoid URL encoding issues.
- **Linux/WSL note:** If you run into connection issues, try replacing `localhost` with `127.0.0.1` in `DATABASE_URL`.
- If your password contains special characters (e.g. `@`), encode them in the URL (`@` → `%40`, `!` → `%21`, etc.).

### 5) Start infrastructure (PostgreSQL + Redis)

```bash
docker-compose up -d
```

### 6) Run database migrations

```bash
alembic upgrade head
```

If migrations fail due to a password mismatch, your Docker volume may contain old credentials. Reset volumes:

```bash
docker-compose down -v
docker-compose up -d
```

> ⚠️ This deletes all existing database data.

### 7) Start the API

```bash
uvicorn app.main:app --reload --env-file .env
```

Open: `http://127.0.0.1:8000/docs`

---

## Common Commands

Run tests:

```bash
pytest -v
```

(Re)start infrastructure:

```bash
docker-compose down
docker-compose up -d
```

---

## API Endpoints

### Auth

| Method | Endpoint      | Description   |
| ------ | ------------- | ------------- |
| POST   | `/auth/login` | Get JWT token |

### Products

| Method | Endpoint         | Description                               | Auth  |
| ------ | ---------------- | ----------------------------------------- | ----- |
| GET    | `/products`      | List products (pagination, filters, sort) | —     |
| GET    | `/products/{id}` | Get product by ID                         | —     |
| POST   | `/products`      | Create product                            | admin |
| PATCH  | `/products/{id}` | Update product                            | admin |
| DELETE | `/products/{id}` | Soft delete product                       | admin |

### Orders

| Method | Endpoint                       | Description            | Auth |
| ------ | ------------------------------ | ---------------------- | ---- |
| POST   | `/orders`                      | Create order (draft)   | user |
| GET    | `/orders/{id}`                 | Get order details      | user |
| POST   | `/orders/{id}/items`           | Add item to order      | user |
| DELETE | `/orders/{id}/items/{item_id}` | Remove item            | user |
| POST   | `/orders/{id}/pay`             | Pay order (idempotent) | user |

---

## Authentication

The API uses **JWT Bearer tokens**.

```bash
# 1) Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin-secret"}'

# 2) Use the token
curl http://localhost:8000/products \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Mock credentials:

| Username | Password     | Role  |
| -------- | ------------ | ----- |
| admin    | admin-secret | admin |
| user     | user-secret  | user  |

---

## Idempotent Payments

The `/pay` endpoint supports an `Idempotency-Key` header to prevent double charges.

```bash
curl -X POST http://localhost:8000/orders/{id}/pay \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Idempotency-Key: unique-key-per-attempt"
```

Calling `/pay` multiple times with the same key returns the same response without re-charging.

---

## License

MIT
