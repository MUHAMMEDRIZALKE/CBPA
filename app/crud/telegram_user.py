from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import TelegramUser
from app.schemas.telegram_user import TelegramUserCreate, TelegramUserUpdate
from app.crud.base import CRUDBase


class CRUDTelegramUser(CRUDBase[TelegramUser, TelegramUserCreate, TelegramUserUpdate]):
    def get_by_telegram_id(self, db: Session, telegram_id: str) -> Optional[TelegramUser]:
        """
        Get TelegramUser by telegram_id

        Args:
            db (Session): Database session.
            telegram_id (str): Telegram user ID.

        Returns:
            Optional[TelegramUser]: TelegramUser object if found, otherwise None.
        """
        return db.query(TelegramUser).filter(TelegramUser.telegram_id == telegram_id,
                                             TelegramUser.is_deleted == False).first()

telegram_user_crud = CRUDTelegramUser(TelegramUser)