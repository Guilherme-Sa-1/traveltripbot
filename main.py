import os

from dotenv import load_dotenv

from telegram.ext import (Application,CommandHandler,)

from app.bot.commands import start

load_dotenv()

TOKEN=os.getenv("TELEGRAM_TOKEN")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start",start))

    print("Bot iniciado!")

    app.run_polling()


if __name__ == "__main__":
    main()