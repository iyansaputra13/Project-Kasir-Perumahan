from model.transaksi_model import TransaksiModel
from utils.perhitungan import hitung_luas_dari_tipe

class TransaksiController:
    def __init__(self):
        self.model = TransaksiModel()

    def simpan_transaksi(self, data):
        self.model.simpan_transaksi(data)

    def ambil_semua_transaksi(self):
        return self.model.ambil_semua_transaksi()

    def update_transaksi(self, transaksi_id, data_baru):
        self.model.update_transaksi(transaksi_id, data_baru)

    def hapus_transaksi(self, transaksi_id):
        self.model.hapus_transaksi(transaksi_id)
