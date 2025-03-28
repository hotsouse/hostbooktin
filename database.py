from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

app = Flask(__name__)

# Настройка URI для базы данных PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:[covdeP-higtup-mimgi7]@db.krtkebdtxypgczlamacx.supabase.co:5432/postgres"

# Если URL начинается с postgres://, заменяем на postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
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