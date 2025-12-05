import sqlite3

conn = sqlite3.connect("crypto_prices.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM crypto_prices;")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
