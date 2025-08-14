from config.db_config import get_connection

class TransaksiModel:
    def simpan_transaksi(self, data):
        if 'dp' not in data:
            data['dp'] = data.get('dp_total', 0)

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
                utj, dp, cicilan_per_bulan, foto_ktp
            FROM transaksi
            ORDER BY id ASC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def update_transaksi(self, transaksi_id, data_baru):
        if 'dp' not in data_baru:
            data_baru['dp'] = data_baru.get('dp_total', 0)

        conn = get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE transaksi SET
                nama = %s,
                nik = %s,
                tempat_lahir = %s,
                tanggal_lahir = %s,
                alamat = %s,
                no_hp = %s,
                email = %s,
                nama_proyek = %s,
                blok_kavling = %s,
                tipe_rumah = %s,
                harga_rumah = %s,
                skema_pembayaran = %s,
                utj = %s,
                dp = %s,
                cicilan_per_bulan = %s,
                foto_ktp = %s
            WHERE id = %s
        """
        cursor.execute(query, (
            data_baru['nama'],
            data_baru['nik'],
            data_baru['tempat_lahir'],
            data_baru['tanggal_lahir'],
            data_baru['alamat'],
            data_baru['no_hp'],
            data_baru['email'],
            data_baru['nama_proyek'],
            data_baru['blok_kavling'],
            data_baru['tipe_rumah'],
            data_baru['harga_rumah'],
            data_baru['skema_pembayaran'],
            data_baru['utj'],
            data_baru['dp'],
            data_baru['cicilan_per_bulan'],
            data_baru['foto_ktp'],
            transaksi_id
        ))
        conn.commit()
        cursor.close()
        conn.close()

    def hapus_transaksi(self, transaksi_id):
        conn = get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM transaksi WHERE id = %s"
        cursor.execute(query, (transaksi_id,))
        conn.commit()
        cursor.close()
        conn.close()

    # =======================
    # Tambahan untuk cicilan DP
    # =======================
    def ambil_cicilan_dp(self, transaksi_id):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT 
                id, bulan_ke, cicilan, bayar, sisa, tanggal_bayar, catatan
            FROM cicilan_dp
            WHERE transaksi_id = %s
            ORDER BY bulan_ke ASC
        """
        cursor.execute(query, (transaksi_id,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def simpan_cicilan_dp(self, transaksi_id, data_cicilan):
        conn = get_connection()
        cursor = conn.cursor()

        # Hapus data cicilan lama untuk transaksi ini
        delete_query = "DELETE FROM cicilan_dp WHERE transaksi_id = %s"
        cursor.execute(delete_query, (transaksi_id,))

        # Insert ulang data cicilan baru
        insert_query = """
            INSERT INTO cicilan_dp (
                transaksi_id, bulan_ke, cicilan, bayar, sisa, tanggal_bayar, catatan
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        for cicilan in data_cicilan:
            cursor.execute(insert_query, (
                transaksi_id,
                cicilan.get('bulan_ke'),
                cicilan.get('cicilan', 0),
                cicilan.get('bayar', 0),
                cicilan.get('sisa', 0),
                cicilan.get('tanggal_bayar'),
                cicilan.get('catatan', '')
            ))

        conn.commit()
        cursor.close()
        conn.close()
