from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView, QLabel
)
from PySide6.QtCore import Qt
from view.form_input_dialog import FormInputDialog
from controller.transaksi_controller import TransaksiController


class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard - KasirPerumahan 1.0")
        self.setMinimumSize(1200, 700)

        self.controller = TransaksiController()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Header
        header = QLabel("📋 Daftar Transaksi Penjualan Rumah")
        header.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            margin-bottom: 20px;
            color: #2c3e50;
        """)
        main_layout.addWidget(header)

        # Tombol Tambah
        button_layout = QHBoxLayout()
        tambah_button = QPushButton("➕ Tambah Transaksi")
        tambah_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        tambah_button.clicked.connect(self.tampilkan_form_input)
        button_layout.addWidget(tambah_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Tabel Transaksi
        self.tabel = QTableWidget()
        self.tabel.setColumnCount(16)  # Sesuai jumlah label
        self.tabel.setHorizontalHeaderLabels([
            "ID", "Nama", "NIK", "Tempat Lahir", "Tanggal Lahir", 
            "Alamat", "No HP", "Email", "Proyek", "Blok/Kavling", 
            "Tipe Rumah", "Harga Jual", "Skema", "UTJ", "DP", "Cicilan/Bulan"
        ])
        self.tabel.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

        # Atur lebar kolom
        self.tabel.setColumnWidth(0, 50)   # ID
        self.tabel.setColumnWidth(1, 150)  # Nama
        self.tabel.setColumnWidth(2, 120)  # NIK
        self.tabel.setColumnWidth(4, 100)  # Tanggal Lahir
        self.tabel.setColumnWidth(11, 150) # Harga Jual
        self.tabel.setColumnWidth(15, 120) # Cicilan/Bulan

        main_layout.addWidget(self.tabel)

        # Load data awal
        self.load_data()

    def load_data(self):
        try:
            transaksi_list = self.controller.ambil_semua_transaksi()
            self.tabel.setRowCount(0)

            for row_index, transaksi in enumerate(transaksi_list):
                self.tabel.insertRow(row_index)

                for col_index, value in enumerate(transaksi):
                    item = QTableWidgetItem()

                    if col_index in [11, 13, 14, 15]:  # Kolom harga dan pembayaran
                        if value is not None:
                            item.setText(f"Rp {int(value):,}")
                        else:
                            item.setText("Rp 0")
                    else:
                        item.setText(str(value) if value is not None else "-")

                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    self.tabel.setItem(row_index, col_index, item)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data transaksi:\n{str(e)}")

    def tampilkan_form_input(self):
        dialog = FormInputDialog(self)
        if dialog.exec():
            self.load_data()
            QMessageBox.information(self, "Sukses", "Transaksi berhasil disimpan.")
