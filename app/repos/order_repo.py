from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.models.order import OrderModel, OrderItemModel


async def create(db: AsyncSession, data: dict) -> OrderModel:
    order = OrderModel(**data)
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


async def add_item(db: AsyncSession, data: dict) -> OrderItemModel:
    item = OrderItemModel(**data)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def get_by_id(db: AsyncSession, order_id: UUID) -> OrderModel | None:
    result = await db.execute(
        select(OrderModel).where(OrderModel.id == order_id)
    )
    return result.scalar_one_or_none()


async def get_item_by_product(
    db: AsyncSession, order_id: UUID, product_id: UUID
) -> OrderItemModel | None:
    result = await db.execute(
        select(OrderItemModel).where(
            OrderItemModel.order_id == order_id,
            OrderItemModel.product_id == product_id,
        )
    )
    return result.scalar_one_or_none()


async def get_item_by_id(
    db: AsyncSession, item_id: UUID
) -> OrderItemModel | None:
    result = await db.execute(
        select(OrderItemModel).where(OrderItemModel.id == item_id)
    )
    return result.scalar_one_or_none()


async def update_total(db: AsyncSession, order: OrderModel) -> OrderModel:
    order.total_cents = sum(item.line_total_cents for item in order.items)
    await db.commit()
    await db.refresh(order)
    return order


async def save(db: AsyncSession, obj) -> None:
    await db.commit()
    await db.refresh(obj)


async def remove_item(
    db: AsyncSession, order_id: UUID, item_id: UUID
) -> bool:
    result = await db.execute(
        select(OrderItemModel).where(
            OrderItemModel.id == item_id,
            OrderItemModel.order_id == order_id,
        )
    )
    item = result.scalar_one_or_none()
    if not item:
        return False
    await db.delete(item)
    await db.commit()
    return True