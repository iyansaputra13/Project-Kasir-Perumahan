from model.transaksi_model import TransaksiModel
from utils.perhitungan import hitung_luas_dari_tipe

class TransaksiController:
    def __init__(self):
        self.model = TransaksiModel()

    def simpan_transaksi(self, data):
        # Tambahkan luas tanah otomatis jika tipe rumah ada
        if "tipe_rumah" in data and "luas" not in data:
            data["luas"] = hitung_luas_dari_tipe(data["tipe_rumah"])
        return self.model.simpan_transaksi(data)

    def ambil_semua_transaksi(self):
        return self.model.ambil_semua_transaksi()

    def ambil_transaksi_by_id(self, transaksi_id):
        return self.model.ambil_transaksi_by_id(transaksi_id)

    def update_transaksi(self, transaksi_id, data_baru):
        # Hitung luas tanah jika belum ada
        if "tipe_rumah" in data_baru and "luas" not in data_baru:
            data_baru["luas"] = hitung_luas_dari_tipe(data_baru["tipe_rumah"])
        return self.model.update_transaksi(transaksi_id, data_baru)

    def hapus_transaksi(self, transaksi_id):
        return self.model.hapus_transaksi(transaksi_id)

    # Cicilan DP
    def ambil_cicilan_dp(self, transaksi_id):
        return self.model.ambil_cicilan_dp(transaksi_id)

    def simpan_cicilan_dp(self, transaksi_id, data_cicilan):
        return self.model.simpan_cicilan_dp(transaksi_id, data_cicilan)
