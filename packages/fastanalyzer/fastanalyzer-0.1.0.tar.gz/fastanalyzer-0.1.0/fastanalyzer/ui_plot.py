# -*- coding: utf-8 -*-

##########################################################################
# Form generated from reading UI file 'plot.ui'
##
# Created by: Qt User Interface Compiler version 6.6.1
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
##########################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QMainWindow, QMenuBar,
                               QSizePolicy, QStatusBar, QWidget)


class Ui_Plot(object):
    def setupUi(self, Plot):
        if not Plot.objectName():
            Plot.setObjectName(u"Plot")
        Plot.resize(1200, 800)
        Plot.setMinimumSize(QSize(1200, 800))
        self.centralwidget = QWidget(Plot)
        self.centralwidget.setObjectName(u"centralwidget")
        Plot.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Plot)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 19))
        Plot.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Plot)
        self.statusbar.setObjectName(u"statusbar")
        Plot.setStatusBar(self.statusbar)
        self.settingsDock = QDockWidget(Plot)
        self.settingsDock.setObjectName(u"settingsDock")
        self.settingsDock.setFeatures(QDockWidget.DockWidgetMovable)
        self.settingsDockContents = QWidget()
        self.settingsDockContents.setObjectName(u"settingsDockContents")
        self.settingsDock.setWidget(self.settingsDockContents)
        Plot.addDockWidget(Qt.LeftDockWidgetArea, self.settingsDock)

        self.retranslateUi(Plot)

        QMetaObject.connectSlotsByName(Plot)
    # setupUi

    def retranslateUi(self, Plot):
        Plot.setWindowTitle(
            QCoreApplication.translate(
                "Plot", u"MainWindow", None))
    # retranslateUi
