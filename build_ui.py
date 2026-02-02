"""
FILE: build_ui.py

EXAMPLE USAGE:
To add a standard input row inside a build function:
    spin_box = QDoubleSpinBox()
    spin_box.setRange(0, 500)
    spin_box.setSuffix(" mm")
    layout.addRow("Label Name:", spin_box)
"""

from qtpy.QtWidgets import QWidget, QFormLayout, QLabel, QDoubleSpinBox, QPlainTextEdit, QSpacerItem, QSizePolicy, QToolBox, QComboBox
from qtpy.QtCore import Qt
from qtpy.QtGui import QFont

class BuildUI:
    def __init__(self):
        # Dictionary to store references to widgets for easy access later
        self.widgets = {}

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

        # Custom standoff location definer
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

        # --- FILL THIS OUT ---
        # Hint: Add Side selection and Dimension inputs

        self.add_vertical_spacer(layout)

        return page

    def add_vertical_spacer(self, layout):
        """Helper to push widgets to the top of the form."""
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding) # type: ignore

        layout.addItem(spacer)

    def populate_toolbox(self, toolbox: QToolBox):
        """Clears and rebuilds the toolbox pages."""

        while toolbox.count() > 0:
            toolbox.removeItem(0)

        toolbox.addItem(self.build_dimensions_page(), "Dimensions")
        toolbox.addItem(self.build_assembly_page(), "Lid && Joinery")
        toolbox.addItem(self.build_hardware_page(), "Internal Hardware")
        toolbox.addItem(self.build_cutouts_page(), "Cutouts && Ports")
