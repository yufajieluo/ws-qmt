# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_window_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/image/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(0, 30, 800, 158))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.table_widget_article = QtWidgets.QTableWidget(self.frame_2)
        self.table_widget_article.setGeometry(QtCore.QRect(260, 0, 390, 158))
        self.table_widget_article.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_widget_article.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_widget_article.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_widget_article.setRowCount(0)
        self.table_widget_article.setColumnCount(4)
        self.table_widget_article.setObjectName("table_widget_article")
        self.table_widget_article.horizontalHeader().setVisible(True)
        self.table_widget_article.horizontalHeader().setCascadingSectionResizes(False)
        self.text_browser_active = QtWidgets.QTextBrowser(self.frame_2)
        self.text_browser_active.setGeometry(QtCore.QRect(30, 38, 200, 120))
        self.text_browser_active.setDocumentTitle("")
        self.text_browser_active.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.text_browser_active.setPlaceholderText("")
        self.text_browser_active.setObjectName("text_browser_active")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(30, 0, 121, 31))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.frame1 = QtWidgets.QFrame(self.frame_2)
        self.frame1.setGeometry(QtCore.QRect(670, 0, 100, 151))
        self.frame1.setObjectName("frame1")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.push_button_modify = QtWidgets.QPushButton(self.frame1)
        self.push_button_modify.setObjectName("push_button_modify")
        self.gridLayout_3.addWidget(self.push_button_modify, 2, 0, 1, 1)
        self.push_button_add = QtWidgets.QPushButton(self.frame1)
        self.push_button_add.setObjectName("push_button_add")
        self.gridLayout_3.addWidget(self.push_button_add, 1, 0, 1, 1)
        self.push_button_active = QtWidgets.QPushButton(self.frame1)
        self.push_button_active.setObjectName("push_button_active")
        self.gridLayout_3.addWidget(self.push_button_active, 0, 0, 1, 1)
        self.push_button_remove = QtWidgets.QPushButton(self.frame1)
        self.push_button_remove.setObjectName("push_button_remove")
        self.gridLayout_3.addWidget(self.push_button_remove, 3, 0, 1, 1)
        self.gridFrame = QtWidgets.QFrame(self.centralwidget)
        self.gridFrame.setGeometry(QtCore.QRect(0, 188, 800, 33))
        self.gridFrame.setObjectName("gridFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.gridFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.line = QtWidgets.QFrame(self.gridFrame)
        self.line.setMinimumSize(QtCore.QSize(782, 0))
        self.line.setMaximumSize(QtCore.QSize(782, 16777215))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(0, 221, 800, 158))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setGeometry(QtCore.QRect(30, 0, 121, 31))
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setObjectName("label_2")
        self.text_browser_login = QtWidgets.QTextBrowser(self.frame_3)
        self.text_browser_login.setGeometry(QtCore.QRect(30, 38, 200, 120))
        self.text_browser_login.setStyleSheet("")
        self.text_browser_login.setDocumentTitle("")
        self.text_browser_login.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.text_browser_login.setPlaceholderText("")
        self.text_browser_login.setObjectName("text_browser_login")
        self.label_qrcode = QtWidgets.QLabel(self.frame_3)
        self.label_qrcode.setGeometry(QtCore.QRect(260, 0, 390, 158))
        self.label_qrcode.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_qrcode.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_qrcode.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_qrcode.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_qrcode.setText("")
        self.label_qrcode.setAlignment(QtCore.Qt.AlignCenter)
        self.label_qrcode.setObjectName("label_qrcode")
        self.gridFrame1 = QtWidgets.QFrame(self.frame_3)
        self.gridFrame1.setGeometry(QtCore.QRect(670, 0, 100, 151))
        self.gridFrame1.setObjectName("gridFrame1")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gridFrame1)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.push_button_getqr = QtWidgets.QPushButton(self.gridFrame1)
        self.push_button_getqr.setObjectName("push_button_getqr")
        self.gridLayout_4.addWidget(self.push_button_getqr, 0, 0, 1, 1)
        self.gridFrame_2 = QtWidgets.QFrame(self.centralwidget)
        self.gridFrame_2.setGeometry(QtCore.QRect(0, 379, 800, 33))
        self.gridFrame_2.setObjectName("gridFrame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridFrame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.line_2 = QtWidgets.QFrame(self.gridFrame_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_2.addWidget(self.line_2, 1, 0, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.centralwidget)
        self.frame_4.setGeometry(QtCore.QRect(0, 412, 800, 158))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.label_3 = QtWidgets.QLabel(self.frame_4)
        self.label_3.setGeometry(QtCore.QRect(30, 0, 121, 31))
        self.label_3.setTextFormat(QtCore.Qt.AutoText)
        self.label_3.setObjectName("label_3")
        self.text_browser_seckill = QtWidgets.QTextBrowser(self.frame_4)
        self.text_browser_seckill.setGeometry(QtCore.QRect(30, 38, 200, 120))
        self.text_browser_seckill.setStyleSheet("")
        self.text_browser_seckill.setDocumentTitle("")
        self.text_browser_seckill.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.text_browser_seckill.setPlaceholderText("")
        self.text_browser_seckill.setObjectName("text_browser_seckill")
        self.gridFrame_3 = QtWidgets.QFrame(self.frame_4)
        self.gridFrame_3.setGeometry(QtCore.QRect(670, 0, 100, 151))
        self.gridFrame_3.setObjectName("gridFrame_3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.gridFrame_3)
        self.gridLayout_5.setContentsMargins(1, 1, 1, 1)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.push_button_seckill = QtWidgets.QPushButton(self.gridFrame_3)
        self.push_button_seckill.setObjectName("push_button_seckill")
        self.gridLayout_5.addWidget(self.push_button_seckill, 3, 0, 1, 1)
        self.push_button_reserve = QtWidgets.QPushButton(self.gridFrame_3)
        self.push_button_reserve.setMinimumSize(QtCore.QSize(98, 0))
        self.push_button_reserve.setMaximumSize(QtCore.QSize(98, 16777215))
        self.push_button_reserve.setObjectName("push_button_reserve")
        self.gridLayout_5.addWidget(self.push_button_reserve, 1, 0, 1, 1)
        self.push_button_stop = QtWidgets.QPushButton(self.gridFrame_3)
        self.push_button_stop.setMinimumSize(QtCore.QSize(98, 0))
        self.push_button_stop.setMaximumSize(QtCore.QSize(98, 16777215))
        self.push_button_stop.setObjectName("push_button_stop")
        self.gridLayout_5.addWidget(self.push_button_stop, 4, 0, 1, 1)
        self.label_seckill = QtWidgets.QLabel(self.frame_4)
        self.label_seckill.setGeometry(QtCore.QRect(260, 0, 390, 158))
        self.label_seckill.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_seckill.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_seckill.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_seckill.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_seckill.setText("")
        self.label_seckill.setAlignment(QtCore.Qt.AlignCenter)
        self.label_seckill.setObjectName("label_seckill")
        self.frame_5 = QtWidgets.QFrame(self.centralwidget)
        self.frame_5.setGeometry(QtCore.QRect(0, 570, 800, 30))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.text_browser_active, self.table_widget_article)
        MainWindow.setTabOrder(self.table_widget_article, self.push_button_active)
        MainWindow.setTabOrder(self.push_button_active, self.push_button_add)
        MainWindow.setTabOrder(self.push_button_add, self.push_button_modify)
        MainWindow.setTabOrder(self.push_button_modify, self.push_button_remove)
        MainWindow.setTabOrder(self.push_button_remove, self.text_browser_login)
        MainWindow.setTabOrder(self.text_browser_login, self.push_button_getqr)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "秒"))
        self.table_widget_article.setSortingEnabled(True)
        self.label.setText(_translate("MainWindow", "激活商品"))
        self.push_button_modify.setText(_translate("MainWindow", "修改"))
        self.push_button_add.setText(_translate("MainWindow", "添加"))
        self.push_button_active.setText(_translate("MainWindow", "激活"))
        self.push_button_remove.setText(_translate("MainWindow", "删除"))
        self.label_2.setText(_translate("MainWindow", "登录商城"))
        self.push_button_getqr.setText(_translate("MainWindow", "获取二维码"))
        self.label_3.setText(_translate("MainWindow", "预约抢购"))
        self.push_button_seckill.setText(_translate("MainWindow", "抢购"))
        self.push_button_reserve.setText(_translate("MainWindow", "预约"))
        self.push_button_stop.setText(_translate("MainWindow", "停止"))
from . import resource_rc
