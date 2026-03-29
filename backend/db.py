import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST") or "127.0.0.1",
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        database=os.environ.get("DB_NAME"),
    )

# ✅ USER FUNCTIONS

def create_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (%s, %s)",
            (email, password)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        cursor.close()
        conn.close()


def get_user(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, email, password FROM users WHERE email=%s",
        (email,)
    )
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

# ✅ SUBSCRIBERS (NOW USER-SPECIFIC)

def add_subscriber(email, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO subscribers (email, user_id) VALUES (%s, %s)",
            (email, user_id)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        cursor.close()
        conn.close()


def unsubscribe(email, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE subscribers SET status='unsubscribed' WHERE email=%s AND user_id=%s",
        (email, user_id)
    )
    conn.commit()

    cursor.close()
    conn.close()


def get_all_subscribers(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT email, status FROM subscribers WHERE user_id=%s",
        (user_id,)
    )
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


def get_active_subscribers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT email FROM subscribers WHERE status='active'"
    )
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return [row[0] for row in result]