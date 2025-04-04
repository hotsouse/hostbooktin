from database import db, app, User
from sqlalchemy import inspect

def check_database():
    with app.app_context():
        # 1. Проверяем существование таблиц
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Таблицы в базе данных: {tables}")

        # 2. Проверяем таблицу users
        if 'users' not in tables:
            print("❌ Таблица 'users' не найдена!")
            return

        # 3. Проверяем структуру таблицы
        columns = inspector.get_columns('users')
        print("\nСтруктура таблицы 'users':")
        for col in columns:
            print(f"{col['name']}: {col['type']}")

        # 4. Проверяем первые 5 записей
        print("\nПервые 5 записей:")
        users = User.query.limit(5).all()
        for u in users:
            print(f"ID: {u.id}, Username: {u.username}, Name: {u.full_name}, Books: {u.books}, Started: {u.started}")

        # 5. Проверяем общее количество
        count = User.query.count()
        print(f"\nВсего пользователей: {count}")

if __name__ == "__main__":
    print("🔍 Проверка базы данных...")
    check_database()