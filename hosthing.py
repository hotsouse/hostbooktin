import os
import sqlite3
from telebot import TeleBot, types
from flask import Flask, request, abort
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

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

def get_env_var(var_name):
    """Получение переменной окружения с проверкой"""
    value = os.getenv(var_name)
    if not value:
        logger.error(f"Ошибка: Переменная окружения {var_name} не установлена")
        if var_name == 'WEBHOOK_URL':
            logger.error(f"WEBHOOK_URL должен быть установлен в настройках Render")
            logger.error(f"Формат: https://your-app-name.onrender.com")
            logger.error(f"Пример: https://hostbooktin.onrender.com")
        elif var_name == 'TOKEN':
            logger.error(f"TOKEN должен быть установлен в настройках Render")
            logger.error(f"Получите токен у @BotFather в Telegram")
        sys.exit(1)
    return value

# Инициализация переменных окружения
TOKEN = get_env_var('TOKEN')
WEBHOOK_URL = get_env_var('WEBHOOK_URL').rstrip('/')  # Удаляем trailing slash если есть

# Константы для базы данных
DB_FILE = 'users_books.db'

# Создаем Flask приложение
app = Flask(__name__)

# Инициализация бота с parse_mode='HTML'
bot = TeleBot(TOKEN, parse_mode='HTML', threaded=False)

# Флаг для контроля работы бота
is_running = True

# Добавляем блокировку для безопасного доступа к соединению
db_lock = Lock()

# Добавляем файл блокировки
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
    try:
        fcntl.flock(lock_file, fcntl.LOCK_UN)
        lock_file.close()
        os.remove(LOCK_FILE)
    except Exception as e:
        logger.error(f"Ошибка при освобождении блокировки: {e}")

def cleanup():
    """Функция очистки при завершении"""
    global is_running, bot, lock_file
    logger.info("Выполняется очистка...")
    is_running = False
    if bot:
        try:
            bot.remove_webhook()
        except Exception as e:
            logger.error(f"Ошибка при удалении вебхука: {e}")
    release_lock(lock_file)

# Регистрируем функцию очистки
atexit.register(cleanup)

def signal_handler(signum, frame):
    """Обработчик сигналов"""
    logger.info(f"Получен сигнал {signum}")
    cleanup()
    sys.exit(0)

# Регистрируем обработчики сигналов
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

@app.route('/')
def home():
    return "Bot is running"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        try:
            json_string = request.get_data().decode('utf-8')
            update = types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        except Exception as e:
            logger.error(f"Ошибка при обработке вебхука: {e}")
            abort(500)
    abort(403)

def exponential_backoff():
    """Экспоненциальная задержка для повторных попыток"""
    return backoff.on_exception(
        backoff.expo,
        (RequestException, ConnectionError),
        max_tries=5,
        max_time=300
    )

@exponential_backoff()
def setup_webhook_with_retry():
    """Установка вебхука с механизмом повторных попыток"""
    setup_webhook()

def get_db():
    """Получение соединения с базой данных"""
    return sqlite3.connect(DB_FILE)

def init_database():
    """Инициализация базы данных"""
    try:
        conn = get_db()
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                username TEXT,
                full_name TEXT,
                books TEXT,
                started BOOLEAN DEFAULT FALSE
            )
            ''')
        logger.info("База данных успешно инициализирована")
    except Exception as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")
        sys.exit(1)

# Словарь для хранения состояний пользователей
user_states = {}

def set_user_state(user_id, state):
    user_states[user_id] = state

def get_user_state(user_id):
    return user_states.get(user_id)

def clear_user_state(user_id):
    if user_id in user_states:
        del user_states[user_id]

# Главное меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("Старт"),
        types.KeyboardButton("Зарегистрироваться"),
        types.KeyboardButton("Добавить книги"),
        types.KeyboardButton("Доступные книги"),
        types.KeyboardButton("Search"),
        types.KeyboardButton("FAQ"),
        types.KeyboardButton("Мои книги"),
        types.KeyboardButton("Users")
    )
    return markup

# Список команд меню
MENU_COMMANDS = ["Старт", "Зарегистрироваться", "Добавить книги", "Доступные книги", 
                "Search", "FAQ", "Мои книги", "Users"]

# Обработчик всех сообщений
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    current_state = get_user_state(user_id)
    
    # Если сообщение является командой меню
    if message.text in MENU_COMMANDS:
        if message.text == "Search":
            set_user_state(user_id, "searching")
            bot.send_message(message.chat.id, "Введите название книги для поиска.", reply_markup=main_menu())
            return
        elif message.text == "Добавить книги":
            set_user_state(user_id, "adding_books")
            bot.send_message(message.chat.id, "Отправьте список книг через запятую.", reply_markup=main_menu())
            return
        elif message.text == "Зарегистрироваться":
            set_user_state(user_id, "registering")
            bot.send_message(message.chat.id, "Пожалуйста, напишите свое полное имя для регистрации.", reply_markup=main_menu())
            return
        elif message.text == "Старт":
            handle_start_button(message)
            return
        elif message.text == "Доступные книги":
            available_books(message)
            return
        elif message.text == "FAQ":
            faq_message(message)
            return
        elif message.text == "Мои книги":
            my_books(message)
            return
        elif message.text == "Users":
            users_message(message)
            return

    # Обработка сообщений в зависимости от состояния пользователя
    if current_state == "searching":
        search_books(message)
    elif current_state == "adding_books":
        add_books(message)
    elif current_state == "registering":
        register_user(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите действие из меню.", reply_markup=main_menu())

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в Book Crossing! Выберите 'Зарегистрироваться', чтобы начать обмен книгами.",
        reply_markup=main_menu(),
    )

# Обработка нажатия на кнопку "Старт"
@bot.message_handler(func=lambda message: message.text == "Старт")
def handle_start_button(message):
    user_id = message.from_user.id
    try:
        conn = get_db()
        with conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET started = TRUE WHERE user_id = ?', (user_id,))
            conn.commit()
        bot.send_message(
            message.chat.id,
            "Добро пожаловать! Выберите 'Зарегистрироваться', чтобы начать обмен книгами.",
            reply_markup=main_menu(),
        )
    except Exception as e:
        logger.error(f"Ошибка в handle_start_button: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка. Пожалуйста, попробуйте позже.")

# Обработка нажатия на кнопку "Зарегистрироваться"
@bot.message_handler(func=lambda message: message.text == "Зарегистрироваться")
def register_message(message):
    bot.send_message(message.chat.id, "Пожалуйста, напишите свое полное имя для регистрации.", reply_markup=main_menu())
    bot.register_next_step_handler(message, register_user)

def register_user(message):
    full_name = message.text
    user_id = message.from_user.id
    username = message.from_user.username

    try:
        conn = get_db()
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            if cursor.fetchone():
                bot.send_message(message.chat.id, "Регистрация завершена! Теперь можете добавить свои книги для обмена нажимая 'Добавить книги'.", reply_markup=main_menu())
            else:
                cursor.execute('INSERT INTO users (user_id, username, full_name, books) VALUES (?, ?, ?, ?)',
                             (user_id, username, full_name, ""))
                conn.commit()
                bot.send_message(
                    message.chat.id,
                    "Регистрация завершена! Теперь отправьте список книг, которые вы хотите обменять.",
                    reply_markup=main_menu()
                )
    except Exception as e:
        logger.error(f"Ошибка в register_user: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка при регистрации. Пожалуйста, попробуйте позже.", reply_markup=main_menu())
    clear_user_state(user_id)

# Обработка добавления книг после регистрации
def add_books(message):
    if not message.text:
        bot.send_message(message.chat.id, "Пожалуйста, отправьте текстовое сообщение.", reply_markup=main_menu())
        return

    books = message.text
    user_id = message.from_user.id
    try:
        conn = get_db()
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT books FROM users WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            if result:
                current_books = result[0] or ""
                updated_books = current_books + (", " if current_books else "") + books
                cursor.execute('UPDATE users SET books = ? WHERE user_id = ?', (updated_books, user_id))
                conn.commit()
                bot.send_message(message.chat.id, "Ваши книги успешно добавлены!", reply_markup=main_menu())
            else:
                bot.send_message(message.chat.id, "Ошибка! Вы не зарегистрированы.", reply_markup=main_menu())
    except Exception as e:
        logger.error(f"Ошибка в add_books: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка при добавлении книг. Пожалуйста, попробуйте позже.", reply_markup=main_menu())
    clear_user_state(user_id)

# Функция: показать все доступные книги
@bot.message_handler(func=lambda message: message.text == "Доступные книги")
def available_books(message):
    conn = get_db()
    with conn:
        cursor = conn.cursor()
        cursor.execute('SELECT username, books FROM users WHERE books IS NOT NULL AND books != \'\'')
        results = cursor.fetchall()

    if results:
        books_list = "\n\n".join([f"@{row[0]}:\n{row[1]}" for row in results])
        bot.send_message(message.chat.id, f"Доступные книги:\n\n{books_list}")
    else:
        bot.send_message(message.chat.id, "На данный момент доступных книг нет.")

# Обработка нажатия на кнопку "Search"
@bot.message_handler(func=lambda message: message.text == "Search")
def search_message(message):
    set_user_state(message.from_user.id, "searching")
    bot.send_message(message.chat.id, "Введите название книги для поиска.", reply_markup=main_menu())

def search_books(message):
    if not message.text:
        bot.send_message(message.chat.id, "Пожалуйста, отправьте текстовое сообщение.", reply_markup=main_menu())
        return

    book_name = message.text.lower()
    try:
        conn = get_db()
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT full_name, username, books FROM users')
            results = []
            for row in cursor.fetchall():
                full_name, username, books = row
                if books and book_name in books.lower():
                    results.append(f"{full_name} (@{username}): {books}")
        if results:
            bot.send_message(message.chat.id, "\n".join(results), reply_markup=main_menu())
        else:
            bot.send_message(message.chat.id, "Книга не найдена.", reply_markup=main_menu())
    except Exception as e:
        logger.error(f"Ошибка в search_books: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка при поиске. Пожалуйста, попробуйте позже.", reply_markup=main_menu())
    clear_user_state(message.from_user.id)

# Обработка нажатия на кнопку "FAQ"
@bot.message_handler(func=lambda message: message.text == "FAQ")
def faq_message(message):
    bot.send_message(message.chat.id, "Если есть какие-то неполадки, свяжитесь с администратором.\nTelegram: @microkosmoos")

# Обработка нажатия на кнопку "Мои книги"
@bot.message_handler(func=lambda message: message.text == "Мои книги")
def my_books(message):
    user_id = message.from_user.id
    conn = get_db()
    with conn:
        cursor = conn.cursor()
        cursor.execute('SELECT books FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        if result and result[0]:
            bot.send_message(message.chat.id, f"Ваши книги:\n{result[0]}")
        else:
            bot.send_message(message.chat.id, "У вас пока нет добавленных книг.")

# Обработка нажатия на кнопку "Users" (для админа)
@bot.message_handler(func=lambda message: message.text == "Users")
def users_message(message):
    # Проверка, является ли пользователь администратором
    if message.from_user.id == 1213579921:  # Замените на свой ID
        try:
            conn = get_db()
            with conn:
                cursor = conn.cursor()
                cursor.execute('SELECT full_name, username, started FROM users')
                users = cursor.fetchall()

                if users:
                    registered_users = [f"{user[0]} (@{user[1]})" for user in users if not user[2]]
                    started_users = [f"{user[0]} (@{user[1]})" for user in users if user[2]]

                    # Общее количество пользователей
                    total_users = len(users)

                    # Формируем ответ
                    response = f"Общее количество пользователей: {total_users}\n\n"
                    
                    # Список зарегистрированных пользователей
                    response += f"Список пользователей, которые зарегистрировались:\n\n"
                    if registered_users:
                        response += "\n".join(registered_users) + "\n\n"
                    else:
                        response += "Нет зарегистрированных пользователей.\n\n"
                    
                    # Список пользователей, которые нажали на 'Старт'
                    response += "Список пользователей, которые нажали на 'Старт':\n\n"
                    if started_users:
                        response += "\n".join(started_users)
                    else:
                        response += "Нет пользователей, которые нажали на 'Старт'."

                    bot.send_message(message.chat.id, response)
                else:
                    bot.send_message(message.chat.id, "Нет пользователей.")
        except Exception as e:
            logger.error(f"Ошибка при получении списка пользователей: {e}")
            bot.send_message(message.chat.id, "Произошла ошибка при получении списка пользователей.")
    else:
        bot.send_message(message.chat.id, "У вас нет прав для доступа к этому меню.")

def setup_webhook():
    """Установка вебхука"""
    try:
        # Сначала удаляем все вебхуки
        bot.delete_webhook()
        time.sleep(0.1)
        
        # Устанавливаем новый вебхук
        webhook_url = f"{WEBHOOK_URL}/{TOKEN}"
        webhook_info = bot.get_webhook_info()
        
        # Проверяем текущий URL вебхука
        if webhook_info.url != webhook_url:
            bot.set_webhook(
                url=webhook_url,
                max_connections=100,
                allowed_updates=['message', 'callback_query']
            )
            logger.info(f"Вебхук успешно установлен на {webhook_url}")
        else:
            logger.info("Вебхук уже установлен корректно")
            
    except Exception as e:
        logger.error(f"Ошибка при установке вебхука: {str(e)}")
        logger.error(f"Проверьте правильность WEBHOOK_URL и TOKEN")
        logger.error(f"Текущий WEBHOOK_URL: {WEBHOOK_URL}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        # Получаем блокировку процесса
        lock_file = acquire_lock()

        # Инициализируем базу данных
        init_database()

        max_retries = 5
        retry_delay = 5  # начальная задержка в секундах

        while max_retries > 0:
            try:
                # Устанавливаем вебхук с механизмом повторных попыток
                setup_webhook_with_retry()
                
                # Запускаем Flask с gunicorn
                port = int(os.getenv('PORT', 10000))
                app.run(host='0.0.0.0', port=port)
                break  # Если успешно запустились, выходим из цикла
            except (RequestException, ConnectionError) as e:
                max_retries -= 1
                if max_retries > 0:
                    logger.warning(f"Ошибка подключения: {e}. Повторная попытка через {retry_delay} секунд...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # увеличиваем задержку экспоненциально
                else:
                    logger.error(f"Не удалось установить соединение после всех попыток: {e}")
                    raise
            except Exception as e:
                logger.error(f"Критическая ошибка: {e}")
                raise
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        cleanup()
        sys.exit(1)
    finally:
        cleanup()
