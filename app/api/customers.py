from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.auth import require_admin
from app.models.user import UserModel
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.services import customer_service

router = APIRouter(prefix='/customers', tags=['Customers'])


@router.post('', response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(require_admin),
):
    return await customer_service.create_customer(data, db)


@router.get('', response_model=list[CustomerResponse])
async def list_customers(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(require_admin),
):
    return await customer_service.list_customers(db, skip=skip, limit=limit)


@router.get('/{customer_id}', response_model=CustomerResponse)
async def get_customer(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(require_admin),
):
    return await customer_service.get_customer(customer_id, db)


@router.patch('/{customer_id}', response_model=CustomerResponse)
async def update_customer(
    customer_id: UUID,
    data: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(require_admin),
):
    return await customer_service.update_customer(customer_id, data, db)


@router.delete('/{customer_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: UserModel = Depends(require_admin),
):
    await customer_service.delete_customer(customer_id, db)