from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID

from sqlalchemy import func
from app.db.session import SessionLocal
from app.models.expense_tracker import Transaction
from app.models.user import User
from app.models.currency import Currency

class TransactionType(StrEnum):
    INCOME = "income"
    EXPENSE = "expense"

class TransactionCategory(StrEnum):
    FOOD = "food"
    TRANSPORT = "transport"
    SHOPPING = "shopping"
    SALARY = "salary"
    OTHER = "other"

class TransactionController:
    def __init__(self, user_id: UUID):
        self.db = SessionLocal()
        self.user_id = user_id

    def add_transaction(
        self,
        amount: float,
        description: str,
        transaction_type: TransactionType,
        currency_code: Optional[str] = None,
        category: Optional[str] = None,
        date: Optional[str] = None
    ) -> str:
        # Resolve Currency
        user = self.db.query(User).filter(User.id == self.user_id).first()
        if not user:
            return "User not found."

        target_currency = None
        
        # 1. Try to find currency from input
        if currency_code:
            target_currency = self.db.query(Currency).filter(Currency.code == currency_code.upper()).first()
            if not target_currency:
                return f"Currency {currency_code} not supported."
            
            # If user has no default, set this as default
            if not user.currency_id:
                user.currency_id = target_currency.id
                self.db.add(user)
                self.db.commit()
                self.db.refresh(user)

        # 2. If no input currency, use user default
        elif user.currency:
            target_currency = user.currency
        
        # 3. If neither, fail and prompt user
        else:
            return "Please set your default currency first. Use /set_currency <CODE> or specify currency in your request (e.g., 'spent 100 USD')."

        # Parse date
        occurred_at = datetime.now()
        if date:
            try:
                # Basic parsing, might need more robust handling
                occurred_at = datetime.fromisoformat(date)
            except ValueError:
                pass # Fallback to now

        transaction = Transaction(
            user_id=self.user_id,
            currency_id=target_currency.id,
            amount=amount,
            description=description,
            category=category or TransactionCategory.OTHER,
            type=transaction_type,
            occurred_at=occurred_at
        )
        self.db.add(transaction)
        self.db.commit()
        
        return f"Recorded {transaction_type}: {amount} {target_currency.code} for {description}."

    def get_analytics(self, time_range: str = "current_month") -> str:
        # TODO: Implement more complex time ranges
        # For now, just simple total
        
        income = self.db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == self.user_id,
            Transaction.type == TransactionType.INCOME
        ).scalar() or 0.0

        expense = self.db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == self.user_id,
            Transaction.type == TransactionType.EXPENSE
        ).scalar() or 0.0

        balance = income - expense
        
        # We need to get the currency symbol/code. Assuming user has one if they have transactions.
        user = self.db.query(User).filter(User.id == self.user_id).first()
        currency_code = user.currency.code if user and user.currency else ""

        return (
            f"📊 Analytics ({time_range}):\n"
            f"Income: {income} {currency_code}\n"
            f"Expense: {expense} {currency_code}\n"
            f"Balance: {balance} {currency_code}"
        )

    def __del__(self):
        if self.db:
            self.db.close()
