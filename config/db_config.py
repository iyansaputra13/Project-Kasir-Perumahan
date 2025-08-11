# config/db_config.py

import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Kasirperumahan133123!',
    'database': 'kasir_perumahan',
}

def get_connection():
    return mysql.connector.connect(**db_config)
