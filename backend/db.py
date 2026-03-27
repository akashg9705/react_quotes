import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST") or "127.0.0.1",
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        database=os.environ.get("DB_NAME"),
    )

def add_subscriber(email):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO subscribers (email) VALUES (%s)",
            (email,)
        )
        conn.commit()
        return True
    except mysql.connector.Error:
        return False
    finally:
        cursor.close()
        conn.close()

def unsubscribe(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE subscribers SET status='unsubscribed' WHERE email=%s",
        (email,)
    )
    conn.commit()

    cursor.close()
    conn.close()

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

def get_all_subscribers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT email, status FROM subscribers")
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result