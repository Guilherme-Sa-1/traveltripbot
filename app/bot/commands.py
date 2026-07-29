from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from app.bot.states import TripState
from app.services.trip_service import TripService

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bem-vindo, Guilherme!!\n\n"
        "Use /nova para cadastrar uma viagem.\n"
        "Use /listar para ver suas viagens."
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

async def list_trips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    service = TripService()
    trips = service.get_all_trips()
    
    if not trips:
        await update.message.reply_text("Você ainda não tem nenhuma viagem cadastrada. Use /nova para começar!")
        return

    response = "✈️ *Suas Viagens Cadastradas:*\n\n"
    for trip in trips:
        response += (
            f"🔹 *ID:* {trip.id}\n"
            f"📍 {trip.origin} ➔ {trip.destination}\n"
            f"📅 Ida: {trip.departure_date} | Volta: {trip.return_date}\n"
            f"💰 Orçamento: R$ {trip.budget:.2f}\n"
            "──────────────\n"
        )
    
    await update.message.reply_text(response, parse_mode="Markdown")

async def remove_trip(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Por favor, informe o ID da viagem.\nExemplo: /remover 1")
        return

    try:
        trip_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("O ID deve ser um número inteiro.")
        return

    service = TripService()
    success = service.remove_trip(trip_id)

    if success:
        await update.message.reply_text(f"✅ Viagem {trip_id} removida com sucesso!")
    else:
        await update.message.reply_text(f"❌ Nenhuma viagem encontrada com o ID {trip_id}.")

async def edit_trip(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 2:
        await update.message.reply_text(
            "⚠️ Uso correto: /editar <ID> <Novo Orçamento>\n"
            "Exemplo: /editar 1 5500"
        )
        return

    try:
        trip_id = int(context.args[0])
        
        new_budget = float(context.args[1].replace(",", "."))
    except ValueError:
        await update.message.reply_text("❌ Erro: Certifique-se de que o ID e o orçamento sejam números.")
        return

    service = TripService()
    success = service.update_trip_budget(trip_id, new_budget)

    if success:
        await update.message.reply_text(f"✅ Orçamento da viagem {trip_id} atualizado para R$ {new_budget:.2f}!")
    else:
        await update.message.reply_text(f"❌ Nenhuma viagem encontrada com o ID {trip_id}.")


async def search_trip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Informe o ID da viagem.\nExemplo: /buscar 1")
        return

    try:
        trip_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ O ID deve ser um número inteiro.")
        return

    aguarde_msg = await update.message.reply_text("🔍 Buscando voos no Google Flights... Isso pode levar alguns segundos.")

    service = TripService()
    resultado = service.search_flights_for_trip(trip_id)

    await aguarde_msg.delete()

    if not resultado["success"]:
        await update.message.reply_text(f"❌ Ops: {resultado['error']}")
        return

    trip = resultado["trip"]
    preco = resultado["price"]
    companhia = resultado["airline"]
    orcamento = trip.budget

    mensagem = (
        f"✈️ *Melhor Voo Encontrado!*\n\n"
        f"📍 {trip.origin} ➔ {trip.destination}\n"
        f"🏢 Companhia: {companhia}\n"
        f"💰 Preço atual: R$ {preco:.2f}\n"
        f"🎯 Seu orçamento: R$ {orcamento:.2f}\n"
        "──────────────\n"
    )

    if preco <= orcamento:
        mensagem += "✅ *OBA! O preço está dentro do seu orçamento!*"
    else:
        diferenca = preco - orcamento
        mensagem += f"⚠️ *Alerta:* R$ {diferenca:.2f} ACIMA do orçamento."

    await update.message.reply_text(mensagem, parse_mode="Markdown")