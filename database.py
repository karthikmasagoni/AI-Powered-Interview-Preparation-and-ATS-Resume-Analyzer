import sqlite3
import hashlib

DB_NAME = "users.db"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS scores(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        score INTEGER,
        percentage REAL
    )
    """)

    conn.commit()
    conn.close()


def register_user(username, password):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:

        cur.execute(
            """
            INSERT INTO users(
                username,
                password
            )
            VALUES(?,?)
            """,
            (
                username,
                hash_password(password)
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


def login_user(username, password):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        AND password=?
        """,
        (
            username,
            hash_password(password)
        )
    )

    user = cur.fetchone()

    conn.close()

    return user


def save_score(
    username,
    score,
    percentage
):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO scores(
            username,
            score,
            percentage
        )
        VALUES(?,?,?)
        """,
        (
            username,
            score,
            percentage
        )
    )

    conn.commit()
    conn.close()


def get_scores(username):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
        score,
        percentage
        FROM scores
        WHERE username=?
        """,
        (username,)
    )

    data = cur.fetchall()

    conn.close()

    return data