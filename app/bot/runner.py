import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from app.core.config import settings
from app.bot.command_handler import Handler

logger = logging.getLogger(__name__)

def run_bot():
    """Builds and runs the Telegram bot application."""
    app = Application.builder().token(settings.BOT_TOKEN).build()
    
    # Register handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, Handler.echo))
    app.add_handler(CommandHandler("start", Handler.start))
    app.add_handler(CommandHandler("help", Handler.help_command))
    
    logger.info("Starting bot polling...")
    app.run_polling()
