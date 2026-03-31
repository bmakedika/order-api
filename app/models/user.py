from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime, timezone
from app.core.database import Base
import uuid
from sqlalchemy.orm import relationship


class UserModel(Base):
    __tablename__ = "users"

    id                 = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username           = Column(String, nullable=False, unique=True)
    email              = Column(String, nullable=False, unique=True)
    hashed_password    = Column(String, nullable=False)
    role               = Column(String, nullable=False, default='user')
    is_active          = Column(Boolean, default=True, nullable=False)
    created_at         = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    orders = relationship('OrderModel', back_populates='user')