import os, threading, socketserver, http.server
from qtpy.QtWidgets import QWidget, QVBoxLayout
from qtpy.QtWebEngineWidgets import QWebEngineView # type: ignore
from qtpy.QtCore import QUrl

class ModelViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout and browser
        self.layout = QVBoxLayout(self) # type: ignore
        self.browser = QWebEngineView()
        self.layout.addWidget(self.browser) # type: ignore

        # Serve the current folder via HTTP on a free port
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.base_dir) # Server sereves files from this folder

        handler = http.server.SimpleHTTPRequestHandler
        self.httpd = socketserver.TCPServer(("", 0), handler) # 0 = Pick a free port
        port = self.httpd.server_address[1]

        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

        # Load the HTML file through the server
        self.browser.setUrl(QUrl(f"http://127.0.0.1:{port}/viewer.html"))

    def closeEvent(self, event):
        """ Stop the server when the widget is closed """

        self.httpd.shutdown()

        super().closeEvent(event)
