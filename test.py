import sys
import cadquery as cq
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from modelViewer2 import ModelViewer # Your separated file

from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile

class TestBoxCAD(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connection Test")
        self.resize(800, 600)

        # 1. Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # TODO: TEMP FROM HERE

        # 1. Create a custom profile and disable security on it
        self.profile = QWebEngineProfile.defaultProfile()

        # 2. Apply settings to the GLOBAL profile before creating the browser
        settings = self.profile.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)

        # TODO: TO HERE

        # 2. Add your custom ModelViewer
        self.viewer = ModelViewer()
        layout.addWidget(self.viewer)

        # 3. Add a Test Button
        self.btn = QPushButton("Test Connection: Make Box Bigger")
        self.btn.clicked.connect(self.send_test_cube)
        layout.addWidget(self.btn)

        self.size = 10 # Starting size

    def send_test_cube(self):
        self.size += 5 # Increase size each click
        print(f"Generating cube size: {self.size}...")

        # Create the geometry
        cube = cq.Workplane("XY").box(self.size, self.size, self.size)

        # Send it to your ModelViewer class
        self.viewer.update_display(cube)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestBoxCAD()
    window.show()
    sys.exit(app.exec())
