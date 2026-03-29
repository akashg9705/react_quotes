import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        return mysql.connector.connect(
            host=os.environ.get("DB_HOST") or "127.0.0.1",
            port=int(os.environ.get("DB_PORT", 3306)),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS"),
            database=os.environ.get("DB_NAME"),
        )
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def init_db():
    conn = get_connection()
    if not conn:
        print("Failed to connect to database for initialization.")
        return
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                user_id INT NOT NULL,
                status VARCHAR(50) DEFAULT 'active'
            )
        """)
        conn.commit()
        print("Database tables initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        cursor.close()
        conn.close()

# ✅ USER FUNCTIONS

def create_user(email, password):
    conn = get_connection()
    if not conn:
        return False
        
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (%s, %s)",
            (email, password)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def get_user(email):
    conn = get_connection()
    if not conn:
        return None
        
    cursor = conn.cursor()
    user = None

    try:
        cursor.execute(
            "SELECT id, email, password FROM users WHERE email=%s",
            (email,)
        )
        user = cursor.fetchone()
    except Exception as e:
        print(f"Error getting user: {e}")
    finally:
        cursor.close()
        conn.close()

    return user

# ✅ SUBSCRIBERS (NOW USER-SPECIFIC)

def add_subscriber(email, user_id):
    conn = get_connection()
    if not conn:
        return False
        
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO subscribers (email, user_id) VALUES (%s, %s)",
            (email, user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding subscriber: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def unsubscribe(email, user_id):
    conn = get_connection()
    if not conn:
        return False
        
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE subscribers SET status='unsubscribed' WHERE email=%s AND user_id=%s",
            (email, user_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error unsubscribing: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def get_all_subscribers(user_id):
    conn = get_connection()
    if not conn:
        return []
        
    cursor = conn.cursor()
    result = []
    
    try:
        cursor.execute(
            "SELECT email, status FROM subscribers WHERE user_id=%s",
            (user_id,)
        )
        result = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching subscribers: {e}")
    finally:
        cursor.close()
        conn.close()

    return result


def get_active_subscribers():
    conn = get_connection()
    if not conn:
        return []
        
    cursor = conn.cursor()
    result = []
    
    try:
        cursor.execute(
            "SELECT email FROM subscribers WHERE status='active'"
        )
        result = cursor.fetchall()
    except Exception as e:
        print(f"Error fetching active subscribers: {e}")
    finally:
        cursor.close()
        conn.close()

    return [row[0] for row in result]