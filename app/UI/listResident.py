from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from core.mongodb import residents_collection
import os

class ResidentListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resident List")
        self.resize(600, 500)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Danh sách cư dân:"))

        # List hiển thị cư dân
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # Buttons layout
        btn_layout = QHBoxLayout()
        self.btn_refresh = QPushButton("Refresh")
        self.btn_delete = QPushButton("Xóa cư dân")
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_delete)
        layout.addLayout(btn_layout)

        # Connect button
        self.btn_refresh.clicked.connect(self.load_residents)
        self.btn_delete.clicked.connect(self.delete_resident)

        # Load data ban đầu
        self.load_residents()

    def load_residents(self):
        self.list_widget.clear()
        residents = list(residents_collection.find())
        for r in residents:
            name = f"{r.get('first_name','')} {r.get('last_name','')}"
            age = r.get('age', 'N/A')
            address = r.get('address', 'N/A')
            num_faces = len(r.get('embeddings', []))
            item_text = f"{name} | Tuổi: {age} | Địa chỉ: {address} | Số ảnh: {num_faces}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, r["_id"])  # lưu id để xóa/chi tiết
            self.list_widget.addItem(item)

    def delete_resident(self):
        item = self.list_widget.currentItem()
        if item is None:
            QMessageBox.warning(self, "Chú ý", "Chọn cư dân để xóa")
            return
        resident_id = item.data(Qt.ItemDataRole.UserRole)
        confirm = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc muốn xóa cư dân này?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            # Xóa khỏi MongoDB
            result = residents_collection.delete_one({"_id": resident_id})
            if result.deleted_count:
                # Xóa ảnh trên disk
                # residents_collection lưu path ảnh trong 'faces'
                # Nếu muốn xóa ảnh:
                # faces = residents_collection.find_one({"_id": resident_id})['faces']
                # for f in faces: os.remove(f['path'])
                QMessageBox.information(self, "Xóa thành công", "Đã xóa cư dân")
                self.load_residents()