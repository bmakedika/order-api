from fastapi import APIRouter, HTTPException, Depends, Header
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.auth import require_user, require_admin
from app.repos.user_repo import get_by_email
from app.schemas.order import OrderCreate, OrderItemAdd, OrderResponse, OrderStatusUpdate
from app.services import order_service

router = APIRouter()


@router.post('/orders', response_model=OrderResponse)
async def create_order(
    data: OrderCreate,
    payload=Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    user = await get_by_email(db, email=payload['sub'])
    return await order_service.create_order(db, data, user_id=user.id)


@router.get('/orders/{order_id}', response_model=OrderResponse)
async def get_order(
    order_id: UUID,
    payload=Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    user  = await get_by_email(db, email=payload['sub'])
    order = await order_service.get_order(db, order_id)
    if order.user_id != user.id:
        raise HTTPException(status_code=403, detail='Forbidden')
    return order


@router.post('/orders/{order_id}/items', response_model=OrderResponse)
async def add_item(
    order_id: UUID,
    data: OrderItemAdd,
    _=Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    item, error = await order_service.add_item(db, order_id, data)
    if error == 'order not found':
        raise HTTPException(status_code=404, detail='Order not found')
    if error == 'product not available':
        raise HTTPException(status_code=404, detail='Product not found')
    if error and 'stock' in error:
        raise HTTPException(status_code=409, detail=error)
    order = await order_service.get_order(db, order_id)
    return order


@router.delete('/orders/{order_id}/items/{item_id}', status_code=200)
async def remove_item(
    order_id: UUID,
    item_id: UUID,
    _=Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    deleted, error = await order_service.remove_item(db, order_id, item_id)
    if error == 'order not found':
        raise HTTPException(status_code=404, detail='Order not found')
    if error == 'item not found':
        raise HTTPException(status_code=404, detail='Item not found')


@router.post('/orders/{order_id}/pay', response_model=OrderResponse)
async def pay_order(
    order_id: UUID,
    _=Depends(require_user),
    db: AsyncSession = Depends(get_db),
    idempotency_key: str = Header(..., alias='Idempotency-Key'),
):
    from app.services import payment_service
    order, error = await payment_service.pay_order(db, order_id, idempotency_key)

    if error == 'order_not_found':
        raise HTTPException(status_code=404, detail='Order not found')
    if error == 'invalid_status':
        raise HTTPException(status_code=409, detail='Order already paid or cancelled')
    if error == 'empty_order':
        raise HTTPException(status_code=400, detail='Cannot pay empty order')
    return order


@router.patch('/orders/{order_id}/status', response_model=OrderResponse)
async def update_order_status(
    order_id: UUID,
    status_update: OrderStatusUpdate,
    _=Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    order = await order_service.get_order(db, order_id)
    order.status = status_update.status
    await db.commit()
    await db.refresh(order)
    return order