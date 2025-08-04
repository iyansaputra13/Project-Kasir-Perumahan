# model/transaksi_model.py

from config.db_config import get_connection

class TransaksiModel:
    def simpan_transaksi(self, data):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO transaksi (nama, nik, tempat_lahir, tanggal_lahir, alamat, no_hp, email,
                                   proyek, blok_kavling, tipe_rumah, harga_jual, skema_pembayaran,
                                   utj, dp, cicilan_per_bulan, foto_ktp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data['nama'], data['nik'], data['tempat_lahir'], data['tanggal_lahir'],
            data['alamat'], data['no_hp'], data['email'], data['proyek'], data['blok_kavling'],
            data['tipe_rumah'], data['harga_jual'], data['skema_pembayaran'],
            data['utj'], data['dp'], data['cicilan_per_bulan']
        ))
        conn.commit()
        cursor.close()
        conn.close()

    def ambil_semua_transaksi(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM transaksi"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
