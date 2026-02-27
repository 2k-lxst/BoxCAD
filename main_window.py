# Pyright false positive due to dynamic PySide attributes
# pyright: reportAttributeAccessIssue=false

import sys
import os
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
from enum import Enum, auto

# TODO: Implement listeners for all values

class AppState(Enum):
    UNINITIALIZED = auto()
    INITIALIZING = auto()
    READY = auto()
    ERROR = auto()

def resource_path(relative_path):
    """Get the absolute path to resource, works for dev and PyInstaller."""
    if getattr(sys, 'frozen', False):
        # Path where the .exe lives
        base_path = os.path.dirname(sys.executable)
    else:
        # Path where the script lives
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

class BoxCAD(QMainWindow):
    def __init__(self):
        super().__init__()

        self._state = AppState.UNINITIALIZED

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("BoxCAD - Parametric Enclosure Engine")
        self.resize(1200, 800)

        # Initialize components
        self.ui_builder = BuildUI()
        self.viewer = self.ui.viewer

        self.ui_builder.populate_toolbox(self.ui.parametersToolBox)

        def unlock_ui():
            try:
                import pyi_splash # type: ignore
                pyi_splash.close()
            except ImportError:  # This error happens if running in a development enviroment (IDE)
                pass

            # This reaches into the ui class and enables the specific button
            self.ui_builder.print_to_console("3D Viewer is ready. UI Unlocked!", "success")
            self.viewer.browser.page().runJavaScript("if(window.revealViewer) window.revealViewer();")

        # Tell the viewer to run that function when JavaScript says it's ready
        self.viewer.set_on_ready_callback(unlock_ui)

        self.ui_builder.initialize_btn.clicked.connect(
            lambda: self.set_state(AppState.INITIALIZING)
        )

    def init_project(self):
        self.ui_builder.project_initialized = True
        self.ui_builder.populate_toolbox(self.ui.parametersToolBox)
        self.connect_ui_signals()

        self.rebuild_geometry()

        self.set_state(AppState.READY)

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

            result = (
                cq.Workplane("XY")
                .box(w, l, h)
                .translate((0, 0, h / 2))
            )

            if (self.viewer.update_timer): self.viewer.update_display(result)

        except Exception as e:
            self.print_to_console(str(e), "error")

    def set_state(self, new_state: AppState):
        if self._state == new_state:
            return

        self._state = new_state
        self._update_ui_for_state()

        self.print_to_console(f"State of the app was just changed to *{new_state}*!", "state_change")

    def _update_ui_for_state(self):
        if self._state == AppState.INITIALIZING:
            self.ui_builder.initialize_btn.setText("Initializing...")
            self.ui_builder.initialize_btn.setEnabled(False)

            self.viewer.browser.page().runJavaScript("window.setLoading();")

            self.init_project()

        elif self._state == AppState.READY:
            # self.init_project()
            pass

        elif self._state == AppState.ERROR:
            # TODO: Call the viewer.html error handling
            return

    def print_to_console(self, message = "No message was provided!", type = "info"):
        from termcolor import colored

        colors = {"info": "blue", "warning": "yellow", "error": "red", "success": "green", "silenced": "dark_grey", "state_change": "magenta"}

        color = colors.get(type, "white")

        processed_message = message.replace("*", "\033[3m", 1).replace("*", "\033[23m", 1)

        print(colored(f"[{type.replace("_", " ").upper()}] {processed_message}", color))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = BoxCAD()
    window.show()
    sys.exit(app.exec())
