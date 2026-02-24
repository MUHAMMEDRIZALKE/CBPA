from typing import Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.currency import Currency


class CRUDCurrency(CRUDBase[Currency, BaseModel, BaseModel]):
    def get_by_code(self, db: Session, code: str) -> Optional[Currency]:
        """Fetch a currency by its code (case-insensitive)."""
        return (
            db.query(Currency)
            .filter(Currency.code == code.upper())
            .first()
        )


currency_crud = CRUDCurrency(Currency)

