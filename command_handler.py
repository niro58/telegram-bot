from telegram import Update
from telegram.ext import ContextTypes

from config.data import DataStorage


class CommandHandler:

    async def print_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=message)

    def move_to_real_chat(self, context):
        pass
