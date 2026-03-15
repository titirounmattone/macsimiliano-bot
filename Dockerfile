FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY macsimiliano_bot.py .

# Imposta le variabili d'ambiente (verranno fornite dalla piattaforma di hosting)
# ENV TELEGRAM_BOT_TOKEN=...
# ENV OPENAI_API_KEY=...

CMD ["python", "macsimiliano_bot.py"]
