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
from PySide6.QtWidgets import (QApplication, QDockWidget, QDoubleSpinBox, QFormLayout,
    QFrame, QGridLayout, QLabel, QLayout,
    QMainWindow, QMenu, QMenuBar, QSizePolicy,
    QStatusBar, QToolBox, QWidget)

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
        self.toolBox = QToolBox(self.dockWidgetContents)
        self.toolBox.setObjectName(u"toolBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy2)
        self.toolBox.setMinimumSize(QSize(0, 170))
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setGeometry(QRect(0, 0, 176, 142))
        self.formLayout_2 = QFormLayout(self.page_3)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.lengthLabel = QLabel(self.page_3)
        self.lengthLabel.setObjectName(u"lengthLabel")
        font = QFont()
        font.setFamilies([u"Inter 18pt"])
        font.setPointSize(8)
        self.lengthLabel.setFont(font)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lengthLabel)

        self.lengthInput = QDoubleSpinBox(self.page_3)
        self.lengthInput.setObjectName(u"lengthInput")
        self.lengthInput.setMinimumSize(QSize(0, 0))

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lengthInput)

        self.widthLabel = QLabel(self.page_3)
        self.widthLabel.setObjectName(u"widthLabel")
        self.widthLabel.setFont(font)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.widthLabel)

        self.widthInput = QDoubleSpinBox(self.page_3)
        self.widthInput.setObjectName(u"widthInput")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.widthInput)

        self.heightLabel = QLabel(self.page_3)
        self.heightLabel.setObjectName(u"heightLabel")
        self.heightLabel.setFont(font)

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.heightLabel)

        self.heightInput = QDoubleSpinBox(self.page_3)
        self.heightInput.setObjectName(u"heightInput")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.heightInput)

        self.heightLabel_2 = QLabel(self.page_3)
        self.heightLabel_2.setObjectName(u"heightLabel_2")
        self.heightLabel_2.setFont(font)

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.heightLabel_2)

        self.heightInput_2 = QDoubleSpinBox(self.page_3)
        self.heightInput_2.setObjectName(u"heightInput_2")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.FieldRole, self.heightInput_2)

        self.heightInput_3 = QDoubleSpinBox(self.page_3)
        self.heightInput_3.setObjectName(u"heightInput_3")

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.FieldRole, self.heightInput_3)

        self.heightLabel_3 = QLabel(self.page_3)
        self.heightLabel_3.setObjectName(u"heightLabel_3")
        self.heightLabel_3.setFont(font)

        self.formLayout_2.setWidget(4, QFormLayout.ItemRole.LabelRole, self.heightLabel_3)

        self.toolBox.addItem(self.page_3, u"Dimensions")
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.page_4.setGeometry(QRect(0, 0, 176, 116))
        self.toolBox.addItem(self.page_4, u"Internal Hardware")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.SpanningRole, self.toolBox)

        self.parametersDock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.parametersDock)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuExit.menuAction())

        self.retranslateUi(MainWindow)

        self.toolBox.setCurrentIndex(1)


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
        self.lengthLabel.setText(QCoreApplication.translate("MainWindow", u"Length (X)", None))
        self.widthLabel.setText(QCoreApplication.translate("MainWindow", u"Width (Y)", None))
        self.heightLabel.setText(QCoreApplication.translate("MainWindow", u"Height (Z)", None))
        self.heightLabel_2.setText(QCoreApplication.translate("MainWindow", u"Wall Thickness", None))
        self.heightLabel_3.setText(QCoreApplication.translate("MainWindow", u"Corner Radius", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), QCoreApplication.translate("MainWindow", u"Dimensions", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), QCoreApplication.translate("MainWindow", u"Internal Hardware", None))
    # retranslateUi

