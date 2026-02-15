# Pyright false positive due to dynamic PySide attributes
# pyright: reportAttributeAccessIssue=false

import os

# Silence Chromium hardware errors
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--log-level=3 --disable-gpu-compositing"
os.environ["QT_LOGGING_RULES"] = "qt.webenginecontext.debug=false"

import threading, socketserver, http.server
from qtpy.QtWidgets import QFrame, QVBoxLayout
from qtpy.QtWebEngineWidgets import QWebEngineView # type: ignore
from qtpy.QtCore import QUrl, QObject, QTimer
from qtpy.QtWebChannel import QWebChannel
from PySide6.QtCore import Slot
from http.server import SimpleHTTPRequestHandler

class QuietHandler(SimpleHTTPRequestHandler):
    def send_error(self, code, message=None, explain=None):
        """Override the default error printer to use our custom console."""

        if "favicon.ico" in self.path:
            if hasattr(self.server, 'printer'):
                self.server.printer(f"File not found - GET {self.path} HTTP/1.1", "silenced")
            return

        if hasattr(self.server, "printer"):
            self.server.printer(f"Code {code}: {message or explain} - {self.path}", "error")

    def log_message(self, format, *args):
        message = format % args

        if hasattr(self.server, "printer"):
            if "404" in message:
                self.server.printer(f"Asset Missing: {message}", "error")
            else:
                self.server.printer(f"Served: {message}", "success")

                pass
        else:
            print(message)

class Bridge(QObject):
    """Small helper class to recieve signals from JavaScript"""
    def __init__(self, viewer):
        super().__init__()
        self.viewer = viewer

    @Slot()
    def on_viewer_ready(self):
        # This is the function JavaScript will call
        if hasattr(self.viewer, 'on_ready_callback'):
            self.viewer.on_ready_callback()

class ModelViewer(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout and browser
        self.browser = QWebEngineView()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.browser)

        # Bridge setup
        self.channel = QWebChannel()
        self.bridge = Bridge(self)
        self.channel.registerObject("pybridge", self.bridge)
        self.browser.page().setWebChannel(self.channel)

        # Serve the current folder via HTTP on a free port
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.base_dir) # Server serves files from this folder

        self.httpd = socketserver.TCPServer(("", 0), QuietHandler) # 0 = Pick a free port

        self.httpd.printer = self.print_to_console

        self.port = self.httpd.server_address[1]

        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

        # Load the HTML file through the server
        self.browser.setUrl(QUrl(f"http://127.0.0.1:{self.port}/viewer.html"))

        # Create a debounce timer
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True) # Only fire once
        self.update_timer.setInterval(200) # Wait 200ms before updating
        self.pending_object = None

    def closeEvent(self, event):
        """Stop the server when the widget is closed"""
        self.httpd.shutdown()

        super().closeEvent(event)

    def update_display(self, cq_object):
        """Exports geometry and notifies the browser to reload the file via HTTP"""
        self.pending_object = cq_object
        self.update_timer.start()

        try:
            self.update_timer.timeout.disconnect()
        except:
            pass

        self.update_timer.timeout.connect(self._execute_update)



    def _execute_update(self):
        """The actual update happens here only after the user stops typing"""
        if self.pending_object is None: return

        try:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
            stl_path = os.path.join(self.base_dir, "model.stl")

            self.pending_object.export(stl_path)

            import time
            t = int(time.time() * 1000) # Current time in miliseconds

            url = f"http://127.0.0.1:{self.port}/model.stl?t={t}"

            self.browser.page().runJavaScript(f"window.updateMesh({repr(url)})")

        except Exception as e:
            self.print_to_console(str(e), "error")

    def print_to_console(self, message = "No message was provided!", type = "info"):
        from termcolor import colored

        colors = {"info": "blue", "warning": "yellow", "error": "red", "success": "green", "silenced": "dark_grey"}

        color = colors.get(type, "white")

        print(colored(f"[{type.upper()}] {message}", color))

    def set_on_ready_callback(self, callback_func):
        """Pass a function here from your main app to run when JS is ready"""
        self.on_ready_callback = callback_func
