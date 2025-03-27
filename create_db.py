from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Настройка URI для базы данных PostgreSQL
DATABASE_URL = "postgresql://postgres:[YOUR-PASSWORD]@db.krtkebdtxypgczlamacx.supabase.co:5432/postgres"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", DATABASE_URL)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Определение модели таблицы
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String(80))
    full_name = db.Column(db.String(120))
    books = db.Column(db.Text)
    started = db.Column(db.Boolean, default=False)

# Создание движка базы данных
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Создание метаданных
metadata = MetaData()

# Создаем таблицы, если их нет
with app.app_context():
    # Создаем таблицы в PostgreSQL
    metadata.create_all(engine)
    
    # Проверяем, есть ли данные в старой SQLite базе
    try:
        old_engine = create_engine("sqlite:////data/users_books.db")
        old_session = sessionmaker(bind=old_engine)()
        
        # Получаем все данные из старой базы
        old_users = old_session.query(User).all()
        
        # Переносим данные в новую базу
        for user in old_users:
            new_user = User(
                user_id=user.user_id,
                username=user.username,
                full_name=user.full_name,
                books=user.books,
                started=user.started
            )
            session.add(new_user)
        
        # Сохраняем изменения
        session.commit()
        print("Данные успешно перенесены из SQLite в PostgreSQL")
        
    except Exception as e:
        print(f"Ошибка при переносе данных: {e}")
    finally:
        old_session.close()
        session.close()
