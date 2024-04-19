import json
import os
from dataclasses import dataclass


@dataclass
class User:
    username: str
    chat_id: int
    language: str
    state: str
    reply_message_state: str


class UserData:
    def __init__(self):
        self.load_users()

    def get_user(self, chat_id: int) -> User:
        data = self.users.get(chat_id)
        if not data:
            return None
        user = User(
            username=data["username"],
            chat_id=chat_id,
            language=data["language"],
            state=data["state"],
            reply_message_state=data["reply_message_state"],
        )
        return user

    def update_user(self, user: User):
        if user.chat_id in self.users:
            self.users.pop(user.chat_id)

        self.users[user.chat_id] = {
            "username": user.username,
            "language": user.language,
            "state": user.state,
            "reply_message_state": user.reply_message_state,
        }
        self.save_users()

    def reset_user(self, chat_id: int, username: str):
        self.remove_user(chat_id)
        user = self.create_user(
            chat_id,
            username
        )
        return user

    def remove_user(self, chat_id: int):
        try:
            self.users.pop(chat_id)
            self.save_users()
        except KeyError:
            pass

    def create_user(self, chat_id: int, username: str):
        user = User(
            username=username,
            chat_id=chat_id,
            language="en",
            state="start",
            reply_message_state="start",
        )
        self.users[chat_id] = {
            "username": user.username,
            "language": user.language,
            "state": user.state,
            "reply_message_state": user.reply_message_state,
        }
        self.save_users()
        return user

    def load_users(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists("data/user_data.json"):
            json.dump({}, open("data/user_data.json", "w"))

        self.users = json.load(open("data/user_data.json", encoding="utf-8"))
        self.users = {int(k): v for k, v in json.load(
            open("data/user_data.json", encoding="utf-8")).items()}

    def save_users(self):
        json.dump(self.users, open("data/user_data.json", "w"))
