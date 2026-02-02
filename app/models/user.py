import uuid

from sqlalchemy import UUID, Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), index=True)
    email = Column(String(255), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=True)
    role = Column(String(50), default='user')
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)

    currency = relationship("Currency")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

    telegram_users = relationship("TelegramUser", back_populates="user")


class TelegramUser(Base, TimestampMixin):
    __tablename__ = 'telegram_users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id = Column(String(50), unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    username = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    is_deleted = Column(Boolean, default=False)

    user = relationship("User", back_populates="telegram_users")

