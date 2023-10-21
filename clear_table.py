import sqlite3


db_path = "./instance/users.db"
conn = sqlite3.connect(db_path)

cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

conn.commit()
conn.close()