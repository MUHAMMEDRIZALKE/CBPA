
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

    async def parse_user_message(self, message: str) -> Any:
        ...
        # response_stream = self.client.models.generate_content_stream(
        #     model=self.model_name,
        #     contents=message,
        #     config=types.GenerateContentConfig(
        #         tools=[get_weather_tool],
        #         tool_config=types.ToolConfig(
        #             function_calling_config=types.FunctionCallingConfig(
        #                 mode=types.FunctionCallingConfigMode.AUTO,
        #             )
        #         ),
        #     ),
        # )

        # for chunk in response_stream:
        #     if chunk.function_calls:
        #         function_call = chunk.function_calls[0]
        #         if function_call and function_call.name:
        #             return FunctionRouter.call_function({
        #                 "function": function_call.name,
        #                 "arguments": function_call.args
        #             })
