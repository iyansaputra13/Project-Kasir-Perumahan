# controller/auth_controller.py

from config.supabase_config import get_supabase


class AuthController:
    def __init__(self):
        self.supabase = get_supabase()

    def authenticate(self, username, password):
        """Authenticate user credentials dengan Supabase"""
        try:
            # Query ke tabel "users" di Supabase
            response = (
                self.supabase
                .table("users")
                .select("*")
                .eq("username", username)
                .eq("password", password)
                .execute()
            )

            if response.data and len(response.data) > 0:
                user = response.data[0]  # Ambil user pertama
                # Tambahkan default role jika tidak ada
                user["role"] = user.get("role", "user")
                return user
            else:
                return None

        except Exception as e:
            raise Exception(f"Authentication error: {str(e)}")
