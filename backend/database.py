import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="creditwise"
        )
        return conn
    except Error as e:
        print("Error de conexión:", e)
        raise
