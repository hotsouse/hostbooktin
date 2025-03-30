import os
import logging
import psycopg2
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def initialize_database():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()  # Create a cursor before using it
        # Example SQL to create tables or initialize the database
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) NOT NULL
            );
        """)
        conn.commit()  # Commit the changes
        cursor.close()  # Close the cursor
        conn.close()    # Close the connection
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")

def fetch_users():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()  # Create a cursor before using it
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.close()  # Close the cursor
        conn.close()    # Close the connection
        return rows
    except Exception as e:
        logger.error(f"Ошибка при получении пользователей: {e}")
        return None

# Call the initialize_database function to set up the database
initialize_database() 