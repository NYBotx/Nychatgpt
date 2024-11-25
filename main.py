import os
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import openai
from modes import handle_modes  # Custom mode handler

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
bot = Bot(TELEGRAM_TOKEN)

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Main menu handler
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("💻 Code Developer", callback_data="mode_code")],
        [InlineKeyboardButton("🌐 Website Generator", callback_data="mode_website")],
        [InlineKeyboardButton("🤖 Chat Mode", callback_data="mode_chat")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome to ChatGPT Bot! Choose a mode:", reply_markup=reply_markup)

# Callback query handler for menu buttons
def mode_selector(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    mode = query.data  # Retrieve mode from callback data
    handle_modes(mode, query)

# Typing animation
def send_typing_action(func):
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        return func(update, context, *args, **kwargs)
    return wrapper

# Error handler
def error_handler(update: Update, context: CallbackContext):
    update.message.reply_text("⚠️ An error occurred. Please try again.")

# Main function
def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(mode_selector))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, error_handler))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
  
