import psycopg2
import os
from dotenv import(
    load_dotenv
)

load_dotenv()

class DB:
    def __init__(self):
        DATABASE_HOST = os.getenv('DATABASE_HOST')
        DATABASE_PORT = os.getenv('DATABASE_PORT')
        DATABASE_NAME = os.getenv('DATABASE_NAME')
        DATABASE_USER = os.getenv('DATABASE_USER')
        DATABASE_PASS = os.getenv('DATABASE_PASS')

        self.conn = psycopg2.connect (
            host = DATABASE_HOST,
            port = DATABASE_PORT,
            database = DATABASE_NAME,
            user = DATABASE_USER,
            password = DATABASE_PASS
        )

        self.cur = self.conn.cursor()

    def insert_user(self, tg_id, name): 
        self.cur.execute("INSERT INTO users (tg_id, name) VALUES (%s, %s) RETURNING id;", (tg_id, name))
        self.conn.commit()
        id = self.cur.fetchone()[0]
        return id

    def insert_notification(self, userId, text, date):
        self.cur.execute("INSERT INTO notifications (user_id, text, date) VALUES (%s, %s, %s)", (userId, text, date))
        self.conn.commit()

    def checkTGId(self, tg_id):
        self.cur.execute("SELECT * FROM users WHERE tg_id = %s", (tg_id,))
        self.conn.commit()
        try:
            id = self.cur.fetchone()[0]
            if id is not None:
                return id
        except:
            pass

    def viewData(self):
        self.cur.execute("SELECT * FROM users;")
        print(self.cur.fetchall())
        self.conn.commit()