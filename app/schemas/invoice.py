from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List


class InvoiceItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:               UUID
    product_id:       UUID
    quantity:         int
    unit_price_cents: int
    line_total_cents: int


class InvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:             UUID
    invoice_number: str
    id_order:       UUID
    id_payment:     Optional[UUID] = None
    customer_id:    Optional[UUID] = None
    total_cents:    int
    tax:            int
    created_by:    Optional[UUID] = None
    validated_by:  Optional[UUID] = None
    validated_at:  Optional[datetime] = None
    created_at:    Optional[datetime] = None
    items:         List[InvoiceItemResponse] = []