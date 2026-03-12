from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import require_user
from app.schemas.order import OrderCreate, OrderItemAdd, OrderResponse
from app.services import order_service


router = APIRouter()


@router.post('/orders', response_model=OrderResponse)
def create_order(
    data: OrderCreate,
    _= Depends(require_user),
    db: Session = Depends(get_db)
):
    return order_service.create_order(db, data)



@router.get('/orders/{order_id}', response_model=OrderResponse)
def get_order(
    order_id: UUID,
    _= Depends(require_user),
    db: Session = Depends(get_db)
):
    order = order_service.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    return order



@router.post('/orders/{order_id}/items', response_model=OrderResponse)
def add_item(
    order_id: UUID,
    data: OrderItemAdd,
    _= Depends(require_user),
    db: Session = Depends(get_db)
):
    item, error = order_service.add_item(db, order_id, data)
    if error == 'order_not_found':
        raise HTTPException(status_code=404, detail='Order not found')
    if error == 'product_not_found':
        raise HTTPException(status_code=404, detail='Product not found')
    db.expire_all()
    order = order_service.get_order(db, order_id)
    return order



@router.delete('/orders/{order_id}/items/{item_id}', status_code=200)
def remove_item(
    order_id: UUID,
    item_id: UUID,
    _= Depends(require_user),
    db: Session = Depends(get_db),
):
    deleted, error = order_service.remove_item(db, order_id, item_id)
    if error == 'order_not_found':
        raise HTTPException(status_code=404, detail='Order not found')
    if error == 'item_not_found':
        raise HTTPException(status_code=404, detail='Item not found')