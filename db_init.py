import psycopg2
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# Настройки бота и базы данных
TOKEN = "7194447722:AAFB6uobHo_NogxPkJpmQbtmweLBPJbLqxA"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "covdeP-higtup-mimgi7"
DB_HOST = "@db.krtkebdtxypgczlamacx.supabase.co"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Функция подключения к БД
def connect_db():
    return psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

# Создание таблиц (запускается один раз)
def create_tables():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50),
        full_name VARCHAR(100),
        books TEXT,
        is_active BOOLEAN DEFAULT FALSE
    );
    
    CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        owner_id INTEGER REFERENCES users(id)
    );
    """)
    conn.commit()
    cur.close()
    conn.close()

# Добавление пользователей в базу данных
def insert_users():
    users = [
        (1, 'None', 'Серикбай Рамазан', '', False),
        (2, 'vveeqqpprr', 'Элина', 'Потому что я тебя люблю - Гийом Мюссо', False),
        (3, 'Melovinsgirl', 'Катя', 'Девушка в поезде - Паула Хокинс', False),
    ]
    conn = connect_db()
    cur = conn.cursor()
    for user in users:
        cur.execute("INSERT INTO users (id, username, full_name, books, is_active) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;", user)
    conn.commit()
    cur.close()
    conn.close()

# Основное меню
@dp.message_handler(commands=['start'])
async def send_menu(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Users", callback_data="users"))
    keyboard.add(InlineKeyboardButton("Доступные книги", callback_data="books"))
    await message.answer("Выберите опцию:", reply_markup=keyboard)

# Вывод списка пользователей
@dp.callback_query_handler(lambda c: c.data == "users")
async def show_users(callback_query: types.CallbackQuery):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT full_name FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    users_list = "\n".join(user[0] for user in users)
    await bot.send_message(callback_query.from_user.id, f"Пользователи:\n{users_list}")

# Вывод списка книг
@dp.callback_query_handler(lambda c: c.data == "books")
async def show_books(callback_query: types.CallbackQuery):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT books FROM users WHERE books IS NOT NULL AND books != ''")
    books = cur.fetchall()
    cur.close()
    conn.close()
    books_list = "\n".join(book[0] for book in books)
    await bot.send_message(callback_query.from_user.id, f"Доступные книги:\n{books_list}")

if __name__ == "__main__":
    create_tables()
    insert_users()
    executor.start_polling(dp, skip_updates=True)
