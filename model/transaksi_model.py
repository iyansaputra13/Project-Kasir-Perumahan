# model/transaksi_model.py
from config.db_config import get_connection



class TransaksiModel:
    def simpan_transaksi(self, data):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO transaksi (
                nama, nik, ttl, alamat, no_hp, email,
                proyek, blok, tipe, harga
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data['nama'], data['nik'], data['ttl'], data['alamat'],
            data['no_hp'], data['email'], data['proyek'], data['blok'],
            data['tipe'], data['harga']
        ))
        conn.commit()
        cursor.close()
        conn.close()

    def ambil_semua_transaksi(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transaksi")
        hasil = cursor.fetchall()
        cursor.close()
        conn.close()
        return hasil
