from qtpy.QtWidgets import QApplication, QMessageBox
from qtpy.QtCore import QFile
from qtpy.QtUiTools import QUiLoader

app = QApplication()

loader = QUiLoader()

file = QFile("SimpleForm.ui")
file.open(QFile.ReadOnly) # type: ignore

window = loader.load(file)
file.close()

window.pushButton.clicked.connect( # type: ignore
    lambda: QMessageBox.information(window, "Message", window.lineEdit.text()) # type: ignore
)

window.show()

app.exec()