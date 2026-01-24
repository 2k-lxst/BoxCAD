import os
import sys
import platform
from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QListWidgetItem,
    QWidget,
    QVBoxLayout,
    QLabel
)
from qtpy.QtGui import QIcon, QFont
from qtpy.QtCore import Qt, QSize, QStandardPaths
from qtpy.uic import loadUi
import json
from datetime import datetime, timezone

# Global app settings
app_name = "BoxCAD"
app_version_number = "0.0.1"
app_style = "Fusion"

print("The program is running.")
print(f"Welcome to {app_name} v{app_version_number}!\n")
print(
    "Information:\n"
    "============\n"
    f"{app_name} v{app_version_number}\n"
    f"Python: {sys.version.split()[0]} ({platform.python_implementation()})\n"
    f"Executable: {sys.executable}\n"
    f"OS: {platform.system()} {platform.release()} ({platform.machine()})\n"
)

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path) # type: ignore

    return os.path.join(os.path.abspath("."), relative_path)

# TODO: Update the recent files list by calling self.update_recent_files when user saves a newly-created file

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.set_taskbar_icon()

        # Compile all paths
        # This approach works regardless of where you run the script
        self.recent_file_path = recent_file_path = os.path.join(data_dir, "recentFiles.json")

        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, "assets", "icon.ico")
        welcome_screen_ui_path = os.path.join(script_dir, "ui", "welcome_screen.ui")
        main_window_ui_path = os.path.join(script_dir, "ui", "main_window.ui")
        welcome_screen_ui_path = resource_path("ui/welcome_screen.ui")
        main_window_ui_path = resource_path("ui/main_window.ui")

        self.ui = loadUi(welcome_screen_ui_path, self)

        self.ui.btnCreateProject.clicked.connect(self.create_new_project)
        self.ui.btnHardwareLibrary.clicked.connect(self.hardware_library)
        self.ui.btnTutorials.clicked.connect(self.open_tutorials)
        self.ui.btnExit.clicked.connect(QApplication.quit)

        self.ui.recentProjectsList.itemClicked.connect(self.load_recent)

        # Set the window's title and icon
        self.setWindowTitle(f"{app_name} v{app_version_number}")
        self.setWindowIcon(QIcon(icon_path))

        self.populate_recent_projects_list()

    def set_taskbar_icon(self):
        # This tells Windows to treat this as a unique app otherwise it might show the default Python icon in the taskbar
        if os.name == "nt":
            import ctypes

            myappid = f"2klxst.{app_name}.{app_name}.{app_version_number}"
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
        print(f"Loading: {item.data(Qt.UserRole + 1)}") # Get the item's display name             # type: ignore
        print("Switching to Workspace...")

        # self.ui.stackedWidget.setCurrentIndex(1)

    def load_recent_files(self):
        # Load the recentFiles.json file safely. If it doesn't exist, create it.
        if not os.path.exists(self.recent_file_path):
            with open(self.recent_file_path, "w") as file:
                json.dump([], file)

            print("The recentFiles.json doesn't exist. It was created automatically.")

            return []

        try:
            with open(self.recent_file_path, "r") as file:
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
        with open(self.recent_file_path, "w") as file:
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
        self.ui.recentProjectsList.clear()

        data = self.load_recent_files()
        data = self.sort_by_latest(data)

        if not data:
            item = QListWidgetItem("No recent projects")
            item.setFlags(Qt.NoItemFlags) # type: ignore
            item.setTextAlignment(Qt.AlignCenter) # type: ignore
            item.setForeground(Qt.gray) # type: ignore
            item.setSizeHint(QSize(0, 40))

            self.ui.recentProjectsList.addItem(item)

            return

        for item in data:
            list_item = QListWidgetItem()
            list_item.setSizeHint(QSize(0, 50)) # Controls row height

            widget = QWidget()
            layout = QVBoxLayout(widget)
            layout.setContentsMargins(8, 4, 8, 4)
            layout.setSpacing(2)

            # File name (big and bold)
            name_label = QLabel(item["fileNameNoExt"])

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

            # Store file path and it's display name the item (IMPORTANT!)
            list_item.setData(Qt.UserRole, item["filePath"]) # type: ignore
            list_item.setData(Qt.UserRole + 1, name_label.text()) # Store the item's display name in custom data            # type: ignore

            self.ui.recentProjectsList.addItem(list_item)
            self.ui.recentProjectsList.setItemWidget(list_item, widget)

app = QApplication(sys.argv)

QApplication.setOrganizationName("BoxCAD")
QApplication.setApplicationName("BoxCAD")

data_dir = QStandardPaths.writableLocation(
    QStandardPaths.AppDataLocation # type: ignore
)

os.makedirs(data_dir, exist_ok=True)

# Set the app's style
app.setStyle(app_style)

winddow = MainWindow()
winddow.show()

app.exec()
