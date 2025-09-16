from PostgresDataBase.Connection import DataBase
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

database_class = DataBase()


class DBInit():
    def __init__(self):
        DATABASE_HOST = os.getenv("DATABASE_HOST")
        DATABASE_PORT = os.getenv("DATABASE_PORT")
        DATABASE_NAME = os.getenv("DATABASE_NAME")
        DATABASE_USER = os.getenv("DATABASE_USER")
        DATABASE_PASS = os.getenv("DATABASE_PASS")

        self.conn = psycopg2.connect(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            database=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASS,
        )

        self.cur = self.conn.cursor()



    def db_init(self):
        query = """
            SELECT
                CASE WHEN OBJECT_ID("user_id", "U") IS NOT NULL
                THEN 'Table exists'
                ELSE 'Table not exists'
                END AS TableExistenceStatus;
        """
        self.cur.execute(query)
        print (self.cur.fetchall())
