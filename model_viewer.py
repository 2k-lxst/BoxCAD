import os

# Silence Chromium hardware errors
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--log-level=3 --disable-gpu-compositing"
os.environ["QT_LOGGING_RULES"] = "qt.webenginecontext.debug=false"

import threading, socketserver, http.server
from qtpy.QtWidgets import QWidget, QVBoxLayout
from qtpy.QtWebEngineWidgets import QWebEngineView # type: ignore
from qtpy.QtCore import QUrl
from http.server import SimpleHTTPRequestHandler
import cadquery as cq

class QuietHandler(SimpleHTTPRequestHandler):
    def send_error(self, code, message=None, explain=None):
        """Override the default error printer to use our custom console."""

        if "favicon.ico" in self.path:
            if hasattr(self.server, 'printer'):
                self.server.printer(f"File not found - GET {self.path} HTTP/1.1", "silenced") # type: ignore
            return

        if hasattr(self.server, "printer"):
            self.server.printer(f"Code {code}: {message or explain} - {self.path}", "error") # type: ignore

    def log_message(self, format, *args):
        message = format % args

        if hasattr(self.server, "printer"):
            if "404" in message:
                self.server.printer(f"Asset Missing: {message}", "error") # type: ignore
            else:
                self.server.printer(f"Served: {message}", "success") # type: ignore

                pass
        else:
            print(message)

class ModelViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout and browser
        self.layout = QVBoxLayout(self) # type: ignore
        self.browser = QWebEngineView()
        self.layout.addWidget(self.browser) # type: ignore

        # Serve the current folder via HTTP on a free port
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.base_dir) # Server serves files from this folder

        self.httpd = socketserver.TCPServer(("", 0), QuietHandler) # 0 = Pick a free port

        self.httpd.printer = self.print_to_console # type: ignore

        port = self.httpd.server_address[1]

        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

        # Load the HTML file through the server
        self.browser.setUrl(QUrl(f"http://127.0.0.1:{port}/viewer.html"))

    def closeEvent(self, event):
        """Stop the server when the widget is closed"""
        self.httpd.shutdown()

        super().closeEvent(event)

    def update_display(self, cq_object):
        """Exports geometry and notifies the browser to reload the file via HTTP"""
        try:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
            stl_path = os.path.join(self.base_dir, "model.stl")

            cq_object.export(stl_path)

            import time
            t = int(time.time() * 1000) # Current time in miliseconds

            relative_url = f"./model.stl?t={t}"

            self.browser.page().runJavaScript(f"updateMesh('{relative_url}')")

        except Exception as e:
            self.print_to_console(str(e), "error")

    def print_to_console(self, message = "No message was provided!", type = "info"):
        from termcolor import colored

        colors = {"info": "blue", "warning": "yellow", "error": "red", "success": "green", "silenced": "dark_grey"}

        color = colors.get(type, "white")

        print(colored(f"[{type.upper()}] {message}", color))
