from sqlalchemy import create_engine

# Укажите путь к файлу базы данных
DATABASE_URL = "sqlite:////Users/ajger2/Desktop/hostbook/users_books.db"

# Создание подключения к базе данных
engine = create_engine(DATABASE_URL)

# Создание базы данных и таблицы
with engine.connect() as connection:
    connection.execute("CREATE TABLE IF NOT EXISTS example (id INTEGER PRIMARY KEY, name TEXT)")

print("База данных успешно создана!")
