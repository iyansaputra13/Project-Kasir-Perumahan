from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
)
from controller.transaksi_controller import TransaksiController

class FormInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Form Input Transaksi")
        self.controller = TransaksiController()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Data Pembeli
        self.nama_input = QLineEdit()
        self.nik_input = QLineEdit()
        self.ttl_input = QLineEdit()
        self.alamat_input = QLineEdit()
        self.hp_input = QLineEdit()
        self.email_input = QLineEdit()

        # Data Pemesanan
        self.proyek_input = QComboBox()
        self.proyek_input.addItems([
            "KAWASAN NEW CITY",
            "BULAN TERANG UTAMA"
        ])

        self.blok_input = QLineEdit()
        self.tipe_input = QComboBox()
        self.tipe_input.addItems([
            "DIAMOND POJOK",
            "DIAMOND",
            "SAPHIRE A",
            "SAPHIRE B",
            "RUBY"
        ])
        self.tipe_input.currentIndexChanged.connect(self.atur_blok_otomatis)

        self.harga_input = QLineEdit()

        layout.addWidget(QLabel("Nama"))
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
        layout.addWidget(self.proyek_input)
        layout.addWidget(QLabel("Tipe Rumah"))
        layout.addWidget(self.tipe_input)
        layout.addWidget(QLabel("Blok/Kavling"))
        layout.addWidget(self.blok_input)
        layout.addWidget(QLabel("Harga Jual (Tanah & Bangunan)"))
        layout.addWidget(self.harga_input)

        simpan_button = QPushButton("Simpan Transaksi")
        simpan_button.clicked.connect(self.simpan_data)
        layout.addWidget(simpan_button)

        self.setLayout(layout)

    def atur_blok_otomatis(self):
        tipe = self.tipe_input.currentText()
        tipe_to_blok = {
            "DIAMOND POJOK": "195/150 M²",
            "DIAMOND": "120/142 M²",
            "SAPHIRE A": "105/60 M²",
            "SAPHIRE B": "97.5/48 M²",
            "RUBY": "78/45 M²"
        }
        self.blok_input.setText(tipe_to_blok.get(tipe, ""))

    def simpan_data(self):
        data = {
            "nama": self.nama_input.text(),
            "nik": self.nik_input.text(),
            "ttl": self.ttl_input.text(),
            "alamat": self.alamat_input.text(),
            "no_hp": self.hp_input.text(),
            "email": self.email_input.text(),
            "proyek": self.proyek_input.currentText(),
            "blok": self.blok_input.text(),
            "tipe": self.tipe_input.currentText(),
            "harga": self.harga_input.text()
        }

        self.controller.simpan_transaksi(data)
        self.accept()
