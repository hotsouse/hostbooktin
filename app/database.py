from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
import logging
from flask import Flask
import psycopg2

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)

# Example function to fetch users
def fetch_users():
    # Replace cursor usage with SQLAlchemy session
    result = db.session.execute("SELECT * FROM users")
    rows = result.fetchall()
    return rows

# Example function to fetch users using psycopg2
def fetch_users_psycopg2():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()  # Create a cursor before using it
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    cursor.close()  # Close the cursor
    conn.close()    # Close the connection
    return rows

# ... rest of the original file content ... 