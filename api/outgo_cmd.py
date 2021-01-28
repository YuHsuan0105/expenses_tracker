import logging

from telegram import (
    Update,
)
from telegram.ext import(
    CallbackContext,
    CommandHandler,
)
from api import database

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# /outgo command
def outgo(update: Update, context: CallbackContext) -> None:
    try:
        money = int(context.args[0])
        cate = str(context.args[1])
        if money <= 0:
            raise ValueError

        logger.info("User %s enter a valid command, insert data into database...", update.message.from_user.id)
        # connect to db
        database.insert(
            table="outgo",
            user=update.message.from_user.id,
            money=money,
            category=cate
        )
        # reply
        update.message.reply_text(f"已新增\n支出 ${money} {cate}")
    except IndexError:
        logger.info("User %s cause a IndexError", update.message.from_user.id)
        update.message.reply_text('輸入的參數不足，請查看"/help outgo"')
    except ValueError:
        logger.info("User %s cause a ValueError", update.message.from_user.id)
        update.message.reply_text('格式輸入錯誤，請查看"/help outgo"')
    except Exception:
        logger.exception(f"unexpected error cause by user {update.message.from_user.id}")
        update.message.reply_text("未預期的錯誤")
    else:
        logger.info("User %s executed /outgo successfully", update.message.from_user.id)

def get_handler() -> CommandHandler:
    return CommandHandler('outgo', outgo)