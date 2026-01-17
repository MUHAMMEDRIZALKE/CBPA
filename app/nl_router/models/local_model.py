
import json
import logging
from typing import Any
from openai import AsyncOpenAI
from app.core.config import settings
from app.nl_router.tools.openai import STD_TOOLS
from app.nl_router.router import FunctionRouter
from app.nl_router.models.base import BaseModel

logger = logging.getLogger(__name__)

class LocalModel(BaseModel):
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=settings.LOCAL_MODEL_URL,
            api_key="dummy-key-not-needed",
        )
        self.model_name = settings.LOCAL_MODEL_NAME

    async def parse_user_message(self, message: str) -> Any:
        """
        Queries the locally running OpenAI-compatible model.
        Handles tool calls if the model requests them.
        """
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]

        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=STD_TOOLS,
                tool_choice="auto", 
            )

            response_message = response.choices[0].message

            # Check for tool calls
            if response_message.tool_calls:
                tool_call = response_message.tool_calls[0]
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                logger.info(f"Model requested tool execution: {function_name} with args: {function_args}")
                
                # Reformatted for the router
                parsed_call = {
                    "function": function_name,
                    "arguments": function_args
                }
                return FunctionRouter.call_function(parsed_call)

            # If no tool call, return the content
            return response_message.content

        except Exception as e:
            logger.error(f"Error querying local model: {e}")
            return f"Error: {str(e)}"
