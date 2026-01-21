
from pydantic import BaseModel
import uuid

class TelegramUserBase(BaseModel):
    user_id: uuid.UUID
    telegram_id: int
    username: str
    first_name: str
    last_name: str

class TelegramUserCreate(TelegramUserBase):
    pass

class TelegramUserUpdate(TelegramUserBase):
    pass
    