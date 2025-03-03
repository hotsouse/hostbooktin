import os
import psycopg2
from telebot import TeleBot, types

# Получаем токен из переменных окружения
TOKEN = os.getenv('TOKEN', '7194447722:AAFB6uobHo_NogxPkJpmQbtmweLBPJbLqxA')
bot = TeleBot(TOKEN)

# Получаем URL базы данных из переменных окружения
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://booktinder_user:VURw5VmEpLegLgBOUq20z0ItiuxesLWU@dpg-cup3bil2ng1s73eeoms0-a.singapore-postgres.render.com/booktinder')
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# Создание таблицы пользователей
with conn:
    with conn.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            username TEXT,
            full_name TEXT,
            books TEXT,
            started BOOLEAN DEFAULT FALSE
        )
        ''')
    conn.commit()

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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Старт"),
        types.KeyboardButton("Зарегистрироваться"),
        types.KeyboardButton("Добавить книги"),
        types.KeyboardButton("Доступные книги"),
        types.KeyboardButton("Search"),
        types.KeyboardButton("FAQ"),
        types.KeyboardButton("Мои книги"),
        types.KeyboardButton("Users")  # Добавлена кнопка "Users"
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
            bot.send_message(message.chat.id, "Введите название книги для поиска.")
            return
        elif message.text == "Добавить книги":
            set_user_state(user_id, "adding_books")
            bot.send_message(message.chat.id, "Отправьте список книг через запятую.")
            return
        elif message.text == "Зарегистрироваться":
            set_user_state(user_id, "registering")
            bot.send_message(message.chat.id, "Пожалуйста, напишите свое полное имя для регистрации.")
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
        clear_user_state(user_id)
    elif current_state == "adding_books":
        add_books(message)
        clear_user_state(user_id)
    elif current_state == "registering":
        register_user(message)
        clear_user_state(user_id)
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
    with conn.cursor() as cursor:
        cursor.execute('UPDATE users SET started = TRUE WHERE user_id = %s', (user_id,))
        conn.commit()
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Выберите 'Зарегистрироваться', чтобы начать обмен книгами.",
        reply_markup=main_menu(),
    )

# Обработка нажатия на кнопку "Зарегистрироваться"
@bot.message_handler(func=lambda message: message.text == "Зарегистрироваться")
def register_message(message):
    bot.send_message(message.chat.id, "Пожалуйста, напишите свое полное имя для регистрации.")
    bot.register_next_step_handler(message, register_user)

def register_user(message):
    full_name = message.text
    user_id = message.from_user.id
    username = message.from_user.username

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
        if cursor.fetchone():
            bot.send_message(message.chat.id, "Регистрация завершена! Теперь можете добавить свои книги для обмена нажимая 'Добавить книги'. ")
        else:
            cursor.execute('INSERT INTO users (user_id, username, full_name, books) VALUES (%s, %s, %s, %s)',
                           (user_id, username, full_name, ""))
            conn.commit()
            bot.send_message(
                message.chat.id,
                "Регистрация завершена! Теперь отправьте список книг, которые вы хотите обменять."
            )
            bot.register_next_step_handler(message, add_books)

# Обработка добавления книг после регистрации
def add_books(message):
    books = message.text
    user_id = message.from_user.id
    with conn.cursor() as cursor:
        cursor.execute('SELECT books FROM users WHERE user_id = %s', (user_id,))
        result = cursor.fetchone()
        if result:
            current_books = result[0] or ""
            updated_books = current_books + (", " if current_books else "") + books
            cursor.execute('UPDATE users SET books = %s WHERE user_id = %s', (updated_books, user_id))
            conn.commit()
            bot.send_message(message.chat.id, "Ваши книги успешно добавлены!")
        else:
            bot.send_message(message.chat.id, "Ошибка! Вы не зарегистрированы.")

# Функция: показать все доступные книги
@bot.message_handler(func=lambda message: message.text == "Доступные книги")
def available_books(message):
    with conn.cursor() as cursor:
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
    bot.send_message(message.chat.id, "Введите название книги для поиска.")
    bot.register_next_step_handler(message, search_books)

def search_books(message):
    book_name = message.text.lower()
    with conn.cursor() as cursor:
        cursor.execute('SELECT full_name, username, books FROM users')
        results = []
        for row in cursor.fetchall():
            full_name, username, books = row
            if book_name in books.lower():
                results.append(f"{full_name} (@{username}): {books}")
    if results:
        bot.send_message(message.chat.id, "\n".join(results))
    else:
        bot.send_message(message.chat.id, "Книга не найдена.")

# Обработка нажатия на кнопку "FAQ"
@bot.message_handler(func=lambda message: message.text == "FAQ")
def faq_message(message):
    bot.send_message(message.chat.id, "Если есть какие-то неполадки, свяжитесь с администратором.\nTelegram: @microkosmoos")

# Обработка нажатия на кнопку "Мои книги"
@bot.message_handler(func=lambda message: message.text == "Мои книги")
def my_books(message):
    user_id = message.from_user.id
    with conn.cursor() as cursor:
        cursor.execute('SELECT books FROM users WHERE user_id = %s', (user_id,))
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
        with conn.cursor() as cursor:
            cursor.execute('SELECT full_name, username, started FROM users')
            users = cursor.fetchall()

            if users:
                registered_users = [f"{user[0]} (@{user[1]})" for user in users if not user[2]]
                started_users = [f"{user[0]} (@{user[1]})" for user in users if user[2]]

                # Общее количество пользователей
                total_users = len(registered_users) + len(started_users)

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
    else:
        bot.send_message(message.chat.id, "У вас нет прав для доступа к этому меню.")

# Запуск бота
bot.polling(none_stop=True)
