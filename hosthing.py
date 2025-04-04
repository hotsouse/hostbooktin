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
from database import db, app, User  # Импортируем SQLAlchemy компоненты
from werkzeug.middleware.proxy_fix import ProxyFix

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN environment variable is not set")

# Инициализация бота
bot = TeleBot(TOKEN)

# Настройка ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

# Флаг для контроля работы бота
is_running = True

# Блокировка для безопасного доступа
db_lock = Lock()
LOCK_FILE = "/tmp/telegram_bot.lock"

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
def home():
    return "Book Crossing Bot is running!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_update = request.get_json()
        bot.process_new_updates([types.Update.de_json(json_update)])
        return "OK", 200
    return "Bad Request", 400

# Словарь для хранения состояний пользователей
user_states = {}

def set_user_state(user_id, state):
    user_states[user_id] = state

def get_user_state(user_id):
    return user_states.get(user_id)

def clear_user_state(user_id):
    user_states.pop(user_id, None)

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
    command_handlers.get(message.text, lambda: None)()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в Book Crossing!",
        reply_markup=main_menu()
    )

def handle_start_button(message):
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

def register_message(message):
    set_user_state(message.from_user.id, "registering")
    bot.send_message(
        message.chat.id,
        "Пожалуйста, напишите свое полное имя для регистрации.",
        reply_markup=main_menu()
    )

def register_user(message):
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

def add_books_message(message):
    set_user_state(message.from_user.id, "adding_books")
    bot.send_message(
        message.chat.id,
        "Отправьте список книг через запятую.",
        reply_markup=main_menu()
    )

def add_books(message):
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

@bot.message_handler(func=lambda message: message.text == "Доступные книги")
def available_books(message):
    with app.app_context():
        try:
            # Получаем только пользователей с книгами
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
            
            # Отправляем частями если сообщение слишком длинное
            for i in range(0, len(response), 4096):
                bot.send_message(message.chat.id, response[i:i+4096])
                
        except Exception as e:
            logger.error(f"Ошибка при получении книг: {str(e)}")
            bot.send_message(message.chat.id, "⚠️ Произошла ошибка при загрузке списка книг.")
            
def search_message(message):
    set_user_state(message.from_user.id, "searching")
    bot.send_message(
        message.chat.id,
        "Введите название книги для поиска:",
        reply_markup=main_menu()
    )

def search_books(message):
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

def faq_message(message):
    bot.send_message(
        message.chat.id,
        "По вопросам обращайтесь к @admin",
        reply_markup=main_menu()
    )

def my_books(message):
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

@bot.message_handler(func=lambda message: message.text == "Users")
def users_message(message):
    ADMIN_ID = 1213579921  # Замените на ваш ID
    
    if message.from_user.id != ADMIN_ID:
        return bot.send_message(message.chat.id, "⛔ У вас нет прав для просмотра этой информации.")

    with app.app_context():
        try:
            # Получаем всех пользователей
            all_users = User.query.order_by(User.id).all()
            
            if not all_users:
                return bot.send_message(message.chat.id, "В базе данных пока нет пользователей.")
            
            # Разделяем на зарегистрированных и активных
            registered = [u for u in all_users if u.full_name and not u.started]
            active = [u for u in all_users if u.started]
            
            response = (
                f"👥 Всего пользователей: {len(all_users)}\n\n"
                f"🆕 Зарегистрировались ({len(registered)}):\n"
            )
            
            # Добавляем информацию о зарегистрированных
            for user in registered[:10]:  # Ограничиваем первые 10
                name = f"@{user.username}" if user.username else user.full_name
                response += f"• {name}\n"
            
            response += f"\n🚀 Нажали Старт ({len(active)}):\n"
            
            # Добавляем информацию об активных
            for user in active[:10]:  # Ограничиваем первые 10
                name = f"@{user.username}" if user.username else user.full_name
                book_count = len(user.books.split(',')) if user.books else 0
                response += f"• {name} ({book_count} книг)\n"
            
            # Отправляем частями
            for i in range(0, len(response), 4096):
                bot.send_message(message.chat.id, response[i:i+4096])
                
        except Exception as e:
            logger.error(f"Ошибка при получении пользователей: {str(e)}")
            bot.send_message(message.chat.id, "⚠️ Произошла ошибка при загрузке данных.")

def send_survey(message):
    bot.send_message(
        message.chat.id,
        "Опрос: https://forms.gle/example",
        reply_markup=main_menu()
    )

def set_webhook():
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    data = {"url": f"{WEBHOOK_URL}/{TOKEN}"}
    response = requests.post(url, json=data)
    logger.info("Webhook response: %s", response.json())

@backoff.on_exception(
    backoff.expo,
    (RequestException, ConnectionError),
    max_tries=5,
    max_time=300
)
def setup_webhook_with_retry():
    set_webhook()

if __name__ == "__main__":
    lock_file = None
    try:
        lock_file = acquire_lock()
        
        # Создаем таблицы если их нет
        with app.app_context():
            db.create_all()
        
        setup_webhook_with_retry()
        
        port = int(os.getenv('PORT', 10000))
        if os.getenv('ENVIRONMENT') == 'production':
            from waitress import serve
            serve(app, host="0.0.0.0", port=port)
        else:
            app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        logger.error(f"Ошибка запуска: {e}")
        cleanup()
        sys.exit(1)