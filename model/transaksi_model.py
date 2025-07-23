# model/transaksi_model.py
from config.db import get_connection

class TransaksiModel:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def simpan_transaksi(self, data):
        query = """
            INSERT INTO transaksi (
                nama, nik, tempat_lahir, tanggal_lahir, alamat, no_hp, email,
                proyek, blok, tipe_rumah, harga_jual
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (
            data['nama'], data['nik'], data['tempat_lahir'], data['tanggal_lahir'],
            data['alamat'], data['no_hp'], data['email'],
            data['proyek'], data['blok'], data['tipe_rumah'], data['harga_jual']
        ))
        self.conn.commit()

    def ambil_semua_transaksi(self):
        query = "SELECT * FROM transaksi"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def __del__(self):
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conn'):
            self.conn.close()
