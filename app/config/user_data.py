import json
import os
import time
from dataclasses import dataclass


@dataclass
class User:
    username: str
    chat_id: int
    language: str
    state: str
    reply_message_state: str
    last_message_timestamp: int


class UserData:
    def __init__(self):
        self.filepath = "app/data/user_data.json"
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
            last_message_timestamp=data["last_message_timestamp"]
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
            "last_message_timestamp": time.time(),
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
            last_message_timestamp=int(time.time())
        )
        self.users[chat_id] = {
            "username": user.username,
            "language": user.language,
            "state": user.state,
            "reply_message_state": user.reply_message_state,
            "last_message_timestamp": user.last_message_timestamp,
        }
        self.save_users()
        return user

    def load_users(self):
        if not os.path.exists(self.filepath):
            json.dump({}, open(self.filepath, "w"))

        self.users = json.load(
            open(self.filepath, encoding="utf-8"))
        self.users = {int(k): v for k, v in json.load(
            open(self.filepath, encoding="utf-8")).items()}

    def save_users(self):
        json.dump(self.users, open(self.filepath, "w"))
