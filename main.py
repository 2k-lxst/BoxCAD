import os
from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QListWidgetItem,
    QWidget,
    QVBoxLayout,
    QLabel
)
from qtpy.QtGui import QIcon, QFont
from qtpy.QtCore import Qt, QSize
from qtpy.uic import loadUi
import json
from datetime import datetime, timezone
import ui.resources_rc

# Global app settings
app_name = "BoxCAD"
version_number = "0.0.1"

# App theme
PRIMARY_COLOR = "#5A8DEE"
PRIMARY_HOVER = "#6EA0FF"
BACKGROUND_COLOR = "#1E1E1E"
SURFACE_COLOR = "#252526"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "rgba(255, 255, 255, 0.55)"

print("The program is running.")
print(f"Welcome to {app_name} v{version_number}")

# TODO: Update the recent files list by calling self.update_recent_files when saving a newly-created file

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.set_taskbar_icon()

        # Compile all paths
        # This approach works regardless of where you run the script
        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, "assets", "icon.ico")
        ui_path = os.path.join(script_dir, "ui", "StartupUI.ui")

        self.ui = loadUi(ui_path, self)

        self.ui.btn_create_project.clicked.connect(self.create_new_project)
        self.ui.btn_hardware_library.clicked.connect(self.hardware_library)
        self.ui.btn_tutorials.clicked.connect(self.open_tutorials)

        # self.ui.recent_projects_list.setFocusPolicy(Qt.NoFocus) # type: ignore

        # Set the window's title and icon
        self.setWindowTitle(app_name + " v0.0.1")
        self.setWindowIcon(QIcon(icon_path))

        self.populate_recent_projects_list()

    def set_taskbar_icon(self):
        # This tells Windows to treat this as a unique app otherwise it might show the default Python icon in the taskbar
        if os.name == "nt":
            import ctypes

            myappid = f"2klxst.{app_name}.{app_name}.{version_number}"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # TODO: Finish the create new project functionality
    def create_new_project(self):
        print("'Create new project' button was clicked!")
        print("Switching to Workspace...")

        # self.ui.stackedWidget.setCurrentIndex(1)

    # TODO: Finish the open tutorials functionality
    def open_tutorials(self):
        import webbrowser

        print("'Open tutorials' button was clicked!")
        print("Opening tutorials in default browser...")

        webbrowser.open("https://hackclub.com")

    # TODO: Finish the hardware library functionality
    def hardware_library(self):
        print("'Hardware library' button was clicked!")
        print("Switching to Workspace...")

        # self.ui.stackedWidget.setCurrentIndex(1)

    # TODO: Finish the load recent functionality
    def load_recent(self, item):
        print("A recent project from the list was clicked!")
        print(f"Loading: {item.text()}")
        print("Switching to Workspace...")

        # self.ui.stackedWidget.setCurrentIndex(1)

    def load_recent_files(self):
        # Load the recentFiles.json file safely
        if not os.path.exists("recentFiles.json"):
            print("The recentFiles.json doesn't exist in the same directory as the script!")

            return []

        try:
            with open("recentFiles.json", "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("The recentFiles.json file is corrupted!")

            return []

    def sort_by_latest(self, data):
        return sorted(
            data,
            key=lambda item: datetime.fromisoformat(
                item["lastOpened"].replace("Z", "+00:00") # Fixes the Python parser
            ),
            reverse=True # Newest entries at the top
        )

    def keep_top_five(self, data):
        return data[:5]

    def save_recent_files(self, data):
        with open("recentFiles.json", "w") as file:
            json.dump(data, file, indent=4) # Dump the new data into recentFiles.json

    def update_recent_files(self, file_path):
        data = self.load_recent_files()

        # Remove existing entry with the same path
        data = [item for item in data if item["filePath"] != file_path]

        # Extract filename info
        file_name = os.path.basename(file_path)
        file_name_no_ext = os.path.splitext(file_path)[0]

        # Add updated entry
        data.append({
            "fileName": file_name,
            "fileNameNoExt": file_name_no_ext,
            "filePath": file_path,
            "lastOpened": datetime.now(timezone.utc).isoformat() + "Z"
        })

        # Sort and trim
        data = self.sort_by_latest(data)
        data = self.keep_top_five(data)

        # Save
        self.save_recent_files(data)

    def populate_recent_projects_list(self):
        self.ui.recent_projects_list.clear()

        data = self.load_recent_files()
        data = self.sort_by_latest(data)

        for item in data:
            list_item = QListWidgetItem()
            list_item.setSizeHint(QSize(0, 50)) # Controls row height

            widget = QWidget()
            layout = QVBoxLayout(widget)
            layout.setContentsMargins(8, 4, 8, 4)
            layout.setSpacing(2)

            # File name (big and bold)
            name_label = QLabel(str.capitalize(item["fileNameNoExt"]))

            name_font = QFont()
            name_font.setPointSize(10)
            name_font.setBold(True)

            name_label.setFont(name_font)

            # File path (small, gray and muted)
            path_label = QLabel(item["filePath"])

            path_font = QFont()
            path_font.setPointSize(8)

            path_label.setFont(path_font)

            layout.addWidget(name_label)
            layout.addWidget(path_label)

            widget.setLayout(layout)

            # Store file path in the item (IMPORTANT!)
            list_item.setData(Qt.UserRole, item["filePath"]) # type: ignore

            self.ui.recent_projects_list.addItem(list_item)
            self.ui.recent_projects_list.setItemWidget(list_item, widget)

app = QApplication()

# Apply the global theme to the app
app.setStyleSheet(f"""
QPushButton {{
    background-color: {PRIMARY_COLOR};
    border: none;
    border-radius: 6px;
    padding: 6px 12px;
}}

QPushButton:hover {{
    background-color: {PRIMARY_HOVER};
}}

QPushButton:pressed {{
    background-color: {PRIMARY_COLOR};
}}

QWidget:focus {{
    border: 1px solid {PRIMARY_COLOR};
}}
""")

winddow = MainWindow()
winddow.show()

app.exec()
