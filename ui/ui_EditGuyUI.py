# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\EditGuyUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual modifications made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1289, 712)
        self.guy_gui_insert_button = QtWidgets.QPushButton(Form)
        self.guy_gui_insert_button.setGeometry(QtCore.QRect(500, 70, 171, 21))
        self.guy_gui_insert_button.setObjectName("guy_gui_insert_button")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(500, 300, 171, 20))
        self.label.setObjectName("label")
        self.guy_update_button = QtWidgets.QPushButton(Form)
        self.guy_update_button.setGeometry(QtCore.QRect(500, 170, 181, 28))
        self.guy_update_button.setObjectName("guy_update_button")
        self.guy_id_edit = QtWidgets.QLineEdit(Form)
        self.guy_id_edit.setGeometry(QtCore.QRect(500, 140, 181, 22))
        self.guy_id_edit.setObjectName("guy_id_edit")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(500, 120, 161, 21))
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.guy_delete_button = QtWidgets.QPushButton(Form)
        self.guy_delete_button.setGeometry(QtCore.QRect(570, 230, 111, 28))
        self.guy_delete_button.setObjectName("guy_delete_button")
        self.guy = QtWidgets.QTableWidget(Form)
        self.guy.setGeometry(QtCore.QRect(10, 40, 481, 631))
        self.guy.setObjectName("guy")
        self.guy.setColumnCount(5)
        self.guy.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.guy.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.guy.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.guy.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.guy.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.guy.setHorizontalHeaderItem(4, item)
        self.close_button = QtWidgets.QPushButton(Form)
        self.close_button.setGeometry(QtCore.QRect(1160, 10, 93, 28))
        self.close_button.setObjectName("close_button")
        self.quit_button = QtWidgets.QPushButton(Form)
        self.quit_button.setGeometry(QtCore.QRect(1060, 10, 93, 28))
        self.quit_button.setObjectName("quit_button")
        self.guy_id_new = QtWidgets.QLineEdit(Form)
        self.guy_id_new.setGeometry(QtCore.QRect(500, 40, 171, 22))
        self.guy_id_new.setObjectName("guy_id_new")
        self.guy2guyFalse = QtWidgets.QTableWidget(Form)
        self.guy2guyFalse.setGeometry(QtCore.QRect(1120, 40, 131, 631))
        self.guy2guyFalse.setObjectName("guy2guyFalse")
        self.guy2guyFalse.setColumnCount(4)
        self.guy2guyFalse.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.guy2guyFalse.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.guy2guyFalse.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.guy2guyFalse.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.guy2guyFalse.setHorizontalHeaderItem(3, item)
        self.guy2guyTrue = QtWidgets.QTableWidget(Form)
        self.guy2guyTrue.setGeometry(QtCore.QRect(690, 40, 421, 631))
        self.guy2guyTrue.setObjectName("guy2guyTrue")
        self.guy2guyTrue.setColumnCount(7)
        self.guy2guyTrue.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.guy2guyTrue.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.guy2guyTrue.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.guy2guyTrue.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.guy2guyTrue.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.guy2guyTrue.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.guy2guyTrue.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.guy2guyTrue.setHorizontalHeaderItem(6, item)
        self.edit_belief_button = QtWidgets.QPushButton(Form)
        self.edit_belief_button.setGeometry(QtCore.QRect(500, 320, 181, 31))
        self.edit_belief_button.setObjectName("edit_belief_button")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 680, 47, 13))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.guy_gui_insert_button.setText(_translate("Form", "Add new Guy"))
        self.label.setText(_translate("Form", "Click to see Belief guyship"))
        self.guy_update_button.setText(_translate("Form", "update old guy pid to new"))
        self.label_3.setText(_translate("Form", "Modification PID to:"))
        self.guy_delete_button.setText(_translate("Form", "delete Guy"))
        item = self.guy.horizontalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.guy.horizontalHeaderItem(1)
        item.setText(_translate("Form", "2"))
        item = self.guy.horizontalHeaderItem(2)
        item.setText(_translate("Form", "3"))
        item = self.guy.horizontalHeaderItem(3)
        item.setText(_translate("Form", "4"))
        item = self.guy.horizontalHeaderItem(4)
        item.setText(_translate("Form", "5"))
        self.close_button.setText(_translate("Form", "Close"))
        self.quit_button.setText(_translate("Form", "Quit App"))
        item = self.guy2guyFalse.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Source"))
        item = self.guy2guyFalse.horizontalHeaderItem(1)
        item.setText(_translate("Form", "They do not know..."))
        item = self.guy2guyFalse.horizontalHeaderItem(2)
        item.setText(_translate("Form", "guy_id_source"))
        item = self.guy2guyFalse.horizontalHeaderItem(3)
        item.setText(_translate("Form", "guy_id_target"))
        item = self.guy2guyTrue.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Source"))
        item = self.guy2guyTrue.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Who they know..."))
        item = self.guy2guyTrue.horizontalHeaderItem(2)
        item.setText(_translate("Form", "guy_id_source"))
        item = self.guy2guyTrue.horizontalHeaderItem(3)
        item.setText(_translate("Form", "guy_id_target"))
        item = self.guy2guyTrue.horizontalHeaderItem(4)
        item.setText(_translate("Form", "weight"))
        item = self.guy2guyTrue.horizontalHeaderItem(5)
        item.setText(_translate("Form", "relative_weight"))
        item = self.guy2guyTrue.horizontalHeaderItem(6)
        item.setText(_translate("Form", "guy_id_for_target"))
        self.edit_belief_button.setText(_translate("Form", "Edit Belief Guyship"))
        self.label_2.setText(_translate("Form", "guy_id ="))
