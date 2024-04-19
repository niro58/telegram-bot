import json
from enum import Enum

from my_enums.commands import CommandEnum


class DataStorage:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataStorage, cls).__new__(cls)
            cls.instance.languages = ["cz", "en", "ru", "ua"]
            cls.instance.data = {}
            for language in cls.instance.languages:
                cls.instance.data[language] = {}
                cls.instance.define_insta_reply_data(language)
                cls.instance.define_state_data(language)
            json.dump(cls.instance.data, open("data_defined.json", "w"))

        return cls.instance

    def define_insta_reply_data(self, language: str):
        insta_reply_data = json.load(
            open(f"chat/insta_replies/" + language + ".json", encoding="utf-8"))

        self.data[language]["insta_replies"] = insta_reply_data

    def define_state_data(self, language: str):
        state_data = json.load(
            open(f"chat/states/" + language + ".json", encoding="utf-8"))
        button_data = json.load(open(f"chat/button.json"))
        data = state_data.copy()
        for key, value in state_data.items():
            for key2, value2 in value.items():
                if "button" not in key2:
                    continue

                data[key][key2] = {"text": value2}
                if key in button_data and key2 in button_data[key]:
                    data[key][key2] = data[key][key2] | button_data[key][key2]

        self.data[language]["states"] = data

    def get_state_value(self, key: str, language: str):
        data = None
        if key in self.data[language]["states"]:
            data = self.data[language]["states"][key]
        elif key in self.data[language]["insta_replies"]:
            data = self.data[language]["insta_replies"][key]
        elif data == None:
            return None

        data["key"] = key
        return data

    def get_insta_reply(self, key: str, language: str):
        return self.data[language]["insta_replies"][key]

    def get_button_command(self, state_key, reply_message, language):
        current_state_data = self.get_state_value(state_key, language)

        for key, value in current_state_data.items():
            if "button" in key and value["text"] == reply_message and "command" in value:
                return CommandEnum(value["command"])

        return None

    def get_next_state_key(self, state_key, reply_message, language):
        current_state_data = self.get_state_value(state_key, language)

        for key, value in current_state_data.items():
            if "button" in key and value["text"] == reply_message:
                return value["callback"]

        return state_key
