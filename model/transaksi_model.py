# model/transaksi_model.py
from config.db_config import get_connection

class TransaksiModel:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def simpan_transaksi(self, data):
        query = """
            INSERT INTO transaksi_rumah (
                nama, nik, ttl, alamat, no_hp, email,
                nama_proyek, blok, tipe_rumah, harga_jual, skema,
                utj, dp, cicilan_per_bulan, total_cicilan
            ) VALUES (%s, %s, %s, %s, %s, %s, 
                      %s, %s, %s, %s, %s, 
                      %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(query, (
                data['nama'], data['nik'], data['ttl'], data['alamat'],
                data['no_hp'], data['email'], data['nama_proyek'], data['blok'],
                data['tipe_rumah'], data['harga_jual'], data['skema'],
                data['utj'], data['dp'], data['cicilan_per_bulan'], data['total_cicilan']
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print("Gagal menyimpan transaksi:", e)
            self.conn.rollback()
            return False

    def ambil_semua_transaksi(self):
        try:
            query = "SELECT * FROM transaksi_rumah"
            self.cursor.execute(query)
            hasil = self.cursor.fetchall()
            return hasil
        except Exception as e:
            print("Gagal mengambil data transaksi:", e)
            return []
