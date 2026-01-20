
from app.models.telegram_user import TelegramUser
from app.schemas.telegram_user import TelegramUserCreate, TelegramUserUpdate
from app.crud.base import CRUDBase


class CRUDTelegramUser(CRUDBase[TelegramUser, TelegramUserCreate, TelegramUserUpdate]):
    ...

telegram_user = CRUDTelegramUser(TelegramUser)