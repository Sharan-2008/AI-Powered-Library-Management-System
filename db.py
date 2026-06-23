import os
import mysql.connector
import dotenv

dotenv.load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )


def init_db():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
    conn.database = os.getenv('DB_NAME')

    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        b_id INT PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(255),
        author VARCHAR(255),
        genre VARCHAR(100),
        year INT,
        quantity INT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_interest (
        id INT AUTO_INCREMENT PRIMARY KEY,
        genre VARCHAR(100),
        count INT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        userid VARCHAR(50) PRIMARY KEY,
        username VARCHAR(100),
        password VARCHAR(255),
        role VARCHAR(10) DEFAULT 'user'
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS issued_books(
        issue_id INT AUTO_INCREMENT PRIMARY KEY,
        b_id INT,
        userid VARCHAR(100),
        issue_date DATE,
        return_date DATE,
        FOREIGN KEY(b_id) REFERENCES books(b_id),
        FOREIGN KEY(userid) REFERENCES users(userid) ON DELETE CASCADE)
    ''')

    conn.commit()
    cursor.close()
    conn.close()
