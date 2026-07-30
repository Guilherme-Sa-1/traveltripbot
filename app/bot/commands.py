import os
import requests
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from app.services.trip_service import TripService

ORIGEM, DESTINO, DATA_IDA, DATA_VOLTA, ADULTOS, ORCAMENTO = range(6)

def buscar_sigla(cidade: str) -> str | None:
    api_key = os.environ.get("SERPAPI_KEY") 
    url = f"https://serpapi.com/search.json?engine=google_flights_autocomplete&q={cidade}&hl=pt-BR&api_key={api_key}"
    
    try:
        resposta = requests.get(url).json()
        sugestoes = resposta.get("suggestions", [])
        
        if sugestoes:
            # Pega o primeiro aeroporto da primeira sugestão de cidade
            aeroportos = sugestoes[0].get("airports", [])
            if aeroportos:
                return aeroportos[0].get("id") # Retorna "FOR"
    except Exception as e:
        print(f"Erro ao buscar sigla para {cidade}: {e}")
        
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá! Eu sou seu monitor de passagens aéreas.\n\n"
        "Comandos disponíveis:\n"
        "/nova - Cadastrar uma nova viagem\n"
        "/listar - Ver suas viagens\n"
        "/buscar <id> - Buscar voos agora\n"
        "/editar <id> <novo_orcamento> - Editar limite de preço\n"
        "/remover <id> - Apagar uma viagem\n"
        "/alertas - Ligar o despertador automático"
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operação cancelada.")
    return ConversationHandler.END


async def list_trips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    service = TripService()
    trips = service.get_all_trips()
    
    if not trips:
        await update.message.reply_text("Você ainda não tem viagens cadastradas.")
        return

    msg = "Suas viagens:\n\n"
    for t in trips:
        msg += f"ID: {t.id} | {t.origin} ➔ {t.destination}\nDatas: {t.departure_date} a {t.return_date}\nOrçamento: R$ {t.budget:.2f}\n\n"
    
    await update.message.reply_text(msg)

async def remove_trip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Informe o ID. Ex: /remover 1")
        return
        
    try:
        trip_id = int(context.args[0])
        service = TripService()
        if service.delete_trip(trip_id):
            await update.message.reply_text("✅ Viagem removida com sucesso!")
        else:
            await update.message.reply_text("❌ ID não encontrado.")
    except ValueError:
        await update.message.reply_text("❌ O ID deve ser um número.")

async def edit_trip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Use o formato: /editar <id> <novo_orcamento>")
        return
        
    try:
        trip_id = int(context.args[0])
        new_budget = float(context.args[1])
        service = TripService()
        if service.update_budget(trip_id, new_budget):
            await update.message.reply_text(f"✅ Orçamento da viagem {trip_id} atualizado para R$ {new_budget:.2f}!")
        else:
            await update.message.reply_text("❌ ID não encontrado.")
    except ValueError:
        await update.message.reply_text("❌ Parâmetros inválidos. Digite apenas números.")


async def new_trip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("De qual cidade você vai sair? (Ex: São Paulo)")
    return ORIGEM

async def receive_origin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cidade = update.message.text.strip()
    aguarde = await update.message.reply_text(f"🔍 Buscando a sigla do aeroporto para {cidade}...")
    
    sigla = buscar_sigla(cidade)
    if not sigla:
        await aguarde.edit_text("❌ Não encontrei aeroporto para essa cidade. Tente digitar de outra forma (Ex: São Paulo).")
        return ORIGEM
        
    context.user_data['origem'] = sigla
    await aguarde.edit_text(f"✅ Aeroporto encontrado: *{sigla}*.\n\nPara qual cidade você quer ir?", parse_mode="Markdown")
    return DESTINO

async def receive_destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cidade = update.message.text.strip()
    aguarde = await update.message.reply_text(f"🔍 Buscando a sigla do aeroporto para {cidade}...")
    
    sigla = buscar_sigla(cidade)
    if not sigla:
        await aguarde.edit_text("❌ Não encontrei aeroporto para essa cidade. Tente digitar de outra forma.")
        return DESTINO
        
    context.user_data['destino'] = sigla
    await aguarde.edit_text(f"✅ Aeroporto encontrado: *{sigla}*.\n\nQual a data de ida? (DD/MM/AAAA)", parse_mode="Markdown")
    return DATA_IDA

async def receive_departure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['ida'] = update.message.text.strip()
    await update.message.reply_text("Qual a data de volta? (DD/MM/AAAA)")
    return DATA_VOLTA

async def receive_return(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['volta'] = update.message.text.strip()
    await update.message.reply_text("Quantos adultos irão viajar?")
    return ADULTOS

async def receive_adults(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['adultos'] = int(update.message.text)
        await update.message.reply_text("Qual o seu orçamento MÁXIMO total? (Ex: 2500.50)")
        return ORCAMENTO
    except ValueError:
        await update.message.reply_text("❌ Por favor, digite um número inteiro para a quantidade de adultos.")
        return ADULTOS

async def receive_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['orcamento'] = float(update.message.text)
        
        service = TripService()
        service.add_trip(
            origin=context.user_data['origem'],
            destination=context.user_data['destino'],
            departure_date=context.user_data['ida'],
            return_date=context.user_data['volta'],
            adults=context.user_data['adultos'],
            budget=context.user_data['orcamento']
        )
        
        await update.message.reply_text("✅ Viagem cadastrada com sucesso! Use /alertas para monitorar ou /buscar <id> para testar agora.")
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("❌ Por favor, digite um número válido para o orçamento (Ex: 1500.00).")
        return ORCAMENTO


async def search_trip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Informe o ID da viagem.\nExemplo: /buscar 1")
        return

    try:
        trip_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ O ID deve ser um número inteiro.")
        return

    aguarde_msg = await update.message.reply_text("🔍 Buscando as melhores datas flexíveis... Isso vai demorar um pouquinho.")

    service = TripService()
    resultado = service.search_flights_for_trip(trip_id)
    await aguarde_msg.delete()

    if not resultado["success"]:
        await update.message.reply_text(f"❌ Ops: {resultado['error']}")
        return

    trip = resultado["trip"]
    preco = resultado["price"]

    mensagem = (
        f"✈️ *Melhor Voo Encontrado (Datas Flexíveis)*\n\n"
        f"📍 {resultado['origin_name']} ({trip.origin}) ➔ {resultado['destination_name']} ({trip.destination})\n"
        f"📅 Data ideal: {resultado['date']}\n"
        f"🏢 Companhia: {resultado['airline']}\n"
        f"💰 Preço atual: R$ {preco:.2f}\n"
        f"🎯 Seu orçamento: R$ {trip.budget:.2f}\n\n"
        f"[🔗 Ver Voo no Google Flights]({resultado['link']})\n"
    )

    if preco <= trip.budget:
        mensagem += "\n✅ *OBA! O preço está dentro do seu orçamento!*"
    else:
        mensagem += f"\n⚠️ *Alerta:* R$ {preco - trip.budget:.2f} ACIMA do orçamento."

    await update.message.reply_text(mensagem, parse_mode="Markdown")

async def check_prices_job(context: ContextTypes.DEFAULT_TYPE):
    print("\n⏰ [DEBUG] O despertador tocou! Iniciando checagem automática...")
    chat_id = context.job.chat_id
    service = TripService()
    trips = service.get_all_trips()
    
    for trip in trips:
        resultado = service.search_flights_for_trip(trip.id)
        
        if resultado["success"]:
            preco = resultado["price"]
            ultimo_preco = trip.last_notified_price
            
            if preco <= trip.budget and (ultimo_preco is None or preco < ultimo_preco):
                
                msg = (
                    f"🚨 *ALERTA DE PREÇO BAIXOU!* 🚨\n\n"
                    f"✈️ *Rota:* {resultado['origin_name']} ➔ {resultado['destination_name']}\n"
                    f"📅 *Data Encontrada:* {resultado['date']} (Janela Flexível)\n"
                    f"💵 *Preço Atual:* R$ {preco:.2f}\n"
                    f"📊 *Preço Anterior:* {'R$ ' + f'{ultimo_preco:.2f}' if ultimo_preco else 'Nenhum'}\n"
                    f"🛫 *Companhia:* {resultado['airline']}\n\n"
                    f"[🔗 Clique para ver no Google Flights]({resultado['link']})"
                )
                
                await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown", disable_web_page_preview=True)
                
                service.repository.update_last_notified_price(trip.id, preco)
                print(f"⏰ [DEBUG] Alerta enviado para {trip.origin} ➔ {trip.destination}. Novo preço salvo.")

async def start_alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_message.chat_id
    
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    if current_jobs:
        await update.message.reply_text("✅ Seus alertas já estão ativados!")
        return
    
    context.job_queue.run_repeating(
        check_prices_job, 
        interval=43200, 
        first=10, 
        chat_id=chat_id, 
        name=str(chat_id)
    )
    
    await update.message.reply_text(
        "⏰ *Alertas Automáticos Ativados!*\n\n"
        "Eu vou checar os preços flexíveis a cada 12 horas em segundo plano. "
        "Só te aviso se algo entrar no orçamento e for mais barato que antes!",
        parse_mode="Markdown"
    )