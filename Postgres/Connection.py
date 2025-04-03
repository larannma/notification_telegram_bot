import psycopg2

conn = psycopg2.connect (
    host = "localhost",
    port = 5432,
    database = "postgres",
    user = "postgres",
    password = "56787"
)

cur = conn.cursor()

cur.execute("SELECT * FROM users;")

conn.commit()
print(cur.fetchall())