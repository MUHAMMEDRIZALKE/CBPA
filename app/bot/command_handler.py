
from app.nl_router.nlu import NLURouter

class Handler:

    def __init__(self):
        self.router = NLURouter()

    async def echo(update, context):
        response = await Handler().router.parse_user_message(update.message.text)
        await update.message.reply_text(response)

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
    
