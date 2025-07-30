from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QDateEdit, QMessageBox, QHBoxLayout, QFormLayout,
    QGroupBox
)
from PySide6.QtCore import QDate, QRegularExpression
from PySide6.QtGui import QFont, QRegularExpressionValidator
from controller.transaksi_controller import TransaksiController


class FormInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Form Input Transaksi Rumah")
        self.setMinimumSize(600, 800)
        self.controller = TransaksiController()
        self._harga = 0
        self._utj = 0
        self._dp = 0
        self._cicilan = 0

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        font_label = QFont()
        font_label.setBold(True)

        # --- Data Pembeli ---
        pembeli_group = QGroupBox("Data Pembeli")
        pembeli_layout = QFormLayout()

        self.nama_input = QLineEdit()

        self.nik_input = QLineEdit()
        nik_validator = QRegularExpressionValidator(QRegularExpression(r"\d{0,16}"))  # Max 16 digit
        self.nik_input.setValidator(nik_validator)

        self.tempat_lahir_input = QLineEdit()

        self.tanggal_lahir_input = QDateEdit()
        self.tanggal_lahir_input.setCalendarPopup(True)
        self.tanggal_lahir_input.setDate(QDate.currentDate().addYears(-20))
        self.tanggal_lahir_input.setDisplayFormat("dd/MM/yyyy")

        self.alamat_input = QLineEdit()

        self.hp_input = QLineEdit()
        hp_validator = QRegularExpressionValidator(QRegularExpression(r"\d{0,13}"))  # Max 13 digit
        self.hp_input.setValidator(hp_validator)

        self.email_input = QLineEdit()

        pembeli_layout.addRow(QLabel("Nama Lengkap:"), self.nama_input)
        pembeli_layout.addRow(QLabel("NIK:"), self.nik_input)
        pembeli_layout.addRow(QLabel("Tempat Lahir:"), self.tempat_lahir_input)
        pembeli_layout.addRow(QLabel("Tanggal Lahir:"), self.tanggal_lahir_input)
        pembeli_layout.addRow(QLabel("Alamat:"), self.alamat_input)
        pembeli_layout.addRow(QLabel("No. HP:"), self.hp_input)
        pembeli_layout.addRow(QLabel("Email:"), self.email_input)

        pembeli_group.setLayout(pembeli_layout)
        layout.addWidget(pembeli_group)

        # --- Data Pemesanan ---
        pemesanan_group = QGroupBox("Data Pemesanan")
        pemesanan_layout = QFormLayout()

        self.proyek_combo = QComboBox()
        self.proyek_combo.addItems(["Kawasan NEW CITY", "Kawasan GREEN VILLAGE"])

        self.tipe_combo = QComboBox()
        self.tipe_combo.addItems([
            "DIAMOND POJOK", "DIAMOND",
            "SAPHIRE A", "SAPHIRE B", "RUBY"
        ])
        self.tipe_combo.currentTextChanged.connect(self.hitung_pembayaran)

        self.blok_input = QLineEdit()

        self.skema_combo = QComboBox()
        self.skema_combo.addItems(["Tunai Bertahap", "KPR"])

        pemesanan_layout.addRow(QLabel("Proyek:"), self.proyek_combo)
        pemesanan_layout.addRow(QLabel("Tipe Rumah:"), self.tipe_combo)
        pemesanan_layout.addRow(QLabel("Blok/Kavling:"), self.blok_input)
        pemesanan_layout.addRow(QLabel("Skema Pembayaran:"), self.skema_combo)

        pemesanan_group.setLayout(pemesanan_layout)
        layout.addWidget(pemesanan_group)

        # --- Detail Pembayaran ---
        pembayaran_group = QGroupBox("Detail Pembayaran")
        pembayaran_layout = QFormLayout()

        self.harga_label = QLabel("Rp 0")
        self.harga_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        self.utj_label = QLabel("Rp 0")
        self.dp_label = QLabel("Rp 0")
        self.cicilan_label = QLabel("Rp 0")

        pembayaran_layout.addRow(QLabel("Harga Rumah:"), self.harga_label)
        pembayaran_layout.addRow(QLabel("Uang Tanda Jadi (UTJ):"), self.utj_label)
        pembayaran_layout.addRow(QLabel("Down Payment (DP):"), self.dp_label)
        pembayaran_layout.addRow(QLabel("Cicilan per Bulan:"), self.cicilan_label)

        pembayaran_group.setLayout(pembayaran_layout)
        layout.addWidget(pembayaran_group)

        # --- Tombol ---
        button_layout = QHBoxLayout()

        self.simpan_btn = QPushButton("Simpan Transaksi")
        self.simpan_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        self.simpan_btn.clicked.connect(self.simpan_transaksi)

        self.batal_btn = QPushButton("Batal")
        self.batal_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.batal_btn.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.batal_btn)
        button_layout.addWidget(self.simpan_btn)

        layout.addLayout(button_layout)

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

        self.harga_label.setText(f"Rp {harga_jual:,}")
        self.utj_label.setText(f"Rp {utj:,}")
        self.dp_label.setText(f"Rp {dp:,}")
        self.cicilan_label.setText(f"Rp {cicilan:,}")

    def simpan_transaksi(self):
        if not self.nama_input.text().strip():
            QMessageBox.warning(self, "Peringatan", "Nama harus diisi!")
            return
        if len(self.nik_input.text()) != 16:
            QMessageBox.warning(self, "Peringatan", "NIK harus 16 digit!")
            return
        if not self.blok_input.text().strip():
            QMessageBox.warning(self, "Peringatan", "Blok/Kavling harus diisi!")
            return

        data = {
            "nama": self.nama_input.text().strip(),
            "nik": self.nik_input.text().strip(),
            "tempat_lahir": self.tempat_lahir_input.text().strip(),
            "tanggal_lahir": self.tanggal_lahir_input.date().toString("yyyy-MM-dd"),
            "alamat": self.alamat_input.text().strip(),
            "no_hp": self.hp_input.text().strip(),
            "email": self.email_input.text().strip(),
            "proyek": self.proyek_combo.currentText(),
            "tipe_rumah": self.tipe_combo.currentText(),
            "blok_kavling": self.blok_input.text().strip(),
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
            QMessageBox.critical(self, "Gagal", f"Gagal menyimpan transaksi:\n{str(e)}")
