# config/db_config.py

import mysql.connector
db_config = {
    'host': '192.168.1.23',
    'user': 'haron',
    'password': 'Haron123!',
    'database': 'kasir_perumahan'
}

def get_connection():
    return mysql.connector.connect(**db_config)
