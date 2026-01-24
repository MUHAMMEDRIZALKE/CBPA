
from sqlalchemy import Column, Integer, String

from app.models.base import Base

class Currency(Base):
    __tablename__ = "currency"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    code = Column(String(10), nullable=False)
    symbol = Column(String(10), nullable=False)
    numeric_code = Column(Integer, nullable=False)
    minor_unit = Column(Integer, nullable=False)
