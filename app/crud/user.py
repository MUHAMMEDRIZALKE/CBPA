from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.crud.base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def create(self, db: Session, obj_in: UserCreate, hashed_password: Optional[str] = None) -> User:
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
        if 'password' in obj_data:
            del obj_data['password']

        obj_data['password_hash'] = hashed_password

        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj




user_crud = CRUDUser(User)