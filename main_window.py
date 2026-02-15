# Pyright false positive due to dynamic PySide attributes
# pyright: reportAttributeAccessIssue=false

import sys
import cadquery as cq
import PySide6 as PySide
from PySide6 import QtWidgets, QtCore

# Qt shortcut aliases
QtWidgets = PySide.QtWidgets
QtCore = PySide.QtCore

# Common Qt classes
QApplication = QtWidgets.QApplication
QMainWindow  = QtWidgets.QMainWindow

# Import UI class
from ui.main_window_ui import Ui_MainWindow

# Import custom classes
from build_ui import BuildUI
from model_viewer import ModelViewer

# TODO: Implement listeners for all values

class BoxCAD(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("BoxCAD - Parametric Enclosure Engine")
        self.resize(1200, 800)

        # Initialize components
        self.ui_builder = BuildUI()
        self.viewer = self.ui.viewer

        self.ui_builder.populate_toolbox(self.ui.parametersToolBox)

        def unlock_ui():
            # This reaches into the ui class and enables the specific button
            self.ui.initialize_btn.setEnabled(True)
            self.ui.initialize_btn.setToolTip("Click to begin your design")
            self.ui.print_to_console("3D Viewer is ready. UI Unlocked!", "success")

        # 4. Tell the viewer to run that function when JS says it's ready
        self.viewer.set_on_ready_callback(unlock_ui)

        self.ui_builder.initialize_btn.clicked.connect(self.init_project)

    def init_project(self):
        self.ui_builder.project_initialized = True

        self.ui_builder.populate_toolbox(self.ui.parametersToolBox)

        self.connect_ui_signals()
        self.rebuild_geometry()

        self.print_to_console("Project initialized!", "success")

    def connect_ui_signals(self):
        self.ui_builder.widgets["length"].valueChanged.connect(self.rebuild_geometry)
        self.ui_builder.widgets["width"].valueChanged.connect(self.rebuild_geometry)
        self.ui_builder.widgets["height"].valueChanged.connect(self.rebuild_geometry)

    def rebuild_geometry(self):
        try:
            l = self.ui_builder.widgets["length"].value()
            w = self.ui_builder.widgets["width"].value()
            h = self.ui_builder.widgets["height"].value()

            result = cq.Workplane("XY").box(l, w, h)

            self.viewer.update_display(result)

        except Exception as e:
            self.print_to_console(str(e), "error")

    def print_to_console(self, message = "No message was provided!", type = "info"):
        from termcolor import colored

        colors = {"info": "blue", "warning": "yellow", "error": "red", "success": "green", "silenced": "dark_grey"}

        color = colors.get(type, "white")

        print(colored(f"[{type.upper()}] {message}", color))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = BoxCAD()
    window.show()
    sys.exit(app.exec())
