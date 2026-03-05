# Pyright false positive due to dynamic PySide attributes
# pyright: reportAttributeAccessIssue=false

from qtpy.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QDoubleSpinBox, QPlainTextEdit, QSpacerItem, QSizePolicy, QToolBox, QComboBox, QPushButton, QScrollArea, QGroupBox, QCheckBox
from qtpy.QtCore import Qt
from qtpy.QtGui import QFont
from ui.main_window_ui import Ui_MainWindow

class BuildUI:
    def __init__(self):
        super().__init__()

        # Dictionary to store references to widgets for easy access later
        self.widgets = {}

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
    # TODO: Update the background color of the checkboxes

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
            "To begin your design, click the button below!<br><br>"
            "<i>This will unlock all editing tools</i>"
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

        # Style and configure the footer text
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

        # Add to layout
        layout.addWidget(explainer)             # Welcome text
        layout.addWidget(self.initialize_btn)   # The button
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

        layout.addRow("Outer Width (X):", self.width_input)
        self.widgets["outer_width"] = self.width_input

        # Length
        self.length_input = QDoubleSpinBox()
        self.length_input.setRange(20, 400)
        self.length_input.setValue(50)
        self.length_input.setSuffix(" mm")

        layout.addRow("Outer Length (Y):", self.length_input)
        self.widgets["outer_length"] = self.length_input

        # Height
        self.height_input = QDoubleSpinBox()
        self.height_input.setRange(15, 400)
        self.height_input.setValue(25)
        self.height_input.setSuffix(" mm")

        layout.addRow("Outer Height (Z):", self.height_input)
        self.widgets["outer_height"] = self.height_input

        # Connect all dimension spin boxes to the update_min_max_values function
        self.width_input.valueChanged.connect(self.update_min_max_values)
        self.length_input.valueChanged.connect(self.update_min_max_values)
        self.height_input.valueChanged.connect(self.update_min_max_values)

        self.wall_thickness_input = QDoubleSpinBox()
        self.wall_thickness_input.setMinimum(1)
        self.wall_thickness_input.setSuffix(" mm")

        layout.addRow("Wall Thickness:", self.wall_thickness_input)
        self.widgets["wall_thickness"] = self.wall_thickness_input

        self.side_radius_input = QDoubleSpinBox()
        self.side_radius_input.setSuffix(" mm")

        layout.addRow("Side Radius:", self.side_radius_input)
        self.widgets["side_radius"] = self.side_radius_input

        self.edge_rounding_input = QDoubleSpinBox()
        self.edge_rounding_input.setSuffix(" mm")

        layout.addRow("Edge Rounding:", self.edge_rounding_input)
        self.widgets["edge_rounding"] = self.edge_rounding_input

        self.add_vertical_spacer(layout)

        return page

    # TODO:   Update:
    # TODO: -

    def update_min_max_values(self):
        w = self.width_input.value()
        l = self.length_input.value()
        h = self.height_input.value()

        absoulte_min_dimensions = min(w, l, h)
        max_wall_thickness = (absoulte_min_dimensions / 2.0) - 1.0
        self.wall_thickness_input.setRange(0.5, max(0.5, max_wall_thickness))

        max_side_radius = (min(w, l) / 2.0) - 0.1
        self.side_radius_input.setMaximum(max(0.0, max_side_radius))

        max_edge_round = (h / 2.0) - 0.1
        self.edge_rounding_input.setMaximum(max(0.0, max_edge_round))

        max_inset = (min(w, l) / 2.0) - 2.0
        self.screwpost_inset_input.setMaximum(max(1.0, max_inset))

    def build_assembly_page(self):
        page, layout = self.create_form_page()

        # Lid
        invert_lid_checkbox = QCheckBox()

        layout.addRow("Invert Lid (for 3D printing):", invert_lid_checkbox)
        self.widgets["invert_lid"] = invert_lid_checkbox

        lip_height_input = QDoubleSpinBox()
        lip_height_input.setRange(5, 200)
        lip_height_input.setSuffix(" mm")

        layout.addRow("Lip Height:", lip_height_input)
        self.widgets["lip_height"] = lip_height_input

        # Joint selection
        joint_type = QComboBox()
        joint_type.addItems(["Screwposts", "Butt Joint", "Lap Joint (Lip)"])
        # QComboBox Index:   ===== 0 ====  ===== 1 ====  ======= 2 =======

        layout.addRow("Joint type:", joint_type)
        self.widgets["joint_type"] = joint_type

        # TODO: Update the min/max value dyanmically
        self.screwpost_inset_input = QDoubleSpinBox()
        self.screwpost_inset_input.setRange(1, 50)
        self.screwpost_inset_input.setValue(5)
        self.screwpost_inset_input.setSuffix(" mm")

        layout.addRow("Screwpost Inset:", self.screwpost_inset_input)
        self.widgets["screwpost_inset"] = self.screwpost_inset_input

        # TODO: Update the min/max value dyanmically
        screwpost_inner_diameter_input = QDoubleSpinBox()
        screwpost_inner_diameter_input.setRange(1, 10)
        screwpost_inner_diameter_input.setValue(3) # Default to M3 screws (3mm)
        screwpost_inner_diameter_input.setSuffix(" mm")

        layout.addRow("Screwpost Inner Diameter:", screwpost_inner_diameter_input)
        self.widgets["screwpost_inner_diameter"] = screwpost_inner_diameter_input

        # TODO: Update the min/max value dyanmically
        screwpost_outer_diameter_input = QDoubleSpinBox()
        screwpost_outer_diameter_input.setRange(5, 200)
        screwpost_outer_diameter_input.setSuffix(" mm")

        layout.addRow("Screwpost Outer Diameter:", screwpost_outer_diameter_input)
        self.widgets["screwpost_outer_diameter"] = screwpost_outer_diameter_input

        self.add_vertical_spacer(layout)

        return page

    def build_bore_countersink_page(self):
        page, layout = self.create_form_page()

        # Bore
        bore_diameter_input = QDoubleSpinBox()
        bore_diameter_input.setRange(5, 200)
        bore_diameter_input.setSuffix(" mm")

        layout.addRow("Bore Diameter:", bore_diameter_input)
        self.widgets["bore_diameter"] = bore_diameter_input

        bore_depth_input = QDoubleSpinBox()
        bore_depth_input.setRange(5, 200)
        bore_depth_input.setSuffix(" mm")

        layout.addRow("Bore Depth:", bore_depth_input)
        self.widgets["bore_depth"] = bore_depth_input

        countersink_diameter_input = QDoubleSpinBox()
        countersink_diameter_input.setRange(5, 200)
        countersink_diameter_input.setSuffix(" mm")

        layout.addRow("Countersink Diameter:", countersink_diameter_input)
        self.widgets["countersink_diameter"] = countersink_diameter_input

        countersink_angle_input = QDoubleSpinBox()
        countersink_angle_input.setRange(60, 120)
        countersink_angle_input.setValue(90)
        countersink_angle_input.setSuffix(" °")

        layout.addRow("Countersink Angle:", countersink_angle_input)
        self.widgets["countersink_angle"] = countersink_angle_input

        self.add_vertical_spacer(layout)

        return page

    def build_hardware_page(self):
        page, layout = self.create_form_page()

        # Standoff Height
        standoff_height_input = QDoubleSpinBox()
        standoff_height_input.setRange(1, 50)
        standoff_height_input.setSuffix(" mm")

        layout.addRow("Standoff Height:", standoff_height_input)
        self.widgets["standoff_height"] = standoff_height_input

        # Standoff Diameter
        standoff_diameter_input = QDoubleSpinBox()
        standoff_diameter_input.setRange(1, 20)
        standoff_diameter_input.setValue(5)
        standoff_diameter_input.setSuffix(" mm")

        layout.addRow("Standoff Diameter:", standoff_diameter_input)
        self.widgets["standoff_diameter"] = standoff_diameter_input

        # Define PCB standoff location
        self.pcb_coordinates_input = QPlainTextEdit()
        self.pcb_coordinates_input.setMaximumHeight(150)
        self.pcb_coordinates_input.setMaximumWidth(170)
        self.pcb_coordinates_input.setPlaceholderText(
            "- X, Y (one per line)\n\n"
            "Example:\n"
            "- 12.0, 15.5\n"
            "- 45.0, 10.0"
        )

        mono_font = QFont("Consolas", 10)
        mono_font.setStyleHint(QFont.Monospace) # Fallback to any monospace if Consolas is missing

        self.pcb_coordinates_input.setFont(mono_font)

        layout.addRow("PCB Standoff Coordinates:", self.pcb_coordinates_input)
        self.widgets["pcb_standoff_coordinates"] = self.pcb_coordinates_input

        self.add_vertical_spacer(layout)

        return page

    def build_cutouts_page(self):
        page, layout = self.create_form_page()

        # The creator zone
        creator_box = QGroupBox("Add New Cutout")

        creator_layout = QFormLayout()

        self.cutout_face = QComboBox()
        self.cutout_face.addItems(["Left (-X)", "Right (+X)", "Front (-Y)", "Back (+Y)", "Bottom (-Z)", "Top (+Z)"])

        self.cutout_shape = QComboBox()
        self.cutout_shape.addItems(["Rectangle", "Circle"])

        self.cutout_x = QDoubleSpinBox()
        self.cutout_y = QDoubleSpinBox()

        # Add items to the creator form
        creator_layout.addRow("Target Face:", self.cutout_face)
        creator_layout.addRow("Shape:", self.cutout_shape)
        creator_layout.addRow("X:", self.cutout_x)
        creator_layout.addRow("Y:", self.cutout_y)

        self.add_cutout_btn = QPushButton("Add Cutout to List")
        # self.add_cutout_btn.clicked.connect(self.add_cutout_action)

        creator_layout.addRow(self.add_cutout_btn)

        creator_box.setLayout(creator_layout)

        layout.addRow(creator_box)

        # The manager zone
        layout.addRow(QLabel("Active Cutouts:"))

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(200)
        # self.scroll_area.setMaximumWidth(100)

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

    def add_vertical_spacer(self, layout):
        """Helper to push widgets to the top of the form."""
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        layout.addItem(spacer)

    def populate_toolbox(self, toolbox: QToolBox, viewer):
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
            toolbox.addItem(self.build_assembly_page(), "Lid && Joinery")
            toolbox.addItem(self.build_bore_countersink_page(), "Bore && Countersink")
            toolbox.addItem(self.build_hardware_page(), "Internal Hardware")
            toolbox.addItem(self.build_cutouts_page(), "Cutouts && Ports")

    def refresh_empty_state(self):
        item_count = self.manager_layout.count() - 1 # Subtract 1 because the label is part of the layout

        if item_count > 0:
            self.no_cutouts_label.hide()
        else:
            self.no_cutouts_label.show()

    def print_to_console(self, message = "No message was provided!", type = "info"):
        from termcolor import colored

        colors = {"info": "blue", "warning": "yellow", "error": "red", "success": "green", "silenced": "dark_grey"}

        color = colors.get(type, "white")

        print(colored(f"[{type.upper()}] {message}", color))
