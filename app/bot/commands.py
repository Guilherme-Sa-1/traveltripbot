from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

from app.bot.states import TripState


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Bem-vindo, Guilherme!!\n\n"
        "Use /nova para cadastrar uma viagem."
    )


async def new_trip(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(
        "✈️ Vamos cadastrar uma nova viagem!\n\n"
        "Qual é a cidade de origem?"
    )

    return TripState.ORIGIN


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(
        "Operação cancelada."
    )

    return ConversationHandler.END