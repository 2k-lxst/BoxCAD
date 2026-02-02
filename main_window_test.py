import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QDoubleSpinBox, QPlainTextEdit

# Import compiled UI class and Resources
from ui.main_window_ui import Ui_MainWindow

from modelViewer import ModelViewer
from build_ui import BuildUI

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.build_ui = BuildUI()

        self.build_ui.populate_toolbox(self.ui.parametersToolBox) # type: ignore

        self.setup_testing_connections()

        # Set a title for the test UI
        self.setWindowTitle("BoxCAD - UI Test Environment")

        # --- Embed ModelViewer ---
        container = self.ui.viewer  # QWidget from Designer # type: ignore
        layout = QVBoxLayout(container)  # Add a layout to the placeholder # type: ignore
        self.viewer = ModelViewer()       # Create your viewer widget
        layout.addWidget(self.viewer)     # Put the viewer in the layout

    def setup_testing_connections(self):
        # We look for the widgets we stored in the factory's dictionary
        for name, widget in self.build_ui.widgets.items():
            if isinstance(widget, QDoubleSpinBox):
                widget.valueChanged.connect(lambda val, n=name: self.debug_print(n, val))
            elif isinstance(widget, QPlainTextEdit):
                widget.textChanged.connect(lambda n=name: self.debug_print(n, "Text Updated"))

    def debug_print(self, name, value):
        print(f"TEST: Parameter '{name}' changed to: {value}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    window = TestWindow()
    window.show()
    sys.exit(app.exec())
