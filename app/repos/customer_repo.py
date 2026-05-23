from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.customer import CustomerModel


async def get_by_id(db: AsyncSession, customer_id: UUID) -> CustomerModel | None:
    # SELECT * FROM customers WHERE id = :customer_id LIMIT 1
    result = await db.execute(
        select(CustomerModel).where(CustomerModel.id == customer_id)
    )
    return result.scalar_one_or_none()


async def get_by_email(db: AsyncSession, email: str) -> CustomerModel | None:
    # SELECT * FROM customers WHERE email = :email LIMIT 1
    result = await db.execute(
        select(CustomerModel).where(CustomerModel.email == email)
    )
    return result.scalar_one_or_none()


async def get_all(db: AsyncSession, skip: int = 0, limit: int = 20) -> list[CustomerModel]:
    # SELECT * FROM customers ORDER BY created_at DESC LIMIT :limit OFFSET :skip
    result = await db.execute(
        select(CustomerModel)
        .order_by(CustomerModel.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def create(db: AsyncSession, data: dict) -> CustomerModel:
    customer = CustomerModel(**data)
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return customer


async def update(db: AsyncSession, customer: CustomerModel, data: dict) -> CustomerModel:
    for key, value in data.items():
        setattr(customer, key, value)
    await db.commit()
    await db.refresh(customer)
    return customer


async def delete(db: AsyncSession, customer: CustomerModel) -> None:
    await db.delete(customer)
    await db.commit()