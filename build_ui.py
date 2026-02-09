"""
FILE: build_ui.py

EXAMPLE USAGE:
To add a standard input row inside a build function:
    spin_box = QDoubleSpinBox()
    spin_box.setRange(0, 500)
    spin_box.setSuffix(" mm")
    layout.addRow("Label Name:", spin_box)
"""

from qtpy.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QDoubleSpinBox, QPlainTextEdit, QSpacerItem, QSizePolicy, QToolBox, QComboBox, QPushButton, QScrollArea, QGroupBox
from qtpy.QtCore import Qt
from qtpy.QtGui import QFont

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
        layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow) # type: ignore

        return page, layout

    def build_welcome_page(self):
        """Creates the landing page for the toolbox."""
        page = QWidget()

        # Configure the layout of the page
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        explainer = QLabel(
            "<h1><b>Welcome to BoxCAD!</b></h1><hr>"
            "BoxCAD is a high-fidelity parametric engine designed to bridge the critical gap between internal electronic component architectures and their external physical protection, utilizing logic-driven geometry to automate the path from circuit design to precision-engineered chassis."
            "<h3>To begin your design:</h3>"
            "<ul>"
                "<li>Set your base dimensions</li>"
                "<li>Click the button below to initialize the project</li>"
            "</ul>"
            "<i>This will unlock all editing tools</i>"
        )

        # Style and configure the explainer text
        explainer.setStyleSheet("color: #777777; font-size: 13px;")
        explainer.setWordWrap(True)
        explainer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create and style the initialize project button
        self.initialize_btn = QPushButton("Initialize Project")
        self.initialize_btn.setMinimumHeight(40)

        # Add to layout
        layout.addWidget(explainer)
        layout.addWidget(self.initialize_btn)
        layout.addStretch()

        return page

    def build_dimensions_page(self):
        page, layout = self.create_form_page()

        # Length
        length_input = QDoubleSpinBox()
        length_input.setRange(1, 1000)
        length_input.setSuffix(" mm")

        layout.addRow("Length (X):", length_input)
        self.widgets["length"] = length_input

        # Width
        width_input = QDoubleSpinBox()
        width_input.setRange(1, 1000)
        width_input.setSuffix(" mm")

        layout.addRow("Width (Y):", width_input)
        self.widgets["width"] = width_input

        # Height
        height_input = QDoubleSpinBox()
        height_input.setRange(1, 1000)
        height_input.setSuffix(" mm")

        layout.addRow("Height (Z):", height_input)
        self.widgets["height"] = height_input

        # Wall Thickness
        wall_thickness_input = QDoubleSpinBox()
        wall_thickness_input.setRange(1, 1000)
        wall_thickness_input.setSuffix(" mm")

        layout.addRow("Wall Thickness:", wall_thickness_input)
        self.widgets["wall_thickness"] = wall_thickness_input

        self.add_vertical_spacer(layout)

        return page

    def build_assembly_page(self):
        page, layout = self.create_form_page()

        # Lid
        lid_height_input = QDoubleSpinBox()
        lid_height_input.setRange(5, 200)
        lid_height_input.setSuffix(" mm")

        layout.addRow("Lid Height:", lid_height_input)
        self.widgets["lid_height"] = lid_height_input

        # Joint selection
        joint_type = QComboBox()
        joint_type.addItems(["Butt Joint", "Lap Joint (Lip)"])

        layout.addRow("Joint type:", joint_type)
        self.widgets["joint_type"] = joint_type

        # Fasteners
        screw_diameter = QDoubleSpinBox()
        screw_diameter.setRange(0, 10)
        screw_diameter.setSingleStep(0.5)
        screw_diameter.setValue(3.0) # Default to M3
        screw_diameter.setSuffix(" mm")

        layout.addRow("Screw Diameter:", screw_diameter)
        self.widgets["screw_diameter"] = screw_diameter

        self.add_vertical_spacer(layout)

        return page

    def build_hardware_page(self):
        page, layout = self.create_form_page()

        # --- FILL THIS OUT ---
        # Hint: Add the short explainer QLabel and the QPlainTextEdit

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
        mono_font.setStyleHint(QFont.Monospace) # Fallback to any monospace if Consolas is missing # type: ignore

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
        self.manager_layout.setAlignment(Qt.AlignTop) # Keeps items at the top # type: ignore
        self.scroll_area.setWidget(self.manager_container)

        self.manager_layout.addWidget(self.no_cutouts_label)

        layout.addRow(self.scroll_area)

        self.add_vertical_spacer(layout)

        return page

    def add_vertical_spacer(self, layout):
        """Helper to push widgets to the top of the form."""
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding) # type: ignore

        layout.addItem(spacer)

    def populate_toolbox(self, toolbox: QToolBox):
        """Clears and rebuilds the toolbox pages."""
        self.print_to_console("Populating toolbox!", "info")

        toolbox.setMinimumWidth(300)

        page_0 = toolbox.widget(0)

        layout = page_0.layout()

        if layout is None:
            layout = QVBoxLayout(page_0)

        if not self.project_initialized:
            self.print_to_console("Project not initialized yet! Building welcome page...", "info")

            welcome_widget = self.build_welcome_page()

            toolbox.setMinimumWidth(300)

            layout.addWidget(welcome_widget)

            self.print_to_console("Welcome page was built successfully!", "success")
        else:
            toolbox.setMinimumWidth(0)

            toolbox.addItem(self.build_dimensions_page(), "Dimensions")
            toolbox.addItem(self.build_assembly_page(), "Lid && Joinery")
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
