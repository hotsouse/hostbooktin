from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_migrate import Migrate


load_dotenv()

app = Flask(__name__)

# Используем проверенную строку подключения
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres.krtkebdtxypgczlamacx:covdeP-higtup-mimgi7@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db) 

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, unique=True)  # Changed to BigInteger
    username = db.Column(db.String(100))
    full_name = db.Column(db.String(100))
    books = db.Column(db.Text)
    started = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'
    
# database.py
class Exchange(db.Model):
    __tablename__ = 'exchanges'
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'))  # Изменили на BigInteger
    to_user_id = db.Column(db.BigInteger, db.ForeignKey('users.user_id'))   # Изменили на BigInteger
    book_given = db.Column(db.String(100))
    book_received = db.Column(db.String(100))
    exchange_date = db.Column(db.DateTime)
    status = db.Column(db.String(20))

# Создаём таблицы при первом запуске
with app.app_context():
    db.create_all()
    print("✅ Таблицы успешно созданы/проверены")