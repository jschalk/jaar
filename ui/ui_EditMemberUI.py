# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\EditPartyUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1289, 712)
        self.party_insert_button = QtWidgets.QPushButton(Form)
        self.party_insert_button.setGeometry(QtCore.QRect(500, 70, 171, 21))
        self.party_insert_button.setObjectName("party_insert_button")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(500, 300, 171, 20))
        self.label.setObjectName("label")
        self.party_update_button = QtWidgets.QPushButton(Form)
        self.party_update_button.setGeometry(QtCore.QRect(500, 170, 181, 28))
        self.party_update_button.setObjectName("party_update_button")
        self.party_name_edit = QtWidgets.QLineEdit(Form)
        self.party_name_edit.setGeometry(QtCore.QRect(500, 140, 181, 22))
        self.party_name_edit.setObjectName("party_name_edit")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(500, 120, 161, 21))
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.party_delete_button = QtWidgets.QPushButton(Form)
        self.party_delete_button.setGeometry(QtCore.QRect(570, 230, 111, 28))
        self.party_delete_button.setObjectName("party_delete_button")
        self.party = QtWidgets.QTableWidget(Form)
        self.party.setGeometry(QtCore.QRect(10, 40, 481, 631))
        self.party.setObjectName("party")
        self.party.setColumnCount(5)
        self.party.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.party.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.party.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.party.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.party.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.party.setHorizontalHeaderItem(4, item)
        self.close_button = QtWidgets.QPushButton(Form)
        self.close_button.setGeometry(QtCore.QRect(1160, 10, 93, 28))
        self.close_button.setObjectName("close_button")
        self.quit_button = QtWidgets.QPushButton(Form)
        self.quit_button.setGeometry(QtCore.QRect(1060, 10, 93, 28))
        self.quit_button.setObjectName("quit_button")
        self.party_name_new = QtWidgets.QLineEdit(Form)
        self.party_name_new.setGeometry(QtCore.QRect(500, 40, 171, 22))
        self.party_name_new.setObjectName("party_name_new")
        self.party2partyFalse = QtWidgets.QTableWidget(Form)
        self.party2partyFalse.setGeometry(QtCore.QRect(1120, 40, 131, 631))
        self.party2partyFalse.setObjectName("party2partyFalse")
        self.party2partyFalse.setColumnCount(4)
        self.party2partyFalse.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.party2partyFalse.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.party2partyFalse.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.party2partyFalse.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.party2partyFalse.setHorizontalHeaderItem(3, item)
        self.party2partyTrue = QtWidgets.QTableWidget(Form)
        self.party2partyTrue.setGeometry(QtCore.QRect(690, 40, 421, 631))
        self.party2partyTrue.setObjectName("party2partyTrue")
        self.party2partyTrue.setColumnCount(7)
        self.party2partyTrue.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.party2partyTrue.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.party2partyTrue.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.party2partyTrue.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.party2partyTrue.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.party2partyTrue.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.party2partyTrue.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.party2partyTrue.setHorizontalHeaderItem(6, item)
        self.edit_group_button = QtWidgets.QPushButton(Form)
        self.edit_group_button.setGeometry(QtCore.QRect(500, 320, 181, 31))
        self.edit_group_button.setObjectName("edit_group_button")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 680, 47, 13))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.party_insert_button.setText(_translate("Form", "Add new Party"))
        self.label.setText(_translate("Form", "Click to see Group partyship"))
        self.party_update_button.setText(
            _translate("Form", "update old party name to new")
        )
        self.label_3.setText(_translate("Form", "Change Name to:"))
        self.party_delete_button.setText(_translate("Form", "delete Party"))
        item = self.party.horizontalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.party.horizontalHeaderItem(1)
        item.setText(_translate("Form", "2"))
        item = self.party.horizontalHeaderItem(2)
        item.setText(_translate("Form", "3"))
        item = self.party.horizontalHeaderItem(3)
        item.setText(_translate("Form", "4"))
        item = self.party.horizontalHeaderItem(4)
        item.setText(_translate("Form", "5"))
        self.close_button.setText(_translate("Form", "Close"))
        self.quit_button.setText(_translate("Form", "Quit App"))
        item = self.party2partyFalse.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Source"))
        item = self.party2partyFalse.horizontalHeaderItem(1)
        item.setText(_translate("Form", "They do not know..."))
        item = self.party2partyFalse.horizontalHeaderItem(2)
        item.setText(_translate("Form", "party_id_source"))
        item = self.party2partyFalse.horizontalHeaderItem(3)
        item.setText(_translate("Form", "party_id_target"))
        item = self.party2partyTrue.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Source"))
        item = self.party2partyTrue.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Who they know..."))
        item = self.party2partyTrue.horizontalHeaderItem(2)
        item.setText(_translate("Form", "party_id_source"))
        item = self.party2partyTrue.horizontalHeaderItem(3)
        item.setText(_translate("Form", "party_id_target"))
        item = self.party2partyTrue.horizontalHeaderItem(4)
        item.setText(_translate("Form", "weight"))
        item = self.party2partyTrue.horizontalHeaderItem(5)
        item.setText(_translate("Form", "relative_weight"))
        item = self.party2partyTrue.horizontalHeaderItem(6)
        item.setText(_translate("Form", "huh_name_for_target"))
        self.edit_group_button.setText(_translate("Form", "Edit Group Partyship"))
        self.label_2.setText(_translate("Form", "party_id ="))
