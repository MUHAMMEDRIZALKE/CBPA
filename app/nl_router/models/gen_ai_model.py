
from typing import Any
from google import genai
from google.genai import types
from app.core.config import settings
from app.nl_router.models.base import BaseModel
from app.nl_router.tools.gen_ai import get_weather_tool
from app.nl_router.router import FunctionRouter

class GenAIModel(BaseModel):
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEN_AI_API_KEY)
        self.model_name = settings.GEN_AI_MODEL_NAME

    async def parse_user_message(self, message: str, user_id: str) -> Any:
        return "GenAI Model not implemented yet."
