# controller/transaksi_controller.py
from model.transaksi_model import TransaksiModel
from utils.perhitungan import hitung_luas_dari_tipe


class TransaksiController:
    def __init__(self):
        self.model = TransaksiModel()

    def simpan_transaksi(self, data):
        self.model.simpan_transaksi(data)

    def ambil_semua_transaksi(self):
        return self.model.ambil_semua_transaksi()
