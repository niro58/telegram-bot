from os import environ as env

from dotenv import load_dotenv
from handlers.reply_handler import ReplyHandler
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)


def main():
    load_dotenv()

    application = Application.builder().token(env.get("TELEGRAM_API_KEY")).build()
    commands = ReplyHandler()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", commands.start)],
        states={
            1: [
                CommandHandler("start", commands.start),
                MessageHandler(filters.TEXT, commands.basic_command)
            ],
        },
        fallbacks=[CommandHandler("cancel", commands.cancel)],
    )
    application.add_handler(conv_handler)

    application.run_polling()


main()
