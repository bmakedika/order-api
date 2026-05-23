import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String, Integer, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class OrderStatus(enum.Enum):
    DRAFT           = 'draft'
    PENDING_PAYMENT = 'pending_payment'
    PAID            = 'paid'
    SHIPPED         = 'shipped'
    CANCELLED       = 'cancelled'
    DELIVERED       = 'delivered'
    REFUNDED        = 'refunded'
    FAILED          = 'failed'


class OrderModel(Base):
    __tablename__ = 'orders'

    id          = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id     = Column(PG_UUID(as_uuid=True), ForeignKey('users.id'),     nullable=True,  index=True)
    customer_id = Column(PG_UUID(as_uuid=True), ForeignKey('customers.id'), nullable=False, index=True)
    status      = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.DRAFT, index=True)
    total_cents = Column(Integer,           nullable=False, default=0)
    currency    = Column(String,            nullable=False, default='EUR')
    created_at  = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    user     = relationship('UserModel',      back_populates='orders', lazy='selectin')
    customer = relationship('CustomerModel', back_populates='orders', lazy='selectin')
    items    = relationship('OrderItemModel', back_populates='order', cascade='all, delete-orphan', lazy='selectin')
    invoices = relationship('InvoiceModel',   back_populates='order', lazy='selectin')


class OrderItemModel(Base):
    __tablename__ = 'order_items'

    id               = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id         = Column(PG_UUID(as_uuid=True), ForeignKey('orders.id'),   nullable=False)
    product_id       = Column(PG_UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    quantity         = Column(Integer, nullable=False)
    unit_price_cents = Column(Integer, nullable=False)
    line_total_cents = Column(Integer, nullable=False)
    created_at       = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    order   = relationship('OrderModel',   back_populates='items', lazy='selectin')
    product = relationship('ProductModel', back_populates='order_items', lazy='selectin')