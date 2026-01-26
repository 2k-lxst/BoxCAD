import sys
import cadquery as cq
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton
# Ensure your class name starts with a letter!
from OCP.AIS import AIS_ColoredShape # type: ignore
from ModelViewer import ModelViewer

class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BoxCAD OCP Test")
        self.resize(800, 600)

        layout = QVBoxLayout(self)
        self.viewer = ModelViewer()
        layout.addWidget(self.viewer)

        self.btn = QPushButton("Generate Test Box")
        self.btn.clicked.connect(self.make_box)
        layout.addWidget(self.btn)

    def make_box(self):
        # Create a simple CadQuery box
        result = cq.Workplane("XY").box(10, 10, 10).edges().fillet(2)
        self.viewer.display_shape(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())
