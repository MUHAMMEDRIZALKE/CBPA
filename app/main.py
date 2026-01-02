import logging

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from app.core.config import settings
from app.bot.command_handler import Handler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

def main():
    app = Application.builder().token(settings.BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, Handler.echo))
    app.add_handler(CommandHandler("start", Handler.start))
    app.add_handler(CommandHandler("help", Handler.help_command))
    app.run_polling()


if __name__ == "__main__":
    main()
