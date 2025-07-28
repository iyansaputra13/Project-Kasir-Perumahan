from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QDateEdit, QMessageBox, QHBoxLayout
)
from PySide6.QtCore import QDate
from PySide6.QtGui import QFont
from controller.transaksi_controller import TransaksiController


class FormInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Form Input Transaksi Rumah")
        self.controller = TransaksiController()
        self._harga = 0
        self._utj = 0
        self._dp = 0
        self._cicilan = 0

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        font_label = QFont("Arial", 10)

        # --- Data Pembeli ---
        self.nama_input = QLineEdit()
        self.nik_input = QLineEdit()
        self.tempat_lahir_input = QLineEdit()
        self.tanggal_lahir_input = QDateEdit()
        self.tanggal_lahir_input.setCalendarPopup(True)
        self.tanggal_lahir_input.setDate(QDate.currentDate())
        self.alamat_input = QLineEdit()
        self.hp_input = QLineEdit()
        self.email_input = QLineEdit()

        layout.addWidget(QLabel("Data Pembeli", font=font_label))
        layout.addWidget(QLabel("Nama:"))
        layout.addWidget(self.nama_input)
        layout.addWidget(QLabel("NIK:"))
        layout.addWidget(self.nik_input)
        layout.addWidget(QLabel("Tempat Lahir:"))
        layout.addWidget(self.tempat_lahir_input)
        layout.addWidget(QLabel("Tanggal Lahir:"))
        layout.addWidget(self.tanggal_lahir_input)
        layout.addWidget(QLabel("Alamat:"))
        layout.addWidget(self.alamat_input)
        layout.addWidget(QLabel("No. HP:"))
        layout.addWidget(self.hp_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)

        # --- Data Pemesanan ---
        layout.addWidget(QLabel("Data Pemesanan", font=font_label))

        self.proyek_combo = QComboBox()
        self.proyek_combo.addItem("Kawasan NEW CITY")  # bisa ditambah nanti

        self.tipe_combo = QComboBox()
        self.tipe_combo.addItems([
            "DIAMOND POJOK", "DIAMOND",
            "SAPHIRE A", "SAPHIRE B", "RUBY"
        ])
        self.tipe_combo.currentTextChanged.connect(self.hitung_pembayaran)

        self.blok_input = QLineEdit()

        self.skema_combo = QComboBox()
        self.skema_combo.addItems(["Tunai Bertahap"])  # nanti bisa ditambah "KPR"

        layout.addWidget(QLabel("Nama Proyek:"))
        layout.addWidget(self.proyek_combo)
        layout.addWidget(QLabel("Tipe Rumah:"))
        layout.addWidget(self.tipe_combo)
        layout.addWidget(QLabel("Blok/Kavling:"))
        layout.addWidget(self.blok_input)
        layout.addWidget(QLabel("Skema Pembayaran:"))
        layout.addWidget(self.skema_combo)

        # --- Tombol ---
        self.simpan_btn = QPushButton("Simpan")
        self.simpan_btn.clicked.connect(self.simpan_transaksi)

        self.batal_btn = QPushButton("Batal")
        self.batal_btn.clicked.connect(self.reject)

        tombol_layout = QHBoxLayout()
        tombol_layout.addWidget(self.simpan_btn)
        tombol_layout.addWidget(self.batal_btn)

        layout.addLayout(tombol_layout)
        self.setLayout(layout)

        # Hitung awal saat dibuka
        self.hitung_pembayaran()

    def hitung_pembayaran(self):
        tipe = self.tipe_combo.currentText()

        harga_tipe = {
            "DIAMOND POJOK": 2090500000,
            "DIAMOND": 1615500000,
            "SAPHIRE A": 910500000,
            "SAPHIRE B": 805500000,
            "RUBY": 660500000
        }

        harga_jual = harga_tipe.get(tipe, 0)
        utj = 10000000
        sisa_setelah_utj = harga_jual - utj
        dp = int(sisa_setelah_utj * 0.2)
        cicilan = int((sisa_setelah_utj - dp) / 12)

        self._harga = harga_jual
        self._utj = utj
        self._dp = dp
        self._cicilan = cicilan

    def simpan_transaksi(self):
        data = {
            "nama": self.nama_input.text(),
            "nik": self.nik_input.text(),
            "tempat_lahir": self.tempat_lahir_input.text(),
            "tanggal_lahir": self.tanggal_lahir_input.date().toString("yyyy-MM-dd"),
            "alamat": self.alamat_input.text(),
            "no_hp": self.hp_input.text(),
            "email": self.email_input.text(),
            "proyek": self.proyek_combo.currentText(),
            "tipe_rumah": self.tipe_combo.currentText(),
            "blok_kavling": self.blok_input.text(),
            "harga_jual": self._harga,
            "skema_pembayaran": self.skema_combo.currentText(),
            "utj": self._utj,
            "dp": self._dp,
            "cicilan_per_bulan": self._cicilan,
        }

        try:
            self.controller.simpan_transaksi(data)
            QMessageBox.information(self, "Berhasil", "Transaksi berhasil disimpan!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Gagal", f"Gagal menyimpan transaksi:\n{e}")
