# Pyright false positive due to dynamic PySide attributes
# pyright: reportAttributeAccessIssue=false

from qtpy.QtWidgets import (
    QCheckBox, QComboBox, QDialog, QDoubleSpinBox, QSpinBox, QFormLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel, QMessageBox,
    QPlainTextEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QToolBox,
    QVBoxLayout, QWidget
)

from qtpy.QtCore import Qt
from qtpy.QtGui import QFont, QCursor

class PortGuideDialog(QDialog):
    def __init__(self, parent=None, fill_callback=None):
        super().__init__(parent)
        self.fill_callback = fill_callback  # ✅ store the callback
        self.setWindowTitle("Port Reference Guide")
        self.setMinimumSize(450, 500)

        layout = QVBoxLayout(self)

        header = QLabel("<h3>Global Port Reference</h3>")
        subtitle = QLabel("Click [Fill] to apply dimensions to the cutout spinboxes.\nRemember: Filling in the dimensions will replace the current values - this CANNOT be undone!")
        subtitle.setStyleSheet("color: #888888; font-size: 11px; margin-bottom: 10px;")
        layout.addWidget(header)
        layout.addWidget(subtitle)

        self.table = QTableWidget(14, 3)
        self.table.setHorizontalHeaderLabels(["Port Type", "Width (X)", "Height (Y)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        ports = [
            ("USB Type-C / 4.0", 8.4, 2.6),
            ("USB 2.0 Standard-A", 12.0, 4.5),
            ("USB 3.0 Standard-A", 12.0, 4.5),
            ("USB Micro-B", 6.85, 1.8),
            ("HDMI (Standard)", 15.0, 6.0),
            ("DisplayPort", 19.0, 10.0),
            ("Ethernet (RJ45)", 16.0, 14.0),
            ("SD Card Slot", 24.0, 2.1),
            ("Micro SD Slot", 15.0, 2.0),
            ("3.5mm Audio Jack", 6.0, 6.0),
            ("DC Jack (Typical)", 11.0, 11.0),
            ("IEC C14 (Power)", 27.5, 20.0),
            ("DB9 (Serial)", 31.0, 13.0),
            ("VGA (Old)", 31.0, 13.0)
        ]

        for row, (name, w, h) in enumerate(ports):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self._add_fill_cell(row, 1, w)
            self._add_fill_cell(row, 2, h)

            # Add a Fill Row button in the second column that fills both width and height
            self._add_fill_row_btn(row, w, h)

        layout.addWidget(self.table)

        footer = QLabel("<i>Last Updated: 26th of March 2026</i>")
        footer.setStyleSheet("font-size: 12px; color: #bbbbbb;")

        layout.addWidget(footer)

    def _add_fill_cell(self, row, col, value):
        container = QWidget()
        cell_layout = QHBoxLayout(container)
        cell_layout.setContentsMargins(2, 2, 2, 2)

        label = QLabel(f"{value} mm")
        cell_layout.addWidget(label)

        self.table.setCellWidget(row, col, container)

    def _add_fill_row_btn(self, row, w, h):
        """Replaces the second column with a label and the fill button."""
        container = QWidget()
        cell_layout = QHBoxLayout(container)
        cell_layout.setContentsMargins(2, 2, 2, 2)

        label = QLabel(f"{h}mm")
        btn = QPushButton("Fill")
        btn.setFixedSize(36, 20)
        btn.setToolTip(f"Fill width={w}, height={h} into cutout fields")
        btn.setStyleSheet("font-size: 10px; background-color: #1a6b3a; color: white; border: none; border-radius: 3px;")
        btn.setCursor(QCursor(Qt.PointingHandCursor))

        btn.clicked.connect(lambda: self._fill(w, h))

        cell_layout.addWidget(label)
        cell_layout.addStretch()
        cell_layout.addWidget(btn)

        self.table.setCellWidget(row, 2, container)

    def _fill(self, w, h):
        if self.fill_callback:
            self.fill_callback(w, h)

        self.accept() # Close the dialog after filling

class BuildUI:
    def __init__(self):
        super().__init__()

        # Define the rebuild callback to call later
        self.rebuild_callback = None

        # Dictionaries to store references to widgets and cutouts for easy access later
        self.widgets = {}
        self.cutouts = []

        # Bool to describe if the project is initialized yet
        self.project_initialized = False

    def create_form_page(self):
        """Creates a page with the specific layout constraints requested."""
        page = QWidget()
        layout = QFormLayout(page)

        # User defined constraints
        layout.setObjectName("formLayout")
        layout.setContentsMargins(12, 10, 12, 12)
        layout.setHorizontalSpacing(7)
        layout.setVerticalSpacing(10)
        layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        return page, layout

    # TODO: Add explainer tooltips to all parameters
    # TODO: Add comments above each parameter to explain what the parameter does

    def build_welcome_page(self, viewer):
        """Creates the landing page for the toolbox."""
        page = QWidget()

        # Configure the layout of the page
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        explainer = QLabel(
            "<h1><b>Welcome to BoxCAD!</b></h1><hr>"
            "BoxCAD is a high-fidelity parametric engine designed to bridge the critical gap between internal electronic component architectures and their external physical protection, utilizing logic-driven geometry to automate the path from circuit design to precision-engineered chassis.<hr>"
            "To open an existing project, first initialize the engine (with button below), then press <b>CTRL + O</b> or head up to <b>File > Open Project</b><hr>"
            "To begin your design, click the button below!<br><br>"
            "<i>This will unlock all editing tools</i>"
        )

        self.performance_warning = QLabel(
            "<b>Note:</b> Initializing the 3D engine and updating the screen to show the loading screen may take a few moments depending on your hardware specifications."
        )

        footer = QLabel(
            "<div style='width:100%; text-align: center;'>"
                "<span style='font-size: 12px; font-weight: bold; color: #737373;'>"
                    "HACKCLUB"
                    "<span style='color: transparent;'>.</span>"
                    "<span style='font-size: 8px;'>ORG.</span> "
                    "<span style='color: transparent;'>-</span>" # Invisible spacer
                    "<span style='color: #ec3750;'>X</span> "
                    "<span style='color: transparent;'>-</span>" # Invisible spacer
                    "FLAVORTOWN"
                "</span><br>"
                "<span style='font-size: 11px; color: #9c9c9c;'>"
                    "Made with <span style='color: #ec3750;'>❤️</span> in Slovenia"
                "</span>"
            "</div>"
        )

        # Style and configure the explainer text
        explainer.setStyleSheet("color: #777777; font-size: 13px;")
        explainer.setWordWrap(True)
        explainer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        viewer_page = viewer.browser.page()
        js_reveal_command = "if (window.revealViewer) window.revealViewer();"

        # Create and configure the initialize project button
        self.initialize_btn = QPushButton("Initialize Project")
        self.initialize_btn.setEnabled(False)
        self.initialize_btn.setToolTip("Waiting for 3D viewer to load...")
        self.initialize_btn.setMinimumHeight(40)
        self.initialize_btn.clicked.connect(lambda: viewer_page.runJavaScript(js_reveal_command))

        self.performance_warning.setWordWrap(True)
        self.performance_warning.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Using a distinct "Warning Orange" color
        self.performance_warning.setStyleSheet("color: #E68A00; font-size: 11px; margin-top: 5px;")

        # Add to layout
        layout.addWidget(explainer)             # Welcome text
        layout.addWidget(self.initialize_btn)   # The button
        layout.addWidget(self.performance_warning) # The warning label
        layout.addStretch(1)                    # Pushes everything below it to the bottom
        layout.addWidget(footer)                # Footer

        return page

    def build_dimensions_page(self):
        page, layout = self.create_form_page()

        # Width
        self.width_input = QDoubleSpinBox()
        self.width_input.setRange(20, 400)
        self.width_input.setValue(50)
        self.width_input.setSuffix(" mm")
        self.width_input.setToolTip("The outer width of the enclosure")

        layout.addRow("Outer Width (X):", self.width_input)
        self.widgets["outer_width"] = self.width_input

        # Length
        self.length_input = QDoubleSpinBox()
        self.length_input.setRange(20, 400)
        self.length_input.setValue(50)
        self.length_input.setSuffix(" mm")
        self.length_input.setToolTip("The outer length of the enclosure")

        layout.addRow("Outer Length (Y):", self.length_input)
        self.widgets["outer_length"] = self.length_input

        # Height
        self.height_input = QDoubleSpinBox()
        self.height_input.setRange(15, 400)
        self.height_input.setValue(25)
        self.height_input.setSuffix(" mm")
        self.height_input.setToolTip("The outer height of the enclosure")

        layout.addRow("Outer Height (Z):", self.height_input)
        self.widgets["outer_height"] = self.height_input

        self.wall_thickness_input = QDoubleSpinBox()
        self.wall_thickness_input.setMinimum(1)
        self.wall_thickness_input.setSuffix(" mm")
        self.wall_thickness_input.setToolTip("The wall thickness of the enclosure")

        layout.addRow("Wall Thickness:", self.wall_thickness_input)
        self.widgets["wall_thickness"] = self.wall_thickness_input

        self.corner_radius_input = QDoubleSpinBox()
        self.corner_radius_input.setSuffix(" mm")
        self.corner_radius_input.setToolTip("Rounds the corners of the enclosure")

        layout.addRow("Corner Radius:", self.corner_radius_input)
        self.widgets["corner_radius"] = self.corner_radius_input

        self.edge_rounding_input = QDoubleSpinBox()
        self.edge_rounding_input.setSuffix(" mm")
        self.edge_rounding_input.setToolTip("Rounds the edges of the enclosure")

        layout.addRow("Edge Rounding:", self.edge_rounding_input)
        self.widgets["edge_rounding"] = self.edge_rounding_input

        # Define the lid roof thickness
        self.lid_roof_thickness = 2.0
        self.widgets["lid_roof_thickness"] = self.lid_roof_thickness

        self.add_vertical_spacer(layout)

        return page

    def update_min_max_values(self):
        w = self.width_input.value()
        l = self.length_input.value()
        h = self.height_input.value()

        t = self.wall_thickness_input.value()

        i_d = self.screwpost_inner_diameter_input.value()

        absoulte_min_dimensions = min(w, l, h)
        max_wall_thickness = (absoulte_min_dimensions / 2.0) - 1.0
        self.wall_thickness_input.setRange(0.5, max(0.5, max_wall_thickness))

        max_side_radius = (min(w, l) / 2.0) - 0.1
        self.corner_radius_input.setMaximum(max(0.0, max_side_radius))

        max_inset = (min(w, l) / 2.0) - 2.0
        self.screwpost_inset_input.setMaximum(max(1.0, max_inset))

        max_bore_depth = self.lid_roof_thickness
        self.bore_depth_input.setMaximum(max(0, max_bore_depth))

        max_edge_round = (h / 2.0) - 0.5
        self.edge_rounding_input.setMaximum(max(0, max_edge_round))

        if self.hole_type.currentText() == "None (no modifications)":
            self.bore_diameter_input.setDisabled(True)
            self.bore_depth_input.setDisabled(True)
            self.countersink_diameter_input.setDisabled(True)
            self.countersink_angle_input.setDisabled(True)
        elif self.hole_type.currentText() == "Counterbore":
            self.bore_diameter_input.setEnabled(True)
            self.bore_depth_input.setEnabled(True)
            self.countersink_diameter_input.setDisabled(True)
            self.countersink_angle_input.setDisabled(True)
        elif self.hole_type.currentText() == "Countersink":
            self.countersink_diameter_input.setEnabled(True)
            self.countersink_angle_input.setEnabled(True)
            self.bore_diameter_input.setDisabled(True)
            self.bore_depth_input.setDisabled(True)

        self.countersink_diameter_input.setMinimum(i_d + 1)

    def build_assembly_page(self):
        page, layout = self.create_form_page()

        self.lid_connection_type = QComboBox()
        self.lid_connection_type.addItems(["Simple (no lip)", "Lip"])
        self.lid_connection_type.setToolTip("Choose which connection type should be used to (None, Counterbore, Countersink)")

        layout.addRow("Lid Connection Type:", self.lid_connection_type)
        self.widgets["lid_connection_type"] = self.lid_connection_type

        # Lid
        invert_lid_checkbox = QCheckBox()
        invert_lid_checkbox.setToolTip("Inverts the lid (useful for 3D printing)")

        layout.addRow("Invert Lid (for 3D printing):", invert_lid_checkbox)
        self.widgets["invert_lid"] = invert_lid_checkbox

        self.lip_height_input = QDoubleSpinBox()
        self.lip_height_input.setRange(5, 200)
        self.lip_height_input.setSuffix(" mm")
        self.lip_height_input.setToolTip("The lip height of the lid")

        layout.addRow("Lip Height:", self.lip_height_input)
        self.widgets["lip_height"] = self.lip_height_input

        self.screwpost_inset_input = QDoubleSpinBox()
        self.screwpost_inset_input.setRange(1, 50)
        self.screwpost_inset_input.setValue(5)
        self.screwpost_inset_input.setSuffix(" mm")
        self.screwpost_inset_input.setToolTip("The inset of the screwposts (relative to the inner wall)")

        layout.addRow("Screwpost Inset:", self.screwpost_inset_input)
        self.widgets["screwpost_inset"] = self.screwpost_inset_input

        self.screwpost_outer_diameter_input = QDoubleSpinBox()
        self.screwpost_outer_diameter_input.setRange(5, 200)
        self.screwpost_outer_diameter_input.setSuffix(" mm")
        self.screwpost_outer_diameter_input.setToolTip("The outer diameter of the screwposts")

        layout.addRow("Screwpost Outer Diameter:", self.screwpost_outer_diameter_input)
        self.widgets["screwpost_outer_diameter"] = self.screwpost_outer_diameter_input

        self.screwpost_inner_diameter_input = QDoubleSpinBox()
        self.screwpost_inner_diameter_input.setRange(1, 10)
        self.screwpost_inner_diameter_input.setValue(3) # Default to M3 screws (3mm)
        self.screwpost_inner_diameter_input.setSuffix(" mm")
        self.screwpost_inner_diameter_input.setToolTip("The inner diameter of the screwposts")

        layout.addRow("Screwpost Inner Diameter:", self.screwpost_inner_diameter_input)
        self.widgets["screwpost_inner_diameter"] = self.screwpost_inner_diameter_input

        self.add_vertical_spacer(layout)

        return page

    def build_bore_countersink_page(self):
        page, layout = self.create_form_page()

        # Bore
        self.hole_type = QComboBox()
        self.hole_type.addItems(["None (no modifications)", "Counterbore", "Countersink"])
        self.hole_type.setToolTip("Choose which modification to apply to the screwhole (None, Counterbore, Countersink)")

        layout.addRow("Hole type:", self.hole_type)
        self.widgets["hole_type"] = self.hole_type

        self.bore_diameter_input = QDoubleSpinBox()
        self.bore_diameter_input.setRange(0, 200)
        self.bore_diameter_input.setSuffix(" mm")
        self.bore_diameter_input.setDisabled(True)
        self.bore_diameter_input.setToolTip("The diameter of the bore, if using counterbore")

        layout.addRow("Bore Diameter:", self.bore_diameter_input)
        self.widgets["bore_diameter"] = self.bore_diameter_input

        self.bore_depth_input = QDoubleSpinBox()
        self.bore_depth_input.setRange(0, 200)
        self.bore_depth_input.setSuffix(" mm")
        self.bore_depth_input.setDisabled(True)

        layout.addRow("Bore Depth:", self.bore_depth_input)
        self.widgets["bore_depth"] = self.bore_depth_input

        self.countersink_diameter_input = QDoubleSpinBox()
        self.countersink_diameter_input.setMaximum(200)
        self.countersink_diameter_input.setValue(self.screwpost_inner_diameter_input.value() + 1)
        self.countersink_diameter_input.setSuffix(" mm")
        self.countersink_diameter_input.setDisabled(True)

        layout.addRow("Countersink Diameter:", self.countersink_diameter_input)
        self.widgets["countersink_diameter"] = self.countersink_diameter_input

        self.countersink_angle_input = QDoubleSpinBox()
        self.countersink_angle_input.setRange(60, 90)
        self.countersink_angle_input.setValue(90)
        self.countersink_angle_input.setSuffix(" °")
        self.countersink_angle_input.setDisabled(True)

        layout.addRow("Countersink Angle:", self.countersink_angle_input)
        self.widgets["countersink_angle"] = self.countersink_angle_input

        self.add_vertical_spacer(layout)

        return page

    def build_hardware_page(self):
        page, layout = self.create_form_page()

        pcb_screwposts_outer_diameter_input = QDoubleSpinBox()
        pcb_screwposts_outer_diameter_input.setRange(1, 20)
        pcb_screwposts_outer_diameter_input.setValue(5)
        pcb_screwposts_outer_diameter_input.setSuffix(" mm")

        layout.addRow("PCB Screwposts Outer Diameter:", pcb_screwposts_outer_diameter_input)
        self.widgets["pcb_screwposts_outer_diameter"] = pcb_screwposts_outer_diameter_input

        pcb_screwposts_inner_diameter_input = QDoubleSpinBox()
        pcb_screwposts_inner_diameter_input.setRange(1, 20)
        pcb_screwposts_inner_diameter_input.setValue(3)
        pcb_screwposts_inner_diameter_input.setSuffix(" mm")

        layout.addRow("PCB Screwposts Inner Diameter:", pcb_screwposts_inner_diameter_input)
        self.widgets["pcb_screwposts_inner_diameter"] = pcb_screwposts_inner_diameter_input

        pcb_screwposts_height_input = QDoubleSpinBox()
        pcb_screwposts_height_input.setRange(1, 50)
        pcb_screwposts_height_input.setValue(5)
        pcb_screwposts_height_input.setSuffix(" mm")

        layout.addRow("PCB Screwposts Height:", pcb_screwposts_height_input)
        self.widgets["pcb_screwposts_height"] = pcb_screwposts_height_input

        # Define PCB screwposts location
        self.pcb_screwposts_coordinates_input = QPlainTextEdit()
        self.pcb_screwposts_coordinates_input.setMaximumHeight(150)
        self.pcb_screwposts_coordinates_input.setMaximumWidth(170)
        self.pcb_screwposts_coordinates_input.setPlaceholderText(
            "X, Y (one per line, in mm)\n\n"
            "Example:\n"
            "12.0, 15.5\n"
            "45, 10.05"
        )

        mono_font = QFont("Consolas", 10)
        mono_font.setStyleHint(QFont.Monospace) # Fallback to any monospace if Consolas is missing

        self.pcb_screwposts_coordinates_input.setFont(mono_font)

        layout.addRow("PCB Screwposts Coordinates:", self.pcb_screwposts_coordinates_input)
        self.widgets["pcb_screwposts_coordinates"] = self.pcb_screwposts_coordinates_input

        self.add_vertical_spacer(layout)

        return page

    def build_cutouts_page(self, guide_callback):
        page, layout = self.create_form_page()

        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 5) # Small bottom margin

        title_label = QLabel("<b>Configuration</b>")
        title_label.setStyleSheet("font-size: 13px; color: #555;")

        # Create the "?" button
        self.port_guide_btn = QPushButton("?")
        self.port_guide_btn.setFixedSize(22, 22)
        self.port_guide_btn.setToolTip("Show port size reference guide")
        self.port_guide_btn.setCursor(Qt.PointingHandCursor)
        self.port_guide_btn.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                border-radius: 11px;
                font-weight: bold;
                border: none;
            }

            QPushButton:hover {
                background-color: #1c2833;
            }
        """)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.port_guide_btn)

        # Add the header to the main page layout
        layout.addRow(header_widget)

        # The creator zone
        creator_box = QGroupBox("Add New Cutout")

        creator_layout = QFormLayout()

        self.cutout_face = QComboBox()
        self.cutout_face.addItems(["Left (-X)", "Right (+X)", "Front (-Y)", "Back (+Y)", "Bottom (-Z)", "Top (+Z)"])

        self.cutout_shape = QComboBox()
        self.cutout_shape.addItems(["Rectangle", "Circle"])

        self.cutout_width_input = QDoubleSpinBox()
        self.cutout_width_input.setRange(1, 200)
        self.cutout_width_input.setSuffix(" mm")

        self.cutout_height_input = QDoubleSpinBox()
        self.cutout_height_input.setRange(1, 200)
        self.cutout_height_input.setSuffix(" mm")

        self.cutout_diameter_input = QDoubleSpinBox()
        self.cutout_diameter_input.setRange(1, 200)
        self.cutout_diameter_input.setSuffix(" mm")

        self.cutout_x_input = QDoubleSpinBox()
        self.cutout_x_input.setMaximum(200)
        self.cutout_x_input.setSuffix(" mm")

        self.cutout_y_input = QDoubleSpinBox()
        self.cutout_y_input.setMaximum(200)
        self.cutout_y_input.setSuffix(" mm")

        # Add items to the creator form
        creator_layout.addRow("Target Face:", self.cutout_face)
        creator_layout.addRow("Shape:", self.cutout_shape)
        creator_layout.addRow("Width:", self.cutout_width_input)
        creator_layout.addRow("Height", self.cutout_height_input)
        creator_layout.addRow("Diameter (circle only)", self.cutout_diameter_input)
        creator_layout.addRow("Horizontal Offset:", self.cutout_x_input)
        creator_layout.addRow("Vertical Offset:", self.cutout_y_input)

        self.add_cutout_btn = QPushButton("Add Cutout to List")
        self.add_cutout_btn.clicked.connect(self.add_cutout)

        creator_layout.addRow(self.add_cutout_btn)

        creator_box.setLayout(creator_layout)

        layout.addRow(creator_box)

        # The manager zone
        layout.addRow(QLabel("Active Cutouts:"))

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(200)

        self.no_cutouts_label = QLabel("No Cutouts Active")

        self.no_cutouts_label.setStyleSheet("""
            QLabel {
                color: #777777;
                font-weight: bold;
                font-size: 13px;
                letter-spacing: 1px;
            }
        """)

        self.no_cutouts_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.no_cutouts_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_cutouts_label.setFixedHeight(100)
        self.no_cutouts_label.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.manager_container = QWidget()
        self.manager_layout = QVBoxLayout(self.manager_container)
        self.manager_layout.setAlignment(Qt.AlignTop) # Keeps items at the top
        self.scroll_area.setWidget(self.manager_container)

        self.manager_layout.addWidget(self.no_cutouts_label)

        layout.addRow(self.scroll_area)

        self.add_vertical_spacer(layout)

        return page

    def add_cutout(self):
        cutout = {
            "face": self.cutout_face.currentText(),
            "shape": self.cutout_shape.currentText(),
            "x": self.cutout_x_input.value(),
            "y": self.cutout_y_input.value(),
            "width": self.cutout_width_input.value(),
            "height": self.cutout_height_input.value(),
            "diameter": self.cutout_diameter_input.value()
        }

        self.cutouts.append(cutout)
        self._add_cutout_to_list(cutout)
        self.refresh_empty_state()

    def _add_cutout_to_list(self, cutout: dict):
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(4, 2, 4, 2)

        if cutout["shape"] == "Circle":
            label_text = f"Circle on {cutout["face"]} | ⌀{cutout['diameter']}mm @ ({cutout["x"]}, {cutout["y"]})"
        else:
            label_text = f"Rectangle on {cutout["face"]} | {cutout["width"]}x{cutout["height"]}mm @ ({cutout["x"]}, {cutout["y"]})"

        label = QLabel(label_text)
        label.setWordWrap(True)

        delete_btn = QPushButton("✕")
        delete_btn.setFixedWidth(30)
        delete_btn.setToolTip("Remove this cutout")

        def on_delete():
            msg = QMessageBox()
            msg.setWindowTitle("Remove Cutout")
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setText("Are you sure you want to remove this cutout?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)

            if msg.exec() == QMessageBox.Yes:
                self.cutouts.remove(cutout)
                self.manager_layout.removeWidget(row_widget)
                row_widget.deleteLater()
                self.refresh_empty_state()

                if self.rebuild_callback: self.rebuild_callback()

        delete_btn.clicked.connect(on_delete)

        row_layout.addWidget(label)
        row_layout.addWidget(delete_btn)

        self.manager_layout.addWidget(row_widget)

    def add_vertical_spacer(self, layout):
        """Helper to push widgets to the top of the form."""
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        layout.addItem(spacer)

    def populate_toolbox(self, toolbox: QToolBox, viewer, guide_callback):
        """Clears and rebuilds the toolbox pages."""
        self.print_to_console("Populating toolbox!", "info")

        toolbox.setMinimumWidth(300)

        page_0 = toolbox.widget(0)

        layout = page_0.layout()

        if layout is None:
            layout = QVBoxLayout(page_0)

        if not self.project_initialized:
            self.print_to_console("Project not initialized yet! Building welcome page...", "info")

            welcome_widget = self.build_welcome_page(viewer)

            toolbox.setMinimumWidth(300)

            layout.addWidget(welcome_widget)

            self.print_to_console("Welcome page built successfully!", "success")
        else:
            toolbox.setMinimumWidth(0)

            # Get the widget at index 0 (Getting Started category)
            old_widget = toolbox.widget(0)

            toolbox.removeItem(0) # Remove the Getting Started category from view

            # Delete from memory
            if old_widget:
                old_widget.deleteLater()

            toolbox.addItem(self.build_dimensions_page(), "Dimensions")
            toolbox.addItem(self.build_assembly_page(), "Lid && Screwposts")
            toolbox.addItem(self.build_bore_countersink_page(), "Counterbore && Countersink")
            toolbox.addItem(self.build_hardware_page(), "Internal Hardware")
            toolbox.addItem(self.build_cutouts_page(guide_callback), "Cutouts && Ports")

            for widget in self.widgets.values():
                if isinstance(widget, (QDoubleSpinBox, QSpinBox)):
                    widget.valueChanged.connect(self.update_min_max_values)
                elif isinstance(widget, QComboBox):
                    widget.currentIndexChanged.connect(self.update_min_max_values)

    def refresh_empty_state(self):
        item_count = self.manager_layout.count() - 1 # Subtract 1 because the label is part of the layout

        if item_count > 0:
            self.no_cutouts_label.hide()
        else:
            self.no_cutouts_label.show()

    def print_to_console(self, message = "No message was provided!", type = "info"):
        from termcolor import colored

        colors = {"info": "blue", "warning": "yellow", "error": "red", "success": "green", "silenced": "dark_grey", "state_change": "magenta"}

        color = colors.get(type, "white")

        print(colored(f"[{type.upper()}] {message}", color))
