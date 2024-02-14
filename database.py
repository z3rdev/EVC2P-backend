import sqlite3
import personal

def create_db(tokens, codes):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wallets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT
        )
    ''')
    for token in tokens:
        cursor.execute('INSERT INTO tokens (token) VALUES (?)', (token,))
    for code in codes:
        cursor.execute('INSERT INTO codes (code) VALUES (?)', (code,))
    conn.commit()
    conn.close()

def get_token(code, wallet):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM wallets WHERE wallet = ?', (wallet,))
    if cursor.fetchone() is not None:
        conn.close()
        return None

    if int(code) in personal.data.keys():
        token = personal.data[int(code)]
        cursor.execute('INSERT INTO wallets (wallet) VALUES (?)', (wallet,))
        conn.commit()
        conn.close()
        return token

    cursor.execute('SELECT * FROM codes WHERE code = ?', (code,))
    if cursor.fetchone() is not None:
        cursor.execute('DELETE FROM codes WHERE code = ?', (code,))
        cursor.execute('INSERT INTO wallets (wallet) VALUES (?)', (wallet,))
        cursor.execute('SELECT * FROM tokens ORDER BY RANDOM() LIMIT 1')
        token = cursor.fetchone()
        cursor.execute('DELETE FROM tokens WHERE token = ?', (token[0],))
        conn.commit()
        conn.close()
        print(token)
        return token[1]
    else:
        cursor.execute('SELECT * FROM wallets WHERE wallet = ?', (wallet,))
        if cursor.fetchone() is not None:
            conn.close()
            return None
        else:
            conn.close()
            return None
        
def undo(token, code, wallet):
    if code in personal.data.keys():
        return
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tokens (token) VALUES (?)', (token,))
    cursor.execute('INSERT INTO codes (code) VALUES (?)', (code,))
    cursor.execute('DELETE FROM wallets WHERE wallet = ?', (wallet,))
    conn.commit()
    conn.close()