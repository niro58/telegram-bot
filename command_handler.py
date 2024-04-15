from config.data import DataStorage


class CommandHandler:
    def language_selector(self, language):
        DataStorage().set_language(language)

    def move_to_real_chat(self, context):
        pass
