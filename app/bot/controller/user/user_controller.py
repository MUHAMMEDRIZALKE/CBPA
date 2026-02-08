from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.models.currency import Currency
from app.crud.user import user_crud

class UserController:
    def __init__(self, user_id: str):
        self.db = SessionLocal()
        self.user_id = user_id

    def get_user_currency(self):
        user = self.db.query(User).filter(User.id == self.user_id).first()
        if user and user.currency:
            return user.currency.code
        return None

    def set_default_currency(self, currency_code: str):
        currency = self.db.query(Currency).filter(Currency.code == currency_code.upper()).first()
        if not currency:
            return f"Currency {currency_code} not found."
        
        user = self.db.query(User).filter(User.id == self.user_id).first()
        if not user:
             return "User not found."

        user.currency_id = currency.id
        self.db.commit()
        return f"Currency set to {currency.code}"

    def __del__(self):
        if self.db:
            self.db.close()
