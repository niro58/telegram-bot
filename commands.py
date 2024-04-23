import asyncio
import logging
import os

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
)

from command_handler import CommandHandler
from config.data import DataStorage
from config.user_data import User, UserData
from my_enums.commands import CommandEnum


class Commands:

    def __init__(self, language: str = "en"):
        self.image_folder = "./public"
        self.data: DataStorage = DataStorage()
        self.user_data: UserData = UserData()
        self.command_handler = CommandHandler()
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
        )
        logging.getLogger("httpx").setLevel(logging.WARNING)

        self.logger = logging.getLogger(__name__)

    async def _process_reply(self, user: User, reply_message: str):
        next_state_key = self.data.get_next_state_key(
            user.state,
            reply_message,
            user.language
        )

        button_command = self.data.get_button_command(
            user.state,
            reply_message,
            user.language
        )
        self.logger.log(logging.INFO, f"Reply message: {reply_message}")
        self.logger.log(logging.INFO, f"Next state key: {next_state_key}")
        self.logger.log(logging.INFO, f"Button command: {button_command}")

        if button_command == None:
            user.state = next_state_key
            user.reply_message_state = user.state
        elif button_command == CommandEnum.TEXT_PRINT:
            user.reply_message_state = next_state_key

        elif button_command == CommandEnum.LANGUAGE_SELECTOR:
            if reply_message == "Русский":
                user.language = "ru"
            elif reply_message == "Український":
                user.language = "ua"
            elif reply_message == "Čeština":
                user.language = "cz"
            else:
                user.language = "en"
            user.state = next_state_key
            user.reply_message_state = user.state
        elif button_command == CommandEnum.MOVE_TO_REAL_CHAT:
            self.command_handler.move_to_real_chat()

        self.user_data.update_user(user)

    async def _command_processing(self, user: User, update: Update, context: ContextTypes.DEFAULT_TYPE):

        user_message = update.message.text

        self.logger.log(logging.INFO, f"User message: {user_message}")

        await self._process_reply(user, user_message)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        self.logger.log(logging.INFO, "Start command")

        user = self.user_data.reset_user(
            update.message.chat_id,
            update.message.from_user.username
        )

        user_state = self.data.get_state_value(
            user.state,
            user.language
        )
        user_reply_state = self.data.get_state_value(
            user.reply_message_state,
            user.language
        )
        max_columns = 3
        index = 0
        reply_keyboard = []
        for key, value in user_state.items():
            if len(reply_keyboard) == index:
                reply_keyboard.append([])
            if "button" in key:
                reply_keyboard[index].append(value["text"])
            if len(reply_keyboard[index]) == max_columns:
                index += 1

        if "image" in user_state:
            await context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo=os.path.join(self.image_folder, user_state["image"])
            )
        print("SENDING TEXT AFTER IMAGE")
        await update.message.reply_text(
            user_reply_state["text"],
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True,
                resize_keyboard=True
            )
        )
        return 1

    async def basic_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logger.log(logging.INFO, "Basic command")
        user = self.user_data.get_user(update.message.chat_id)

        if user is None:
            return await self.start(update, context)

        await self._command_processing(user, update, context)

        user_state = self.data.get_state_value(
            user.state,
            user.language
        )
        user_reply_state = self.data.get_state_value(
            user.reply_message_state,
            user.language
        )

        max_columns = 3
        index = 0
        reply_keyboard = []
        for key, value in user_state.items():
            if len(reply_keyboard) == index:
                reply_keyboard.append([])
            if "button" in key:
                reply_keyboard[index].append(value["text"])
            if len(reply_keyboard[index]) == max_columns:
                index += 1
        print(user_reply_state)
        if "image" in user_reply_state:
            await context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo=os.path.join(self.image_folder,
                                   user_reply_state["image"])
            )
        await update.message.reply_text(
            user_reply_state["text"],
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True,
                resize_keyboard=True
            )
        )
        return 1

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user = update.message.from_user
        self.logger.info("User %s canceled the conversation.", user.first_name)

        await update.message.reply_text(
            "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END
