from database import db, app

def recreate_database():
    with app.app_context():
        try:
            print("🔄 Пересоздаем структуру базы...")
            db.drop_all()
            db.create_all()
            print("✅ Структура базы успешно пересоздана")
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    recreate_database()