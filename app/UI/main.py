from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QScrollArea
from sidebar import Sidebar
from createResident import CreateResidentForm
from camera import CameraWidget 
from listResident import ResidentListWidget

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.resize(1000, 600)
       
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        self.sidebar = Sidebar()
        layout.addWidget(self.sidebar)

        self.main_content = QWidget()
        layout.addWidget(self.main_content)
        self.main_content.setStyleSheet("background-color: #2c3e50;")
        # Tạo form
        self.create_resident_form = CreateResidentForm()

        # Kết nối nút
        self.sidebar.btn_create.clicked.connect(self.show_create_form)
        self.sidebar.btn_camera.clicked.connect(self.show_camera)

    def show_create_form(self):
        self.clear_main_content()
        if self.main_content.layout() is not None:
            QWidget().setLayout(self.main_content.layout())

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        create_resident_form = CreateResidentForm()
        scroll.setWidget(create_resident_form)

        layout = QVBoxLayout()
        layout.addWidget(scroll)
        self.main_content.setLayout(layout)
    def show_camera(self):
        self.clear_main_content()
        if self.main_content.layout() is not None:
            QWidget().setLayout(self.main_content.layout())

        layout = QVBoxLayout()
        cam_widget = CameraWidget()
        layout.addWidget(cam_widget)
        self.main_content.setLayout(layout)
  

    def show_resident_list(self):
        self.clear_main_content()
        layout = QVBoxLayout()
        list_widget = ResidentListWidget()
        layout.addWidget(list_widget)
        self.main_content.setLayout(layout)
    def clear_main_content(self):
        layout = self.main_content.layout()
        if layout is not None:
            # Lấy tất cả widget trong layout
            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i).widget()
                if widget is not None:
                    # Nếu là CameraWidget thì stop camera
                    if isinstance(widget, CameraWidget):
                        widget.stop_camera()
                    widget.setParent(None)
            QWidget().setLayout(layout)
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec())