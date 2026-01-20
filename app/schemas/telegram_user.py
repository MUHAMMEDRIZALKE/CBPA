
from pydantic import BaseModel


class TelegramUserBase(BaseModel):
    telegram_id: int
    username: str
    first_name: str
    last_name: str

class TelegramUserCreate(TelegramUserBase):
    pass

class TelegramUserUpdate(TelegramUserBase):
    pass
    