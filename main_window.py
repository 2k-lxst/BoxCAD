# Pyright false positive due to dynamic PySide attributes
# pyright: reportAttributeAccessIssue=false

import sys
import os
import cadquery as cq
import PySide6 as PySide
from PySide6 import QtWidgets
from qtpy import QtCore

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
    """Get the absolute path to resource, works for developement enviroment and PyInstaller."""
    if getattr(sys, 'frozen', False):
        # Path where the .exe lives
        base_path = os.path.dirname(sys.executable)
    else:
        # Path where the script lives
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

class WorkerSignals(QtCore.QObject):
    # Signals must be defined on a QObject
    result_ready = QtCore.Signal(object)
    error_occurred = QtCore.Signal(str, str)

class GeometryTask(QtCore.QRunnable):
    def __init__(self, params):
        super().__init__()
        self.params = params
        self.signals = WorkerSignals()

    def run(self):
        try:
            p = self.params

            p_outerLength = p["outer_length"]
            p_outerWidth = p["outer_width"]
            p_outerHeight = p["outer_height"]

            p_wallThickness = p["wall_thickness"]
            p_sideRadius = p["side_radius"]
            p_edgeRounding = p["edge_rounding"]

            p_screwpostInset = p["screwpost_inset"]
            p_screwpostInnerDiameter = p["screwpost_inner_diameter"]
            p_screwpostOuterDiameter = p["screwpost_outer_diameter"]

            p_boreDiameter = p["bore_diameter"]
            p_boreDepth = p["bore_depth"]
            p_countersinkDiameter = p["countersink_diameter"]
            p_countersinkAngle = p["countersink_angle"]

            p_invertLid = p["invert_lid"]
            p_lipHeight = p["lip_height"]

            outer_shell = (
                cq.Workplane("XY")
                .rect(p_outerWidth, p_outerLength)
                .extrude(p_outerHeight + p_lipHeight)
            )

            limit = min(p_outerWidth, p_outerLength, p_outerHeight) / 2.0 - 0.1

            safe_side = min(p_sideRadius, limit)
            safe_edge = min(p_edgeRounding, limit)

            if safe_side > 0.01 or safe_edge > 0.01:
                try:
                    if safe_side > safe_edge:
                        outer_shell = outer_shell.edges("|Z").fillet(p_sideRadius)
                        outer_shell = outer_shell.edges("#Z").fillet(p_edgeRounding)
                    else:
                        outer_shell = outer_shell.edges("#Z").fillet(p_edgeRounding)
                        outer_shell = outer_shell.edges("|Z").fillet(p_sideRadius)
                except Exception:
                    # Use the signal bridge to send the message back to the main window
                    self.signals.error_occurred.emit("Fillet math failed, skipping rounding to prevent crash.", "warning")

            # Prevent negative/zero inner fillets
            # The inner radius must be at least 0.1 to prevent BRep errors
            safe_inner_radius = max(0.1, p_sideRadius - p_wallThickness)

            # Prevent wall thickness from exceeding box size
            # Wall thickness can't be more than half the smallest dimension
            max_wall_thickness = min(p_outerWidth, p_outerLength, p_outerHeight) / 2.1
            actual_wall_thickness = min(p_wallThickness, max_wall_thickness)

            inner_shell = (
                outer_shell.faces("<Z")
                .workplane(actual_wall_thickness, True)
                .rect((p_outerWidth - 2.0 * actual_wall_thickness), (p_outerLength - 2.0 * actual_wall_thickness))
                .extrude(
                    (p_outerHeight - 2.0 * actual_wall_thickness), False
                )
            )

            inner_shell = inner_shell.edges("|Z").fillet(safe_inner_radius)

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

            (lid, bottom) = (
                box.faces(">Z")
                .workplane(-p_wallThickness - p_lipHeight)
                .split(keepTop=True, keepBottom=True)
                .all()
            )

            lowerLid = lid.translate((0, 0, -p_lipHeight))
            cutLip = lowerLid.cut(bottom).translate(
                (p_outerWidth + p_wallThickness, 0, p_wallThickness - p_outerHeight + p_lipHeight)
            )

            screwHoleCenters = (
                cutLip.faces(">Z")
                .workplane(centerOption="CenterOfMass")
                .rect(screwpost_width, screwpost_length, forConstruction=True)
                .vertices()
            )

            if p_boreDiameter > 0 and p_boreDepth > 0:
                topOfLid = screwHoleCenters.cboreHole(
                    p_screwpostInnerDiameter,
                    p_boreDiameter,
                    p_boreDepth,
                    p_outerHeight * 2 # Cut through everything
                )
            elif p_countersinkDiameter > 0 and p_countersinkAngle > 0:
                topOfLid = screwHoleCenters.cskHole(
                    p_screwpostInnerDiameter,
                    p_countersinkDiameter,
                    p_countersinkAngle,
                    p_outerHeight * 2 # Cut through everything
                )
            else:
                topOfLid = screwHoleCenters.hole(
                    p_screwpostInnerDiameter,
                    p_outerHeight * 2 # Cut through everything
                )

            if p_invertLid:
                topOfLid = topOfLid.rotateAboutCenter((1, 0, 0), 180)

            result = topOfLid.union(bottom)

            self.signals.result_ready.emit(result)
        except Exception as e:
            self.signals.error_occurred.emit(str(e), "error")

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

        self.ui_builder.populate_toolbox(self.ui.parametersToolBox, self.viewer)

        def unlock_ui():
            # This reaches into the ui class and enables the specific button
            self.ui_builder.initialize_btn.setEnabled(True)
            self.ui_builder.initialize_btn.setToolTip("Click to begin your design")
            self.ui_builder.print_to_console("3D Viewer is ready!", "success")

        # Tell the viewer to run that function when JavaScript says it's ready
        self.viewer.set_on_ready_callback(unlock_ui)

        self.ui_builder.initialize_btn.clicked.connect(
            lambda: self.set_state(AppState.INITIALIZING)
        )

        self.thread_pool = QtCore.QThreadPool.globalInstance()

        self.rebuild_timer = QtCore.QTimer()
        self.rebuild_timer.setSingleShot(True)
        self.rebuild_timer.setInterval(200)
        self.rebuild_timer.timeout.connect(self.execute_thread_build)

    def rebuild_geometry(self):
        """Called by UI signals. Just restarts the timer."""
        self.rebuild_timer.start()

    def execute_thread_build(self):
        """Starts the background work and shows the loader."""
        # Show loader instantly
        self.viewer.browser.page().runJavaScript("window.showLoader();")

        # Extract plain data from widgets (must stay on main thread)
        params = {}

        for k, v in self.ui_builder.widgets.items():
            if hasattr(v, 'value'): # QDoubleSpinBox / QSpinBox
                params[k] = v.value()
            elif hasattr(v, 'isChecked'): # QCheckBox
                params[k] = v.isChecked()
            elif hasattr(v, 'currentText'): # QComboBox
                params[k] = v.currentText()
            elif hasattr(v, 'toPlainText'): # QPlainTextEdit (for coordinates)
                params[k] = v.toPlainText()

        # Create and connect the task
        task = GeometryTask(params)
        task.signals.result_ready.connect(self.on_render_success)
        task.signals.error_occurred.connect(self.on_render_error)

        # Dispatch to the pool
        self.thread_pool.start(task)

    def on_render_success(self, result):
        """Update 3D viewer and hide loader"""
        self.viewer.update_display(result)
        self.viewer.browser.page().runJavaScript("window.hideLoader();")

    def on_render_error(self, message, type):
        """Print error and hide loader"""
        self.print_to_console(message, type)
        self.viewer.browser.page().runJavaScript("window.hideLoader();")

    def init_project(self):
        self.ui_builder.project_initialized = True
        self.ui_builder.populate_toolbox(self.ui.parametersToolBox, self.viewer)
        self.connect_ui_signals()

        self.rebuild_geometry()

        self.set_state(AppState.READY)

        self.print_to_console("Project initialized!", "success")

    def connect_ui_signals(self):
        for key, widget in self.ui_builder.widgets.items():
            if isinstance(widget, (QtWidgets.QDoubleSpinBox, QtWidgets.QSpinBox)):
                widget.valueChanged.connect(self.rebuild_geometry)
            elif isinstance(widget, QtWidgets.QCheckBox):
                widget.stateChanged.connect(self.rebuild_geometry)
            elif isinstance(widget, QtWidgets.QComboBox):
                widget.currentIndexChanged.connect(self.rebuild_geometry)
            elif isinstance(widget, QtWidgets.QPlainTextEdit):
                widget.textChanged.connect(self.rebuild_geometry)

        if hasattr(self.ui_builder, 'add_cutout_btn'):
            self.ui_builder.add_cutout_btn.clicked.connect(self.rebuild_geometry)

    def set_state(self, new_state: AppState):
        if self._state == new_state:
            return

        self._state = new_state
        self._update_ui_for_state()

        self.print_to_console(f"State of the app was just changed to {str(new_state).lstrip("AppState.")} ({new_state})!", "state_change")

    def _update_ui_for_state(self):
        if self._state == AppState.INITIALIZING:
            self.ui_builder.initialize_btn.setText("Initializing...")
            self.ui_builder.initialize_btn.setEnabled(False)
            self.viewer.browser.page().runJavaScript("window.setLoading();")

            # Delay the heavy function by 1s (1000 ms)
            QtCore.QTimer.singleShot(1000, self.init_project)

        elif self._state == AppState.READY:
            pass

        elif self._state == AppState.ERROR:
            # TODO: Call the viewer.html error handling
            pass

    def print_to_console(self, message = "No message was provided!", type = "info"):
        from termcolor import colored

        colors = {"info": "blue", "warning": "yellow", "error": "red", "success": "green", "silenced": "dark_grey", "state_change": "magenta"}

        color = colors.get(type, "white")

        print(colored(f"[{type.replace("_", " ").upper()}] {message}", color))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = BoxCAD()
    window.show()
    sys.exit(app.exec())
