# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\Edit_AgendaUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1267, 722)
        self.refresh_button = QtWidgets.QPushButton(Form)
        self.refresh_button.setGeometry(QtCore.QRect(580, 20, 161, 31))
        self.refresh_button.setObjectName("refresh_button")
        self.close_button = QtWidgets.QPushButton(Form)
        self.close_button.setGeometry(QtCore.QRect(800, 20, 93, 28))
        self.close_button.setObjectName("close_button")
        self.goal_table = QtWidgets.QTableWidget(Form)
        self.goal_table.setGeometry(QtCore.QRect(40, 90, 1181, 601))
        self.goal_table.setObjectName("goal_table")
        self.goal_table.setColumnCount(8)
        self.goal_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.goal_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.goal_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.goal_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.goal_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.goal_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.goal_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.goal_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.goal_table.setHorizontalHeaderItem(7, item)
        self.label_13 = QtWidgets.QLabel(Form)
        self.label_13.setGeometry(QtCore.QRect(40, 20, 421, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.acptfact_base_update_combo = QtWidgets.QComboBox(Form)
        self.acptfact_base_update_combo.setGeometry(QtCore.QRect(140, 50, 421, 26))
        self.acptfact_base_update_combo.setObjectName("acptfact_base_update_combo")
        self.acptfact_open = QtWidgets.QLineEdit(Form)
        self.acptfact_open.setGeometry(QtCore.QRect(1020, 60, 71, 31))
        self.acptfact_open.setObjectName("acptfact_open")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(1100, 40, 71, 20))
        self.label_11.setObjectName("label_11")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(30, 50, 81, 20))
        self.label_6.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_6.setObjectName("label_6")
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(1020, 40, 71, 20))
        self.label_10.setObjectName("label_10")
        self.acptfact_nigh = QtWidgets.QLineEdit(Form)
        self.acptfact_nigh.setGeometry(QtCore.QRect(1100, 60, 71, 31))
        self.acptfact_nigh.setObjectName("acptfact_nigh")
        self.acptfact_open_2 = QtWidgets.QLineEdit(Form)
        self.acptfact_open_2.setGeometry(QtCore.QRect(610, 50, 71, 31))
        self.acptfact_open_2.setObjectName("acptfact_open_2")
        self.label_12 = QtWidgets.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(570, 60, 41, 20))
        self.label_12.setObjectName("label_12")
        self.label_14 = QtWidgets.QLabel(Form)
        self.label_14.setGeometry(QtCore.QRect(710, 60, 41, 20))
        self.label_14.setObjectName("label_14")
        self.acptfact_nigh_2 = QtWidgets.QLineEdit(Form)
        self.acptfact_nigh_2.setGeometry(QtCore.QRect(750, 50, 131, 31))
        self.acptfact_nigh_2.setObjectName("acptfact_nigh_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowHandle(_translate("Form", "Form"))
        self.refresh_button.setText(_translate("Form", "Refresh All"))
        self.close_button.setText(_translate("Form", "Close"))
        item = self.goal_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.goal_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "2"))
        item = self.goal_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "3"))
        item = self.goal_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "New Colu4mn"))
        item = self.goal_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "5"))
        item = self.goal_table.horizontalHeaderItem(5)
        item.setText(_translate("Form", "6"))
        item = self.goal_table.horizontalHeaderItem(6)
        item.setText(_translate("Form", "7"))
        item = self.goal_table.horizontalHeaderItem(7)
        item.setText(_translate("Form", "Task Status"))
        self.label_13.setText(
            _translate("Form", "Select what it to be done immediately")
        )
        self.label_11.setText(_translate("Form", "Nigh"))
        self.label_6.setText(_translate("Form", "AcptFact Base:"))
        self.label_10.setText(_translate("Form", "Open"))
        self.label_12.setText(_translate("Form", "Open"))
        self.label_14.setText(_translate("Form", "Nigh"))
