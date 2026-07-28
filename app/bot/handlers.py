from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from app.utils.validators import (
    validate_date,
    validate_positive_integer,
    validate_budget,
)
from app.bot.states import TripState
from app.services.trip_service import TripService

async def origin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["origin"] = update.message.text
    await update.message.reply_text("Agora informe o destino.")
    return TripState.DESTINATION

async def destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["destination"] = update.message.text
    await update.message.reply_text("Qual a data de ida? (dd/mm/aaaa)")
    return TripState.DEPARTURE_DATE

async def departure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if not validate_date(text):
        await update.message.reply_text("Data inválida.\n\nUse o formato:\n15/03/2027")
        return TripState.DEPARTURE_DATE
        
    context.user_data["departure_date"] = text
    await update.message.reply_text("Qual a data de volta?")
    return TripState.RETURN_DATE

async def return_trip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if not validate_date(text):
        await update.message.reply_text("Data inválida. Use o formato: 15/03/2027")
        return TripState.RETURN_DATE
        
    # Validação para impedir que a volta seja antes da ida
    departure_date = datetime.strptime(context.user_data["departure_date"], "%d/%m/%Y")
    return_date = datetime.strptime(text, "%d/%m/%Y")
    
    if return_date < departure_date:
        await update.message.reply_text("A data de volta não pode ser anterior à data de ida. Tente novamente.")
        return TripState.RETURN_DATE
        
    context.user_data["return_date"] = text
    await update.message.reply_text("Quantos adultos?")
    return TripState.ADULTS

async def adults(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if not validate_positive_integer(text):
        await update.message.reply_text("Digite apenas números maiores que zero.")
        return TripState.ADULTS
        
    context.user_data["adults"] = int(text)
    await update.message.reply_text("Qual o orçamento máximo?")
    return TripState.BUDGET

async def budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if not validate_budget(text):
        await update.message.reply_text("Digite um valor válido.")
        return TripState.BUDGET
        
    context.user_data["budget"] = float(text.replace(",", "."))
    data = context.user_data
    
    service = TripService()
    service.register_trip(data)
    
    await update.message.reply_text(
        f"Viagem cadastrada com sucesso!\n\n"
        f"Origem: {data['origin']}\n"
        f"Destino: {data['destination']}\n"
        f"Ida: {data['departure_date']}\n"
        f"Volta: {data['return_date']}\n"
        f"Adultos: {data['adults']}\n"
        f"Orçamento: R$ {data['budget']:.2f}"
    )
    
    return ConversationHandler.END