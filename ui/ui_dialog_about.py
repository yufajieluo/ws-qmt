# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_dialog_about.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogAbout(object):
    def setupUi(self, DialogAbout):
        DialogAbout.setObjectName("DialogAbout")
        DialogAbout.resize(450, 200)
        DialogAbout.setMinimumSize(QtCore.QSize(450, 200))
        DialogAbout.setMaximumSize(QtCore.QSize(450, 200))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/image/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogAbout.setWindowIcon(icon)
        self.verticalWidget = QtWidgets.QWidget(DialogAbout)
        self.verticalWidget.setGeometry(QtCore.QRect(0, 150, 430, 50))
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridWidget = QtWidgets.QWidget(DialogAbout)
        self.gridWidget.setGeometry(QtCore.QRect(0, 0, 120, 150))
        self.gridWidget.setMinimumSize(QtCore.QSize(120, 150))
        self.gridWidget.setMaximumSize(QtCore.QSize(120, 150))
        self.gridWidget.setObjectName("gridWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_image = QtWidgets.QLabel(self.gridWidget)
        self.label_image.setMinimumSize(QtCore.QSize(80, 80))
        self.label_image.setMaximumSize(QtCore.QSize(80, 80))
        self.label_image.setStyleSheet("background-image: url(:/image/image/about_show.png);")
        self.label_image.setText("")
        self.label_image.setObjectName("label_image")
        self.gridLayout.addWidget(self.label_image, 0, 0, 1, 1)
        self.gridWidget1 = QtWidgets.QWidget(DialogAbout)
        self.gridWidget1.setGeometry(QtCore.QRect(120, 0, 330, 150))
        self.gridWidget1.setMinimumSize(QtCore.QSize(330, 150))
        self.gridWidget1.setMaximumSize(QtCore.QSize(330, 150))
        self.gridWidget1.setObjectName("gridWidget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridWidget1)
        self.gridLayout_2.setContentsMargins(0, 10, 0, 10)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_version = QtWidgets.QLabel(self.gridWidget1)
        self.label_version.setMinimumSize(QtCore.QSize(300, 0))
        self.label_version.setMaximumSize(QtCore.QSize(300, 16777215))
        self.label_version.setText("")
        self.label_version.setObjectName("label_version")
        self.gridLayout_2.addWidget(self.label_version, 1, 0, 1, 1)
        self.label_title = QtWidgets.QLabel(self.gridWidget1)
        self.label_title.setMinimumSize(QtCore.QSize(300, 0))
        self.label_title.setMaximumSize(QtCore.QSize(300, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setText("")
        self.label_title.setObjectName("label_title")
        self.gridLayout_2.addWidget(self.label_title, 0, 0, 1, 1)
        self.label_explanation = QtWidgets.QLabel(self.gridWidget1)
        self.label_explanation.setMinimumSize(QtCore.QSize(300, 0))
        self.label_explanation.setMaximumSize(QtCore.QSize(300, 16777215))
        self.label_explanation.setText("")
        self.label_explanation.setWordWrap(True)
        self.label_explanation.setObjectName("label_explanation")
        self.gridLayout_2.addWidget(self.label_explanation, 2, 0, 1, 1)
        self.label_copyright = QtWidgets.QLabel(self.gridWidget1)
        self.label_copyright.setMinimumSize(QtCore.QSize(300, 0))
        self.label_copyright.setMaximumSize(QtCore.QSize(300, 16777215))
        self.label_copyright.setText("")
        self.label_copyright.setObjectName("label_copyright")
        self.gridLayout_2.addWidget(self.label_copyright, 3, 0, 1, 1)

        self.retranslateUi(DialogAbout)
        self.buttonBox.accepted.connect(DialogAbout.accept)
        self.buttonBox.rejected.connect(DialogAbout.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogAbout)

    def retranslateUi(self, DialogAbout):
        _translate = QtCore.QCoreApplication.translate
        DialogAbout.setWindowTitle(_translate("DialogAbout", "关于"))
from . import resource_rc
