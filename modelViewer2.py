import os
from qtpy.QtWidgets import QWidget, QVBoxLayout


class ModelViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize OCP Graphic Driver
        self.display_connection = Aspect_DisplayConnection()
        self.driver = OpenGl_GraphicDriver(self.display_connection)

        # Create the Viewer and Context
        self.viewer = V3d_Viewer(self.driver)
        self.context = AIS_InteractiveContext(self.viewer)

        # Create the View
        self.view = self.viewer.CreateView()

        # Set the background color (e.g., dark gray for CAD look)
        self.view.SetBackgroundColor(Quantity_Color(0.2, 0.2, 0.2, Quantity_TOC_RGB))

        # Pass the window ID of the widget to the OCP view
        handle = Aspect_Handle(int(self.winId()))
        window_handle = int(self.winId()) # Get the raw integer ID from PySide
        ocp_window = WNT_Window(handle) # Wrap it in a WNT_Window object so OCP understands it
        self.view.SetWindow(ocp_window) # Pass the wrapped window to the view

    def display_shape(self, cq_object):
        """Displays a CaddQuery generated object in the viewer"""

        # CadQuery objects have a .wrapped property that contains the OCP shape
        ocp_shape = cq_object.val().wrapped

        # Create an AIS (Application Interactive Services) object for rendering
        ais_shape = AIS_ColoredShape(ocp_shape)

        # Display it!
        self.context.Display(ais_shape, True)
        self.view.MustBeResized()
        self.view.Redraw()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.view.MustBeResized()
