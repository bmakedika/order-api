from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
from pathlib import Path
from app.core.config import DATABASE_URL

load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / '.env')

if DATABASE_URL.startswith('postgresql://'):
    async_url = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://')
elif DATABASE_URL.startswith('sqlite://'):
    async_url = DATABASE_URL.replace('sqlite://', 'sqlite+aiosqlite://')
else:
    async_url = DATABASE_URL

engine = create_async_engine(
    async_url,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise