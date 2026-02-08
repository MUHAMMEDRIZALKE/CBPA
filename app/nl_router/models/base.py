
from abc import ABC, abstractmethod
from typing import Any

class BaseModel(ABC):
    @abstractmethod
    async def parse_user_message(self, message: str, user_id: str) -> Any:
        pass
