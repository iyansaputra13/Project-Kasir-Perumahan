from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView, QLabel
)
from PySide6.QtCore import Qt, Signal
from view.form_input_dialog import FormInputDialog
from controller.transaksi_controller import TransaksiController

class DashboardView(QWidget):
    logout_requested = Signal()

    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.controller = TransaksiController()
        self._logging_out = False  # Flag untuk membedakan logout manual dan close biasa
        self.init_ui()
        self.load_data()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Header with user info
        header_layout = QHBoxLayout()
        
        title = QLabel("📋 Daftar Transaksi Penjualan Rumah")
        title.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            color: #2c3e50;
        """)
        
        self.user_info_label = QLabel(
            f"User: {self.user_data.get('full_name', '')} | "
            f"Role: {self.user_data.get('role', 'user')}"
        )
        self.user_info_label.setStyleSheet("""
            font-size: 12px; 
            color: #7f8c8d;
            padding: 5px;
            background-color: #f0f0f0;
            border-radius: 3px;
        """)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        logout_btn.clicked.connect(self.confirm_logout)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.user_info_label)
        header_layout.addWidget(logout_btn)
        
        main_layout.addLayout(header_layout)

        # Action buttons
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
        
        refresh_button = QPushButton("🔄 Refresh Data")
        refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        refresh_button.clicked.connect(self.load_data)
        
        button_layout.addWidget(tambah_button)
        button_layout.addWidget(refresh_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)

        # Transaction table
        self.tabel = QTableWidget()
        self.tabel.setColumnCount(16)
        self.tabel.setHorizontalHeaderLabels([
            "ID", "Nama", "NIK", "Tempat Lahir", "Tanggal Lahir", 
            "Alamat", "No HP", "Email", "Proyek", "Blok/Kavling", 
            "Tipe Rumah", "Harga Jual", "Skema", "UTJ", "DP", "Cicilan/Bulan"
        ])
        
        header = self.tabel.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)
        
        self.tabel.setColumnWidth(0, 50)   # ID
        self.tabel.setColumnWidth(1, 150)  # Nama
        self.tabel.setColumnWidth(2, 120)  # NIK
        self.tabel.setColumnWidth(4, 100)  # Tanggal Lahir
        self.tabel.setColumnWidth(11, 150) # Harga Jual
        self.tabel.setColumnWidth(15, 120) # Cicilan/Bulan
        
        self.tabel.setSortingEnabled(True)
        main_layout.addWidget(self.tabel)

        # Status message label
        self.status_label = QLabel("Sistem siap")
        self.status_label.setStyleSheet("""
            font-size: 10px;
            color: #7f8c8d;
            border-top: 1px solid #ddd;
            padding: 5px;
        """)
        main_layout.addWidget(self.status_label)

    def update_status(self, message):
        self.status_label.setText(message)

    def load_data(self):
        try:
            self.tabel.setSortingEnabled(False)
            self.tabel.setRowCount(0)
            self.update_status("Memuat data...")
            
            transaksi_list = self.controller.ambil_semua_transaksi()
            
            if not transaksi_list:
                self.update_status("Tidak ada data transaksi")
                return

            for row_index, transaksi in enumerate(transaksi_list):
                if not isinstance(transaksi, (list, tuple)) or len(transaksi) != 16:
                    continue
                    
                self.tabel.insertRow(row_index)

                for col_index, value in enumerate(transaksi):
                    item = QTableWidgetItem()
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    
                    if value is None:
                        item.setText("-")
                        self.tabel.setItem(row_index, col_index, item)
                        continue
                        
                    if col_index in [11, 13, 14, 15]:
                        try:
                            nilai = int(value)
                            item.setText(f"Rp {nilai:,}")
                            item.setData(Qt.UserRole, nilai)
                        except (ValueError, TypeError):
                            item.setText(str(value))
                    elif col_index == 4:
                        item.setText(str(value) if value else "-")
                    else:
                        text = str(value)
                        if len(text) > 20:
                            text = text[:17] + "..."
                        item.setText(text)

                    self.tabel.setItem(row_index, col_index, item)
            
            self.update_status(f"Data berhasil dimuat ({len(transaksi_list)} transaksi)")
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"Gagal memuat data transaksi:\n{str(e)}")
        finally:
            self.tabel.setSortingEnabled(True)

    def tampilkan_form_input(self):
        dialog = FormInputDialog(self)
        if dialog.exec():
            self.load_data()
            self.update_status("Transaksi baru ditambahkan")
            QMessageBox.information(self, "Sukses", "Transaksi berhasil disimpan.")

    def confirm_logout(self):
        confirm = QMessageBox.question(
            self,
            "Konfirmasi Logout",
            "Apakah Anda yakin ingin logout?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            self._logging_out = True
            self.close()

    def closeEvent(self, event):
        if self._logging_out:
            self.logout_requested.emit()
            event.accept()
        else:
            confirm = QMessageBox.question(
                self,
                "Konfirmasi Keluar",
                "Apakah Anda yakin ingin keluar aplikasi?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
