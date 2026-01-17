
from typing import Any, Dict
from app.nl_router.functions import send_money, check_balance

class FunctionRouter:
    @staticmethod
    def call_function(parsed_call: Dict[str, Any]) -> Any:
        fn = parsed_call.get("function")
        args = parsed_call.get("arguments", {})

        if fn == "send_money":
            return send_money(**args)

        if fn == "check_balance":
            return check_balance()

        return "❌ Unknown function"
