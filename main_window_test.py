import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout

# Import compiled UI class and Resources
from ui.main_window_ui import Ui_MainWindow

from modelViewer import ModelViewer

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set a title for the test UI
        self.setWindowTitle("BoxCAD - UI Test Environment")

        # --- Embed ModelViewer ---
        container = self.ui.viewer  # QWidget from Designer # type: ignore
        layout = QVBoxLayout(container)  # Add a layout to the placeholder # type: ignore
        self.viewer = ModelViewer()       # Create your viewer widget
        layout.addWidget(self.viewer)     # Put the viewer in the layout

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    window = TestWindow()
    window.show()
    sys.exit(app.exec())