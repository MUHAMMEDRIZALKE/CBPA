


class Handler:

    @staticmethod
    async def echo(update, context):
        await update.message.reply_text(update.message.text)

    @staticmethod
    async def start(update, context):
        await update.message.reply_text(
            "Hello! 👋\n\nI am your first Telegram bot."
        )
    
    @staticmethod
    async def help_command(update, context):
        await update.message.reply_text(
            "Here are the commands you can use:\n"
            "/start - Start the bot\n"
            "/help - Show this help message"
        )
    
