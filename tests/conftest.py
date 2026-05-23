import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool
from app.main import app
from app.core.database import Base, get_db
from app.core.auth import require_admin, require_user
from app.core.redis_client import get_redis
from app.models.user import UserModel
from uuid import uuid4

SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///:memory:'

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def override_get_db():
    async with TestingSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


def override_require_admin():
    return {'sub': 'admin@example.com', 'role': 'admin'}


def override_require_user():
    return {'sub': 'user@example.com', 'role': 'user'}


@pytest_asyncio.fixture(scope='function')
async def client():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    get_redis().flushdb()
    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test'
    ) as ac:
        yield ac

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    app.dependency_overrides = {}


@pytest_asyncio.fixture(scope='function')
async def client_auth():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    get_redis().flushdb()

    async with TestingSessionLocal() as db:
        db.add(UserModel(
            id=uuid4(),
            username='testuser',
            email='user@example.com',
            hashed_password='fake',
            role='user',
            is_active=True,
        ))
        db.add(UserModel(
            id=uuid4(),
            username='adminuser',
            email='admin@example.com',
            hashed_password='fake',
            role='admin',
            is_active=True,
        ))
        await db.commit()

    app.dependency_overrides[get_db]            = override_get_db
    app.dependency_overrides[require_admin]     = override_require_admin
    app.dependency_overrides[require_user]      = override_require_user

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test'
    ) as ac:
        yield ac

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    app.dependency_overrides = {}