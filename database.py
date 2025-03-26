from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Создаем каталог "mp", если он не существует
os.makedirs("mp", exist_ok=True)

# Настройка URI для базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///data/users_books.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем отслеживание изменений

db = SQLAlchemy(app)

# Определение модели таблицы
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String(80))
    full_name = db.Column(db.String(120))
    books = db.Column(db.Text)
    started = db.Column(db.Boolean, default=False)

# Создаем таблицы, если их нет
with app.app_context():
    db.create_all()