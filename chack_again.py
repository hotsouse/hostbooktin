from sqlalchemy import text
from database import db, app

def check_database():
    with app.app_context():
        try:
            # 1. Проверяем существование таблицы 'user'
            table_exists = db.session.execute(
                text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'user')")
            ).scalar()
            
            print(f"Таблица 'user' существует: {'Да' if table_exists else 'Нет'}")
            
            # 2. Если таблица есть - проверяем данные
            if table_exists:
                # Количество записей
                count = db.session.execute(
                    text("SELECT COUNT(*) FROM user")
                ).scalar()
                print(f"Количество записей в 'user': {count}")
                
                # Пример данных
                sample = db.session.execute(
                    text("SELECT * FROM user LIMIT 5")
                ).fetchall()
                
                print("\nПример записей:")
                for row in sample:
                    print(row)
            
            # 3. Проверяем текущую таблицу 'users'
            users_count = db.session.execute(
                text("SELECT COUNT(*) FROM users")
            ).scalar()
            print(f"\nКоличество записей в 'users': {users_count}")
            
        except Exception as e:
            print(f"❌ Ошибка проверки: {e}")

if __name__ == "__main__":
    print("🔍 Проверка базы данных...")
    check_database()