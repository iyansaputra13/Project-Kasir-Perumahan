# models/transaksi_model.py
from config.supabase_config import get_supabase
from datetime import datetime

class TransaksiModel:
    def __init__(self):
        self.supabase = get_supabase()

    def simpan_transaksi(self, data):
        if 'dp' not in data:
            data['dp'] = data.get('dp_total', 0)

        # Prepare data for Supabase
        transaksi_data = {
            'nama': data['nama'],
            'nik': data['nik'],
            'tempat_lahir': data['tempat_lahir'],
            'tanggal_lahir': data['tanggal_lahir'],
            'alamat': data['alamat'],
            'no_hp': data['no_hp'],
            'email': data['email'],
            'nama_proyek': data['nama_proyek'],
            'blok_kavling': data['blok_kavling'],
            'tipe_rumah': data['tipe_rumah'],
            'harga_rumah': float(data['harga_rumah']),
            'skema_pembayaran': data['skema_pembayaran'],
            'utj': float(data['utj']),
            'dp': float(data['dp']),
            'cicilan_per_bulan': float(data['cicilan_per_bulan']),
            'foto_ktp': data['foto_ktp'],
            'created_at': datetime.now().isoformat()
        }

        # Insert to Supabase
        response = self.supabase.table('transaksi').insert(transaksi_data).execute()
        return response.data[0] if response.data else None

    def ambil_semua_transaksi(self):
        response = self.supabase.table('transaksi').select('*').order('id', desc=False).execute()
        return response.data

    def ambil_transaksi_by_id(self, transaksi_id):
        response = self.supabase.table('transaksi').select('*').eq('id', transaksi_id).execute()
        return response.data[0] if response.data else None

    def update_transaksi(self, transaksi_id, data_baru):
        if 'dp' not in data_baru:
            data_baru['dp'] = data_baru.get('dp_total', 0)

        update_data = {
            'nama': data_baru['nama'],
            'nik': data_baru['nik'],
            'tempat_lahir': data_baru['tempat_lahir'],
            'tanggal_lahir': data_baru['tanggal_lahir'],
            'alamat': data_baru['alamat'],
            'no_hp': data_baru['no_hp'],
            'email': data_baru['email'],
            'nama_proyek': data_baru['nama_proyek'],
            'blok_kavling': data_baru['blok_kavling'],
            'tipe_rumah': data_baru['tipe_rumah'],
            'harga_rumah': float(data_baru['harga_rumah']),
            'skema_pembayaran': data_baru['skema_pembayaran'],
            'utj': float(data_baru['utj']),
            'dp': float(data_baru['dp']),
            'cicilan_per_bulan': float(data_baru['cicilan_per_bulan']),
            'foto_ktp': data_baru['foto_ktp'],
            'updated_at': datetime.now().isoformat()
        }

        response = self.supabase.table('transaksi').update(update_data).eq('id', transaksi_id).execute()
        return response.data[0] if response.data else None

    def hapus_transaksi(self, transaksi_id):
        response = self.supabase.table('transaksi').delete().eq('id', transaksi_id).execute()
        return response.data[0] if response.data else None

    # =======================
    # Methods untuk cicilan DP
    # =======================
    def ambil_cicilan_dp(self, transaksi_id):
        response = self.supabase.table('cicilan_dp').select('*').eq('transaksi_id', transaksi_id).order('bulan_ke', desc=False).execute()
        return response.data

    def simpan_cicilan_dp(self, transaksi_id, data_cicilan):
        # Hapus data cicilan lama
        self.supabase.table('cicilan_dp').delete().eq('transaksi_id', transaksi_id).execute()

        # Siapkan data cicilan baru (tanpa kolom 'sisa' karena generated)
        cicilan_data = []
        for cicilan in data_cicilan:
            cicilan_item = {
                'transaksi_id': transaksi_id,
                'bulan_ke': cicilan.get('bulan_ke'),
                'cicilan': float(cicilan.get('cicilan', 0)),
                'bayar': float(cicilan.get('bayar', 0)),
                'tanggal_bayar': cicilan.get('tanggal_bayar'),
                'catatan': cicilan.get('catatan', ''),
                'created_at': datetime.now().isoformat()
            }
            cicilan_data.append(cicilan_item)

        # Insert data cicilan baru
        if cicilan_data:
            response = self.supabase.table('cicilan_dp').insert(cicilan_data).execute()
            return response.data
        return []

    def hapus_cicilan_dp(self, transaksi_id):
        response = self.supabase.table('cicilan_dp').delete().eq('transaksi_id', transaksi_id).execute()
        return response.data