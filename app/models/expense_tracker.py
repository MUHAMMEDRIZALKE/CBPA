import uuid
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base, TimestampMixin

class Transaction(Base, TimestampMixin):
    __tablename__ = 'transactions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=False)
    category = Column(String(50), nullable=True)
    occurred_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="transactions")
    currency = relationship("Currency")
