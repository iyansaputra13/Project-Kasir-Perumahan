# config/db_config.py

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kasirperumahan133123!",
        database="kasir_perumahan"
    )
