from database import app, db, User, engine, session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def migrate_data():
    # Создаем контекст приложения
    with app.app_context():
        try:
            # Создаем таблицы в PostgreSQL
            db.create_all()
            print("Таблицы успешно созданы в PostgreSQL")
            
            # Список реальных пользователей
            real_users = [
                (1, 'None', 'Серикбай Рамазан', '', False),
                (2, 'vveeqqpprr', 'Элина', 'Потому что я тебя люблю - Гийом Мюссо', False),
                # ... остальные пользователи ...
            ]
            
            # Добавляем пользователей в новую базу
            for user_id, username, full_name, books, started in real_users:
                new_user = User(
                    user_id=user_id,
                    username=username,
                    full_name=full_name,
                    books=books,
                    started=started
                )
                session.add(new_user)
            
            # Сохраняем изменения
            session.commit()
            print("Данные успешно перенесены в PostgreSQL")
                
        except Exception as e:
            print(f"Ошибка при миграции данных: {e}")
            session.rollback()
        finally:
            session.close()

if __name__ == "__main__":
    migrate_data()
