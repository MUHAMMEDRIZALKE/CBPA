from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID

from app.db.session import SessionLocal
from app.models.user import User
from app.models.currency import Currency
from app.crud.transaction import transaction_crud


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
        date: Optional[str] = None,
    ) -> str:
        # Resolve Currency
        user = self.db.query(User).filter(User.id == self.user_id).first()
        if not user:
            return "User not found."

        target_currency = None

        # 1. Try to find currency from input
        if currency_code:
            target_currency = (
                self.db.query(Currency)
                .filter(Currency.code == currency_code.upper())
                .first()
            )
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
                # Fallback to now
                pass

        transaction_crud.create_for_user(
            db=self.db,
            user_id=self.user_id,
            currency_id=target_currency.id,
            amount=amount,
            description=description,
            category=category or TransactionCategory.OTHER,
            type=transaction_type,
            occurred_at=occurred_at,
        )

        return f"Recorded {transaction_type}: {amount} {target_currency.code} for {description}."

    def list_transactions(self, limit: Optional[int] = None) -> str:
        try:
            limit_value = int(limit) if limit is not None else 10
        except (TypeError, ValueError):
            limit_value = 10

        if limit_value <= 0:
            limit_value = 10

        # Hard cap to avoid overly long responses
        if limit_value > 50:
            limit_value = 50

        transactions = transaction_crud.list_recent_for_user(
            db=self.db,
            user_id=self.user_id,
            limit=limit_value,
        )

        if not transactions:
            return "You don't have any recorded transactions yet."

        lines = ["Here are your most recent transactions:"]
        for idx, tx in enumerate(transactions, start=1):
            currency_code = tx.currency.code if tx.currency else ""
            date_str = tx.occurred_at.strftime("%Y-%m-%d")
            category_str = tx.category or ""
            lines.append(
                f"{idx}. {date_str} | {tx.type} | {tx.amount} {currency_code} | {tx.description} | {category_str} | id: {tx.id}"
            )

        return "\n".join(lines)

    def delete_transaction(self, transaction_id: str) -> str:
        if not transaction_id:
            return "Please provide a transaction ID or prefix to delete."

        prefix = transaction_id.strip()
        if not prefix:
            return "Please provide a transaction ID or prefix to delete."

        # Allow matching by UUID prefix as shown in the list output.
        matches = transaction_crud.find_active_by_id_prefix(
            db=self.db,
            user_id=self.user_id,
            prefix=prefix,
        )

        if not matches:
            return "Transaction not found for your account."

        if len(matches) > 1:
            # Show a few matching candidates to help the user refine.
            lines = ["Multiple transactions match that ID prefix. Please enter more characters from the transaction ID to narrow it down."]
            for tx in matches[:5]:
                currency_code = tx.currency.code if tx.currency else ""
                date_str = tx.occurred_at.strftime("%Y-%m-%d")
                lines.append(
                    f"- {tx.id} | {date_str} | {tx.amount} {currency_code} | {tx.description}"
                )
            return "\n".join(lines)

        transaction = matches[0]

        currency_code = transaction.currency.code if transaction.currency else ""
        date_str = transaction.occurred_at.strftime("%Y-%m-%d")
        summary = (
            f"{transaction.amount} {currency_code} on {date_str} - {transaction.description}"
        )

        transaction_crud.soft_delete(self.db, tx=transaction)

        return f"Deleted transaction {transaction.id}: {summary}."

    def get_analytics(
        self,
        time_range: str = "current_month",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> str:
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
                query_start = now.replace(
                    day=1,
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                )
                # query_end is explicitly None (up to now)
                display_range = "Current Month"
            elif time_range == "today":
                query_start = now.replace(
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                )
                display_range = "Today"
            elif time_range == "last_month":
                # First day of this month
                first_this_month = now.replace(
                    day=1,
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                )
                # Find first day of last month
                # If current month is Jan, last month is Dec of prev year
                if now.month == 1:
                    query_start = now.replace(
                        year=now.year - 1,
                        month=12,
                        day=1,
                        hour=0,
                        minute=0,
                        second=0,
                        microsecond=0,
                    )
                else:
                    query_start = now.replace(
                        month=now.month - 1,
                        day=1,
                        hour=0,
                        minute=0,
                        second=0,
                        microsecond=0,
                    )

                query_end = first_this_month
                display_range = "Last Month"
            else:
                # Fallback to current month if unknown range
                query_start = now.replace(
                    day=1,
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                )
                display_range = time_range

        # 3. Aggregate values via CRUD layer
        income = transaction_crud.sum_amount_for_user_and_type(
            db=self.db,
            user_id=self.user_id,
            tx_type=TransactionType.INCOME,
            start=query_start,
            end=query_end,
        )
        expense = transaction_crud.sum_amount_for_user_and_type(
            db=self.db,
            user_id=self.user_id,
            tx_type=TransactionType.EXPENSE,
            start=query_start,
            end=query_end,
        )
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
