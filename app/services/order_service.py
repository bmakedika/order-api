from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime, timezone
from app.repos import order_repo, product_repo
from app.schemas.order import OrderCreate, OrderItemAdd
from app.models.order import OrderStatus


def create_order(db: Session, data: OrderCreate):
    return order_repo.create(db, {
        'id': uuid4(),
        'customer_id': data.customer_id,
        'currency': data.currency,
        'status': OrderStatus.DRAFT,
        'total_cents': 0,
        'created_at': datetime.now(timezone.utc),
    })



def get_order(db: Session, order_id: UUID):
    return order_repo.get_by_id(db, order_id)


def add_item(db: Session, order_id: UUID, data: OrderItemAdd):
    # check if order exists
    order = order_repo.get_by_id(db, order_id)
    if not order:
        return None, 'order not found'
    
    # check if product exists
    product = product_repo.get_by_id(db, data.product_id)
    if not product:
        return None, 'product not found'
    
    # compute item total
    line_total_cents = product.price_cents * data.quantity


    # add item to order
    item = order_repo.add_item(db, {
        'id': uuid4(),
        'order_id': order_id,
        'product_id': data.product_id,
        'quantity': data.quantity,
        'unit_price_cents': product.price_cents,
        'line_total_cents': line_total_cents,

    })

    # update order total
    order_repo.update_total(db, order)

    return item, None



def remove_item(db: Session, order_id: UUID, item_id: UUID):
    order = order_repo.get_by_id(db, order_id)
    if not order:
        return None, 'order not found'
    
    deleted = order_repo.remove_item(db, order_id, item_id)
    if not deleted:
        return None, 'item not found'

    order_repo.update_total(db, order)
    return True, None