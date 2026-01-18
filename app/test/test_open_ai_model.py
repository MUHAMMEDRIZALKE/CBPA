
import asyncio
import os
from app.nl_router.nlu import NLURouter
from app.core.config import settings

async def test_local_model():
    # Force use of local model for test
    settings.MODEL_TYPE = "open_ai"
    # settings.MODEL_TYPE = "gen_ai" # Uncomment to test gen_ai
    
    # Check if OPEN_AI_MODEL_URL is set, if not fallback to LOCAL_MODEL_URL logic or just set it for test
    if not settings.OPEN_AI_MODEL_URL:
        # Assuming we want to test with the local qwen model logic
        settings.OPEN_AI_MODEL_URL = "http://host.docker.internal:12434/engines/v1"
        settings.OPEN_AI_MODEL_NAME = "ai/qwen2.5:7B-Q4_0"

    print(f"Testing OpenAI compatible model: {settings.OPEN_AI_MODEL_NAME} at {settings.OPEN_AI_MODEL_URL}")
    
    router = NLURouter()

    # Test 1: Simple query
    print("\n--- Test 1: Simple Query ---")
    response = await router.parse_user_message("Hello, how are you?")
    print(f"Response: {response}")

    # Test 2: Tool Call (Send Money)
    print("\n--- Test 2: Tool Call (Send Money) ---")
    response_tool = await router.parse_user_message("Send 50 dollars to Alice on tomorrow")
    print(f"Response: {response_tool}")
    
    # Test 3: Tool Call (Check Balance)
    print("\n--- Test 3: Tool Call (Check Balance) ---")
    response_balance = await router.parse_user_message("Check my balance")
    print(f"Response: {response_balance}")

if __name__ == "__main__":
    asyncio.run(test_local_model())
