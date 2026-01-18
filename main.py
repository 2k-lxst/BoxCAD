import os
from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QSlider,
    QMessageBox,
    QRadioButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)
from qtpy.QtGui import QIcon
from qtpy.QtCore import Qt

# Global app settings
app_name = "BoxCAD"
version_number = "0.0.1"

print("The program is running.")
print(f"Welcome to {app_name} v{version_number}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.set_taskbar_icon()

        # Compile the icon path
        # This approach works regardless of where you run the script
        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, "assets", "Icon.ico")

        # Set the window's title and icon
        self.setWindowTitle(app_name + " v0.0.1")
        self.setWindowIcon(QIcon(icon_path))

        container = QWidget()
        layout = QVBoxLayout(container)
        self.setCentralWidget(container)

        inner_container = QWidget()
        inner_layout = QHBoxLayout(inner_container)

        label = QLabel("Hello, BoxCAD!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        button = QPushButton("Click me for a message!")
        button.clicked.connect(lambda: QMessageBox.information(self, "A message", "Hello, BoxCAD!"))

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 5)

        radio1 = QRadioButton("One")
        radio2 = QRadioButton("Two")
        radio3 = QRadioButton("Three")
        radio4 = QRadioButton("Four")
        radio5 = QRadioButton("Five")

        inner_layout.addWidget(radio1)
        inner_layout.addWidget(radio2)
        inner_layout.addWidget(radio3)
        inner_layout.addWidget(radio4)
        inner_layout.addWidget(radio5)

        layout.addWidget(label)
        layout.addWidget(button)
        layout.addWidget(slider)
        layout.addWidget(inner_container)

    def set_taskbar_icon(self):
        # This tells Windows to treat this as a unique app otherwise it might show the default Python icon in the taskbar
        if os.name == "nt":
            import ctypes

            myappid = f"2klxst.{app_name}.{app_name}.{version_number}"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

app = QApplication()

winddow = MainWindow()
winddow.show()

app.exec()
