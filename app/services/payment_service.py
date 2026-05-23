from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4
from app.repos import order_repo
from app.models.order import OrderStatus
from app.core.redis_client import get_redis
from app.services.invoice_service import create_invoice

IDEMPOTENCY_TTL = 86400


async def pay_order(db: AsyncSession, order_id: UUID, idempotency_key: str):
    redis = get_redis()

    cached = redis.get(f'idempotency:{idempotency_key}')
    if cached:
        order = await order_repo.get_by_id(db, order_id)
        return order, 'already_processed'

    order = await order_repo.get_by_id(db, order_id)
    if not order:
        return None, 'order_not_found'

    if order.status != OrderStatus.DRAFT:
        return order, 'invalid_status'

    if order.total_cents == 0:
        return order, 'empty_order'

    order.status = OrderStatus.PAID
    await db.commit()
    await db.refresh(order)

    for item in order.items:
        from app.repos import product_repo
        product = await product_repo.get_by_id(db, item.product_id)
        if product:
            product.stock_quantity    -= item.quantity
            product.reserved_quantity = max(0, product.reserved_quantity - item.quantity)
            await product_repo.save(db, product)

    await create_invoice(db, order, id_payment=uuid4())

    redis.set(f'idempotency:{idempotency_key}', 'paid', ex=IDEMPOTENCY_TTL)

    return order, None