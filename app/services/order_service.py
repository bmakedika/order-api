from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4
from datetime import datetime, timezone
from fastapi import HTTPException, status
from app.repos import order_repo, product_repo, customer_repo
from app.schemas.order import OrderCreate, OrderItemAdd
from app.models.order import OrderStatus


async def create_order(db: AsyncSession, data: OrderCreate, user_id: UUID):
    # Rule of engagement : the customer must exist in the database before placing an order
    customer = await customer_repo.get_by_id(db, data.customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    return await order_repo.create(db, {
        'id':          uuid4(),
        'user_id':     user_id,
        'customer_id': data.customer_id,
        'currency':    data.currency,
        'status':      OrderStatus.DRAFT,
        'total_cents': 0,
        'created_at':  datetime.now(timezone.utc),
    })


async def get_order(db: AsyncSession, order_id: UUID):
    order = await order_repo.get_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order


async def add_item(db: AsyncSession, order_id: UUID, data: OrderItemAdd):
    order = await order_repo.get_by_id(db, order_id)
    if not order:
        return None, 'order not found'

    if order.status != OrderStatus.DRAFT:
        return None, 'cannot modify a non-draft order'

    product = await product_repo.get_by_id(db, data.product_id)
    if not product or not product.is_active:
        return None, 'product not available'

    if data.quantity <= 0:
        return None, 'invalid quantity'

    # Rule of engagement stock : we verify that there is enough stock available
    available = product.stock_quantity - product.reserved_quantity
    if data.quantity > available:
        return None, f'stock insuffisant (disponible : {available})'

    existing_item = await order_repo.get_item_by_product(db, order_id, data.product_id)
    if existing_item:
        existing_item.quantity += data.quantity
        existing_item.line_total_cents = existing_item.quantity * existing_item.unit_price_cents
        await order_repo.save(db, existing_item)
        item = existing_item
    else:
        line_total_cents = product.price_cents * data.quantity
        item = await order_repo.add_item(db, {
            'id':               uuid4(),
            'order_id':         order_id,
            'product_id':       data.product_id,
            'quantity':         data.quantity,
            'unit_price_cents': product.price_cents,
            'line_total_cents': line_total_cents,
        })

    # Update order total
    await db.refresh(order)
    order.total_cents = sum(i.line_total_cents for i in order.items)
    await db.commit()

    # Reserve stock : block the ordered quantity
    product.reserved_quantity += data.quantity
    await product_repo.save(db, product)

    return item, None


async def remove_item(db: AsyncSession, order_id: UUID, item_id: UUID):
    order = await order_repo.get_by_id(db, order_id)
    if not order:
        return None, 'order not found'

    if order.status != OrderStatus.DRAFT:
        return None, 'cannot modify a non-draft order'

    # Retrieve the item before deletion to release the reserved stock
    item = await order_repo.get_item_by_id(db, item_id)
    if not item:
        return None, 'item not found'

    # Release the reserved stock
    product = await product_repo.get_by_id(db, item.product_id)
    if product:
        product.reserved_quantity = max(0, product.reserved_quantity - item.quantity)
        await product_repo.save(db, product)

    deleted = await order_repo.remove_item(db, order_id, item_id)
    if not deleted:
        return None, 'item not found'

    await db.refresh(order)
    order.total_cents = sum(i.line_total_cents for i in order.items)
    await db.commit()
    return True, None