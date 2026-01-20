from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt
class Sidebar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFixedWidth(200)  
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.btn_camera = QPushButton("Quản lý camera")
        layout.addWidget(self.btn_camera)
        self.btn_create = QPushButton("Tạo cư dân mới")
        layout.addWidget(self.btn_create)
        self.btn_list = QPushButton("Danh sách cư dân")
        layout.addWidget(self.btn_list)
        layout.addStretch()
        self.setLayout(layout)
        self.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;  /* màu nền sidebar */
            }

            QPushButton {
                background-color: #34495e;   /* màu nền button */
                color: white;                /* chữ màu trắng */
                border: none;
                padding: 12px;
                text-align: left;
                font-size: 14px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #1abc9c;  /* đổi màu khi hover */
                color: white;
            }

            QPushButton:pressed {
                background-color: #16a085;  /* khi nhấn */
            }
            """)
        