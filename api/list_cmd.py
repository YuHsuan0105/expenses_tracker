import logging
import re

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

def get_special_time(time: str) -> str:
    if time == "today":
        condi = "created_at = CURRENT_DATE"
    elif time == "week":
        condi = "YEAR(created_at) = YEAR(CURRENT_DATE) and WEEK(created_at) = WEEK(CURRENT_DATE)"
    elif time == "month":
        condi = "YEAR(created_at) = YEAR(CURRENT_DATE) and MONTH(created_at) = MONTH(CURRENT_DATE)"
    elif time == "yesterday":
        condi = "created_at = CURRENT_DATE-1"
    elif time == "last_week":
        condi = "YEAR(created_at) = YEAR(CURRENT_DATE) and WEEK(created_at) = WEEK(CURRENT_DATE)-1"
    elif time == "last_month":
        condi = "YEAR(created_at) = YEAR(CURRENT_DATE) and MONTH(created_at) = MONTH(CURRENT_DATE)-1"
    else:
        raise ValueError
    return condi

def list_cmd(update: Update, context: CallbackContext) -> None:
    try:
        table = str(context.args[0])
        if table not in ["outgo", "income"]:
            raise ValueError
        time1 = str(context.args[1])

        if len(context.args) < 3:
            condi = get_special_time(time1)
        else:
            time2 = str(context.args[2])
            p = re.compile(r'^[0-9]{4}-{0,1}[0-9]{1,2}-{0,1}[0-9]{1,2}$')
            if not (p.match(time1) and p.match(time2)):
                raise ValueError
            condi = f"created_at between '{time1}' and '{time2}'"
        
        logger.info("User %s's input args is valid, connect to database...", update.message.from_user.id)
        # connect to db
        results = database.select(
            table=table,
            user=update.message.from_user.id,
            condition=condi,
        )
        # reply
        if len(results) > 0:
            lines = [f"{table}"]
            for result in results:
                lines.append(f"{result[2]}  {result[1]}  ${result[0]}")
            update.message.reply_text("\n".join(lines))
        else:
            update.message.reply_text("無符合條件的結果")
    except IndexError:
        logger.info("User %s's input args isn't enough", update.message.from_user.id)
        update.message.reply_text('輸入的參數不足，請查看"/help list"')
    except ValueError:
        logger.info("User %s's input args is invalid", update.message.from_user.id)
        update.message.reply_text('格式輸入錯誤，請查看"/help list"')
    except Exception:
        logger.exception(f"unexpected error cause by user {update.message.from_user.id}")
        update.message.reply_text("未預期的錯誤")
    else:
        logger.info("User %s sucessfully exec /list", update.message.from_user.id)

def get_handler() -> CommandHandler:
    return CommandHandler('list', list_cmd)