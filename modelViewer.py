import os
import base64
import cadquery as cq
from qtpy.QtWidgets import QWidget, QVBoxLayout
from qtpy.QtWebEngineWidgets import QWebEngineView # type: ignore
from qtpy.QtCore import QUrl

import time

class ModelViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self) # type: ignore

        # Initialize the browser
        self.browser = QWebEngineView()

        # Enable local file access
        self.browser.settings().setAttribute(
            self.browser.settings().WebAttribute.LocalContentCanAccessFileUrls, True
        )
        self.browser.settings().setAttribute(
            self.browser.settings().WebAttribute.AllowRunningInsecureContent, True
        )

        self.layout.addWidget(self.browser) # type: ignore

        settings = self.browser.settings()
        settings.setAttribute(settings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(settings.WebAttribute.LocalContentCanAccessFileUrls, True)

        # Resolve the path to "viewer.html"
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(self.base_dir, "viewer.html")

        # Set the browser URL to that local file
        self.browser.setUrl(QUrl.fromLocalFile(html_path))

    # def update_display(self, cq_object):
    #     """ This is the 'Handshake' between Python and HTML """

    #     # Parse the path where the .stl file will be saved to
    #     stl_path = os.path.join(self.base_dir, "model.stl")

    #     # Export the cq_object as 'model.stl'
    #     cq.exporters.export(cq_object, stl_path, cq.exporters.ExportTypes.STL)

    #     time.sleep(0.1)

    #     # Tell the browser to run the JavaScript function 'updateMesh()'
    #     self.browser.page().runJavaScript("updateMesh();")

    # TODO: REWRITE THE CODE IF IT WORKS!!!

    def update_display(self, cq_object):
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
            stl_path = os.path.join(self.base_dir, "model.stl")

            # 1. Export the STL as usual
            cq.exporters.export(cq_object, stl_path)

            # 2. Read the file and turn it into a Base64 string
            with open(stl_path, "rb") as f:
                data = f.read()
                base64_data = base64.b64encode(data).decode('utf-8')

            # 3. Pass the string directly into a NEW JavaScript function
            # We send it as a 'data:application/sla;base64,...' string
            js_code = f"updateMeshFromData('{base64_data}');"
            self.browser.page().runJavaScript(js_code)
