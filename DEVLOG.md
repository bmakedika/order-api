# DEVLOG — Order API

Technical journal for the Order API project.  
Documents architecture decisions, problems encountered, and lessons learned.

---

## Sprint 1 — Initial Design

**Goal:** Build a headless e-commerce back office using FastAPI, PostgreSQL, and Redis.

**Stack chosen:**
- FastAPI for async performance and automatic Swagger documentation generation
- PostgreSQL for reliability, ACID transactions, and native UUID support
- SQLAlchemy 2 as ORM with the Repository pattern to separate SQL queries from business logic
- Redis for payment idempotency, JWT blacklisting, and rate limiting
- Alembic for database schema versioning and migrations

**Layered architecture adopted:**
```
Endpoint → Service → Repository → Database
```
Each layer has a single responsibility. The Repository isolates SQL queries: if the database engine changes tomorrow, only the Repository is affected.

**UUID decision:**
All primary keys are UUIDs generated on the application side (Python), not auto-incremented integers. This allows IDs to be generated without querying the database — essential for payment idempotency.

---

## Sprint 2 — Major Refactoring: Separating Customers from Users

### Problem identified

The initial model conflated two distinct entities into a single `customer_id: String` column on the `orders` table. This column was a free-form identifier with no referential integrity — not linked to any table. Any technical reviewer would have flagged this immediately as an integrity flaw.

### Architecture decision

Clear separation into two entities:

| Entity | Role | Table |
|---|---|---|
| `User` | E-commerce team member (staff) | `users` |
| `Customer` | External buyer | `customers` |

`orders.customer_id` becomes a proper `UUID FK → customers.id`.  
`orders.user_id` remains nullable — an order can be placed directly by a customer without staff involvement.

### Most complex migration — step 2

Transforming `orders.customer_id` from `String` to `UUID FK` on an existing table required a 4-step strategy within a single Alembic migration:

1. Drop the old index on `customer_id` (String)
2. Drop the old String column
3. Add the new nullable UUID column
4. Create the FK constraint with an explicit name

FK constraints are named explicitly (`fk_orders_customer_id`) to make `downgrade()` deterministic — without a name, PostgreSQL generates a random identifier that cannot be reliably referenced for deletion.

This migration had a cascade effect across the entire project: models, Pydantic schemas, services, endpoints, and tests all had to be updated in sequence.

### Stock management

Two columns added to `products`:

```
stock_quantity    — physically available in warehouse
reserved_quantity — blocked by unpaid orders in progress
```

Real available stock is always `stock_quantity - reserved_quantity`.  
`stock_quantity` is only decremented upon confirmed payment. Before that, stock is reserved only. If a customer abandons their order, the reserved stock is released with no impact on physical inventory.

---

## Sprint 3 — Synchronous → Asynchronous Migration

### Why migrate to async

FastAPI is an async framework. Using a synchronous SQLAlchemy session (`Session`) in an async context blocks the main thread on every SQL query — cancelling all of FastAPI's performance benefits.

### Structural changes

| Before | After |
|---|---|
| `create_engine` | `create_async_engine` |
| `Session` | `AsyncSession` |
| `db.query(...).filter(...)` | `await db.execute(select(...).where(...))` |
| `db.commit()` | `await db.commit()` |
| sync functions | `async def` functions with `await` |

### Problem discovered: lazy loading forbidden in async

SQLAlchemy async forbids lazy loading by default. When FastAPI tried to serialize `order.items` after the session was closed, it raised:

```
MissingGreenlet: greenlet_spawn has not been called; can't call await_only() here
```

**Solution:** `lazy='selectin'` on all relationships. SQLAlchemy then loads relations with a separate `SELECT ... WHERE id IN (...)` query while the session is still open.

Rule to remember:
> In SQLAlchemy async, all relationships must declare `lazy='selectin'` or `lazy='joined'`. Default lazy loading is incompatible with async.

### Problem discovered: `db.add()` on tracked objects

`db.add()` is only for new objects not yet persisted. Calling `db.add()` on an object already in the database (and especially on a deleted object) raises an `InvalidRequestError`. Fix: `await db.commit()` + `await db.refresh()` are sufficient for existing objects.

### Missing dependency: greenlet

Python 3.14 no longer ships `greenlet` by default. SQLAlchemy async needs it to switch between sync/async contexts. Added explicitly to `requirements.txt`.

---

## Sprint 4 — Async Tests

### Test stack migration

| Before | After |
|---|---|
| `TestClient` (synchronous) | `AsyncClient` + `ASGITransport` (httpx) |
| `sqlite:///./test.db` | `sqlite+aiosqlite:///:memory:` |
| `create_engine` | `create_async_engine` with `StaticPool` |
| sync `pytest.fixture` | async `pytest_asyncio.fixture` |

`StaticPool` is required with in-memory SQLite: without it, each new connection creates a different empty database — tables created by `create_all` disappear on the next connection.

### customer_id fixture

Order tests require a real customer in the database (no more free-form string). A local fixture was created in `test_orders.py`:

```python
@pytest.fixture
async def customer_id(client_auth):
    response = await client_auth.post('/customers', json={...})
    return response.json()['id']
```

Local because it is specific to order tests — unlike `client` and `client_auth` fixtures in `conftest.py` which are global.

### CI issue — async URL

GitHub Actions CI was using `DATABASE_URL: sqlite:///./ci.db` (synchronous). `database.py` was updated to detect the driver and add the appropriate async prefix (`sqlite+aiosqlite://` or `postgresql+psycopg://`).

---

## Final Result

- **25/25 tests passing** locally and in CI
- Fully async stack from database to endpoints
- Complete referential integrity with named FK constraints
- Stock management with reservation and decrement on payment
- Invoice traceability (`created_by`, `validated_by`, `validated_at`)

---

## Identified improvements (future sprints)

- Product filters currently applied in Python memory → should be migrated to SQL for large catalogs
- Additional roles to implement: `manager`, `operator`, `accountant`, `viewer`
- `id_payment` on `invoices` has no local FK → Stripe integration to be planned
- `UUIDv7` (time-sorted) for better index performance at scale
