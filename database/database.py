import sqlite3, random, time

con = sqlite3.connect("database/database.db", check_same_thread=False)
cur = con.cursor()

def user():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user (
            user_name VARCHAR(20),
            user_id INTEGER PRIMARY KEY,
            ava INTEGER,
            reg_time INTEGER
        );
    """)
    con.commit()

def result():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            topic TEXT,
            score TEXT,
            date TEXT
        )
    """)
    con.commit()

def auth():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS auth (
            login TEXT,
            password TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES user(user_id)
        );
    """)
    con.commit()

def db_create():
    user()
    result()
    auth()

def register_user(login, user_name, password):
    user_id = random.randint(100000, 999999)
    reg_time = int(time.time())
    ava = 1
    
    cur.execute("""
        INSERT INTO user (user_name, user_id, ava, reg_time)
        VALUES (?, ?, ?, ?)
    """, (user_name, user_id, ava, reg_time))
    
    cur.execute("""
        INSERT INTO auth (login, password, user_id)
        VALUES (?, ?, ?)
    """, (login, password, user_id))
    
    con.commit()
    return user_id

def authenticate_user(login, password):
    cur.execute("""
        SELECT * FROM auth WHERE login = ? AND password = ?
    """, (login, password))
    
    record = cur.fetchone()
    return bool(record)

def get_user_by_id(user_id):
    con = sqlite3.connect("database/database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM user WHERE user_id = ?", (user_id,))
    user = cur.fetchone()
    con.close()
    return user

def get_user_id_by_login(login):
    cur.execute("SELECT user_id FROM auth WHERE login = ?", (login,))
    row = cur.fetchone()
    return row[0] if row else None

from datetime import datetime

def save_test_result(user_id, topic, correct, total):
    with sqlite3.connect("database/database.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO results (user_id, topic, score, date) VALUES (?, ?, ?, ?)", (
            user_id,
            topic,
            f"{correct}/{total}",
            datetime.now().strftime("%d.%m.%Y")
        ))
        conn.commit()

def get_user_tests(user_id):
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT topic, score, date FROM results WHERE user_id = ?", (user_id,))
    results = cursor.fetchall()
    conn.close()

    return [{"topic": row[0], "score": row[1], "date": row[2]} for row in results]

def update_avatar_filename(user_id, filename):
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE user SET ava = ? WHERE user_id = ?", (filename, user_id))
    conn.commit()
    conn.close()
