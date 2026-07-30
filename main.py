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
    list_trips,
    remove_trip,
    edit_trip,
    search_trip,
    start_alerts,
    receive_origin,
    receive_destination,
    receive_departure,
    receive_return,
    receive_adults,
    receive_budget,
    ORIGEM,
    DESTINO,
    DATA_IDA,
    DATA_VOLTA,
    ADULTOS,
    ORCAMENTO,
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
from app.database.database import engine
from app.database.models import Base



load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

def main():
    Base.metadata.create_all(bind=engine)
    app = Application.builder().token(TOKEN).build()
    
    conversation = ConversationHandler(
        entry_points=[CommandHandler("nova", new_trip)],
        states={
            ORIGEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_origin)],
            DESTINO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_destination)],
            DATA_IDA: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_departure)],
            DATA_VOLTA: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_return)],
            ADULTOS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_adults)],
            ORCAMENTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_budget)],
        },
        fallbacks=[CommandHandler("cancelar", cancel)]
    )
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("listar", list_trips))
    app.add_handler(CommandHandler("remover", remove_trip))
    app.add_handler(CommandHandler("editar", edit_trip))
    app.add_handler(CommandHandler("buscar", search_trip))
    app.add_handler(CommandHandler("alertas", start_alerts))
    app.add_handler(conversation)
    
    print("🤖 TripBot iniciado com sucesso!")
    app.run_polling()

if __name__ == "__main__":
    main()