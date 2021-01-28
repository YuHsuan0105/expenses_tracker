import logging

from telegram import (
    Update,
)
from telegram.ext import(
    CallbackContext,
    CommandHandler,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

helptext = {
    "help": ("指令列表：\n"
            "/outgo ： 紀錄支出\n"
            "/income ： 紀錄收入\n"
            "/list ： 查詢紀錄\n"
            "/graph ： 將紀錄以圓餅圖顯示\n\n"
            "可以使用 /help [指令] 來查詢該指令更詳細的介紹\n"
            "ex: /help outgo"),
    "outgo": ("/outgo [金額] [類別]\n"
            "其中金額必須要大於零，而類別會被用來統計花費，會在 /graph 中被使用\n"
            "ex: /outgo 100 lunch"),
    "income": ("/income [金額] [類別]\n"
            "其中金額必須要大於零，而類別會被用來統計收入，會在 /graph 中被使用\n"
            "ex: /income 30000 salary"),
    "list": ("/list [outgo or income] [特殊日期格式]\n"
            "/list [outgo or income] [日期1] [日期2]\n\n"
            "outgo or income 是選擇要查詢支出或收入\n\n"
            "特殊日期是幾個常用的時間區間：\n"
            "today, week, month, yesterday, last_week, last_month\n"
            "分別代表本日、本週、本月、昨日、上週、上個月\n\n"
            "日期1,2是指定的日期，代表查詢日期1到日期2區間中的紀錄\n"
            "日期2必須比日期1大，否則查詢會沒有結果\n"
            "2021-01-01, 2021-1-1, 20210101 都是允許的格式\n\n"
            "ex: /list outgo month or /list outgo 2021-01-01 2021-01-31"),
    "graph": "/graph [outgo or income] [特殊日期格式]\n"
            "/graph [outgo or income] [日期1] [日期2]\n\n"
            "outgo or income 是選擇要查詢支出或收入\n\n"
            "特殊日期是幾個常用的時間區間：\n"
            "today, week, month, yesterday, last_week, last_month\n"
            "分別代表本日、本週、本月、昨日、上週、上個月\n\n"
            "日期1,2是指定的日期，代表查詢日期1到日期2區間中的紀錄\n"
            "日期2必須比日期1大，否則查詢會沒有結果\n"
            "2021-01-01, 2021-1-1, 20210101 都是允許的格式\n\n"
            "ex: /graph outgo month or /graph outgo 2021-01-01 2021-01-31",
}

# /help command
def help_cmd(update: Update, context: CallbackContext) -> None:
    try:
        if len(context.args) == 0:
            update.message.reply_text(helptext["help"])
        else:
            switch = str(context.args[0])
            if switch not in helptext:
                raise ValueError
            update.message.reply_text(helptext[switch])
    except ValueError:
        logger.info("User %s cause a ValueError", update.message.from_user.id)
        update.message.reply_text('你輸入的參數不正確，請查看"/help"')
    except Exception:
        logger.exception(f"unexpected error cause by user {update.message.from_user.id}")
        update.message.reply_text("未預期的錯誤")
    else:
        logger.info("User %s executed /help successfully", update.message.from_user.id)

def get_handler() -> CommandHandler:
    return CommandHandler('help', help_cmd)