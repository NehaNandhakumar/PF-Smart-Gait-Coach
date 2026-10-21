import os
import asyncio
import psycopg2
import ollama
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- 1. DATABASE SETUP ---
DB_NAME = "shoefit"
DB_USER = "nehanandhakumar"    
DB_PASSWORD = ""        
DB_HOST = "localhost"
DB_PORT = "5432"

def get_latest_gait_data():
    """Fetches the most recent stride logs from PostgreSQL."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        cursor = conn.cursor()
        
        # Pulling the latest stride data from stride_logs
        cursor.execute("SELECT * FROM stride_logs ORDER BY id DESC LIMIT 5;")
        logs = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return logs
    except Exception as e:
        print(f"Database error: {e}")
        return []

# --- 2. OLLAMA RAG RESPONSE GENERATION ---
def generate_coaching_response(user_message):
    """Retrieves gait logs and feeds them into Ollama for context-aware coaching."""
    recent_logs = get_latest_gait_data()
    
    # System prompt assigning the AI assistant the role of an expert gait analyst
    system_prompt = f"""
    You are an expert athletic gait analyst and shoe-fitting coach.
    Here is the user's recent stride/pressure sensor data from the database:
    {recent_logs}
    
    Use this data to answer the user's question with actionable feedback on their walking or running form.
    Keep your response concise, clear, and conversational.
    """
    
    response = ollama.chat(
        model='llama3',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message}
        ]
    )
    return response['message']['content']

# --- 3. TELEGRAM BOT HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your Smart Gait & ShoeFit Coach. How can I help your run today?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("Analyzing your gait data...")
    
    # Run Ollama in a separate thread so the bot stays responsive
    bot_reply = await asyncio.to_thread(generate_coaching_response, user_text)
    
    await update.message.reply_text(bot_reply)

# --- 4. MAIN EXECUTION ---
if __name__ == '__main__':
    TELEGRAM_TOKEN = "8671037194:AAGq4UDb2JmMC6uy_iNPcggeDsew-cwqLF8"
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Gait Coach Bot is running...")
    app.run_polling()