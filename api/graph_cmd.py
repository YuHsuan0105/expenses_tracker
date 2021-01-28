import logging
import re
from typing import Tuple
import os

from telegram import (
    Update,
)
from telegram.ext import(
    CallbackContext,
    CommandHandler,
)
import matplotlib.pyplot as plt

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

def count(filepath: str, data: Tuple[int,str,str]) -> int:
    catemap = {}
    total = 0
    for d in data:
        total += d[0]
        if d[1] in catemap:
            catemap[d[1]] += d[0]
        else:    
            catemap[d[1]] = d[0]

    sizes = [v for k,v in catemap.items()]
    labels = [k for k,v in catemap.items()]
    
    fig1, ax1 = plt.subplots(figsize=(4, 3))
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax1.axis('equal')

    fig1.savefig(
        filepath,
        bbox_inches='tight',
        pad_inches=0.0
    )
    return total

def graph(update: Update, context: CallbackContext) -> None:
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
            time1 = time1+" ~ "+time2
        
        logger.info("User %s's input args is valid, connect to database...", update.message.from_user.id)
        # connect to db
        results = database.select(
            table=table,
            user=update.message.from_user.id,
            condition=condi,
        )
        # deal with reply
        if len(results) > 0:
            # set image path
            imgdir = "./tmp"
            if not os.path.isdir(imgdir):
                os.mkdir(imgdir)
            imgpath = f"{imgdir}/{update.message.from_user.id}.png"
            # count data
            total = count(imgpath, results)
            # reply
            update.message.reply_photo(open(imgpath,"rb"))
            update.message.reply_text(f"{table}\n總計 ${total}\n日期 {time1}")
            # cleanup
            os.remove(imgpath)
        else:
            update.message.reply_text("無符合條件的結果")
    except IndexError:
        logger.info("User %s's input args isn't enough", update.message.from_user.id)
        update.message.reply_text('輸入的參數不足，請查看"/help graph"')
    except ValueError:
        logger.info("User %s's input args is invalid", update.message.from_user.id)
        update.message.reply_text('格式輸入錯誤，請查看"/help graph"')
    except OSError:
        logger.exception("User %s get error while saving or cleaning image", update.message.from_user.id)
    except Exception:
        logger.exception(f"unexpected error cause by user {update.message.from_user.id}")
        update.message.reply_text("未預期的錯誤")
    else:
        logger.info("User %s executed /graph sucessfully", update.message.from_user.id)

def get_handler() -> CommandHandler:
    return CommandHandler('graph', graph)