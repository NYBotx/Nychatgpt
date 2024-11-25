import openai
from telegram import Update, ParseMode
from telegram.ext import CallbackContext

# OpenAI ChatGPT API setup
def gpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Handle modes
def handle_modes(mode, query):
    if mode == "mode_code":
        query.edit_message_text("💻 Code Developer Mode Activated! Send me a coding request.")
    elif mode == "mode_website":
        query.edit_message_text("🌐 Website Generator Mode Activated! Describe your website idea.")
    elif mode == "mode_chat":
        query.edit_message_text("🤖 Chat Mode Activated! Ask me anything.")
    else:
        query.edit_message_text("⚠️ Unknown mode. Please try again.")

# Process user inputs in each mode
def process_mode_input(update: Update, context: CallbackContext, mode):
    user_message = update.message.text

    if mode == "mode_code":
        prompt = f"Write code for: {user_message}"
        response = gpt_response(prompt)
        update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
    elif mode == "mode_website":
        prompt = f"Generate a website for: {user_message}"
        response = gpt_response(prompt)
        update.message.reply_text(response, parse_mode=ParseMode.HTML)
    elif mode == "mode_chat":
        response = gpt_response(user_message)
        update.message.reply_text(response)

    
      import pyfiglet
def style_text(text):
    return pyfiglet.figlet_format(text)

