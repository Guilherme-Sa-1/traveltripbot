import os

from dotenv import load_dotenv

from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.bot.commands import (
    start,
    new_trip,
    cancel,
)

from app.bot.handlers import (
    origin,
    destination,
    departure,
    return_trip,
    adults,
    budget,
)

from app.bot.states import TripState

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")


def main():
    app = Application.builder().token(TOKEN).build()

    conversation = ConversationHandler(
        entry_points=[
            CommandHandler("nova", new_trip),
        ],
        states={
            TripState.ORIGIN: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, origin)
            ],
            TripState.DESTINATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, destination)
            ],
            TripState.DEPARTURE_DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, departure)
            ],
            TripState.RETURN_DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, return_trip)
            ],
            TripState.ADULTS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, adults)
            ],
            TripState.BUDGET: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, budget)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
        ],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conversation)

    print("🤖 TripBot iniciado com sucesso!")

    app.run_polling()


if __name__ == "__main__":
    main()