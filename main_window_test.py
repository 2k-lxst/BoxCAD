import sys
from PySide6.QtWidgets import QApplication, QMainWindow

# Import compiled UI class and Resources
from ui.main_window_ui import Ui_MainWindow

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set a title for the test UI
        self.setWindowTitle("BoxCAD - UI Test Environment")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    window = TestWindow()
    window.show()
    sys.exit(app.exec())