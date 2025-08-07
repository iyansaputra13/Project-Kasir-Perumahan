from mysql.connector import Error
from config.db_config import get_connection

class AuthController:
    def __init__(self):
        pass  # Inisialisasi jika diperlukan

    def authenticate(self, username, password):
        """Authenticate user credentials"""
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT id, username, full_name 
                FROM users 
                WHERE username = %s AND password = %s
            """
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            # Tambahkan default role jika tidak ada
            if user:
                user['role'] = user.get('role', 'user')  # Default role
            
            return user
            
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
        except Exception as e:
            raise Exception(f"Authentication error: {str(e)}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()