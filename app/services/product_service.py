from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional
from app.repos import product_repo
from app.schemas.product import ProductCreate, ProductUpdate


async def get_product_by_id(db: AsyncSession, product_id: UUID):
    return await product_repo.get_by_id(db, product_id)


async def list_products(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 10,
    category: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    sort: Optional[str] = None,
):
    filtered = await product_repo.list_active(db)

    if category:
        filtered = [p for p in filtered if p.category == category]
    if min_price is not None:
        filtered = [p for p in filtered if p.price_cents >= min_price]
    if max_price is not None:
        filtered = [p for p in filtered if p.price_cents <= max_price]

    if sort == 'price_asc':
        filtered = sorted(filtered, key=lambda p: p.price_cents)
    elif sort == 'price_desc':
        filtered = sorted(filtered, key=lambda p: p.price_cents, reverse=True)
    elif sort == 'newest':
        filtered = sorted(filtered, key=lambda p: p.created_at, reverse=True)

    total = len(filtered)
    start = (page - 1) * page_size
    end = start + page_size

    return {
        'items': filtered[start:end],
        'page': page,
        'page_size': page_size,
        'total': total,
    }


async def create_product(db: AsyncSession, data: ProductCreate):
    return await product_repo.create(db, {
        'id':          uuid4(),
        'name':        data.name,
        'description': data.description,
        'price_cents': data.price_cents,
        'currency':    data.currency,
        'category':    data.category,
        'is_active':   True,
        'stock_quantity':    data.stock_quantity,
        'reserved_quantity': data.reserved_quantity,
        'created_at':  datetime.now(timezone.utc),
    })


async def update_product(db: AsyncSession, product_id: UUID, data: ProductUpdate):
    product = await product_repo.get_by_id(db, product_id)
    if not product:
        return None
    # exclude_unset=True : ne met à jour que les champs envoyés
    updates = data.model_dump(exclude_unset=True)
    return await product_repo.update(db, product, updates)


async def delete_product(db: AsyncSession, product_id: UUID) -> bool:
    product = await product_repo.get_by_id(db, product_id)
    if not product:
        return False
    await product_repo.soft_delete(db, product)
    return True