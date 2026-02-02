"""
FILE: build_ui.py

EXAMPLE USAGE:
To add a standard input row inside a build function:
    spin_box = QDoubleSpinBox()
    spin_box.setRange(0, 500)
    spin_box.setSuffix(" mm")
    layout.addRow("Label Name:", spin_box)
"""

from qtpy.QtWidgets import QWidget, QFormLayout, QLabel, QDoubleSpinBox, QPlainTextEdit, QSpacerItem, QSizePolicy, QToolBox
from qtpy.QtCore import Qt

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

        # --- FILL THIS OUT ---
        # Hint: Add Length, Width, Height, and Wall Thickness

        # Length
        length_input = QDoubleSpinBox()
        length_input.setRange(1, 1000)
        length_input.setSuffix(" mm")

        layout.addRow("Length (X):", length_input)
        self.widgets["length"] = length_input

        self.add_vertical_spacer(layout)

        return page

    def build_assembly_page(self):
        page, layout = self.create_form_page()

        # --- FILL THIS OUT ---
        # Hint: Add Lid Split Height and Joint Type

        self.add_vertical_spacer(layout)

        return page

    def build_hardware_page(self):

        page, layout = self.create_form_page()

        # --- FILL THIS OUT ---
        # Hint: Add the short explainer QLabel and the QPlainTextEdit

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
        toolbox.addItem(self.build_assembly_page(), "Lid & Joinery")
        toolbox.addItem(self.build_hardware_page(), "Internal Hardware")
        toolbox.addItem(self.build_cutouts_page(), "Cutouts & Ports")
