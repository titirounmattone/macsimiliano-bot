# Guida al Deployment del Bot MaCsimiliano

Per garantire che il bot **MaCsimiliano** rimanga sempre attivo gratuitamente e in modo permanente, ho selezionato **Koyeb** come soluzione di hosting. Koyeb offre un piano gratuito (Eco) che è perfetto per i bot Telegram, poiché non "dorme" come altri servizi gratuiti (es. Render) e fornisce risorse sufficienti (512MB RAM, 0.1 vCPU).

## Passaggi per il Deployment su Koyeb

### 1. Preparazione del Repository
Il bot è già pronto con i file necessari:
- `macsimiliano_bot.py`: Il codice sorgente del bot.
- `requirements.txt`: Le dipendenze Python.
- `Dockerfile`: Le istruzioni per creare l'ambiente di esecuzione.

Dovrai caricare questi file su un repository **GitHub** (pubblico o privato).

### 2. Configurazione su Koyeb
1. Vai su [Koyeb.com](https://www.koyeb.com/) e crea un account gratuito.
2. Clicca su **"Create Service"**.
3. Seleziona **GitHub** come sorgente e collega il tuo repository.
4. Seleziona il repository del bot.
5. Scegli il tipo di deployment **"Dockerfile"** (Koyeb lo rileverà automaticamente).
6. Nella sezione **"Environment Variables"**, aggiungi le seguenti variabili:
   - `TELEGRAM_BOT_TOKEN`: Il token del tuo bot (`8353631523:AAG78Wl6wQZkS7duKmi8T7FmxPM8p9mckLY`).
   - `OPENAI_API_KEY`: La tua chiave API di OpenAI (già configurata nell'ambiente Manus).
7. Scegli la regione più vicina (es. Frankfurt).
8. Clicca su **"Deploy"**.

### 3. Verifica del Funzionamento
Una volta completato il deployment, lo stato del servizio passerà a **"Healthy"**.
- Puoi monitorare i log direttamente dalla dashboard di Koyeb per vedere i messaggi ricevuti.
- Invia un messaggio al bot su Telegram per confermare che risponda con la sua solita ironia.

## Perché Koyeb?
| Caratteristica | Vantaggio |
| :--- | :--- |
| **Uptime 24/7** | Il bot non va in standby (no "sleeping"). |
| **Piano Gratuito** | 1 istanza gratuita permanente (Nano Instance). |
| **Semplicità** | Deployment automatico tramite GitHub e Dockerfile. |
| **Affidabilità** | Infrastruttura moderna basata su micro-VM. |

## Alternativa: PythonAnywhere
Se preferisci una soluzione senza Docker:
1. Crea un account su [PythonAnywhere](https://www.pythonanywhere.com/).
2. Carica il file `macsimiliano_bot.py`.
3. Apri una console Bash e installa le dipendenze: `pip3 install --user python-telegram-bot openai requests`.
4. Crea un "Task" programmato o avvia lo script in background (nota: il piano gratuito di PythonAnywhere richiede un rinnovo manuale ogni 24 ore cliccando su un pulsante nel pannello di controllo).

**Consiglio:** Koyeb è la scelta migliore per un bot veramente "sempre attivo" senza interventi manuali.
