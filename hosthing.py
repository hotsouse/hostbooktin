import os
from telebot import TeleBot, types
from flask import Flask, request
from threading import Lock
import signal
import sys
import time
import atexit
import fcntl
import logging
from dotenv import load_dotenv
import requests
from requests.exceptions import RequestException
import backoff
from database import db, app, User
from werkzeug.middleware.proxy_fix import ProxyFix

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
WEBHOOK_URL = os.getenv('WEBHOOK_URL').rstrip('/') if os.getenv('WEBHOOK_URL') else None
TOKEN = os.getenv("TOKEN")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")
RENDER = os.getenv("RENDER", "").lower() == "true"

# Проверка обязательных переменных
if not TOKEN:
    raise ValueError("Токен бота не установлен! Проверьте переменную TOKEN")

if RENDER and not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL обязателен для работы на Render")

if RENDER and not SECRET_TOKEN:
    raise ValueError("SECRET_TOKEN обязателен для работы на Render")

# Инициализация бота
bot = TeleBot(TOKEN)

# Настройка ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

# Флаг для контроля работы бота
is_running = True

# Блокировка для безопасного доступа
db_lock = Lock()
LOCK_FILE = "/tmp/telegram_bot.lock"

# Словарь для хранения состояний пользователей
user_states = {}

def set_user_state(user_id, state):
    """Установить состояние пользователя"""
    user_states[user_id] = state

def get_user_state(user_id):
    """Получить состояние пользователя"""
    return user_states.get(user_id)

def clear_user_state(user_id):
    """Очистить состояние пользователя"""
    user_states.pop(user_id, None)

def acquire_lock():
    """Получить блокировку процесса"""
    try:
        lock_file = open(LOCK_FILE, 'w')
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return lock_file
    except IOError:
        logger.error("Бот уже запущен в другом процессе")
        sys.exit(1)

def release_lock(lock_file):
    """Освободить блокировку процесса"""
    if lock_file and not lock_file.closed:
        try:
            fcntl.flock(lock_file, fcntl.LOCK_UN)
            lock_file.close()
            os.remove(LOCK_FILE)
        except Exception as e:
            logger.error(f"Ошибка при освобождении блокировки: {e}")

def cleanup():
    """Функция очистки при завершении"""
    global is_running
    logger.info("Выполняется очистка...")
    is_running = False
    try:
        bot.remove_webhook()
    except Exception as e:
        logger.error(f"Ошибка при удалении вебхука: {e}")
    if 'lock_file' in globals():
        release_lock(lock_file)

atexit.register(cleanup)

def signal_handler(signum, frame):
    """Обработчик сигналов"""
    logger.info(f"Получен сигнал {signum}")
    cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

@app.route('/')
def index():
    return 'Book Crossing Bot is running!'

@app.route('/ping')
def ping():
    """Эндпоинт для поддержания активности сервера на Render"""
    return "pong", 200

@app.route('/webhook/bot_webhook', methods=['POST'])
def bot_webhook():
    """Обработчик вебхука для Telegram бота"""
    if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != SECRET_TOKEN:
        return "Unauthorized", 403
    
    json_data = request.get_json()
    update = types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200

def setup_webhook():
    """Настройка вебхука с подробным логированием"""
    try:
        logger.info("Удаляем старый вебхук...")
        bot.remove_webhook()
        time.sleep(1)

        webhook_url = f"{WEBHOOK_URL}/webhook/bot_webhook"
        logger.info(f"Пытаемся установить вебхук на: {webhook_url}")

        result = bot.set_webhook(
            url=webhook_url,
            secret_token=SECRET_TOKEN,
            max_connections=40,
            allowed_updates=["message", "callback_query"],
            drop_pending_updates=True
        )
        
        time.sleep(2)
        webhook_info = bot.get_webhook_info()
        logger.info(f"Информация о вебхуке: {webhook_info}")

        if webhook_info.url != webhook_url:
            logger.error(f"URL вебхука не совпадает! Ожидалось: {webhook_url}, Получено: {webhook_info.url}")
            return False
            
        logger.info("✅ Вебхук успешно установлен")
        return True

    except Exception as e:
        logger.error(f"🚨 Ошибка при настройке вебхука: {str(e)}", exc_info=True)
        return False

@backoff.on_exception(
    backoff.expo,
    (RequestException, ConnectionError),
    max_tries=5,
    max_time=300
)
def setup_webhook_with_retry():
    return setup_webhook()

def run_webhook_server():
    """Запуск Flask сервера для вебхука"""
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def run_polling():
    """Режим polling для локальной разработки"""
    logger.info("🚀 Запуск в режиме POLLING (локально)")
    bot.remove_webhook()
    bot.infinity_polling()

def run_production():
    """Режим вебхука для Render"""
    logger.info("🌐 Запуск в режиме WEBHOOK (Render)")
    if not setup_webhook_with_retry():
        logger.error("Не удалось установить вебхук, переключаюсь на polling")
        run_polling()
        return
    
    run_webhook_server()

# Главное меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        "Старт", "Зарегистрироваться", "Добавить книги",
        "Доступные книги", "Search", "FAQ",
        "Мои книги", "Users", "📋 Пройти опрос"
    ]
    markup.add(*[types.KeyboardButton(btn) for btn in buttons])
    return markup

MENU_COMMANDS = [
    "Старт", "Зарегистрироваться", "Добавить книги",
    "Доступные книги", "Search", "FAQ",
    "Мои книги", "Users", "📋 Пройти опрос"
]

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    try:
        user_id = message.from_user.id
        current_state = get_user_state(user_id)

        if message.text in MENU_COMMANDS:
            handle_menu_command(message)
        elif current_state == "searching":
            search_books(message)
        elif current_state == "adding_books":
            add_books(message)
        elif current_state == "registering":
            register_user(message)
        else:
            bot.send_message(message.chat.id, "Выберите действие из меню:", reply_markup=main_menu())
    except Exception as e:
        logger.error(f"Ошибка в handle_messages: {e}")
        bot.send_message(message.chat.id, "⚠️ Произошла ошибка. Попробуйте еще раз.")

def handle_menu_command(message):
    command_handlers = {
        "Search": lambda: search_message(message),
        "Добавить книги": lambda: add_books_message(message),
        "Зарегистрироваться": lambda: register_message(message),
        "Старт": lambda: handle_start_button(message),
        "Доступные книги": lambda: available_books(message),
        "FAQ": lambda: faq_message(message),
        "Мои книги": lambda: my_books(message),
        "Users": lambda: users_message(message),
        "📋 Пройти опрос": lambda: send_survey(message)
    }
    handler = command_handlers.get(message.text, lambda: None)
    try:
        handler()
    except Exception as e:
        logger.error(f"Ошибка обработки команды {message.text}: {e}")
        bot.send_message(message.chat.id, "⚠️ Произошла ошибка при обработке команды.")

@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.send_message(
            message.chat.id,
            "Добро пожаловать в Book Crossing!",
            reply_markup=main_menu()
        )
    except Exception as e:
        logger.error(f"Ошибка в команде /start: {e}")

def handle_start_button(message):
    try:
        user_id = message.from_user.id
        with app.app_context():
            user = User.query.filter_by(user_id=user_id).first()
            if user:
                user.started = True
                db.session.commit()
            bot.send_message(
                message.chat.id,
                "Добро пожаловать! Выберите 'Зарегистрироваться', чтобы начать.",
                reply_markup=main_menu()
            )
    except Exception as e:
        logger.error(f"Ошибка в handle_start_button: {e}")
        bot.send_message(message.chat.id, "⚠️ Произошла ошибка при обработке.")

def register_message(message):
    try:
        set_user_state(message.from_user.id, "registering")
        bot.send_message(
            message.chat.id,
            "Пожалуйста, напишите свое полное имя для регистрации.",
            reply_markup=main_menu()
        )
    except Exception as e:
        logger.error(f"Ошибка в register_message: {e}")

def register_user(message):
    try:
        user_id = message.from_user.id
        username = message.from_user.username
        full_name = message.text
        
        with app.app_context():
            user = User.query.filter_by(user_id=user_id).first()
            if user:
                bot.send_message(
                    message.chat.id,
                    "Вы уже зарегистрированы!",
                    reply_markup=main_menu()
                )
            else:
                new_user = User(
                    user_id=user_id,
                    username=username,
                    full_name=full_name,
                    books="",
                    started=False
                )
                db.session.add(new_user)
                db.session.commit()
                bot.send_message(
                    message.chat.id,
                    "Регистрация завершена! Теперь можете добавить книги.",
                    reply_markup=main_menu()
                )
        clear_user_state(user_id)
    except Exception as e:
        logger.error(f"Ошибка в register_user: {e}")
        bot.send_message(message.chat.id, "⚠️ Произошла ошибка при регистрации.")

def add_books_message(message):
    try:
        set_user_state(message.from_user.id, "adding_books")
        bot.send_message(
            message.chat.id,
            "Отправьте список книг через запятую.",
            reply_markup=main_menu()
        )
    except Exception as e:
        logger.error(f"Ошибка в add_books_message: {e}")

def add_books(message):
    try:
        user_id = message.from_user.id
        books = message.text
        
        with app.app_context():
            user = User.query.filter_by(user_id=user_id).first()
            if user:
                if user.books:
                    user.books += f", {books}"
                else:
                    user.books = books
                db.session.commit()
                bot.send_message(
                    message.chat.id,
                    "Книги успешно добавлены!",
                    reply_markup=main_menu()
                )
            else:
                bot.send_message(
                    message.chat.id,
                    "Сначала зарегистрируйтесь!",
                    reply_markup=main_menu()
                )
        clear_user_state(user_id)
    except Exception as e:
        logger.error(f"Ошибка в add_books: {e}")
        bot.send_message(message.chat.id, "⚠️ Произошла ошибка при добавлении книг.")

@bot.message_handler(func=lambda message: message.text == "Доступные книги")
def available_books(message):
    try:
        with app.app_context():
            users_with_books = User.query.filter(
                User.books.isnot(None),
                User.books != '',
                ~User.books.ilike('None')
            ).all()
            
            if not users_with_books:
                return bot.send_message(message.chat.id, "📚 На данный момент нет доступных книг.")
            
            response = "📚 Доступные книги:\n\n"
            for user in users_with_books:
                username = f"@{user.username}" if user.username else user.full_name
                response += f"👤 {username}:\n{user.books}\n\n"
            
            for i in range(0, len(response), 4096):
                bot.send_message(message.chat.id, response[i:i+4096])
                
    except Exception as e:
        logger.error(f"Ошибка в available_books: {e}")
        bot.send_message(message.chat.id, "⚠️ Произошла ошибка при загрузке списка книг.")
            
def search_message(message):
    try:
        set_user_state(message.from_user.id, "searching")
        bot.send_message(
            message.chat.id,
            "Введите название книги для поиска:",
            reply_markup=main_menu()
        )
    except Exception as e:
        logger.error(f"Ошибка в search_message: {e}")

def search_books(message):
    try:
        search_term = message.text.lower()
        with app.app_context():
            users = User.query.filter(User.books.ilike(f'%{search_term}%')).all()
            
            if users:
                results = []
                for user in users:
                    if user.username != 'None':
                        results.append(f"@{user.username}: {user.books}")
                
                bot.send_message(
                    message.chat.id,
                    "Найдены книги:\n\n" + "\n\n".join(results),
                    reply_markup=main_menu()
                )
            else:
                bot.send_message(
                    message.chat.id,
                    "Книги не найдены.",
                    reply_markup=main_menu()
                )
        clear_user_state(message.from_user.id)
    except Exception as e:
        logger.error(f"Ошибка в search_books: {e}")
        bot.send_message(message.chat.id, "⚠️ Произошла ошибка при поиске.")

def faq_message(message):
    try:
        bot.send_message(
            message.chat.id,
            "Если есть какие-то неполадки, свяжитесь с администратором. Telegram: @microkosmoos",
            reply_markup=main_menu()
        )
    except Exception as e:
        logger.error(f"Ошибка в faq_message: {e}")

def my_books(message):
    try:
        user_id = message.from_user.id
        with app.app_context():
            user = User.query.filter_by(user_id=user_id).first()
            if user and user.books:
                bot.send_message(
                    message.chat.id,
                    f"Ваши книги:\n{user.books}",
                    reply_markup=main_menu()
                )
            else:
                bot.send_message(
                    message.chat.id,
                    "У вас пока нет книг.",
                    reply_markup=main_menu()
                )
    except Exception as e:
        logger.error(f"Ошибка в my_books: {e}")
        bot.send_message(message.chat.id, "⚠️ Произошла ошибка при загрузке ваших книг.")

@bot.message_handler(func=lambda message: message.text == "Users")
def users_message(message):
    try:
        ADMIN_ID = 1213579921
        
        if message.from_user.id != ADMIN_ID:
            return bot.send_message(message.chat.id, "⛔ У вас нет прав для просмотра этой информации.")

        with app.app_context():
            all_users = User.query.order_by(User.id).all()
            
            if not all_users:
                return bot.send_message(message.chat.id, "В базе данных пока нет пользователей.")
            
            registered = [u for u in all_users if u.full_name and not u.started]
            active = [u for u in all_users if u.started]
            
            response = (
                f"👥 Всего пользователей: {len(all_users)}\n\n"
                f"🆕 Зарегистрировались ({len(registered)}):\n"
            )
            
            for user in registered[:10]:
                name = f"@{user.username}" if user.username else user.full_name
                response += f"• {name}\n"
            
            response += f"\n🚀 Нажали Старт ({len(active)}):\n"
            
            for user in active[:10]:
                name = f"@{user.username}" if user.username else user.full_name
                book_count = len(user.books.split(',')) if user.books else 0
                response += f"• {name} ({book_count} книг)\n"
            
            for i in range(0, len(response), 4096):
                bot.send_message(message.chat.id, response[i:i+4096])
                
    except Exception as e:
        logger.error(f"Ошибка в users_message: {e}")
        bot.send_message(message.chat.id, "⚠️ Произошла ошибка при загрузке данных.")

def send_survey(message):
    try:
        bot.send_message(
            message.chat.id,
            "Опрос: https://forms.gle/example",
            reply_markup=main_menu()
        )
    except Exception as e:
        logger.error(f"Ошибка в send_survey: {e}")

if __name__ == "__main__":
    # Инициализация БД
    with app.app_context():
        db.create_all()
        logger.info("✅ Таблицы созданы/проверены")

    try:
        if RENDER:
            logger.info("🌐 Обнаружена среда Render, запускаю в режиме WEBHOOK")
            run_production()
        else:
            logger.info("💻 Локальный запуск, использую режим POLLING")
            run_polling()
    except Exception as e:
        logger.critical(f"Критическая ошибка: {str(e)}")
        sys.exit(1)