from config.db_config import get_connection

class TransaksiModel:
    def simpan_transaksi(self, data):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO transaksi (
                nama, nik, tempat_lahir, tanggal_lahir, alamat, no_hp, email,
                nama_proyek, blok_kavling, tipe_rumah, harga_rumah, skema_pembayaran,
                utj, dp, cicilan_per_bulan, foto_ktp
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data['nama'],
            data['nik'],
            data['tempat_lahir'],
            data['tanggal_lahir'],
            data['alamat'],
            data['no_hp'],
            data['email'],
            data['nama_proyek'],
            data['blok_kavling'],
            data['tipe_rumah'],
            data['harga_rumah'],
            data['skema_pembayaran'],
            data['utj'],
            data['dp'],
            data['cicilan_per_bulan'],
            data['foto_ktp']
        ))
        conn.commit()
        cursor.close()
        conn.close()

    def ambil_semua_transaksi(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                id, nama, nik, tempat_lahir, tanggal_lahir, alamat, no_hp, email,
                nama_proyek, blok_kavling, tipe_rumah, harga_rumah, skema_pembayaran,
                utj, dp, cicilan_per_bulan
            FROM transaksi
            ORDER BY id ASC
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
