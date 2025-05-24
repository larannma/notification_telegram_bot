import psycopg2
import os
from dotenv import(
    load_dotenv
)

load_dotenv()
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASS = os.getenv('DATABASE_PASS')

conn = psycopg2.connect(
    host = DATABASE_HOST,
    port = DATABASE_PORT,
    database = DATABASE_NAME,
    user = DATABASE_USER,
    password = DATABASE_PASS
)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS notifications;")
cur.execute("DROP TABLE IF EXISTS users;")

cur.execute("""
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        tg_id TEXT UNIQUE,
        name TEXT
    );
""")

cur.execute("""
    CREATE TABLE notifications (
        id SERIAL PRIMARY KEY,
        user_id INTEGER,
        text TEXT,
        date DATE,
        CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id)
            ON UPDATE NO ACTION
            ON DELETE NO ACTION
    );
""")

conn.commit()
cur.close()
conn.close()