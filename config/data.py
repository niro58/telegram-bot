import json

from my_enums.commands import CommandEnum


class DataStorage:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataStorage, cls).__new__(cls)
            cls.instance.text_data = {}
            cls.instance.button_data = {}
            cls.instance.command_data = {}

        return cls.instance

    def set_language(self, language: str):
        self.text_data = json.load(open(f"chat/" + language + ".json"))
        self.button_data = json.load(open(f"chat/button.json"))
        self.command_data = json.load(open(f"chat/command_enum_value.json"))

    def get_state_text(self, name: str):
        res = self.text_data[name].copy()
        button = self.button_data[name].copy()
        for key, value in button.items():
            res[key] = {
                "text": res[key],
                "callback": value["callback"]
            }

        return res

    def get_all(self):
        res = self.text_data
        for key, value in self.button_data.items():
            for key2, value2 in value.items():
                res[key][key2] = {
                    "text": res[key][key2],
                    "callback": value2["callback"]
                }
        return res

    def get_state_names(self):
        states = []
        for key in self.text_data.keys():
            states.append(key)
        return states

    def get_next_state_name(self, current_state, reply_text):
        current_state_data = self.get_state_text(current_state)

        for key, value in current_state_data.items():
            if "button" in key and value["text"] == reply_text:
                return value["callback"]
        return current_state

    def get_state_command(self, state: str):
        return self.command_data[state] if state in self.command_data else CommandEnum.BASIC_COMMAND.value
