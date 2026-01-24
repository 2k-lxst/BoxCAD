# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'welcome_screen.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QListWidget,
    QListWidgetItem, QMainWindow, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(550, 500)
        MainWindow.setMinimumSize(QSize(550, 500))
        MainWindow.setMaximumSize(QSize(550, 500))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.labelWelcome = QLabel(self.centralwidget)
        self.labelWelcome.setObjectName(u"labelWelcome")
        self.labelWelcome.setGeometry(QRect(0, 20, 551, 31))
        font = QFont()
        font.setFamilies([u"Inter 18pt"])
        font.setPointSize(12)
        self.labelWelcome.setFont(font)
        self.labelWelcome.setAlignment(Qt.AlignCenter)
        self.labelTitle = QLabel(self.centralwidget)
        self.labelTitle.setObjectName(u"labelTitle")
        self.labelTitle.setGeometry(QRect(0, 50, 551, 41))
        font1 = QFont()
        font1.setFamilies([u"Inter 18pt"])
        font1.setPointSize(35)
        font1.setBold(True)
        self.labelTitle.setFont(font1)
        self.labelTitle.setAlignment(Qt.AlignCenter)
        self.labelVersion = QLabel(self.centralwidget)
        self.labelVersion.setObjectName(u"labelVersion")
        self.labelVersion.setGeometry(QRect(0, 100, 551, 20))
        font2 = QFont()
        font2.setFamilies([u"Inter 18pt"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(True)
        font2.setUnderline(False)
        font2.setKerning(True)
        self.labelVersion.setFont(font2)
        self.labelVersion.setAlignment(Qt.AlignCenter)
        self.labelProgressBar = QLabel(self.centralwidget)
        self.labelProgressBar.setObjectName(u"labelProgressBar")
        self.labelProgressBar.setGeometry(QRect(10, 445, 81, 16))
        font3 = QFont()
        font3.setFamilies([u"Inter 18pt"])
        font3.setPointSize(9)
        font3.setBold(False)
        font3.setItalic(False)
        self.labelProgressBar.setFont(font3)
        self.btnCreateProject = QPushButton(self.centralwidget)
        self.btnCreateProject.setObjectName(u"btnCreateProject")
        self.btnCreateProject.setGeometry(QRect(40, 194, 171, 41))
        self.btnTutorials = QPushButton(self.centralwidget)
        self.btnTutorials.setObjectName(u"btnTutorials")
        self.btnTutorials.setGeometry(QRect(50, 290, 151, 36))
        self.btnExit = QPushButton(self.centralwidget)
        self.btnExit.setObjectName(u"btnExit")
        self.btnExit.setGeometry(QRect(60, 345, 131, 31))
        self.btnHardwareLibrary = QPushButton(self.centralwidget)
        self.btnHardwareLibrary.setObjectName(u"btnHardwareLibrary")
        self.btnHardwareLibrary.setGeometry(QRect(50, 245, 151, 36))
        self.recentProjectsList = QListWidget(self.centralwidget)
        self.recentProjectsList.setObjectName(u"recentProjectsList")
        self.recentProjectsList.setGeometry(QRect(270, 180, 236, 221))
        self.labelRecentProjects = QLabel(self.centralwidget)
        self.labelRecentProjects.setObjectName(u"labelRecentProjects")
        self.labelRecentProjects.setGeometry(QRect(270, 150, 236, 21))
        self.labelRecentProjects.setFont(font)
        self.labelRecentProjects.setAlignment(Qt.AlignCenter)
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(10, 470, 530, 20))
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(False)
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(60, 335, 131, 3))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 550, 21))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.labelWelcome.setText(QCoreApplication.translate("MainWindow", u"Welcome to", None))
        self.labelTitle.setText(QCoreApplication.translate("MainWindow", u"BoxCAD", None))
        self.labelVersion.setText(QCoreApplication.translate("MainWindow", u"v0.0.1", None))
        self.labelProgressBar.setText(QCoreApplication.translate("MainWindow", u"Initializing...", None))
        self.btnCreateProject.setText(QCoreApplication.translate("MainWindow", u"Create New Project", None))
        self.btnTutorials.setText(QCoreApplication.translate("MainWindow", u"Tutorials", None))
        self.btnExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.btnHardwareLibrary.setText(QCoreApplication.translate("MainWindow", u"Hardware Library", None))
        self.labelRecentProjects.setText(QCoreApplication.translate("MainWindow", u"Recent Projects", None))
    # retranslateUi

