from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Настройка URI для базы данных PostgreSQL
DATABASE_URL = "postgresql://postgres:[covdeP-higtup-mimgi7]@db.krtkebdtxypgczlamacx.supabase.co:5432/postgres"
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

# Создание движка базы данных PostgreSQL
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Создание метаданных
metadata = MetaData()

# Создаем таблицы, если их нет
with app.app_context():
    try:
        # Создаем таблицы в PostgreSQL
        metadata.create_all(engine)
        print("Таблицы успешно созданы в PostgreSQL")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")