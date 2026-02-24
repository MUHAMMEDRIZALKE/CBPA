from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.crud.base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(
        self,
        db: Session,
        obj_in: UserCreate,
        hashed_password: Optional[str] = None,
    ) -> User:
        """
        Create a new user.

        Args:
            db (Session): Database session.
            obj_in (UserCreate): User create schema.
            hashed_password (Optional[str]): Hashed password.

        Returns:
            User: Created user.
        """
        obj_data = obj_in.dict()
        if "password" in obj_data:
            del obj_data["password"]

        obj_data["password_hash"] = hashed_password

        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_active(self, db: Session, user_id) -> Optional[User]:
        """Get a non-deleted user by ID."""
        return (
            db.query(User)
            .filter(
                User.id == user_id,
                User.is_deleted == False,  # noqa: E712
            )
            .first()
        )

    def set_default_currency(
        self,
        db: Session,
        user_id,
        currency_id: int,
    ) -> Optional[User]:
        """Set the default currency for a user and persist the change."""
        user = self.get_active(db, user_id)
        if not user:
            return None

        user.currency_id = currency_id
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


user_crud = CRUDUser(User)