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

        try:
            import pyi_splash # type: ignore
            pyi_splash.close()
        except ImportError:  # This error happens if running in a development enviroment (IDE)
            pass

        # Initialize components
        self.ui_builder = BuildUI()
        self.viewer = self.ui.viewer

        self.ui_builder.populate_toolbox(self.ui.parametersToolBox)

        def unlock_ui():
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
        self.ui_builder.widgets["outer_length"].valueChanged.connect(self.rebuild_geometry)
        self.ui_builder.widgets["outer_width"].valueChanged.connect(self.rebuild_geometry)
        self.ui_builder.widgets["outer_height"].valueChanged.connect(self.rebuild_geometry)

    def rebuild_geometry(self):
        try:
            p_outerLength = self.ui_builder.widgets["outer_length"].value()
            p_outerWidth = self.ui_builder.widgets["outer_width"].value()
            p_outerHeight = self.ui_builder.widgets["outer_height"].value()

            p_wallThickness = self.ui_builder.widgets["wall_thickness"].value()
            p_sideRadius = self.ui_builder.widgets["side_radius"].value()
            p_edgeRounding = self.ui_builder.widgets["edge_rounding"].value()

            p_screwpostInset = self.ui_builder.widgets["screwpost_inset"].value()
            p_screwpostInnerDiameter = self.ui_builder.widgets["screwpost_inner_diameter"].value()
            p_screwpostOuterDiameter = self.ui_builder.widgets["screwpost_outer_diameter"].value()

            p_boreDiameter = self.ui_builder.widgets["bore_diameter"].value()
            p_boreDepth = self.ui_builder.widgets["bore_depth"].value()
            p_countersinkDiameter = self.ui_builder.widgets["countersink_diameter"].value()
            p_countersinkAngle = self.ui_builder.widgets["countersink_angle"].value()

            p_invertLid = self.ui_builder.widgets["invert_lid"].checked()
            p_lipHeight = self.ui_builder.widgets["lip_height"].value()

            outer_shell = (
                cq.Workplane("XY")
                .rect(p_outerWidth, p_outerLength)
                .extrude(p_outerHeight + p_lipHeight)
            )

            if p_sideRadius > p_edgeRounding:
                outer_shell = outer_shell.edges("|Z").fillet(p_sideRadius)
                outer_shell = outer_shell.edges("#Z").fillet(p_edgeRounding)
            else:
                outer_shell = outer_shell.edges("#Z").fillet(p_edgeRounding)
                outer_shell = outer_shell.edges("|Z").fillet(p_sideRadius)

            inner_shell = (
                outer_shell.faces("<Z")
                .workplane(p_wallThickness, True)
                .rect((p_outerWidth - 2.0 * p_wallThickness), (p_outerLength - 2.0 * p_wallThickness))
                .extrude(
                    (p_outerHeight - 2.0 * p_wallThickness), False
                )
            )

            inner_shell = inner_shell.edges("|Z").fillet(p_sideRadius - p_wallThickness)

            box = outer_shell.cut(inner_shell)
            box = outer_shell.cut(inner_shell)

            screwpost_width = p_outerWidth - 2.0 * p_screwpostInset
            screwpost_length = p_outerLength - 2.0 * p_screwpostInset

            box = (
                box.faces(">Z")
                .workplane(-p_wallThickness)
                .rect(screwpost_width, screwpost_length, forConstruction=True)
                .vertices()
                .circle(p_screwpostOuterDiameter / 2.0)
                .circle(p_screwpostInnerDiameter / 2.0)
                .extrude(-1.0 * (p_outerHeight + p_lipHeight - p_wallThickness), True)
            )

            # if (self.viewer.update_timer): self.viewer.update_display(result)

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
            pass

        elif self._state == AppState.ERROR:
            # TODO: Call the viewer.html error handling
            pass

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
