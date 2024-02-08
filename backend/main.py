import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from commands.user import command_user
from commands.hello import hello
from database import database

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Start the database
database.get_engine()

def main():
    print("Starting bot...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("start", command_user))

    app.run_polling()


if __name__ == "__main__":
    main()
