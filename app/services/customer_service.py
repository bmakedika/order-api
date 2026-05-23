from uuid import UUID
from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repos import customer_repo
from app.schemas.customer import CustomerCreate, CustomerUpdate


async def create_customer(data: CustomerCreate, db: AsyncSession):
    # Rule: unique email
    existing = await customer_repo.get_by_email(db, data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A customer with email '{data.email}' already exists."
        )

    payload = data.model_dump(exclude_unset=True)
    payload['created_at'] = datetime.now(timezone.utc)

    return await customer_repo.create(db, payload)


async def get_customer(customer_id: UUID, db: AsyncSession):
    customer = await customer_repo.get_by_id(db, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer


async def list_customers(db: AsyncSession, skip: int = 0, limit: int = 20):
    return await customer_repo.get_all(db, skip=skip, limit=limit)


async def update_customer(customer_id: UUID, data: CustomerUpdate, db: AsyncSession):
    customer = await get_customer(customer_id, db)

    # If email is being updated, check for uniqueness
    if data.email and data.email != customer.email:
        existing = await customer_repo.get_by_email(db, data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{data.email}' is already in use."
            )

        payload = data.model_dump(exclude_unset=True)
    return await customer_repo.update(db, customer, payload)


async def delete_customer(customer_id: UUID, db: AsyncSession):
    customer = await get_customer(customer_id, db)
    await customer_repo.delete(db, customer)