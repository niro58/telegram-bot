import json

# from my_enums.commands import CommandEnum
from enum import Enum


class CommandEnum(Enum):
    BASIC_COMMAND = 0,
    LANGUAGE_SELECTOR = 1,
    MOVE_TO_REAL_CHAT = 2,
    TEXT_PRINT = 3,

# todo: rework names, functions


class DataStorage:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataStorage, cls).__new__(cls)
            cls.instance.data = {}

        return cls.instance

    def set_language(self, language: str):
        text_data = json.load(
            open(f"chat/" + language + ".json", encoding="utf-8"))
        button_data = json.load(open(f"chat/button.json"))
        data = text_data.copy()
        for key, value in text_data.items():
            for key2, value2 in value.items():
                if "button" not in key2:
                    continue

                data[key][key2] = {"text": value2}
                if key in button_data and key2 in button_data[key]:
                    data[key][key2] = data[key][key2] | button_data[key][key2]

        self.data = data

    def get_state_value(self, name: str):
        return self.data[name]

    def get_all(self):
        return self.data

    def get_state_keys(self):
        return list(self.data.keys())

    def get_next_state_key(self, state_key, choice):
        current_state_data = self.get_state_value(state_key)

        for key, value in current_state_data.items():
            if "button" in key and value["text"] == choice:
                return value["callback"]

        return state_key


data = DataStorage()
data.set_language("en")
print(data.get_state_value("start"))
