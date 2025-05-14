import sqlite3

import bcrypt

def init_db():
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Table 'users' créée ou déjà existante.")

def authenticate_user(username, password):
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_hashed_pw = result[0]  # string depuis SQLite
        return bcrypt.checkpw(password.encode(), stored_hashed_pw.encode())  # conversion ici
    return False



def add_user(username,email ,password ):
    try:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  # hachage sécurisé
        conn = sqlite3.connect("database/users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                       (username, email , hashed.decode()))  # stocker en string
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def reset_password(username, email, new_password):
    hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND email=?", (username, email))
    user = cursor.fetchone()

    if user:
        cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_pw, username))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False



def store_reset_code(email, code):
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reset_codes (
            email TEXT PRIMARY KEY,
            code TEXT NOT NULL
        )
    ''')
    cursor.execute("REPLACE INTO reset_codes (email, code) VALUES (?, ?)", (email, code))
    conn.commit()
    conn.close()

def verify_reset_code(email, code):
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT code FROM reset_codes WHERE email=?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0] == code

def clear_reset_code(email):
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reset_codes WHERE email=?", (email,))
    conn.commit()
    conn.close()

