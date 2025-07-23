from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QHBoxLayout
from PySide6.QtCore import QDate
from model.transaksi_model import TransaksiModel

transaksi_model = TransaksiModel()  # buat objek global hanya sekali

class FormInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Input Transaksi")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # ==== Data Pembeli ====
        self.nama_input = QLineEdit()
        self.nik_input = QLineEdit()
        self.tempat_lahir_input = QLineEdit()
        self.tanggal_lahir_input = QDateEdit()
        self.tanggal_lahir_input.setCalendarPopup(True)
        self.tanggal_lahir_input.setDate(QDate.currentDate())
        self.alamat_input = QLineEdit()
        self.no_hp_input = QLineEdit()
        self.email_input = QLineEdit()

        layout.addWidget(QLabel("Nama"))
        layout.addWidget(self.nama_input)
        layout.addWidget(QLabel("NIK"))
        layout.addWidget(self.nik_input)
        layout.addWidget(QLabel("Tempat Lahir"))
        layout.addWidget(self.tempat_lahir_input)
        layout.addWidget(QLabel("Tanggal Lahir"))
        layout.addWidget(self.tanggal_lahir_input)
        layout.addWidget(QLabel("Alamat"))
        layout.addWidget(self.alamat_input)
        layout.addWidget(QLabel("No. HP"))
        layout.addWidget(self.no_hp_input)
        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.email_input)

        # ==== Data Pemesanan ====
        self.proyek_input = QLineEdit()
        self.blok_input = QLineEdit()
        self.tipe_input = QComboBox()
        self.tipe_input.addItems(["RUBY", "EMERALD", "SAFIR"])
        self.harga_input = QLineEdit()
        self.skema_input = QComboBox()
        self.skema_input.addItems(["KPR", "Tunai Bertahap"])

        layout.addWidget(QLabel("Nama Proyek"))
        layout.addWidget(self.proyek_input)
        layout.addWidget(QLabel("Blok/Kavling"))
        layout.addWidget(self.blok_input)
        layout.addWidget(QLabel("Tipe Rumah"))
        layout.addWidget(self.tipe_input)
        layout.addWidget(QLabel("Harga Jual (Rp)"))
        layout.addWidget(self.harga_input)
        layout.addWidget(QLabel("Skema Pembayaran"))
        layout.addWidget(self.skema_input)

        # Tombol Simpan
        btn_layout = QHBoxLayout()
        simpan_btn = QPushButton("Simpan")
        simpan_btn.clicked.connect(self.simpan)
        batal_btn = QPushButton("Batal")
        batal_btn.clicked.connect(self.reject)
        btn_layout.addWidget(simpan_btn)
        btn_layout.addWidget(batal_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def simpan(self):
        data = {
            "nama": self.nama_input.text(),
            "nik": self.nik_input.text(),
            "tempat_lahir": self.tempat_lahir_input.text(),
            "tanggal_lahir": self.tanggal_lahir_input.date().toString("yyyy-MM-dd"),
            "alamat": self.alamat_input.text(),
            "no_hp": self.no_hp_input.text(),
            "email": self.email_input.text(),
            "proyek": self.proyek_input.text(),
            "blok": self.blok_input.text(),
            "tipe": self.tipe_input.currentText(),
            "harga": self.harga_input.text(),
            "skema": self.skema_input.currentText()
        }

        # Simpan ke database
        transaksi_model.simpan_transaksi(data)
        self.accept()
