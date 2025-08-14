from PySide6.QtWidgets import (
    QDialog, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QSpinBox,
    QDateEdit, QStyledItemDelegate, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, QDate
from controller.transaksi_controller import TransaksiController
from openpyxl import Workbook


# ---------- helper ----------
def idr(n: int) -> str:
    try:
        return f"Rp {int(n):,}".replace(",", ".")
    except Exception:
        return "Rp 0"


class DateDelegate(QStyledItemDelegate):
    """Editor tanggal langsung di tabel"""
    def createEditor(self, parent, option, index):
        editor = QDateEdit(parent)
        editor.setCalendarPopup(True)
        editor.setDisplayFormat("yyyy-MM-dd")
        editor.setDate(QDate.currentDate())
        return editor

    def setEditorData(self, editor, index):
        text = index.data() or ""
        d = QDate.fromString(text, "yyyy-MM-dd")
        editor.setDate(d if d.isValid() else QDate.currentDate())

    def setModelData(self, editor, model, index):
        model.setData(index, editor.date().toString("yyyy-MM-dd"), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


# ---------- main dialog ----------
class DetailPembayaranView(QDialog):
    COL_BULAN = 0
    COL_CICILAN = 1
    COL_TANGGAL = 2

    def __init__(self, data_transaksi, parent=None):
        super().__init__(parent)

        # ---- data dasar dari tuple transaksi ----
        self.data = data_transaksi
        self.transaksi_id = int(self.data[0])
        self.nama_pembeli = str(self.data[1] or "")
        self.dp_total = int(self.data[14] or 0)
        self.cicilan_per_bulan = int(self.data[15] or 0)
        self.tenor = self._calc_default_tenor(self.dp_total, self.cicilan_per_bulan)

        # ---- controller DB ----
        self.ctrl = TransaksiController()

        # ---- window ----
        self.setWindowTitle(f"Cicilan DP – {self.nama_pembeli}")
        self.resize(920, 560)
        self.setModal(True)

        # ---- UI ----
        self._build_ui()

        # ---- Data awal ----
        self._load_or_generate()

    def _build_ui(self):
        root = QHBoxLayout(self)

        # === Panel kiri ===
        left = QVBoxLayout()
        left_panel = QWidget()
        left_panel.setLayout(left)
        left_panel.setStyleSheet("""
            QWidget {
                background: #f5f5f5;
                border-radius: 12px;
            }
        """)
        lbl_title_total = QLabel("TOTAL DP")
        lbl_title_total.setStyleSheet("font-weight:700;color:#555;font-size:12px;")
        self.lbl_total_dp = QLabel(idr(self.dp_total))
        self.lbl_total_dp.setAlignment(Qt.AlignCenter)
        self.lbl_total_dp.setStyleSheet("""
            QLabel { 
                font-size: 28px; 
                font-weight: 800; 
                background: white;
                border: 1px solid #e5e7eb; 
                border-radius: 10px; 
                padding: 14px 10px; 
            }
        """)
        left.addSpacing(10)
        left.addWidget(lbl_title_total, 0, Qt.AlignHCenter)
        left.addWidget(self.lbl_total_dp)
        left.addStretch()

        divider = QFrame()
        divider.setFrameShape(QFrame.VLine)
        divider.setStyleSheet("color:#e5e7eb;")

        # === Panel kanan ===
        right = QVBoxLayout()

        # bar kontrol
        topbar = QHBoxLayout()
        self.lbl_header = QLabel(f"Cicilan {self.tenor} x")
        self.lbl_header.setStyleSheet("font-size:18px;font-weight:700;color:#111827;")
        topbar.addWidget(self.lbl_header)
        topbar.addStretch()

        topbar.addWidget(QLabel("Tenor:"))
        self.spin_tenor = QSpinBox()
        self.spin_tenor.setRange(1, 360)
        self.spin_tenor.setValue(self.tenor)
        self.spin_tenor.setFixedWidth(90)
        topbar.addWidget(self.spin_tenor)

        btn_gen = QPushButton("Generate")
        btn_gen.setStyleSheet("background:#2563eb;color:white;padding:6px 12px;border-radius:8px;")
        btn_gen.clicked.connect(self._generate_schedule)
        topbar.addWidget(btn_gen)

        btn_save = QPushButton("💾 Simpan")
        btn_save.setStyleSheet("background:#16a34a;color:white;padding:6px 12px;border-radius:8px;")
        btn_save.clicked.connect(self._save_all)
        topbar.addWidget(btn_save)

        btn_export = QPushButton("📤 Export Excel")
        btn_export.setStyleSheet("background:#f59e0b;color:white;padding:6px 12px;border-radius:8px;")
        btn_export.clicked.connect(self._export_to_excel)
        topbar.addWidget(btn_export)

        right.addLayout(topbar)

        # tabel
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Bulan", "Cicilan (Rp)", "Tanggal Bayar"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setHighlightSections(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setItemDelegateForColumn(self.COL_TANGGAL, DateDelegate())
        self.table.itemChanged.connect(self._on_item_changed)
        right.addWidget(self.table)

        total_bar = QHBoxLayout()
        total_bar.addStretch()
        total_bar.addWidget(QLabel("TOTAL"))
        self.lbl_total_table = QLabel("Rp 0")
        self.lbl_total_table.setStyleSheet("font-weight:700;")
        total_bar.addWidget(self.lbl_total_table)
        right.addLayout(total_bar)

        root.addWidget(left_panel, 2)
        root.addWidget(divider)
        root.addLayout(right, 5)

    def _load_or_generate(self):
        try:
            rows = self.ctrl.ambil_cicilan_dp(self.transaksi_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal mengambil cicilan:\n{str(e)}")
            rows = []

        if rows:
            self.table.setRowCount(0)
            for (_cid, bulan, cicilan, bayar, sisa, tanggal, _catatan) in rows:
                self._append_row(
                    bulan,
                    int(cicilan or 0),
                    str(tanggal or "")
                )
        else:
            self._generate_schedule()

        self._recalc_total_label()

    def _generate_schedule(self):
        self.tenor = int(self.spin_tenor.value())
        self.lbl_header.setText(f"Cicilan {self.tenor} x")

        if self.dp_total <= 0:
            per_bulan = 0
            last = 0
        else:
            if self.tenor == 1:
                per_bulan = self.dp_total
                last = self.dp_total
            else:
                per_bulan = self.dp_total // self.tenor
                last = self.dp_total - per_bulan * (self.tenor - 1)

        self.table.blockSignals(True)
        self.table.setRowCount(0)
        for i in range(1, self.tenor + 1):
            cicil = per_bulan if i < self.tenor else last
            self._append_row(i, cicil, "")
        self.table.blockSignals(False)
        self._recalc_total_label()

    def _append_row(self, bulan_ke: int, cicilan: int, tanggal_str: str):
        r = self.table.rowCount()
        self.table.insertRow(r)

        it_bulan = QTableWidgetItem(str(int(bulan_ke)))
        it_bulan.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        it_bulan.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(r, self.COL_BULAN, it_bulan)

        it_cicil = QTableWidgetItem(str(int(cicilan)))
        it_cicil.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        it_cicil.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
        self.table.setItem(r, self.COL_CICILAN, it_cicil)

        it_tgl = QTableWidgetItem(str(tanggal_str or ""))
        it_tgl.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
        self.table.setItem(r, self.COL_TANGGAL, it_tgl)

    def _recalc_total_label(self):
        total = 0
        for r in range(self.table.rowCount()):
            try:
                total += int(self.table.item(r, self.COL_CICILAN).text() or 0)
            except Exception:
                pass
        self.lbl_total_table.setText(idr(total))

    def _on_item_changed(self, item: QTableWidgetItem):
        if item.column() == self.COL_CICILAN:
            text = item.text().strip()
            try:
                val = max(int(text or 0), 0)
            except Exception:
                val = 0
            if text != str(val):
                self.table.blockSignals(True)
                item.setText(str(val))
                self.table.blockSignals(False)
            self._recalc_total_label()

    def _calc_default_tenor(self, dp_total: int, per_bulan: int) -> int:
        if dp_total and per_bulan:
            t = dp_total // per_bulan
            return t if t > 0 else 12
        return 12

    def _collect_payload(self):
        data = []
        for r in range(self.table.rowCount()):
            bulan = int(self.table.item(r, self.COL_BULAN).text() or 0)
            cicilan = int(self.table.item(r, self.COL_CICILAN).text() or 0)
            tanggal = (self.table.item(r, self.COL_TANGGAL).text() or "").strip()
            if tanggal:
                bayar = cicilan
                sisa = 0
            else:
                bayar = 0
                sisa = cicilan

            data.append({
                "bulan_ke": bulan,
                "cicilan": cicilan,
                "bayar": bayar,
                "sisa": sisa,
                "tanggal_bayar": tanggal if tanggal else None,
                "catatan": ""
            })
        return data

    def _save_all(self):
        try:
            payload = self._collect_payload()
            self.ctrl.simpan_cicilan_dp(self.transaksi_id, payload)
            QMessageBox.information(self, "Sukses", "Data cicilan berhasil disimpan.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menyimpan cicilan:\n{str(e)}")

    def _export_to_excel(self):
        path, _ = QFileDialog.getSaveFileName(self, "Simpan ke Excel", "", "Excel Files (*.xlsx)")
        if not path:
            return

        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Cicilan DP"

            ws.append(["Nama Pembeli", self.nama_pembeli])
            ws.append(["Total DP", self.dp_total])
            ws.append([])
            ws.append(["Bulan", "Nominal Cicilan", "Tanggal Bayar"])

            for r in range(self.table.rowCount()):
                bulan = self.table.item(r, self.COL_BULAN).text()
                nominal = self.table.item(r, self.COL_CICILAN).text()
                tanggal = self.table.item(r, self.COL_TANGGAL).text()
                ws.append([bulan, nominal, tanggal])

            ws.append([])
            ws.append(["TOTAL", self.lbl_total_table.text()])

            wb.save(path)
            QMessageBox.information(self, "Sukses", f"Data berhasil diexport ke:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal export ke Excel:\n{str(e)}")
