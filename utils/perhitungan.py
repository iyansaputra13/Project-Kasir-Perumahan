#utills/perhitungan.py

def hitung_luas_dari_tipe(tipe):
    mapping = {
        "DIAMOND POJOK": (195, 150),
        "DIAMOND": (120, 142),
        "SAPHIRE A": (105, 60),
        "SAPHIRE B": (97.5, 48),
        "RUBY": (78, 45)
    }
    return mapping.get(tipe.upper(), (0, 0))  # default jika tipe tidak ditemukan
