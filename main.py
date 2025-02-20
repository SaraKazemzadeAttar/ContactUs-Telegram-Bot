import telebot
import os
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Enable logging
logger = telebot.logger
logger.setLevel(logging.INFO)

# Set up the bot with your API token
API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# Start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    direct_connection_button = InlineKeyboardButton("ارتباط مستقیم با ما", callback_data="support_phone")
    ask_problem_button = InlineKeyboardButton("ثبت مشکل", callback_data="ask_problem")
    
    markup.add(direct_connection_button, ask_problem_button)
    
    bot.reply_to(message, "سلام؛ لطفا یکی از گزینه‌های زیر را انتخاب کنید", reply_markup=markup)
    
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "support_phone":
        response = """📞 برای ارتباط مستقیم با ما می‌توانید با شماره‌های پشتیبانی زیر تماس حاصل نمایید:\n\n 0912xxxxxx\n 021xxxxxx"""
        bot.send_message(call.message.chat.id, response)
    
    elif call.data == "ask_problem":
        msg = bot.send_message(call.message.chat.id, "لطفاً مشکل خود را وارد نمایید:")
        bot.register_next_step_handler(msg, process_problem)

def process_problem(message):
    ticket_id = f"#{message.message_id}"
    bot.send_message(message.chat.id, f"کارشناسان ما در اسرع وقت با شما تماس خواهند گرفت.\nشماره پیگیری تیکت: {ticket_id} می باشد" )

bot.infinity_polling()
