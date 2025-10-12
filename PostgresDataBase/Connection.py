import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


class DataBase:
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

    def insert_user(self, tg_id, name):
        self.cur.execute(
            "INSERT INTO users (tg_id, name) VALUES (%s, %s) RETURNING id;",
            (tg_id, name),
        )
        self.conn.commit()
        id = self.cur.fetchone()[0]
        return id

    def insert_notification(self, userId, text, date):
        self.cur.execute(
            "INSERT INTO notifications (user_id, text, date, sent) VALUES (%s, %s, %s, %s)",
            (userId, text, date, False),
        )
        self.conn.commit()

    def get_messages(self):
        # Get all unsent messages first
        query_all = """
            SELECT id, user_id, text, date, sent
            FROM notifications
            WHERE sent = FALSE
        """
        self.cur.execute(query_all)
        all_rows = self.cur.fetchall()
        
        # Debug: print all unsent messages
        print(f"All unsent messages: {len(all_rows)}")
        for row in all_rows:
            print(f"Message {row[0]}: date={row[3]}, sent={row[4]}")
        
        # Filter by time in Python to avoid timezone issues
        import datetime
        now = datetime.datetime.now()
        due_messages = []
        
        for row in all_rows:
            message_date = row[3]
            # Convert to naive datetime if it's timezone-aware
            if hasattr(message_date, 'replace'):
                message_date = message_date.replace(tzinfo=None)
            
            print(f"Comparing: {message_date} <= {now} = {message_date <= now}")
            if message_date <= now:
                due_messages.append(row)
        
        print(f"Due messages: {len(due_messages)}")
        return [
            {
                "id": row[0],
                "user_id": row[1],
                "text": row[2],
                "date": row[3],
                "sent": row[4],
            }
            for row in due_messages
        ]

    def get_user(self, id):
        query = """
            SELECT tg_id
            FROM users
            WHERE id = %s
        """
        self.cur.execute(query, (id,))
        tg_id = self.cur.fetchall()
        return tg_id

    def mark_message_as_sent(self, message_id):
        query = "UPDATE notifications SET sent = TRUE WHERE id = %s"
        self.cur.execute(query, (message_id,))
        self.conn.commit()

    def check_tg_id(self, tg_id):
        self.cur.execute("SELECT * FROM users WHERE tg_id = %s", (tg_id,))
        self.conn.commit()
        try:
            id = self.cur.fetchone()[0]
            if id is not None:
                return id
        except:
            pass
