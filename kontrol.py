import sqlite3

conn = sqlite3.connect("doviz.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM kurlar")
for satir in cursor.fetchall():
    print(satir)
conn.close()