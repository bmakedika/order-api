from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional


class ProductCreate(BaseModel):
    name: str
    description: str
    price_cents: int
    currency: str
    category: str
    stock_quantity:    int = 0
    reserved_quantity: int = 0


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price_cents: Optional[int] = None
    currency: Optional[str] = None
    category: Optional[str] = None
    stock_quantity:    Optional[int] = None
    reserved_quantity: Optional[int] = None


class ProductResponse(BaseModel):
    id: UUID
    name: str
    description: str
    price_cents: int
    currency: str
    category: str
    is_active: bool = True
    created_at: datetime
    stock_quantity:    int
    reserved_quantity: int


class ProductList(BaseModel):
    items: List[ProductResponse]
    page: int
    page_size: int
    total: int