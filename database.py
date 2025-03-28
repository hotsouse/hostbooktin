from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

app = Flask(__name__)

# Настройка URI для базы данных PostgreSQL с использованием Transaction Pooler
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres.krtkebdtxypgczlamacx:covdeP-higtup-mimgi7@aws-0-eu-central-1.pooler.supabase.com:6543/postgres")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}

db = SQLAlchemy(app)

# Определение модели таблицы
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String(80))
    full_name = db.Column(db.String(120))
    books = db.Column(db.Text)
    started = db.Column(db.Boolean, default=False)