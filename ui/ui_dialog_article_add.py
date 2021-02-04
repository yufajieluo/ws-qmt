# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_dialog_article_add.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogArticleAdd(object):
    def setupUi(self, DialogArticleAdd):
        DialogArticleAdd.setObjectName("DialogArticleAdd")
        DialogArticleAdd.resize(450, 200)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/image/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogArticleAdd.setWindowIcon(icon)
        self.push_button_ok = QtWidgets.QPushButton(DialogArticleAdd)
        self.push_button_ok.setGeometry(QtCore.QRect(110, 160, 75, 23))
        self.push_button_ok.setObjectName("push_button_ok")
        self.push_button_cancel = QtWidgets.QPushButton(DialogArticleAdd)
        self.push_button_cancel.setGeometry(QtCore.QRect(265, 160, 75, 23))
        self.push_button_cancel.setObjectName("push_button_cancel")
        self.widget = QtWidgets.QWidget(DialogArticleAdd)
        self.widget.setGeometry(QtCore.QRect(100, 10, 250, 130))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.line_edit_article_id = QtWidgets.QLineEdit(self.widget)
        self.line_edit_article_id.setObjectName("line_edit_article_id")
        self.gridLayout.addWidget(self.line_edit_article_id, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.spin_box_article_num = QtWidgets.QSpinBox(self.widget)
        self.spin_box_article_num.setMinimum(1)
        self.spin_box_article_num.setMaximum(2)
        self.spin_box_article_num.setObjectName("spin_box_article_num")
        self.gridLayout.addWidget(self.spin_box_article_num, 2, 1, 1, 1)
        self.line_edit_article_time = QtWidgets.QLineEdit(self.widget)
        self.line_edit_article_time.setObjectName("line_edit_article_time")
        self.gridLayout.addWidget(self.line_edit_article_time, 3, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.line_edit_article_name = QtWidgets.QLineEdit(self.widget)
        self.line_edit_article_name.setObjectName("line_edit_article_name")
        self.gridLayout.addWidget(self.line_edit_article_name, 4, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 3)

        self.retranslateUi(DialogArticleAdd)
        QtCore.QMetaObject.connectSlotsByName(DialogArticleAdd)
        DialogArticleAdd.setTabOrder(self.line_edit_article_id, self.spin_box_article_num)
        DialogArticleAdd.setTabOrder(self.spin_box_article_num, self.line_edit_article_time)
        DialogArticleAdd.setTabOrder(self.line_edit_article_time, self.line_edit_article_name)
        DialogArticleAdd.setTabOrder(self.line_edit_article_name, self.push_button_ok)
        DialogArticleAdd.setTabOrder(self.push_button_ok, self.push_button_cancel)

    def retranslateUi(self, DialogArticleAdd):
        _translate = QtCore.QCoreApplication.translate
        DialogArticleAdd.setWindowTitle(_translate("DialogArticleAdd", "添加"))
        self.push_button_ok.setText(_translate("DialogArticleAdd", "保存"))
        self.push_button_cancel.setText(_translate("DialogArticleAdd", "取消"))
        self.label_4.setText(_translate("DialogArticleAdd", "抢购时间"))
        self.label_3.setText(_translate("DialogArticleAdd", "抢购数量"))
        self.label_2.setText(_translate("DialogArticleAdd", "商品编号"))
        self.label.setText(_translate("DialogArticleAdd", "商品名称"))
from . import resource_rc
