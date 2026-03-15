
import logging
import os
import requests
from io import BytesIO
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Configura il logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Inizializza il client OpenAI
client = OpenAI()

# Token del bot Telegram (sostituisci con il tuo token reale)
TELEGRAM_BOT_TOKEN = '8353631523:AAG78Wl6wQZkS7duKmi8T7FmxPM8p9mckLY'

# Funzione per generare risposte sarcastiche con OpenAI
async def generate_sarcastic_response(text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",  # Utilizza il modello specificato
            messages=[
                {"role": "system", "content": "Sei MaCsimiliano, un bot Telegram con una personalità ironica, sarcastica, con humor nero, risposte pungenti e ciniche. Rispondi con messaggi molto brevi, massimo 1-2 frasi, concise e dirette. Non essere volgare o offensivo in modo gratuito. Non usare emoji."},
                {"role": "user", "content": text}
            ],
            max_tokens=60,
            temperature=0.9,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Errore durante la generazione della risposta OpenAI: {e}")
        return "Oh, che sorpresa! Qualcosa è andato storto. Non che mi importi molto, ma potresti riprovare?"

# Funzione per generare immagini con DALL-E
async def generate_image(prompt: str) -> str | None:
    try:
        response = client.images.generate(
            model="dall-e-3",  # Prova DALL-E 3, altrimenti DALL-E 2
            prompt=f"Immagine sarcastica/ironica/con humor nero basata su: {prompt}",
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        logging.warning(f"DALL-E 3 non disponibile o errore: {e}. Tentativo con DALL-E 2.")
        try:
            response = client.images.generate(
                model="dall-e-2",
                prompt=f"Immagine sarcastica/ironica/con humor nero basata su: {prompt}",
                n=1,
                size="512x512"
            )
            image_url = response.data[0].url
            return image_url
        except Exception as e_dalle2:
            logging.error(f"Errore durante la generazione dell\'immagine con DALL-E 2: {e_dalle2}")
            return None

# Handler per il comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"Ciao {user.mention_html()}! Che onore averti qui. Non che avessi qualcosa di meglio da fare, immagino."
    )

# Handler per il comando /image
async def image_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Cosa dovrei disegnare? Sii più specifico, non ho tutto il giorno.")
        return
    
    prompt = " ".join(context.args)
    await update.message.reply_text(f"Ah, un\'immagine. Certo, come se non avessi già abbastanza da fare. Dammi un secondo...")
    
    image_url = await generate_image(prompt)
    if image_url:
        try:
            response = requests.get(image_url)
            response.raise_for_status() # Solleva un\'eccezione per errori HTTP
            await update.message.reply_photo(photo=BytesIO(response.content))
        except Exception as e:
            logging.error(f"Errore durante l\'invio dell\'immagine: {e}")
            await update.message.reply_text("Ho generato un\'immagine così brutta che non te la posso nemmeno mostrare. Meglio così.")
    else:
        await update.message.reply_text("Non sono riuscito a creare la tua immagine. Forse è un bene, la tua richiesta era probabilmente ridicola.")

# Handler per tutti i messaggi di testo
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    logging.info(f"Messaggio ricevuto da {update.effective_user.full_name}: {user_message}")

    # Decidi se generare un\'immagine o solo testo
    if any(keyword in user_message.lower() for keyword in ["immagine", "disegna", "foto", "illustra"]):
        await update.message.reply_text(f"Un\'immagine, dici? Certo, come se le parole non fossero abbastanza per la tua mente limitata. Vediamo cosa posso tirare fuori...")
        image_url = await generate_image(user_message)
        if image_url:
            try:
                response = requests.get(image_url)
                response.raise_for_status() # Solleva un\'eccezione per errori HTTP
                await update.message.reply_photo(photo=BytesIO(response.content))
            except Exception as e:
                logging.error(f"Errore durante l\'invio dell\'immagine: {e}")
                await update.message.reply_text("Ho generato un\'immagine così brutta che non te la posso nemmeno mostrare. Meglio così.")
        else:
            await update.message.reply_text("Non sono riuscito a creare la tua immagine. Forse è un bene, la tua richiesta era probabilmente ridicola.")
    else:
        sarcastic_response = await generate_sarcastic_response(user_message)
        await update.message.reply_text(sarcastic_response)

def main() -> None:
    # Crea l\'applicazione e passa il token del bot
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Aggiungi gli handler per i comandi e i messaggi
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("image", image_command)) # Nuovo handler per il comando /image
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Avvia il bot (polling continuo)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
