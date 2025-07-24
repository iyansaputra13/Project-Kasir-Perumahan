from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QDateEdit, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import QDate
from controller.transaksi_controller import TransaksiController


class FormInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Form Input Transaksi")
        self.setMinimumWidth(400)
        self.controller = TransaksiController()

        # Data proyek dan harga rumah
        self.proyek_tipe_harga = {
            "KAWASAN NEW CITY": {
                "DIAMOND POJOK": 2090500000,
                "DIAMOND": 1615500000,
                "SAPHIRE A": 910500000,
                "SAPHIRE B": 805500000,
                "RUBY": 660500000,
            }
        }

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.nama_input = QLineEdit()
        self.nik_input = QLineEdit()
        self.ttl_input = QLineEdit()
        self.alamat_input = QLineEdit()
        self.hp_input = QLineEdit()
        self.email_input = QLineEdit()

        self.proyek_combo = QComboBox()
        self.proyek_combo.addItems(self.proyek_tipe_harga.keys())
        self.proyek_combo.currentTextChanged.connect(self.update_tipe_rumah)

        self.tipe_combo = QComboBox()

        self.harga_label = QLabel("Harga: -")
        self.utj_label = QLabel("UTJ: -")
        self.dp_label = QLabel("DP (20%): -")
        self.cicilan_label = QLabel("Cicilan 12x: -")

        self.hitung_btn = QPushButton("Hitung Skema 12x")
        self.hitung_btn.clicked.connect(self.hitung_skema_angsuran)

        self.simpan_btn = QPushButton("Simpan Transaksi")
        self.simpan_btn.clicked.connect(self.simpan_transaksi)

        # Tambahkan semua input ke layout
        layout.addWidget(QLabel("Nama Pembeli"))
        layout.addWidget(self.nama_input)

        layout.addWidget(QLabel("NIK"))
        layout.addWidget(self.nik_input)

        layout.addWidget(QLabel("Tempat/Tanggal Lahir"))
        layout.addWidget(self.ttl_input)

        layout.addWidget(QLabel("Alamat"))
        layout.addWidget(self.alamat_input)

        layout.addWidget(QLabel("No. HP"))
        layout.addWidget(self.hp_input)

        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.email_input)

        layout.addWidget(QLabel("Nama Proyek"))
        layout.addWidget(self.proyek_combo)

        layout.addWidget(QLabel("Tipe Rumah"))
        layout.addWidget(self.tipe_combo)

        layout.addWidget(self.harga_label)
        layout.addWidget(self.utj_label)
        layout.addWidget(self.dp_label)
        layout.addWidget(self.cicilan_label)

        layout.addWidget(self.hitung_btn)
        layout.addWidget(self.simpan_btn)

        self.setLayout(layout)
        self.update_tipe_rumah()  # Load awal

    def update_tipe_rumah(self):
        proyek = self.proyek_combo.currentText()
        self.tipe_combo.clear()
        if proyek in self.proyek_tipe_harga:
            self.tipe_combo.addItems(self.proyek_tipe_harga[proyek].keys())

    def hitung_skema_angsuran(self):
        proyek = self.proyek_combo.currentText()
        tipe = self.tipe_combo.currentText()
        harga = self.proyek_tipe_harga[proyek][tipe]
        utj = 10_000_000
        sisa_setelah_utj = harga - utj
        dp = int(sisa_setelah_utj * 0.2)
        cicilan = int((sisa_setelah_utj - dp) / 12)

        self.harga_label.setText(f"Harga: Rp{harga:,.0f}")
        self.utj_label.setText(f"UTJ: Rp{utj:,.0f}")
        self.dp_label.setText(f"DP (20%): Rp{dp:,.0f}")
        self.cicilan_label.setText(f"Cicilan 12x: Rp{cicilan:,.0f}")

        # Simpan ke atribut agar bisa digunakan saat menyimpan
        self._harga = harga
        self._utj = utj
        self._dp = dp
        self._cicilan = cicilan

    def simpan_transaksi(self):
        try:
            data = {
                "nama": self.nama_input.text(),
                "nik": self.nik_input.text(),
                "ttl": self.ttl_input.text(),
                "alamat": self.alamat_input.text(),
                "no_hp": self.hp_input.text(),
                "email": self.email_input.text(),
                "nama_proyek": self.proyek_combo.currentText(),
                "blok": "-",  # Sementara default atau tambahkan input jika perlu
                "tipe_rumah": self.tipe_combo.currentText(),
                "harga_jual": self._harga,
                "skema": "Skema 12x",
                "utj": self._utj,
                "dp": self._dp,
                "cicilan_per_bulan": self._cicilan,
                "total_cicilan": self._cicilan * 12
            }

            self.controller.simpan_transaksi(data)

            QMessageBox.information(self, "Berhasil", "Data transaksi berhasil disimpan!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Gagal", f"Gagal menyimpan transaksi: {e}")
