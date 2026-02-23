import json
import logging
from pathlib import Path
from typing import Any
from openai import AsyncOpenAI
from app.core.config import settings
from app.nl_router.tools.openai import STD_TOOLS
from app.nl_router.router import FunctionRouter
from app.nl_router.models.base import BaseModel

logger = logging.getLogger(__name__)

DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."


def _load_system_prompt() -> str:
    prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "system.md"
    try:
        return prompt_path.read_text().strip()
    except OSError as e:
        logger.warning("Could not load system prompt from %s: %s. Using default.", prompt_path, e)
        return DEFAULT_SYSTEM_PROMPT


class OpenAIModel(BaseModel):
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=settings.OPEN_AI_MODEL_URL,
            api_key=settings.OPEN_AI_API_KEY,
        )
        self.model_name = settings.OPEN_AI_MODEL_NAME
        self._system_prompt = _load_system_prompt()

    async def parse_user_message(self, message: str, user_id: str) -> Any:
        """
        Queries the OpenAI-compatible model.
        Handles tool calls if the model requests them.
        """
        messages = [
            {"role": "system", "content": self._system_prompt},
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
                return FunctionRouter.call_function(parsed_call, user_id)

            # If no tool call, return the content
            return response_message.content

        except Exception as e:
            logger.error(f"Error querying OpenAI model: {e}")
            return f"Error: {str(e)}"
