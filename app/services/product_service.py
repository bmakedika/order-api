from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional
from app.repos import product_repo
from app.schemas.product import ProductCreate, ProductUpdate


def get_product_by_id(db: Session, product_id: UUID):
    return product_repo.get_by_id(db, product_id)


def list_products(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    category: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    sort: Optional[str] = None,
):
    products = product_repo.list_active(db)
    

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
        'items': products[start:end],
        'page': page,
        'page_size': page_size,
        'total': total,
    }


def create_product(db: Session, data: ProductCreate):
    return product_repo.create(db, {
        'id': uuid4(),
        'name': data.name,
        'description': data.description,
        'price_cents': data.price_cents,
        'currency': data.currency,
        'category': data.category,
        'is_active': True,
        'created_at': datetime.now(timezone.utc),
    })



def update_product(db: Session, product_id: UUID, data: ProductUpdate):
    product = product_repo.get_by_id(db, product_id)
    if not product:
        return None
    updates = {k: v for k, v in data.model_dump().items() if v is not None}
    return product_repo.update(db, product, updates)



def delete_product(db: Session, product_id: UUID) -> bool:
    product = product_repo.get_by_id(db, product_id)
    if not product:
        return False
    product_repo.soft_delete(db, product)
    return True