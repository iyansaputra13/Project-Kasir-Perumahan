# view/form_input_dialog.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QFileDialog, QMessageBox, QFormLayout, QDateEdit
)
from PySide6.QtCore import QDate
from controller.transaksi_controller import TransaksiController
import os
import shutil


class FormInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Form Input Transaksi")
        self.controller = TransaksiController()
        self.foto_ktp_path = ""
        self.transaksi_id = None  # untuk edit
        self.harga_dict = {
            "DIAMOND POJOK": 2090500000,
            "DIAMOND": 1615500000,
            "SAPHIRE A": 910500000,
            "SAPHIRE B": 805500000,
            "RUBY": 660500000
        }
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # --- Data Pembeli ---
        self.nama_input = QLineEdit()
        self.nik_input = QLineEdit()
        self.tempat_lahir_input = QLineEdit()
        self.tanggal_lahir_input = QDateEdit()
        self.tanggal_lahir_input.setCalendarPopup(True)
        self.tanggal_lahir_input.setDisplayFormat("dd-MM-yyyy")
        self.tanggal_lahir_input.setDate(QDate.currentDate())
        self.alamat_input = QLineEdit()
        self.no_hp_input = QLineEdit()
        self.email_input = QLineEdit()

        self.btn_upload_ktp = QPushButton("📁 Upload Foto KTP")
        self.btn_upload_ktp.clicked.connect(self.upload_ktp)

        form_layout.addRow("Nama:", self.nama_input)
        form_layout.addRow("NIK:", self.nik_input)
        form_layout.addRow("Tempat Lahir:", self.tempat_lahir_input)
        form_layout.addRow("Tanggal Lahir:", self.tanggal_lahir_input)
        form_layout.addRow("Alamat:", self.alamat_input)
        form_layout.addRow("No. HP:", self.no_hp_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Foto KTP:", self.btn_upload_ktp)

        # --- Data Pemesanan ---
        self.proyek_input = QComboBox()
        self.proyek_input.addItems(["Kawasan NEW CITY"])
        self.blok_input = QLineEdit()

        self.tipe_input = QComboBox()
        self.tipe_input.addItems(list(self.harga_dict.keys()))
        self.tipe_input.currentIndexChanged.connect(self.hitung_pembayaran)

        self.harga_input = QLineEdit()
        self.harga_input.setReadOnly(True)

        self.btn_hitung = QPushButton("Hitung Pembayaran")
        self.btn_hitung.clicked.connect(self.hitung_pembayaran)
        self.hasil_label = QLabel("")

        form_layout.addRow("Nama Proyek:", self.proyek_input)
        form_layout.addRow("Blok/Kavling:", self.blok_input)
        form_layout.addRow("Tipe Rumah:", self.tipe_input)
        form_layout.addRow("Harga Rumah:", self.harga_input)
        form_layout.addRow(self.btn_hitung)
        form_layout.addRow(self.hasil_label)

        # --- Tombol Simpan ---
        self.btn_simpan = QPushButton("Simpan Transaksi")
        self.btn_simpan.clicked.connect(self.simpan_transaksi)

        layout.addLayout(form_layout)
        layout.addWidget(self.btn_simpan)
        self.setLayout(layout)

        self.hitung_pembayaran()

    def upload_ktp(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Pilih Foto KTP", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            try:
                target_folder = "assets/foto_ktp"
                os.makedirs(target_folder, exist_ok=True)
                file_name = os.path.basename(file_path)
                target_path = os.path.join(target_folder, file_name)
                shutil.copy(file_path, target_path)
                self.foto_ktp_path = target_path
                QMessageBox.information(self, "Sukses", "Foto KTP berhasil diunggah.")
            except Exception as e:
                QMessageBox.critical(self, "Gagal", f"Gagal menyimpan file:\n{e}")

    def hitung_pembayaran(self):
        tipe = self.tipe_input.currentText()
        harga = self.harga_dict.get(tipe, 0)

        utj = 10_000_000  # pembayaran awal
        dp_total = int((harga - utj) * 0.2)  # 20% dari sisa harga
        cicilan_per_bulan = int(dp_total / 12)  # DP dicicil 12 bulan

        self.harga_input.setText(f"{harga}")
        self.hasil_label.setText(
            f"Harga: Rp{harga:,}\n"
            f"UTJ (bayar di awal): Rp{utj:,}\n"
            f"Total DP: Rp{dp_total:,} (dicicil 12 bulan)\n"
            f"Cicilan per bulan: Rp{cicilan_per_bulan:,}\n"
            f"Catatan: Pembayaran bulanan bisa sebagian, sisa akan tercatat."
        )

    def load_data(self, data: dict):
        """Load data transaksi dari Supabase (format dict)"""
        self.transaksi_id = data.get("id")
        self.nama_input.setText(str(data.get("nama", "")))
        self.nik_input.setText(str(data.get("nik", "")))
        self.tempat_lahir_input.setText(str(data.get("tempat_lahir", "")))

        try:
            tgl_lahir = data.get("tanggal_lahir")
            if isinstance(tgl_lahir, str):
                y, m, d = map(int, tgl_lahir.split("-"))
                self.tanggal_lahir_input.setDate(QDate(y, m, d))
        except Exception as e:
            print("Gagal set tanggal:", e)

        self.alamat_input.setText(str(data.get("alamat", "")))
        self.no_hp_input.setText(str(data.get("no_hp", "")))
        self.email_input.setText(str(data.get("email", "")))
        self.foto_ktp_path = str(data.get("foto_ktp", ""))
        self.proyek_input.setCurrentText(str(data.get("nama_proyek", "")))
        self.blok_input.setText(str(data.get("blok_kavling", "")))
        self.tipe_input.setCurrentText(str(data.get("tipe_rumah", "")))
        self.harga_input.setText(str(data.get("harga_rumah", "")))

        self.hitung_pembayaran()

    def simpan_transaksi(self):
        try:
            tipe = self.tipe_input.currentText()
            harga = self.harga_dict.get(tipe, 0)

            utj = 10_000_000
            dp_total = int((harga - utj) * 0.2)
            cicilan_per_bulan = int(dp_total / 12)

            data = {
                "nama": self.nama_input.text().strip(),
                "nik": self.nik_input.text().strip(),
                "tempat_lahir": self.tempat_lahir_input.text().strip(),
                "tanggal_lahir": self.tanggal_lahir_input.date().toPython().isoformat(),
                "alamat": self.alamat_input.text().strip(),
                "no_hp": self.no_hp_input.text().strip(),
                "email": self.email_input.text().strip(),
                "foto_ktp": self.foto_ktp_path,
                "nama_proyek": self.proyek_input.currentText(),
                "blok_kavling": self.blok_input.text().strip(),
                "tipe_rumah": tipe,
                "harga_rumah": harga,
                "skema_pembayaran": "Cicilan 12x DP",
                "utj": utj,
                "dp_total": dp_total,
                "cicilan_per_bulan": cicilan_per_bulan,
                "catatan": "Pembayaran bulanan bisa sebagian, sisa akan tercatat"
            }

            # Validasi
            for field in ["nama", "nik", "tempat_lahir", "blok_kavling"]:
                if not data[field]:
                    QMessageBox.warning(self, "Validasi", f"{field.replace('_', ' ').title()} wajib diisi.")
                    return

            if self.transaksi_id:
                self.controller.update_transaksi(self.transaksi_id, data)
                QMessageBox.information(self, "Sukses", "Transaksi berhasil diperbarui.")
            else:
                self.controller.simpan_transaksi(data)
                QMessageBox.information(self, "Sukses", "Transaksi berhasil disimpan.")

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Gagal", f"Gagal menyimpan transaksi:\n{e}")
