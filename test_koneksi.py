from database.db_config import create_connection

try:
    conn = create_connection()
    print("✅ Koneksi Berhasil")
    conn.close()
except Exception as e:
    print("❌ Koneksi Gagal:", e)
