# config/db_config.py

import mysql.connector

db_config = {
    'host': '192.168.1.19',
    'user': 'hari',
    'password': 'Hari123!',
}

def get_connection():
    return mysql.connector.connect(**db_config)
