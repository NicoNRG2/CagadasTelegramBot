from typing import Dict
from datetime import datetime
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "your token from bot father"

giocatori: Dict[str, int] = {}
data_inizio = datetime.now()

# comandi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data_inizio = datetime.now()
    risposta = "Inizio del conteggio delle cagate il giorno: "+data_inizio.strftime("%d-%m-%Y")
    await update.message.reply_text(risposta)

async def get_cagate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    risposta = "Ecco i risultati:\n"
    for nome, cagade in giocatori.items():
        risposta += f"{nome}: {cagade} cagadas\n"
    await update.message.reply_text(risposta)

async def set_cagate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text: str = update.message.text
    pattern = r'/set_cagate "(.*?)" (\d+)'
    matches = re.match(pattern, text)
    if matches:
        nome = matches.group(1)
        numero = int(matches.group(2))
        giocatori[nome] = int(numero)
        risposta = f"Set {numero} Cadate a {nome}"
    else:
        risposta = 'Usa /set_cagate "NOME" VALORE'
    await update.message.reply_text(risposta)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    giocatori.clear()
    await update.message.reply_text("Reset cagate")

async def get_inizio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    risposta = "Inizio del conteggio delle cagate il giorno: "+data_inizio.strftime("%d-%m-%Y")
    await update.message.reply_text(risposta)

async def set_inizio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data_inizio = datetime.now()
    risposta = "Inizio del conteggio delle cagate il giorno: "+data_inizio.strftime("%d-%m-%Y")
    await update.message.reply_text(risposta)

# risposte
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text: str = update.message.text
    user: str = update.message.from_user.first_name
    if '💩' in text:
        if user in giocatori:
            giocatori[user] += 1
        else:
            giocatori[user] = 1

app = ApplicationBuilder().token(TOKEN).build()

# comandi
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("get_cagate", get_cagate))
app.add_handler(CommandHandler("set_cagate", set_cagate))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(CommandHandler("get_inizio", get_inizio))
app.add_handler(CommandHandler("set_inizio", set_inizio))

# risposte
app.add_handler(MessageHandler(filters.TEXT, message))
print("In ascolto...")
app.run_polling()
