import sqlite3

# Exemple simple
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute("SELECT sqlite_version();")
print("Version SQLite:", c.fetchone())
conn.close()
