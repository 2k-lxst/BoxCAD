# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'StartupUI.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QMenuBar, QProgressBar, QPushButton,
    QSizePolicy, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(700, 400)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(700, 400))
        MainWindow.setMaximumSize(QSize(700, 400))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"#centralwidget {\n"
"    /* This tells Qt to tile the image while scaling it */\n"
"    border-image: url(:/images/background.png) 0 0 0 0 repeat repeat;\n"
"}")
        self.Subtitle = QLabel(self.centralwidget)
        self.Subtitle.setObjectName(u"Subtitle")
        self.Subtitle.setGeometry(QRect(140, 80, 451, 31))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(14)
        self.Subtitle.setFont(font)
        self.Subtitle.setAlignment(Qt.AlignCenter)
        self.Title = QLabel(self.centralwidget)
        self.Title.setObjectName(u"Title")
        self.Title.setGeometry(QRect(10, 10, 681, 91))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        brush1 = QBrush(QColor(120, 120, 120, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush1)
        self.Title.setPalette(palette)
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(34)
        font1.setBold(True)
        self.Title.setFont(font1)
        self.Title.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        self.Title.setAlignment(Qt.AlignCenter)
        self.btn_create_project = QPushButton(self.centralwidget)
        self.btn_create_project.setObjectName(u"btn_create_project")
        self.btn_create_project.setGeometry(QRect(100, 170, 181, 31))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        self.btn_create_project.setFont(font2)
        self.btn_hardware_library = QPushButton(self.centralwidget)
        self.btn_hardware_library.setObjectName(u"btn_hardware_library")
        self.btn_hardware_library.setGeometry(QRect(100, 210, 181, 31))
        self.btn_hardware_library.setFont(font2)
        self.btn_hardware_library.setStyleSheet(u"")
        self.btn_tutorials = QPushButton(self.centralwidget)
        self.btn_tutorials.setObjectName(u"btn_tutorials")
        self.btn_tutorials.setGeometry(QRect(100, 250, 181, 31))
        self.btn_tutorials.setFont(font2)
        self.progress_bar_init = QProgressBar(self.centralwidget)
        self.progress_bar_init.setObjectName(u"progress_bar_init")
        self.progress_bar_init.setGeometry(QRect(10, 375, 681, 20))
        self.progress_bar_init.setValue(24)
        self.progress_bar_init.setTextVisible(False)
        self.progress_bar_init.setInvertedAppearance(False)
        self.progress_bar_init.setTextDirection(QProgressBar.TopToBottom)
        self.text_init = QLabel(self.centralwidget)
        self.text_init.setObjectName(u"text_init")
        self.text_init.setGeometry(QRect(10, 350, 131, 21))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(9)
        self.text_init.setFont(font3)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(440, 120, 141, 21))
        font4 = QFont()
        font4.setPointSize(14)
        self.label_2.setFont(font4)
        self.recent_projects_list = QListWidget(self.centralwidget)
        self.recent_projects_list.setObjectName(u"recent_projects_list")
        self.recent_projects_list.setGeometry(QRect(380, 150, 256, 192))
        self.recent_projects_list.setStyleSheet(u"QListWidget {\n"
"    outline: 0;        /* Removes the dotted/solid focus outline */\n"
"    border: none;      /* Ensures no frame border exists */\n"
"    background: none;  /* Keeps it transparent against your grid */\n"
"}\n"
"\n"
"/* This ensures that even when clicked, no blue border appears */\n"
"QListWidget:focus {\n"
"    border: none;\n"
"    outline: none;\n"
"}\n"
"\n"
"/* How the item looks when you are actually interacting with the list */\n"
"QListWidget::item:selected:active {\n"
"    background-color: #3b82f6; \n"
"    color: white;\n"
"}\n"
"\n"
"/* How the item looks when you click a button or somewhere else */\n"
"QListWidget::item:selected:!active {\n"
"    background-color: rgba(200, 200, 200, 50); /* Dim the highlight */\n"
"    color: #555; /* Fade the text */\n"
"}")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 700, 21))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Subtitle.setText(QCoreApplication.translate("MainWindow", u"v0.0.1", None))
#if QT_CONFIG(tooltip)
        self.Title.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.Title.setText(QCoreApplication.translate("MainWindow", u"Welcome to BoxCAD!", None))
        self.btn_create_project.setText(QCoreApplication.translate("MainWindow", u"Create New Project", None))
        self.btn_hardware_library.setText(QCoreApplication.translate("MainWindow", u"Hardware Library", None))
        self.btn_tutorials.setText(QCoreApplication.translate("MainWindow", u"Tutorials", None))
        self.text_init.setText(QCoreApplication.translate("MainWindow", u"Initializing ...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Recent Projects:", None))
    # retranslateUi

