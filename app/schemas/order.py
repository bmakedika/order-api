from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import List
from app.models.order import OrderStatus


class OrderCreate(BaseModel):
    customer_id: str
    currency: str


class OrderItemAdd(BaseModel):
    product_id: UUID
    quantity: int


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id : UUID
    product_id: UUID
    quantity : int
    unit_price_cents: int
    line_total_cents: int


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    status: OrderStatus
    total_cents: int
    currency: str
    customer_id: str
    created_at: datetime
    items: List[OrderItemResponse] = []



class OrderStatusUpdate(BaseModel):
    status: OrderStatus
