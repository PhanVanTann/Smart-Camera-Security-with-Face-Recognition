from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QCheckBox, QComboBox, QListWidget, QFileDialog, QMessageBox
)
import os
import shutil
import sys
from core.mongodb import residents_collection
from utils.embeding import get_embedding_from_image
UPLOAD_DIR = "uploads/residents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class CreateResidentForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Resident")
        self.resize(900, 600)

        self.setStyleSheet("""
/* Toàn bộ form */
QWidget {
    font-family: Arial;
    font-size: 13px;
    color: white;
    background-color: #2c3e50; /* nền dark cho toàn bộ form */
}

/* Nhãn */
QLabel {
    font-weight: bold;
    margin-top: 5px;
    color: #ecf0f1;
}

/* Input: QLineEdit và QComboBox */
QLineEdit, QComboBox {
    padding: 6px;
    border-radius: 4px;
    border: 1px solid #34495e;
    background-color: #34495e;   /* màu nền input tối */
    color: white;
}

/* Khi focus input */
QLineEdit:focus, QComboBox:focus {
    border: 1px solid #3498db;   /* viền xanh khi focus */
}

/* CheckBox */
QCheckBox {
    padding: 5px;
    color: #ecf0f1;
}

/* QPushButton */
QPushButton {
    background-color: #3498db;
    color: white;
    border-radius: 5px;
    padding: 10px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:pressed {
    background-color: #1f618d;
}

/* QListWidget */
QListWidget {
    background-color: #34495e;
    color: white;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    padding: 3px;
}

/* Scrollbar cho QListWidget */
QListWidget::item {
    padding: 4px;
}

QScrollBar:vertical {
    background: #2c3e50;
    width: 12px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #2980b9;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

/* ScrollArea */
QScrollArea {
    border: none;
}
""")

        # Layout chính: chia trái phải
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # ----------------- Left: Thông tin cư dân + controls -----------------
        left_layout = QVBoxLayout()

        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.age = QLineEdit()
        self.address = QLineEdit()

        left_layout.addWidget(QLabel("Tên"))
        left_layout.addWidget(self.first_name)
        left_layout.addWidget(QLabel("Họ"))
        left_layout.addWidget(self.last_name)
        left_layout.addWidget(QLabel("Tuổi"))
        left_layout.addWidget(self.age)
        left_layout.addWidget(QLabel("Địa chỉ"))
        left_layout.addWidget(self.address)

        # Controls cho ảnh
        self.angle = QComboBox()
        self.angle.addItems(["nhìn thẳng", "trái", "phải"])
        self.distance = QComboBox()
        self.distance.addItems(["gần", "trung bình", "xa"])
        self.mask = QCheckBox("Đeo khẩu trang")

        left_layout.addWidget(QLabel("Góc nhìn của ảnh"))
        left_layout.addWidget(self.angle)
        left_layout.addWidget(QLabel("Khoảng cách của ảnh"))
        left_layout.addWidget(self.distance)
        left_layout.addWidget(self.mask)

        # Nút upload ảnh
        self.upload_btn = QPushButton("Upload Images")
        self.upload_btn.clicked.connect(self.upload_images)
        left_layout.addWidget(self.upload_btn)

        # Nút lưu toàn bộ cư dân
        self.save_btn = QPushButton("Lưu cư dân")
        self.save_btn.clicked.connect(self.save_resident)
        left_layout.addWidget(self.save_btn)

        main_layout.addLayout(left_layout)

        # ----------------- Right: danh sách ảnh -----------------
        right_layout = QVBoxLayout()
        self.image_list = QListWidget()
        right_layout.addWidget(QLabel("Uploaded Images"))
        right_layout.addWidget(self.image_list)
        main_layout.addLayout(right_layout)

        # Lưu danh sách ảnh tạm
        self.image_paths = []
        
        

    def upload_images(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Images", "", "Images (*.jpg *.png)"
        )
        for f in files:
            # Lưu thông tin ảnh vào danh sách tạm
            img_info = {
                "path": f,
                "góc ": self.angle.currentText(),
                "khoảng cách": self.distance.currentText(),
                "khẩu trang": self.mask.isChecked()
            }
            self.image_paths.append(img_info)

            # Hiển thị bên list
            self.image_list.addItem(
                f"{os.path.basename(f)} - {img_info['góc ']} - {img_info['khoảng cách']} - {'Có khẩu trang' if img_info['khẩu trang'] else 'không khẩu trang'}"
            )

    def save_resident(self):
        if not self.first_name.text() or not self.last_name.text():
            QMessageBox.warning(self, "Warning", "Tên và Họ không được để trống")
            return

        resident_faces = []
        for img_info in self.image_paths:
            # Lấy embedding trực tiếp từ file ảnh, không lưu file
            print("shshhss",img_info["path"])
            embedding = get_embedding_from_image(img_info["path"])
            if embedding is None:
                continue

            # Lưu embedding + thông tin ảnh
            resident_faces.append({
                "angle": img_info.get("góc ", "unknown"),
                "distance": img_info.get("khoảng cách", "unknown"),
                "mask": img_info.get("khẩu trang", False),
                "vector": embedding.tolist() if hasattr(embedding, "tolist") else embedding
            })

        if len(resident_faces) == 0:
            QMessageBox.warning(self, "Warning", "Không có ảnh hợp lệ")
            return

        resident = {
            "first_name": self.first_name.text(),
            "last_name": self.last_name.text(),
            "age": int(self.age.text()) if self.age.text().isdigit() else 0,
            "address": self.address.text(),
            "embeddings": resident_faces
        }

        result = residents_collection.insert_one(resident)
        QMessageBox.information(self, "Success", f"Resident saved with ID: {result.inserted_id}")
        self.close()

