import logging

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
from my_enums.commands import CommandEnum


class Commands:
    def __init__(self, language: str = "en"):
        self.data: DataStorage = DataStorage()
        self.data.set_language(language)
        self.command_handler = CommandHandler()
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
        )
        logging.getLogger("httpx").setLevel(logging.WARNING)

        self.logger = logging.getLogger(__name__)

        self.current_state_data = {
            "name": "start",
            "command": CommandEnum.BASIC_COMMAND
        }

    def _calculate_next_state(self, reply_text):
        self.logger.log(logging.INFO, f"Reply text: {reply_text}")
        self.current_state_data["name"] = self.data.get_next_state_name(
            self.current_state_data["name"],
            reply_text
        )

        self.current_state_data["command"] = self.data.get_state_command(
            self.current_state_data["name"]
        )

    def _command_processing(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logger.log(logging.INFO, "!!!!!!!!!!COMMAND PROCESSING!!!!!!!!!!")
        user_message = update.message.text

        self.logger.log(logging.INFO, f"User message: {user_message}")
        self.logger.log(logging.INFO, self.current_state_data)

        # if self.data.get_state_command(self.current_state_data["name"]) == CommandEnum.LANGUAGE_SELECTOR:
        #    self.command_handler.language_selector(user_message)
        # elif self.data.get_state_command(self.current_state_data["name"]) == CommandEnum.MOVE_TO_REAL_CHAT:
        #    self.command_handler.move_to_real_chat(user_message)

        self._calculate_next_state(reply_text=user_message)

        self.logger.log(logging.INFO, f"Next state: {
                        self.current_state_data['name']}")
        self.logger.log(logging.INFO, f"RETURNING 1")
        return 0

    async def basic_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.logger.log(logging.INFO, "!!!!!!!!!!BASIC COMMAND!!!!!!!!!!")
        self._command_processing(update, context)

        text = self.data.get_state_text(self.current_state_data["name"])

        reply_keyboard = [[]]
        for key, value in text.items():
            if "button" in key:
                reply_keyboard[0].append(value["text"])

        await update.message.reply_text(text["text"],
                                        reply_markup=ReplyKeyboardMarkup(
                                            reply_keyboard,
                                            one_time_keyboard=True)
                                        )
        return 0

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user = update.message.from_user
        self.logger.info("User %s canceled the conversation.", user.first_name)

        await update.message.reply_text(
            "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END
