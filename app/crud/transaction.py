from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import func, cast, String
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.expense_tracker import Transaction


class CRUDTransaction(CRUDBase[Transaction, BaseModel, BaseModel]):
    def create_for_user(
        self,
        db: Session,
        *,
        user_id: UUID,
        currency_id: int,
        amount: float,
        description: str,
        category: Optional[str],
        type: str,
        occurred_at: datetime,
    ) -> Transaction:
        transaction = Transaction(
            user_id=user_id,
            currency_id=currency_id,
            amount=amount,
            description=description,
            category=category,
            type=type,
            occurred_at=occurred_at,
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    def list_recent_for_user(
        self,
        db: Session,
        *,
        user_id: UUID,
        limit: int,
    ) -> List[Transaction]:
        return (
            db.query(Transaction)
            .filter(
                Transaction.user_id == user_id,
                Transaction.is_deleted.is_(False),
            )
            .order_by(Transaction.occurred_at.desc())
            .limit(limit)
            .all()
        )

    def find_active_by_id_prefix(
        self,
        db: Session,
        *,
        user_id: UUID,
        prefix: str,
    ) -> List[Transaction]:
        return (
            db.query(Transaction)
            .filter(
                Transaction.user_id == user_id,
                Transaction.is_deleted.is_(False),
                cast(Transaction.id, String).like(f"{prefix}%"),
            )
            .all()
        )

    def soft_delete(self, db: Session, *, tx: Transaction) -> Transaction:
        tx.is_deleted = True
        db.add(tx)
        db.commit()
        db.refresh(tx)
        return tx

    def sum_amount_for_user_and_type(
        self,
        db: Session,
        *,
        user_id: UUID,
        tx_type: str,
        start: Optional[datetime],
        end: Optional[datetime],
    ) -> float:
        q = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == tx_type,
            Transaction.is_deleted.is_(False),
        )
        if start:
            q = q.filter(Transaction.occurred_at >= start)
        if end:
            q = q.filter(Transaction.occurred_at < end)
        return q.scalar() or 0.0


transaction_crud = CRUDTransaction(Transaction)

