import uuid
from datetime import datetime, timezone, date
from sqlalchemy import Column, String, Boolean, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class CustomerModel(Base):
    __tablename__ = 'customers'

    id               = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email            = Column(String, nullable=False, unique=True)
    full_name        = Column(String, nullable=True)
    phone            = Column(String, nullable=True)
    address          = Column(String, nullable=True)
    birthdate        = Column(Date, nullable=True)
    marketing_optin  = Column(Boolean, nullable=True, default=False)
    kyc_level        = Column(String, nullable=True)
    gdpr_consent_at  = Column(DateTime(timezone=True), nullable=True)
    created_at       = Column(
                           DateTime(timezone=True),
                           nullable=False,
                           default=lambda: datetime.now(timezone.utc)
                       )
    
    # Relationships
    orders   = relationship('OrderModel',   back_populates='customer', lazy='selectin')
    invoices = relationship('InvoiceModel', back_populates='customer', lazy='selectin')