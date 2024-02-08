from telegram.ext import ContextTypes
from telegram import Update
from database import database


class User:
    def __init__(self, id: int, first_name: str, last_name: str, username: str) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username

    def __str__(self) -> str:
        return f"User(id = {self.id}, first_name = {self.first_name}, last_name = {self.last_name}, username = {self.username})"

    def mention_markdown_v2(self) -> str:
        return f"[{self.first_name}](tg://user?id={self.id})"


async def command_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = User(update.effective_user.id, update.effective_user.first_name,
                update.effective_user.last_name, update.effective_user.username)

    try:
        database.create_user(user.id, user.first_name, user.last_name, user.username)
    except Exception as e:
        print(f"An error occurred while creating the user: {e}")


    try:
        saved_user = database.get_user(user.id)

        await update.message.reply_markdown_v2(
            fr"Hi {saved_user.first_name}",
        )
    except Exception as e:
        print(f"An error occurred while retrieving the user: {e}")

    # Debugging
    print(user)
