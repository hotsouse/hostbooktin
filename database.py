from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Используем проверенную строку подключения
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres.krtkebdtxypgczlamacx:covdeP-higtup-mimgi7@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'  # явно указываем таблицу
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), unique=True)  # Для UUID
    username = db.Column(db.String(80), nullable=True)
    full_name = db.Column(db.String(120), nullable=False)
    books = db.Column(db.Text, nullable=True)
    started = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Создаём таблицы при первом запуске
with app.app_context():
    db.create_all()
    print("✅ Таблицы успешно созданы/проверены")