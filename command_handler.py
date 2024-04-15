from config.data import DataStorage


class CommandHandler:
    def select_language(self, language):
        DataStorage().set_language(language)

    def print_message(self, context, message):
        pass

    def move_to_real_chat(self, context):
        pass
