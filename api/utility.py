import logging

from telegram import (
    Update,
)
from telegram.ext import(
    CallbackContext,
    MessageHandler,
    Filters,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# handler that reply illegal command
def unknown_handler() -> MessageHandler:
    def unknown(update: Update, context: CallbackContext) -> int:
        logger.info("unknown is called")
        msg = '未知的指令\n請查看/help'
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    return MessageHandler(Filters.command, unknown)

# error handler
def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

