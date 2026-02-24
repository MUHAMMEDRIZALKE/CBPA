from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.crud.user import user_crud
from app.crud.currency import currency_crud


class UserController:
    def __init__(self, user_id: str):
        self.db: Session = SessionLocal()
        self.user_id = user_id

    def get_user_currency(self):
        user = user_crud.get_active(self.db, self.user_id)
        if user and user.currency:
            return user.currency.code
        return None

    def set_default_currency(self, currency_code: str):
        currency = currency_crud.get_by_code(self.db, currency_code)
        if not currency:
            return f"Currency {currency_code} not found."

        user = user_crud.set_default_currency(self.db, self.user_id, currency.id)
        if not user:
            return "User not found."

        return f"Currency set to {currency.code}"

    def __del__(self):
        if self.db:
            self.db.close()
