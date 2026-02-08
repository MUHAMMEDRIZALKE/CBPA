
from app.nl_router.nlu import NLURouter
from app.bot.controller.user.create_user import CreateUser

import logging
logger = logging.getLogger(__name__)

class Handler:

    def __init__(self):
        self.router = NLURouter()

    async def echo(update, context):
        user_details = update.message.from_user
        user_obj = CreateUser(user_details).create_user()
        response = await Handler().router.parse_user_message(update.message.text, str(user_obj.id))
        await update.message.reply_text(response)

    @staticmethod
    async def start(update, context):
        user_details = update.message.from_user
        user_obj = CreateUser(user_details).create_user()
        await update.message.reply_text(
            "Hello! 👋\n\nI am your first Telegram bot."
        )
    
    @staticmethod
    async def help_command(update, context):
        user_details = update.message.from_user
        user_obj = CreateUser(user_details).create_user()
        await update.message.reply_text(
            "Here are the commands you can use:\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n"
            "/set_currency <currency_code> - Set your default currency (e.g. /set_currency USD)"
        )

    @staticmethod
    async def set_currency(update, context):
        user_details = update.message.from_user
        user_obj = CreateUser(user_details).create_user()
        
        if not context.args:
            await update.message.reply_text("Please provide a currency code. Usage: /set_currency USD")
            return

        currency_code = context.args[0]
        from app.bot.controller.user.user_controller import UserController
        controller = UserController(user_obj.id)
        result = controller.set_default_currency(currency_code)
        await update.message.reply_text(result)
    
