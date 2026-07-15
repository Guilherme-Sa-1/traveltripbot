from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

from app.utils.validators import (
    validate_date,
    validate_positive_integer,
    validate_budget,
)

from app.bot.states import TripState


async def origin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["origin"] = update.message.text

    await update.message.reply_text(
        "Agora informe o destino."
    )

    return TripState.DESTINATION


async def destination(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["destination"] = update.message.text

    await update.message.reply_text(
        "Qual é a data de ida? (dd/mm/aaaa)"
    )

    return TripState.DEPARTURE


async def departure(update, context):

    text = update.message.text

    if not validate_date(text):

        await update.message.reply_text(
            "❌ Data inválida.\n\nUse o formato:\n15/03/2027"
        )

        return TripState.DEPARTURE

    context.user_data["departure"] = text

    await update.message.reply_text(
        "Qual é a data de volta?"
    )

    return TripState.RETURN


async def return_trip(update, context):

    text = update.message.text

    if not validate_date(text):

        await update.message.reply_text(
            "❌ Data inválida."
        )

        return TripState.RETURN

    context.user_data["return_date"] = text

    await update.message.reply_text(
        "Quantos adultos?"
    )

    return TripState.ADULTS


async def adults(update, context):

    text = update.message.text

    if not validate_positive_integer(text):

        await update.message.reply_text(
            "Digite apenas números maiores que zero."
        )

        return TripState.ADULTS

    context.user_data["adults"] = int(text)

    await update.message.reply_text(
        "Qual o orçamento máximo?"
    )

    return TripState.BUDGET


async def budget(update, context):

    text = update.message.text

    if not validate_budget(text):

        await update.message.reply_text(
            "Digite um valor válido."
        )

        return TripState.BUDGET

    context.user_data["budget"] = float(
        text.replace(",", ".")
    )

    data = context.user_data

    await update.message.reply_text(
        f"""
✅ Viagem cadastrada!

Origem: {data['origin']}
Destino: {data['destination']}
Ida: {data['departure']}
Volta: {data['return']}
Adultos: {data['adults']}
Orçamento: R$ {data['budget']:.2f}
"""
    )

    return ConversationHandler.END