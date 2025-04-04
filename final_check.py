from database import db, app, User

def check_data():
    with app.app_context():
        try:
            # 1. Проверяем общее количество
            count = User.query.count()
            print(f"Всего пользователей: {count}")
            
            # 2. Проверяем пользователей с книгами
            with_books = User.query.filter(
                User.books.isnot(None),
                db.func.trim(User.books) != ''
            ).count()
            print(f"Пользователей с книгами: {with_books}")
            
            # 3. Примеры данных
            print("\nПримеры записей:")
            for user in User.query.limit(5).all():
                print(f"ID: {user.user_id}, Имя: {user.full_name}, Книги: {user.books}")
                
        except Exception as e:
            print(f"❌ Ошибка проверки: {e}")

if __name__ == "__main__":
    print("🔍 Финальная проверка данных...")
    check_data()