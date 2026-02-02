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
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QFormLayout, QFrame,
    QGridLayout, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QToolBox, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.viewer = QFrame(self.centralwidget)
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

        self.gridLayout.addWidget(self.viewer, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuExit = QMenu(self.menubar)
        self.menuExit.setObjectName(u"menuExit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.outputDock = QDockWidget(MainWindow)
        self.outputDock.setObjectName(u"outputDock")
        self.outputDock.setMinimumSize(QSize(500, 100))
        self.outputDock.setMaximumSize(QSize(524287, 524287))
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.outputDock.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.outputDock)
        self.parametersDock = QDockWidget(MainWindow)
        self.parametersDock.setObjectName(u"parametersDock")
        self.parametersDock.setMinimumSize(QSize(200, 374))
        self.parametersDock.setMaximumSize(QSize(524287, 524287))
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.formLayout = QFormLayout(self.dockWidgetContents)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setVerticalSpacing(10)
        self.formLayout.setContentsMargins(12, 10, 12, 12)
        self.parametersToolBox = QToolBox(self.dockWidgetContents)
        self.parametersToolBox.setObjectName(u"parametersToolBox")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setGeometry(QRect(0, 0, 170, 69))
        self.parametersToolBox.addItem(self.page, u"Page 1")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setGeometry(QRect(0, 0, 170, 69))
        self.parametersToolBox.addItem(self.page_2, u"Page 2")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.parametersToolBox)

        self.parametersDock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.parametersDock)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuExit.menuAction())

        self.retranslateUi(MainWindow)

        self.parametersToolBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuExit.setTitle(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.outputDock.setWindowTitle(QCoreApplication.translate("MainWindow", u"Hardware Library", None))
        self.parametersDock.setWindowTitle(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.parametersToolBox.setItemText(self.parametersToolBox.indexOf(self.page), QCoreApplication.translate("MainWindow", u"Page 1", None))
        self.parametersToolBox.setItemText(self.parametersToolBox.indexOf(self.page_2), QCoreApplication.translate("MainWindow", u"Page 2", None))
    # retranslateUi

