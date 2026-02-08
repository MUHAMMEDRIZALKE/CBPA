
from typing import Any
from app.core.config import settings
from app.nl_router.enums import ModelType
from app.nl_router.models.base import BaseModel
from app.nl_router.models.openai_model import OpenAIModel
from app.nl_router.models.gen_ai_model import GenAIModel

class NLURouter:
    def __init__(self):
        self.model: BaseModel = self._get_model()

    def _get_model(self) -> BaseModel:
        model_type = settings.MODEL_TYPE
        
        if model_type == ModelType.OPEN_AI.value:
            return OpenAIModel()
        elif model_type == ModelType.GEN_AI.value:
            return GenAIModel()
        else:
            if not model_type:
                 return OpenAIModel()
            raise ValueError(f"Unknown MODEL_TYPE: {model_type}")

    async def parse_user_message(self, message: str, user_id: str) -> Any:
        return await self.model.parse_user_message(message, user_id)