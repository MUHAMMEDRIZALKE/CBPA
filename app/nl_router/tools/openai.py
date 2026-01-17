
STD_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "send_money",
            "description": "Send money to a person",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "Amount of money to send"
                    },
                    "recipient": {
                        "type": "string",
                        "description": "Who receives the money"
                    },
                    "date": {
                        "type": "string",
                        "description": "When to send the money"
                    }
                },
                "required": ["amount", "recipient", "date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_balance",
            "description": "Check the user's account balance",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]
