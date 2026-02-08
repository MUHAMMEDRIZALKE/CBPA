from typing import Any, Dict
from app.bot.controller.expense.transaction_controller import TransactionController, TransactionType


class FunctionRouter:
    @staticmethod
    def call_function(parsed_call: Dict[str, Any], user_id: str) -> Any:
        fn = parsed_call.get("function")
        args = parsed_call.get("arguments", {})
        
        controller = TransactionController(user_id=user_id)

        if fn == "add_expense":
            return controller.add_transaction(
                amount=args.get("amount"),
                description=args.get("description"),
                transaction_type=TransactionType.EXPENSE,
                currency_code=args.get("currency_code"),
                category=args.get("category"),
                date=args.get("date")
            )
        
        if fn == "add_income":
            return controller.add_transaction(
                amount=args.get("amount"),
                description=args.get("description"),
                transaction_type=TransactionType.INCOME,
                currency_code=args.get("currency_code"),
                category=args.get("category"),
                date=args.get("date")
            )
            
        if fn == "get_analytics":
            return controller.get_analytics(time_range=args.get("time_range"))

        return "❌ Unknown function"
