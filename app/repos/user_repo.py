from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.models.user import UserModel


async def create(db: AsyncSession, data: dict) -> UserModel:
    user = UserModel(**data)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_by_id(db: AsyncSession, user_id: UUID) -> UserModel | None:
    result = await db.execute(
        select(UserModel).where(UserModel.id == user_id)
    )
    return result.scalar_one_or_none()


async def get_by_email(db: AsyncSession, email: str) -> UserModel | None:
    result = await db.execute(
        select(UserModel).where(UserModel.email == email)
    )
    return result.scalar_one_or_none()