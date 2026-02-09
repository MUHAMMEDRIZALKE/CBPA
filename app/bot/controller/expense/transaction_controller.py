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

    def get_analytics(self, time_range: str = "current_month", start_date: Optional[str] = None, end_date: Optional[str] = None) -> str:
        query_start = None
        query_end = None

        # 1. Helper to parse date strings
        def parse_date(date_str: str) -> Optional[datetime]:
            try:
                return datetime.fromisoformat(date_str)
            except (ValueError, TypeError):
                return None

        # 2. Determine time range
        if start_date or end_date:
            # Custom range
            if start_date:
                query_start = parse_date(start_date)
            if end_date:
                query_end = parse_date(end_date)
            
            # If provided but invalid, we might want to handle it. For now, let's assume valid or ignore.
            display_range = f"{start_date or '...'} to {end_date or 'now'}"
        
        else:
            # Preset ranges
            now = datetime.now()
            if time_range == "current_month":
                query_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                # query_end is explicitly None (up to now)
                display_range = "Current Month"
            elif time_range == "today":
                query_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
                display_range = "Today"
            elif time_range == "last_month":
                # First day of this month
                first_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                # Last day of last month is first_this_month - 1 microsecond (effectively)
                # But safer:
                # Find first day of last month
                # If current month is Jan, last month is Dec of prev year
                if now.month == 1:
                    query_start = now.replace(year=now.year-1, month=12, day=1, hour=0, minute=0, second=0, microsecond=0)
                else:
                    query_start = now.replace(month=now.month-1, day=1, hour=0, minute=0, second=0, microsecond=0)
                
                query_end = first_this_month
                display_range = "Last Month"
            else:
                # Fallback to current month if unknown range
                query_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                display_range = time_range

        # 3. Build Queries
        def build_query(tx_type: TransactionType):
            q = self.db.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == self.user_id,
                Transaction.type == tx_type
            )
            if query_start:
                q = q.filter(Transaction.occurred_at >= query_start)
            if query_end:
                q = q.filter(Transaction.occurred_at < query_end)
            return q.scalar() or 0.0

        income = build_query(TransactionType.INCOME)
        expense = build_query(TransactionType.EXPENSE)
        balance = income - expense
        
        # We need to get the currency symbol/code. Assuming user has one if they have transactions.
        user = self.db.query(User).filter(User.id == self.user_id).first()
        currency_code = user.currency.code if user and user.currency else ""

        # Format the actual date range applied
        start_str = query_start.strftime("%Y-%m-%d") if query_start else "..."
        end_str = "Now"
        if query_end:
            # If query_end is exactly midnight, it usually means "up to this date" (exclusive)
            # For display, it might be clearer to show the previous day if it's a generated range like last_month
            # But for custom ranges, user might expect what they typed.
            # Let's just show the calculated query boundary for clarity.
            end_str = query_end.strftime("%Y-%m-%d")

        date_range_line = f"📅 {start_str} - {end_str}"

        return (
            f"📊 Analytics ({display_range}):\n"
            f"{date_range_line}\n"
            f"Income: {income} {currency_code}\n"
            f"Expense: {expense} {currency_code}\n"
            f"Balance: {balance} {currency_code}"
        )

    def __del__(self):
        if self.db:
            self.db.close()
