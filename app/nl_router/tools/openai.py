
STD_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_expense",
            "description": "Add an expense transaction",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "description": "Amount spent"},
                    "description": {"type": "string", "description": "Description of the expense"},
                    "currency_code": {"type": "string", "description": "Currency code (e.g., USD, EUR). Optional if default set."},
                    "category": {"type": "string", "description": "Category of expense (e.g., food, transport). Optional."},
                    "date": {"type": "string", "description": "Date of transaction (YYYY-MM-DD). Optional."}
                },
                "required": ["amount", "description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_income",
            "description": "Add an income transaction",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "description": "Amount earned"},
                    "description": {"type": "string", "description": "Source of income"},
                    "currency_code": {"type": "string", "description": "Currency code. Optional."},
                    "category": {"type": "string", "description": "Category (e.g., salary, gift). Optional."},
                    "date": {"type": "string", "description": "Date of transaction. Optional."}
                },
                "required": ["amount", "description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_analytics",
            "description": "Get expense analytics for a time range. You can specify a preset time_range OR a custom date range (start_date and end_date).",
            "parameters": {
                "type": "object",
                "properties": {
                    "time_range": {"type": "string", "enum": ["current_month", "last_month", "today"], "description": "Preset time range. Default is current_month."},
                    "start_date": {"type": "string", "description": "Start date for custom range (YYYY-MM-DD). Optional."},
                    "end_date": {"type": "string", "description": "End date for custom range (YYYY-MM-DD). Optional."}
                },
                "required": []
            }
        }
    }
]
