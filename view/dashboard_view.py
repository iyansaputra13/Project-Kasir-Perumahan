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
        self.setMinimumSize(1000, 600)

        self.controller = TransaksiController()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Header
        header = QLabel("📋 Daftar Transaksi Penjualan Rumah")
        header.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        main_layout.addWidget(header)

        # Tombol Tambah
        button_layout = QHBoxLayout()
        tambah_button = QPushButton("➕ Tambah Transaksi")
        tambah_button.clicked.connect(self.tampilkan_form_input)
        button_layout.addWidget(tambah_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Tabel Transaksi
        self.tabel = QTableWidget()
        self.tabel.setColumnCount(10)
        self.tabel.setHorizontalHeaderLabels([
            "ID", "Nama", "NIK", "Proyek", "Kavling", "Tipe Rumah",
            "Harga Jual", "Skema", "Total Cicilan", "Tanggal"
        ])
        self.tabel.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.tabel)

        # Load data awal
        self.load_data()

    def load_data(self):
        try:
            transaksi_list = self.controller.ambil_semua_transaksi()
            self.tabel.setRowCount(0)  # kosongkan tabel

            for row_index, transaksi in enumerate(transaksi_list):
                self.tabel.insertRow(row_index)
                for col_index, value in enumerate(transaksi):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    self.tabel.setItem(row_index, col_index, item)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data transaksi:\n{str(e)}")

    def tampilkan_form_input(self):
        dialog = FormInputDialog(self)
        if dialog.exec():
            self.load_data()
            QMessageBox.information(self, "Sukses", "Transaksi berhasil disimpan.")
