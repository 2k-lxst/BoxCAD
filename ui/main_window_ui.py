# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QDockWidget, QFormLayout,
    QFrame, QHBoxLayout, QMainWindow, QPlainTextEdit,
    QSizePolicy, QStatusBar, QToolBox, QVBoxLayout,
    QWidget)

from model_viewer import ModelViewer

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 700)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.viewer = ModelViewer(self.centralwidget)
        self.viewer.setObjectName(u"viewer")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.viewer.sizePolicy().hasHeightForWidth())
        self.viewer.setSizePolicy(sizePolicy1)
        self.viewer.setMinimumSize(QSize(200, 200))
        self.viewer.setStyleSheet(u"background-color: #121212;")
        self.viewer.setFrameShape(QFrame.StyledPanel)
        self.viewer.setFrameShadow(QFrame.Raised)

        self.horizontalLayout.addWidget(self.viewer)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.outputDock = QDockWidget(MainWindow)
        self.outputDock.setObjectName(u"outputDock")
        self.outputDock.setEnabled(True)
        self.outputDock.setMinimumSize(QSize(500, 20))
        self.outputDock.setMaximumSize(QSize(524287, 130))
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.consoleOutput = QPlainTextEdit(self.dockWidgetContents_2)
        self.consoleOutput.setObjectName(u"consoleOutput")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.consoleOutput.sizePolicy().hasHeightForWidth())
        self.consoleOutput.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setFamilies([u"Consolas,Monospace"])
        self.consoleOutput.setFont(font)
        self.consoleOutput.setStyleSheet(u"QPlainTextEdit {\n"
"	background-color: transparent;\n"
"	border: none;\n"
"	color: #dcdcdc; /* Subtle light gray text */\n"
"	font-family: 'Consolas', 'Monospace'; /* Terminal look */\n"
"	font-size: 12px;\n"
"}")
        self.consoleOutput.setFrameShape(QFrame.NoFrame)
        self.consoleOutput.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.consoleOutput.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.consoleOutput.setReadOnly(True)

        self.verticalLayout.addWidget(self.consoleOutput)

        self.outputDock.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.outputDock)
        self.parametersDock = QDockWidget(MainWindow)
        self.parametersDock.setObjectName(u"parametersDock")
        sizePolicy.setHeightForWidth(self.parametersDock.sizePolicy().hasHeightForWidth())
        self.parametersDock.setSizePolicy(sizePolicy)
        self.parametersDock.setMinimumSize(QSize(200, 555))
        self.parametersDock.setMaximumSize(QSize(524287, 524287))
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        sizePolicy.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy)
        self.formLayout = QFormLayout(self.dockWidgetContents)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setRowWrapPolicy(QFormLayout.DontWrapRows)
        self.formLayout.setVerticalSpacing(10)
        self.formLayout.setContentsMargins(12, 10, 12, 12)
        self.parametersToolBox = QToolBox(self.dockWidgetContents)
        self.parametersToolBox.setObjectName(u"parametersToolBox")
        sizePolicy.setHeightForWidth(self.parametersToolBox.sizePolicy().hasHeightForWidth())
        self.parametersToolBox.setSizePolicy(sizePolicy)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setGeometry(QRect(0, 0, 300, 52))
        sizePolicy.setHeightForWidth(self.page.sizePolicy().hasHeightForWidth())
        self.page.setSizePolicy(sizePolicy)
        self.page.setMinimumSize(QSize(300, 0))
        self.parametersToolBox.addItem(self.page, u"Getting Started...")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.parametersToolBox)

        self.parametersDock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.parametersDock)

        self.retranslateUi(MainWindow)

        self.parametersToolBox.setCurrentIndex(0)
        self.parametersToolBox.layout().setSpacing(7)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.outputDock.setWindowTitle(QCoreApplication.translate("MainWindow", u"Project Output", None))
        self.parametersDock.setWindowTitle(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.parametersToolBox.setItemText(self.parametersToolBox.indexOf(self.page), QCoreApplication.translate("MainWindow", u"Getting Started...", None))
    # retranslateUi

