from typing import Dict
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "6938292958:AAHAtiXdVOYFcmqjR3gK6i1KirRAmSW71bQ"

giocatori: Dict[str, int] = {}
data_inizio = datetime.now()

def estrai_nome_e_numero(testo):
    parole = testo.split()
    if len(parole) == 3:
        nome = parole[1]
        numero = parole[2]
        return nome, numero

    return None

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
    risultato = estrai_nome_e_numero(text)
    if risultato:
        nome, numero = risultato
        giocatori[nome] = int(numero)
        risposta = f"Set {numero} Cadate a {nome}"
    else:
        risposta = "Non hai scritto giusto"
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
