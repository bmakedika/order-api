from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.models.product import ProductModel


async def list_active(db: AsyncSession) -> list[ProductModel]:
    result = await db.execute(
        select(ProductModel)
        .where(ProductModel.is_active == True)
    )
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, product_id: UUID) -> ProductModel | None:
    result = await db.execute(
        select(ProductModel)
        .where(
            ProductModel.id == product_id,
            ProductModel.is_active == True
        )
    )
    return result.scalar_one_or_none()


async def create(db: AsyncSession, data: dict) -> ProductModel:
    product = ProductModel(**data)
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def update(db: AsyncSession, product: ProductModel, data: dict) -> ProductModel:
    for key, value in data.items():
        setattr(product, key, value)
    await db.commit()
    await db.refresh(product)
    return product


async def soft_delete(db: AsyncSession, product: ProductModel) -> None:
    product.is_active = False
    await db.commit()


async def save(db: AsyncSession, product: ProductModel) -> None:
    await db.commit()
    await db.refresh(product)