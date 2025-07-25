# view/form_input_dialog.py

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
        self.setWindowTitle("Form Input Transaksi")
        self.setMinimumWidth(500)
        self.controller = TransaksiController()

        self.setStyleSheet("""
            QLabel {
                font: 11pt 'Segoe UI';
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 6px;
                font: 11pt 'Segoe UI';
                border: 1px solid #ccc;
                border-radius: 8px;
            }
            QPushButton {
                padding: 10px;
                font: bold 11pt 'Segoe UI';
                border-radius: 10px;
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        self.proyek_tipe_harga = {
            "KAWASAN NEW CITY": {
                "DIAMOND POJOK": 2090500000,
                "DIAMOND": 1615500000,
                "SAPHIRE A": 910500000,
                "SAPHIRE B": 805500000,
                "RUBY": 660500000,
            }
        }

        self.tipe_luas_mapping = {
            "DIAMOND POJOK": (195, 150),
            "DIAMOND": (120, 142),
            "SAPHIRE A": (105, 60),
            "SAPHIRE B": (97.5, 48),
            "RUBY": (78, 45)
        }

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Data Diri
        self.nama_input = QLineEdit()
        self.nik_input = QLineEdit()
        self.tempat_lahir_input = QLineEdit()
        self.tanggal_lahir_input = QDateEdit()
        self.tanggal_lahir_input.setDisplayFormat("yyyy-MM-dd")
        self.tanggal_lahir_input.setDate(QDate.currentDate())
        self.alamat_input = QLineEdit()
        self.hp_input = QLineEdit()
        self.email_input = QLineEdit()

        # Pemesanan
        self.proyek_combo = QComboBox()
        self.proyek_combo.addItems(self.proyek_tipe_harga.keys())
        self.proyek_combo.currentTextChanged.connect(self.update_tipe_rumah)

        self.tipe_combo = QComboBox()
        self.tipe_combo.currentTextChanged.connect(self.update_luas)

        self.blok_input = QLineEdit()

        self.luas_tanah_input = QLineEdit()
        self.luas_bangunan_input = QLineEdit()

        # Skema & Harga
        self.harga_label = QLabel("Harga: -")
        self.utj_label = QLabel("UTJ: -")
        self.dp_label = QLabel("DP 20%: -")
        self.cicilan_label = QLabel("Cicilan 12x: -")

        self.skema_combo = QComboBox()
        self.skema_combo.addItems(["KPR", "Tunai Bertahap"])

        self.hitung_btn = QPushButton("Hitung Skema 12x")
        self.hitung_btn.clicked.connect(self.hitung_skema)

        self.simpan_btn = QPushButton("💾 Simpan Transaksi")
        self.simpan_btn.clicked.connect(self.simpan_transaksi)

        # Tambahkan ke layout
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
        layout.addWidget(self.hp_input)

        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.email_input)

        layout.addWidget(QLabel("Nama Proyek"))
        layout.addWidget(self.proyek_combo)

        layout.addWidget(QLabel("Tipe Rumah"))
        layout.addWidget(self.tipe_combo)

        layout.addWidget(QLabel("Blok/Kavling"))
        layout.addWidget(self.blok_input)

        layout.addWidget(QLabel("Luas Tanah (m²)"))
        layout.addWidget(self.luas_tanah_input)

        layout.addWidget(QLabel("Luas Bangunan (m²)"))
        layout.addWidget(self.luas_bangunan_input)

        layout.addWidget(QLabel("Skema Pembayaran"))
        layout.addWidget(self.skema_combo)

        layout.addWidget(self.harga_label)
        layout.addWidget(self.utj_label)
        layout.addWidget(self.dp_label)
        layout.addWidget(self.cicilan_label)

        layout.addWidget(self.hitung_btn)
        layout.addWidget(self.simpan_btn)

        self.setLayout(layout)
        self.update_tipe_rumah()

    def update_tipe_rumah(self):
        proyek = self.proyek_combo.currentText()
        self.tipe_combo.clear()
        if proyek in self.proyek_tipe_harga:
            self.tipe_combo.addItems(self.proyek_tipe_harga[proyek].keys())
        self.update_luas()

    def update_luas(self):
        tipe = self.tipe_combo.currentText()
        tanah, bangunan = self.tipe_luas_mapping.get(tipe.upper(), (0, 0))
        self.luas_tanah_input.setText(str(tanah))
        self.luas_bangunan_input.setText(str(bangunan))

    def hitung_skema(self):
        proyek = self.proyek_combo.currentText()
        tipe = self.tipe_combo.currentText()
        harga = self.proyek_tipe_harga[proyek][tipe]
        utj = 10_000_000
        sisa = harga - utj
        dp = int(sisa * 0.2)
        cicilan = int((sisa - dp) / 12)

        self._harga = harga
        self._utj = utj
        self._dp = dp
        self._cicilan = cicilan

        self.harga_label.setText(f"Harga: Rp{harga:,.0f}")
        self.utj_label.setText(f"UTJ: Rp{utj:,.0f}")
        self.dp_label.setText(f"DP 20%: Rp{dp:,.0f}")
        self.cicilan_label.setText(f"Cicilan 12x: Rp{cicilan:,.0f}")

    def simpan_transaksi(self):
        try:
            data = {
                "nama": self.nama_input.text(),
                "nik": self.nik_input.text(),
                "tempat_lahir": self.tempat_lahir_input.text(),
                "tanggal_lahir": self.tanggal_lahir_input.date().toString("yyyy-MM-dd"),
                "alamat": self.alamat_input.text(),
                "no_hp": self.hp_input.text(),
                "email": self.email_input.text(),
                "nama_proyek": self.proyek_combo.currentText(),
                "blok": self.blok_input.text(),
                "tipe_rumah": self.tipe_combo.currentText(),
                "luas_tanah": float(self.luas_tanah_input.text()),
                "luas_bangunan": float(self.luas_bangunan_input.text()),
                "harga_jual": self._harga,
                "skema": self.skema_combo.currentText(),
                "utj": self._utj,
                "dp": self._dp,
                "cicilan_per_bulan": self._cicilan,
                "total_cicilan": self._cicilan * 12
            }

            self.controller.simpan_transaksi(data)
            QMessageBox.information(self, "Sukses", "Transaksi berhasil disimpan.")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menyimpan: {e}")
