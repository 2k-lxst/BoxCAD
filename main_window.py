# Pyright false positive due to dynamic PySide attributes
# pyright: reportAttributeAccessIssue=false

import sys
import os
import shutil
import json
import webbrowser
import platform
import subprocess
import cadquery as cq
import PySide6 as PySide
from PySide6 import QtWidgets
from qtpy import QtCore
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QFileDialog, QMessageBox

# Qt shortcut aliases
QtWidgets = PySide.QtWidgets
QtCore = PySide.QtCore

# Common Qt classes
QApplication = QtWidgets.QApplication
QMainWindow  = QtWidgets.QMainWindow

# Import UI class
from ui.main_window_ui import Ui_MainWindow

# Import custom classes
from build_ui import BuildUI, PortGuideDialog
from enum import Enum, auto

# The universal AppState enum
class AppState(Enum):
    UNINITIALIZED = auto()
    INITIALIZING = auto()
    READY = auto()
    ERROR = auto()

# The file ExportFormat enum
class ExportFormat(Enum):
    STL = auto()
    STEP = auto()

def resource_path(relative_path):
    """Get the absolute path to resource, works for developement enviroment and PyInstaller."""
    if getattr(sys, "frozen", False):
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
            p_cornerRadius = p["corner_radius"]
            p_edgeRounding = p["edge_rounding"]
            p_floorThickness = 2.0

            p_holeType = p["hole_type"]
            p_lidConnectionType = p["lid_connection_type"]
            p_invertLid = p["invert_lid"]
            p_lidHeight = p["lid_height"]
            p_screwpostInset = p["screwpost_inset"]
            p_screwpostOuterDiameter = p["screwpost_outer_diameter"]
            p_screwpostInnerDiameter = p["screwpost_inner_diameter"]

            p_boreDiameter = p["bore_diameter"]
            p_boreDepth = p["bore_depth"]
            p_countersinkDiameter = p["countersink_diameter"]
            p_countersinkAngle = p["countersink_angle"]

            p_pcbScrewpostsOuterDiameter = p["pcb_screwposts_outer_diameter"]
            p_pcbScrewpostsInnerDiameter = p["pcb_screwposts_inner_diameter"]
            p_pcbScrewpostsHeight = p["pcb_screwposts_height"]
            p_pcbScrewpostsCoordinates = p["pcb_screwposts_coordinates"]

            p_cutouts = p["cutouts"]

            outer_shell = (
                cq.Workplane("XY")
                .rect(p_outerWidth, p_outerLength)
                .extrude(p_outerHeight + p_lidHeight)
            )

            limit = min(p_outerWidth, p_outerLength, p_outerHeight) / 2.0 - 0.1

            safe_side = min(p_cornerRadius, limit)
            safe_edge = min(p_edgeRounding, limit)

            if safe_side > 0.01 or safe_edge > 0.01:
                try:
                    if safe_side > safe_edge:
                        outer_shell = outer_shell.edges("|Z").fillet(p_cornerRadius)
                        outer_shell = outer_shell.edges("#Z").fillet(p_edgeRounding)
                    else:
                        outer_shell = outer_shell.edges("#Z").fillet(p_edgeRounding)
                        outer_shell = outer_shell.edges("|Z").fillet(p_cornerRadius)
                except Exception:
                    # Use the signal bridge to send the message back to the main window
                    self.signals.error_occurred.emit("Fillet math failed, skipping rounding to prevent crash.", "warning")

            # Prevent negative/zero inner fillets
            # The inner radius must be at least 0.1 to prevent BRep errors
            safe_inner_radius = max(0.1, p_cornerRadius - p_wallThickness)

            # Prevent wall thickness from exceeding box size
            # Wall thickness can't be more than half the smallest dimension
            max_wall_thickness = min(p_outerWidth, p_outerLength, p_outerHeight) / 2.1
            actual_wall_thickness = min(p_wallThickness, max_wall_thickness)

            lid_roof_thickness = min(p_floorThickness, p_lidHeight - 0.5)

            inner_shell_height = (p_outerHeight + p_lidHeight) - p_floorThickness - lid_roof_thickness

            inner_shell = (
                cq.Workplane("XY")
                .workplane(offset=p_floorThickness)
                .rect((p_outerWidth - 2.0 * actual_wall_thickness), (p_outerLength - 2.0 * actual_wall_thickness))
                .extrude(inner_shell_height)
            )

            inner_shell = inner_shell.edges("|Z").fillet(safe_inner_radius)

            box = outer_shell.cut(inner_shell)

            mapping = {
                "Left (-X)": "<X",
                "Right (+X)": ">X",
                "Front (-Y)": "<Y",
                "Back (+Y)": ">Y",
                "Bottom (-Z)": "<Z",
                "Top (+Z)": ">Z"
            }

            for cutout in p_cutouts:
                box = cq.Workplane("XY").add(box.val())
                face_selector = mapping.get(cutout["face"], ">Z")

                try:
                    if cutout["shape"] == "Rectangle":
                        box = (
                            box.faces(face_selector)
                            .workplane()
                            .center(cutout["x"], cutout["y"])
                            .rect(cutout["width"], cutout["height"])
                            .cutBlind(-100)
                        )
                    elif cutout["shape"] == "Circle":
                        box = (
                            box.faces(face_selector)
                            .workplane()
                            .center(cutout["x"], cutout["y"])
                            .circle(cutout["diameter"] / 2)
                            .cutBlind(-100)
                        )
                except Exception as e:
                    self.signals.error_occurred.emit(f"Cutout failed on {cutout["face"]}: {e}", "warning")

            if p_pcbScrewpostsCoordinates.strip():
                for line in p_pcbScrewpostsCoordinates.strip().splitlines():
                    line = line.strip()

                    if not line: continue

                    try:
                        x_str, y_str = line.split(",")

                        sx = float(x_str.strip())
                        sy = float(y_str.strip())

                        box = (
                            cq.Workplane("XY").add(box.val())
                            .faces("<Z")
                            .workplane(offset=p_floorThickness, invert=True)
                            .center(sx, sy)
                            .circle(p_pcbScrewpostsOuterDiameter / 2.0)
                            .extrude(p_pcbScrewpostsHeight)
                        )

                        box = (
                            cq.Workplane("XY").add(box.val())
                            .faces("<Z")
                            .workplane(offset=p_floorThickness, invert=True)
                            .center(sx, sy)
                            .circle(p_pcbScrewpostsInnerDiameter / 2.0)
                            .cutBlind(p_pcbScrewpostsHeight)
                        )
                    except Exception as e:
                        self.signals.error_occurred.emit(f"PCB screwpost parse error on '{line}': {e}", "warning")

            box = cq.Workplane("XY").add(box.val())

            screwpost_width = (p_outerWidth - 2.0 * actual_wall_thickness) - 2.0 * p_screwpostInset
            screwpost_length = (p_outerLength - 2.0 * actual_wall_thickness) - 2.0 * p_screwpostInset

            # TODO: Fix comments

            lid_top_z = box.val().BoundingBox().zmax
            pillar_height = lid_top_z - p_floorThickness

            box = (
                box.faces(">Z")
                .workplane(-lid_roof_thickness)
                .rect(screwpost_width, screwpost_length, forConstruction=True)
                .vertices()
                .circle(p_screwpostOuterDiameter / 2.0)
                .circle(p_screwpostInnerDiameter / 2.0)
                .extrude(-pillar_height, True)
            )

            (lid, bottom) = (
                box.faces(">Z")
                .workplane(-p_lidHeight)
                .split(keepTop=True, keepBottom=True)
                .all()
            )

            if p_lidConnectionType == "Lip":
                lip_clearance = 0.2
                lip_wall = 1.2

                lip_outer_width = p_outerWidth - 2.0 * actual_wall_thickness
                lip_outer_length = p_outerLength - 2.0 * actual_wall_thickness

                lip_inner_width = lip_outer_width - 2.0 * lip_wall
                lip_inner_length = lip_outer_length - 2.0 * lip_wall

                if lip_inner_width > 1 and lip_inner_length > 1:
                    # Create lip at origin
                    lip = (
                        cq.Workplane("XY")
                        .rect(lip_outer_width, lip_outer_length)
                        .rect(lip_inner_width, lip_inner_length)
                        .extrude(p_lidHeight)
                    )

                    # Attach lip to lid, but keep the lip origin unchanged
                    lid = lid.union(lip.translate((0, 0, -p_lidHeight + p_outerHeight)))

                    # Cut bottom for clearance
                    lip_cutout = (
                        cq.Workplane("XY")
                        .rect(lip_outer_width + lip_clearance, lip_outer_length + lip_clearance)
                        .rect(
                            max(1, lip_inner_width - lip_clearance),
                            max(1, lip_inner_length - lip_clearance)
                        )
                        .extrude(p_lidHeight)
                        .translate((0, 0, -p_lidHeight + lip_clearance))
                    )

                    # Move the enclosure down because the lip pushes it up
                    bottom = bottom.translate((0, 0, -p_lidHeight * 2))

            screwHoleCenters = (
                cq.Workplane("XY").add(lid.val())
                .faces(">Z")
                .workplane()
                .rect(screwpost_width, screwpost_length, forConstruction=True)
                .vertices()
            )

            if p_holeType == "Counterbore" and p_boreDiameter > 0 and p_boreDepth > 0:
                topOfLid = screwHoleCenters.cboreHole(
                    p_screwpostInnerDiameter,
                    p_boreDiameter,
                    p_boreDepth,
                    p_outerHeight * 2
                )
            elif p_holeType == "Countersink" and p_countersinkDiameter > 0 and p_countersinkAngle > 0:
                topOfLid = screwHoleCenters.cskHole(
                    p_screwpostInnerDiameter,
                    p_countersinkDiameter,
                    p_countersinkAngle,
                    p_outerHeight * 2
                )
            else:
                topOfLid = screwHoleCenters.hole(
                    p_screwpostInnerDiameter,
                    p_outerHeight * 2
                )

            lid_z_offset = -p_outerHeight - (p_lidHeight if p_lidConnectionType == "Lip" else 0)

            # Translate after holes are drilled
            topOfLid = topOfLid.translate(
                (p_outerWidth + p_wallThickness, 0, lid_z_offset)
            )

            if p_invertLid:
                lid_center = topOfLid.val().BoundingBox().center

                topOfLid = topOfLid.rotate(
                    lid_center.toTuple(),
                    (lid_center.x + 1, lid_center.y, lid_center.z),
                    180
                )

                if (p_lidConnectionType == "Simple (no lip)"):
                    bottom = bottom.translate((0, 0, p_lidHeight / 2))

            result = topOfLid.union(bottom)

            self.signals.result_ready.emit(result)
        except Exception as e:
            self.signals.error_occurred.emit(str(e), "error")

class BoxCAD(QMainWindow):
    def __init__(self, project_path, app_version = "Unknown Version"):
        super().__init__()

        self.last_result = None
        self._loading = False

        self.app_version = app_version

        self._history: list[dict] = []
        self._history_index: int = -1

        if project_path is None:
            self.current_filename = "Untitled project"
            self.current_filepath: str | None = None
        else:
            # If path is "C:/Users/You/Box1.json", this makes filename "Box1.json"
            self.current_filename = os.path.basename(project_path)
            self.current_filepath = project_path

        self._state = AppState.UNINITIALIZED # Set the starting application state

        # Setup the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Configure the window
        self.setWindowTitle(f"BoxCAD - {self.current_filename}")
        self.mark_unsaved()
        self.resize(1200, 800)

        # Create menu bar
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")
        self.action_new = file_menu.addAction("New Project", self.new_project, "Ctrl+N")
        self.action_open = file_menu.addAction("Open Project", self.open_project, "Ctrl+O")
        file_menu.addSeparator()
        self.action_save = file_menu.addAction("Save", self.save_project, "Ctrl+S")
        self.action_save_as = file_menu.addAction("Save As", self.save_project_as, "Ctrl+Shift+S")
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close, "Alt+F4")

        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        self.action_undo = edit_menu.addAction("Undo", self.undo, "Ctrl+Z")
        self.action_redo = edit_menu.addAction("Redo", self.redo, "Ctrl+Y")

        # Export menu
        export_menu = menubar.addMenu("Export")
        self.action_export_stl = export_menu.addAction("Export as STL", lambda: self.export(ExportFormat.STL), "Ctrl+E")
        self.action_export_step = export_menu.addAction("Export as STEP", lambda: self.export(ExportFormat.STEP), "Ctrl+Shift+E")

        # Help menu
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("Documentation", self.open_documentation)
        help_menu.addAction("About BoxCAD", self.show_about)

        # Disable until initialized
        self.action_new.setEnabled(False)
        self.action_open.setEnabled(False)
        self.action_save.setEnabled(False)
        self.action_save_as.setEnabled(False)
        self.action_undo.setEnabled(False)
        self.action_redo.setEnabled(False)
        self.action_export_step.setEnabled(False)
        self.action_export_stl.setEnabled(False)

        # Close the splash screen
        try:
            import pyi_splash # type: ignore
            pyi_splash.close()
        except ImportError: # This error happens if running in a development enviroment (IDE)
            pass

        header = f"Information: BoxCAD v{app_version}"

        self.print_to_console(
            f"{header}\n"
            f"{'=' * len(header)}\n"
            f"Python: {sys.version.split()[0]} ({platform.python_implementation()})\n"
            f"Executable: {sys.executable}\nOS: {platform.system()} {platform.release()} ({platform.machine()})\n",
            "startup"
        )

        if not os.path.isfile(resource_path("model.stl")):
            shutil.copy(resource_path("startingModel.stl"), resource_path("model.stl"))
            os.remove(resource_path("startingModel.stl"))

        # Initialize components
        self.ui_builder = BuildUI()
        self.viewer = self.ui.viewer
        self.viewer.set_logger(self.print_to_console)

        self.ui_builder.populate_toolbox(self.ui.parametersToolBox, self.viewer, self.show_port_guide)

        def unlock_ui():

            # This reaches into the UI class and enables the specific button
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

    def show_port_guide(self):
        def fill(w, h):
            self.ui_builder.cutout_width_input.setValue(w)
            self.ui_builder.cutout_height_input.setValue(h)

        self.guide_dialog = PortGuideDialog(self, fill_callback=fill)

        self.guide_dialog.show()
        self.guide_dialog.raise_()
        self.guide_dialog.activateWindow()

        self.print_to_console("Opened port reference guide", "info")

    def new_project(self):
        # Reset file state
        self.current_filepath = None
        self.current_filename = "Untitled project"
        self.mark_saved()

        # Reset all widgets to their default values
        for k, v in self.ui_builder.widgets.items():
            if isinstance(v, (QtWidgets.QDoubleSpinBox, QtWidgets.QSpinBox)):
                v.setValue(v.minimum())
            elif isinstance(v, QtWidgets.QCheckBox):
                v.setChecked(False)
            elif isinstance(v, QtWidgets.QComboBox):
                v.setCurrentIndex(0)
            elif isinstance(v, QtWidgets.QPlainTextEdit):
                v.setPlainText("")

        self.rebuild_geometry()

    def save_project_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Project As",
            "",
            "BoxCAD Project (*.boxcad)"
        )

        if not path: # User cancelled
            return

        self.current_filepath = path
        self.current_filename = os.path.basename(path)
        self.mark_saved()
        self.save_project()

    def _apply_snapshot(self, data):
        for k, v in data.items():
            if k not in self.ui_builder.widgets:
                continue

            widget = self.ui_builder.widgets[k]

            # Block signals to avoid triggering rebuild/snapshot while restoring
            widget.blockSignals(True)
            if hasattr(widget, "setValue") and isinstance(v, (int, float)):
                widget.setValue(v)
            elif hasattr(widget, "setChecked") and isinstance(v, bool):
                widget.setChecked(v)
            elif hasattr(widget, "setCurrentText") and isinstance(v, str):
                widget.setCurrentText(v)
            elif hasattr(widget, "setPlainText") and isinstance(v, str):
                widget.setPlainText(v)

            widget.blockSignals(False)

        self.rebuild_timer.start()

    def undo(self):
        if self._history_index <= 0:
            self.print_to_console("Nothing to undo.", "warning")
            return

        self._history_index -= 1
        self._apply_snapshot(self._history[self._history_index])

    def redo(self):
        if self._history_index >= len(self._history) - 1:
            self.print_to_console("Nothing to redo.", "warning")
            return

        self._history_index += 1
        self._apply_snapshot(self._history[self._history_index])

    def open_documentation(self):
        webbrowser.open("https://sites.google.com/view/boxcad-docs/home")

    def show_about(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("About BoxCAD")
        msg.setTextFormat(Qt.RichText)
        msg.setText(
            "<h2 style='margin-bottom: 4px;'>BoxCAD</h2>"
            "<p style='color: #888888; margin-top: 0px;'><i>A Parametric Enclosure Designer for Makers</i></p>"
            "<hr>"
            "<p>"
            "BoxCAD is a lightweight, Python-powered desktop application for designing "
            "custom, 3D-printable project enclosures. Instead of manually modeling simple "
            "boxes in CAD software, you define dimensions, preview "
            "the result in real time, and export directly for manufacturing."
            "</p>"
            "<p>"
            "The goal is <b>speed</b>, <b>repeatability</b>, and <b>clean parametric control</b> "
            "— especially for electronics projects."
            "</p>"
            "<hr>"
            f"<p style='color: #888888; font-size: 11px;'>v{self.app_version} &nbsp;·&nbsp; Made with ❤️ in Slovenia</p>"
        )

        msg.setStandardButtons(QMessageBox.Ok)
        msg.button(QMessageBox.Ok).setText("Close")
        msg.exec()

    def _take_snapshot(self):
        data = {}

        for k, v in self.ui_builder.widgets.items():
            if hasattr(v, "value"):
                data[k] = v.value()
            elif hasattr(v, "isChecked"):
                data[k] = v.isChecked()
            elif hasattr(v, "currentText"):
                data[k] = v.currentText()
            elif hasattr(v, "toPlainText"):
                data[k] = v.toPlainText()

        # Discard any redo history beyond current index
        self._history = self._history[:self._history_index + 1]
        self._history.append(data)
        self._history_index += 1

    def rebuild_geometry(self):
        """Called by UI signals. Just restarts the timer."""
        self.mark_unsaved()
        self._take_snapshot()
        self.rebuild_timer.start()

    def execute_thread_build(self):
        """Starts the background work and shows the loader."""
        # Show loader instantly
        self.viewer.browser.page().runJavaScript("window.showLoader();")

        # Extract plain data from widgets (must stay on main thread)
        params = {}

        for k, v in self.ui_builder.widgets.items():
            if hasattr(v, "value"): # QDoubleSpinBox / QSpinBox
                params[k] = v.value()
            elif hasattr(v, "isChecked"): # QCheckBox
                params[k] = v.isChecked()
            elif hasattr(v, "currentText"): # QComboBox
                params[k] = v.currentText()
            elif hasattr(v, "toPlainText"): # QPlainTextEdit (for coordinates)
                params[k] = v.toPlainText()

        params["cutouts"] = self.ui_builder.cutouts

        if params.get("lid_connection_type") == "Lip":
            if hasattr(self.ui_builder, "lid_height_label"):
                self.ui_builder.lid_height_label.setText("Lip Height:")
        else:
            if hasattr(self.ui_builder, "lid_height_label"):
                self.ui_builder.lid_height_label.setText("Lid Height (Z):")

        # Create and connect the task
        task = GeometryTask(params)
        task.signals.result_ready.connect(self.on_render_success)
        task.signals.error_occurred.connect(self.on_render_error)

        # Dispatch to the pool
        self.thread_pool.start(task)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_S and event.modifiers() == QtCore.Qt.ControlModifier:
            self.save_project()
        elif event.key() == QtCore.Qt.Key_O and event.modifiers() == QtCore.Qt.ControlModifier:
            self.open_project()
        else:
            super().keyPressEvent(event)

    def save_project(self):
        if self.current_filename == "Untitled project":
            # No file yet - prompt to save location
            path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Project",
                "",
                "BoxCAD Project (*.boxcad)"
            )

            if not path: # User cancelled
                return

            self.current_filename = os.path.basename(path)
            self.current_filepath = path

            self.mark_saved()
        else:
            path = self.current_filepath

        # Collect all widget values
        data = {}

        for k, v in self.ui_builder.widgets.items():
            if hasattr(v, "value"):
                data[k] = v.value()
            elif hasattr(v, "isChecked"):
                data[k] = v.isChecked()
            elif hasattr(v, "currentText"):
                data[k] = v.currentText()
            elif hasattr(v, "toPlainText"):
                data[k] = v.toPlainText()

        data["cutouts"] = self.ui_builder.cutouts

        with open(path, 'w') as f: # type: ignore
            json.dump(data, f, indent=4)
            self.mark_saved()
            self.print_to_console(f"Project saved to {path}", "success")

    def open_project(self, path: str | None = None):
        self._loading = True

        if path is None:
            path, _ = QFileDialog.getOpenFileName(
                self,
                "Open Project",
                "",
                "BoxCAD Project (*.boxcad)"
            )

            if not path: # User cancelled
                return

        try:
            with open(path, 'r') as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            self.print_to_console(f"Failed to open project: {e}", "error")

            return

        # Update all widgets with the loaded values
        for k, v in data.items():
            if k not in self.ui_builder.widgets:
                continue

            widget = self.ui_builder.widgets[k]

            if hasattr(widget, "setValue") and isinstance(v, (int, float)):
                widget.setValue(v)
            elif hasattr(widget, "setChecked") and isinstance(v, bool):
                widget.setChecked(v)
            elif hasattr(widget, "setCurrentText") and isinstance(v, str):
                widget.setCurrentText(v)
            elif hasattr(widget, "setPlainText") and isinstance(v, str):
                widget.setPlainText(v)

        if "cutouts" in data:
            self.ui_builder.cutouts = []

            # Clear existing cutout widgets from the layout
            for i in reversed(range(self.ui_builder.manager_layout.count())):
                widget = self.ui_builder.manager_layout.itemAt(i).widget()
                if widget and widget != self.ui_builder.no_cutouts_label:
                    widget.deleteLater()

            # Re-add each cutout
            for cutout in data["cutouts"]:
                self.ui_builder.cutouts.append(cutout)
                self.ui_builder._add_cutout_to_list(cutout)

            self.ui_builder.refresh_empty_state()

        # Update state
        self.current_filepath = path
        self.current_filename = os.path.basename(path)

        self._loading = False

        self.print_to_console(f"Project loaded from {path}", "success")

        # Trigger a rebuild with the loaded values
        self.rebuild_geometry()

        self.mark_saved()

    def export(self, format):
        if self.last_result is None:
            self.print_to_console("Nothing to export yet!", "warning")

            return

        if format == ExportFormat.STEP:
            file_filter = "STEP Files (*.step)"
            extension = ".step"
        elif format == ExportFormat.STL:
            file_filter = "STL Files (*.stl)"
            extension = ".stl"
        else: # Prevent PyLance errors
            file_filter = ""
            extension = ""

        default_name = os.path.splitext(self.current_filename)[0] + extension

        path, _ = QFileDialog.getSaveFileName(
            self,
            f"Export as {format.name}",
            default_name,
            file_filter
        )

        if not path: # User cancelled
            return

        try:
            if format == ExportFormat.STL:
                cq.exporters.export(self.last_result, path)
            elif format == ExportFormat.STEP:
                cq.exporters.export(self.last_result, path)

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Export Successful")
            msg.setText(f"<b>{os.path.basename(path)}</b> was exported successfully.")
            msg.setInformativeText(f"Format: {format.name}\nLocation: {os.path.dirname(path)}")

            open_folder_btn = msg.addButton("Open Folder", QMessageBox.ActionRole)
            msg.addButton("Close", QMessageBox.AcceptRole)

            msg.exec()

            if msg.clickedButton() == open_folder_btn:
                folder = os.path.dirname(path)

                if platform.system() == "Windows": # Windows
                    subprocess.Popen(f'explorer /select,"{path.replace("/", "\\")}"')
                elif platform.system() == "Darwin": # Mac
                    subprocess.Popen(["open", "-R", path])
                else: # Linux
                    subprocess.Popen(["xdg-open", folder])

            self.print_to_console(f"Exported {format.name} to {path}", "success")
        except Exception as e:
            self.print_to_console(f"Export failed: {e}", "error")

    def mark_unsaved(self):
        if self._loading: return

        title = self.windowTitle()

        if not title.endswith("*"):
            self.setWindowTitle(title + " *")

    def mark_saved(self):
        title = self.windowTitle()

        if title.endswith("*"):
            self.setWindowTitle(title[:-2])

    def on_render_success(self, result):
        """Update 3D viewer and hide loader"""
        self.last_result = result
        self.viewer.update_display(result)
        self.viewer.browser.page().runJavaScript("window.hideLoader();")

    def on_render_error(self, message, type):
        """Print error and show error message box"""
        self.print_to_console(message, type)
        self.viewer.browser.page().runJavaScript("window.hideLoader();")

    def init_project(self):
        self.ui_builder.project_initialized = True
        self.ui_builder.populate_toolbox(self.ui.parametersToolBox, self.viewer, self.show_port_guide)
        self.connect_ui_signals()

        # Enable menu actions now that project is ready
        self.action_new.setEnabled(True)
        self.action_open.setEnabled(True)
        self.action_save.setEnabled(True)
        self.action_save_as.setEnabled(True)
        self.action_undo.setEnabled(True)
        self.action_redo.setEnabled(True)
        self.action_export_stl.setEnabled(True)
        self.action_export_step.setEnabled(True)

        if self.current_filepath is not None:
            self.open_project(self.current_filepath)
        else:
            self.rebuild_geometry()

        self.set_state(AppState.READY)
        self.print_to_console("Project initialized!", "success")

    def closeEvent(self, event):
        if self._state == AppState.READY and self.windowTitle().endswith(" *"):
            msg = QMessageBox(self)
            msg.setWindowTitle("Unsaved Changes")
            msg.setText("<b>You have unsaved changes.</b>")
            msg.setInformativeText("Do you want to save before closing?")
            msg.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Save)

            result = msg.exec()

            if result == QMessageBox.Save:
                self.save_project()
                event.accept()
            elif result == QMessageBox.Discard:
                event.accept()
            elif result == QMessageBox.Cancel:
                event.ignore() # Cancels the close
        else:
            event.accept()

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

        if hasattr(self.ui_builder, "add_cutout_btn"):
            self.ui_builder.add_cutout_btn.clicked.connect(self.rebuild_geometry)

        if hasattr(self.ui_builder, "port_guide_btn"):
            self.ui_builder.port_guide_btn.clicked.connect(self.show_port_guide)

        self.ui_builder.rebuild_callback = self.rebuild_geometry

    def set_state(self, new_state: AppState):
        if self._state == new_state:
            return

        self._state = new_state
        self._update_ui_for_state()

        self.print_to_console(f"State of the app was just changed to {str(new_state).lstrip('AppState.')} ({new_state})!", "state_change")

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

    def print_to_console(self, message="No message was provided!", type="info", show_tag=True):
        from termcolor import colored
        from datetime import datetime

        colors = {
            "info": "blue",
            "warning": "yellow",
            "error": "red",
            "success": "green",
            "silenced": "dark_grey",
            "state_change": "magenta",
            "model_update": "cyan",
            "startup": "white"
        }

        color = colors.get(type, "white")

        if type == "startup":
            show_tag = False

        tag = f"\033[1m[{type.replace('_', ' ').upper()}]\033[0m " if show_tag else ""

        print(colored(f"{tag}{message}", color))

        gui_colors = {
            "info": "#3498db",
            "warning": "#f1c40f",
            "error": "#e74c3c",
            "success": "#2ecc71",
            "silenced": "#555555",
            "state_change": "#ff00ff",
            "model_update": "#00ffff",
            "startup": "#ffffff"
        }

        selected_color = gui_colors.get(type, "#ffffff")

        timestamp = datetime.now().astimezone().strftime("%H:%M:%S")

        safe_message = message.replace("\n", "<br>")

        if show_tag:
            prefix = f"[{timestamp}] <b>[{type.upper()}]</b> "
        else:
            prefix = ""

        formatted_msg = f"<span style='color:{selected_color};'>{prefix}</span>{safe_message}"

        self.ui.consoleOutput.appendHtml(formatted_msg)
        self.ui.consoleOutput.ensureCursorVisible()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = BoxCAD(project_path=None)
    window.showMaximized()
    sys.exit(app.exec())
