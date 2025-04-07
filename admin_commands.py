# admin_commands.py
from telebot import TeleBot
from demo_data import create_demo_data
from stats_utils import get_exchange_stats

def setup_admin_commands(bot: TeleBot):
    @bot.message_handler(commands=['createdemo'])
    def create_demo(message):
        if message.from_user.id == ADMIN_ID:
            create_demo_data()
            bot.reply_to(message, "Демо-данные созданы")
    
    @bot.message_handler(commands=['stats'])
    def show_stats(message):
        stats = get_exchange_stats()
        # Форматированный вывод статистики