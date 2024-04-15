from os import environ as env

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from commands import Commands


def main():
    load_dotenv()

    application = Application.builder().token(env.get("TELEGRAM_API_KEY")).build()
    commands = Commands()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", commands.basic_command)],
        states={
            0: [MessageHandler(None, commands.basic_command)],
        },
        fallbacks=[CommandHandler("cancel", commands.cancel)],
    )
    application.add_handler(conv_handler)

    application.run_polling()


main()
