import os

from telegram.ext import Updater

from api import(
    utility,
    outgo_cmd,
    income_cmd,
    list_cmd,
)

def main() -> None:
    # create updater and get dispatcher to register handler
    udr = Updater(
        token=os.environ['BOT_TOKEN'],
        use_context=True
    )
    dpr = udr.dispatcher

    dpr.add_handler(outgo_cmd.get_handler())
    dpr.add_handler(income_cmd.get_handler())
    dpr.add_handler(list_cmd.get_handler())
    # must be last added
    dpr.add_handler(utility.unknown_handler())

    # add error handler
    dpr.add_error_handler(utility.error_handler)

    # start the bot
    udr.start_polling()
    udr.idle()

if __name__ == "__main__":
    main()
