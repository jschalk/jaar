# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\econMainUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1557, 750)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.digests_table = QtWidgets.QTableWidget(self.centralwidget)
        self.digests_table.setGeometry(QtCore.QRect(530, 190, 61, 501))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.digests_table.setFont(font)
        self.digests_table.setObjectName("digests_table")
        self.digests_table.setColumnCount(2)
        self.digests_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.digests_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.digests_table.setHorizontalHeaderItem(1, item)
        self.owner_ids_table = QtWidgets.QTableWidget(self.centralwidget)
        self.owner_ids_table.setGeometry(QtCore.QRect(190, 190, 141, 430))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.owner_ids_table.setFont(font)
        self.owner_ids_table.setObjectName("owner_ids_table")
        self.owner_ids_table.setColumnCount(2)
        self.owner_ids_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.owner_ids_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.owner_ids_table.setHorizontalHeaderItem(1, item)
        self.agendas_table = QtWidgets.QTableWidget(self.centralwidget)
        self.agendas_table.setGeometry(QtCore.QRect(10, 310, 171, 381))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.agendas_table.setFont(font)
        self.agendas_table.setObjectName("agendas_table")
        self.agendas_table.setColumnCount(2)
        self.agendas_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.agendas_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.agendas_table.setHorizontalHeaderItem(1, item)
        self.depotlinks_table = QtWidgets.QTableWidget(self.centralwidget)
        self.depotlinks_table.setGeometry(QtCore.QRect(340, 190, 191, 501))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.depotlinks_table.setFont(font)
        self.depotlinks_table.setObjectName("depotlinks_table")
        self.depotlinks_table.setColumnCount(4)
        self.depotlinks_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.depotlinks_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.depotlinks_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.depotlinks_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.depotlinks_table.setHorizontalHeaderItem(3, item)
        self.econ_delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.econ_delete_button.setGeometry(QtCore.QRect(170, 20, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.econ_delete_button.setFont(font)
        self.econ_delete_button.setObjectName("econ_delete_button")
        self.econ_insert_button = QtWidgets.QPushButton(self.centralwidget)
        self.econ_insert_button.setGeometry(QtCore.QRect(20, 50, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.econ_insert_button.setFont(font)
        self.econ_insert_button.setObjectName("econ_insert_button")
        self.econ_id = QtWidgets.QLineEdit(self.centralwidget)
        self.econ_id.setGeometry(QtCore.QRect(20, 20, 141, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.econ_id.setFont(font)
        self.econ_id.setObjectName("econ_id")
        self.econ_update_button = QtWidgets.QPushButton(self.centralwidget)
        self.econ_update_button.setGeometry(QtCore.QRect(20, 80, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.econ_update_button.setFont(font)
        self.econ_update_button.setObjectName("econ_update_button")
        self.agenda_update_button = QtWidgets.QPushButton(self.centralwidget)
        self.agenda_update_button.setGeometry(QtCore.QRect(10, 240, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.agenda_update_button.setFont(font)
        self.agenda_update_button.setObjectName("agenda_update_button")
        self.agenda_insert_button = QtWidgets.QPushButton(self.centralwidget)
        self.agenda_insert_button.setGeometry(QtCore.QRect(10, 210, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.agenda_insert_button.setFont(font)
        self.agenda_insert_button.setObjectName("agenda_insert_button")
        self.agenda_delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.agenda_delete_button.setGeometry(QtCore.QRect(80, 270, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.agenda_delete_button.setFont(font)
        self.agenda_delete_button.setObjectName("agenda_delete_button")
        self.agenda_owner_id = QtWidgets.QLineEdit(self.centralwidget)
        self.agenda_owner_id.setGeometry(QtCore.QRect(10, 180, 141, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.agenda_owner_id.setFont(font)
        self.agenda_owner_id.setObjectName("agenda_owner_id")
        self.owner_id_update_button = QtWidgets.QPushButton(self.centralwidget)
        self.owner_id_update_button.setGeometry(QtCore.QRect(190, 130, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.owner_id_update_button.setFont(font)
        self.owner_id_update_button.setObjectName("owner_id_update_button")
        self.owner_id_insert_button = QtWidgets.QPushButton(self.centralwidget)
        self.owner_id_insert_button.setGeometry(QtCore.QRect(190, 100, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.owner_id_insert_button.setFont(font)
        self.owner_id_insert_button.setObjectName("owner_id_insert_button")
        self.owner_id_delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.owner_id_delete_button.setGeometry(QtCore.QRect(240, 40, 91, 28))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.owner_id_delete_button.setFont(font)
        self.owner_id_delete_button.setObjectName("owner_id_delete_button")
        self.person_id = QtWidgets.QLineEdit(self.centralwidget)
        self.person_id.setGeometry(QtCore.QRect(190, 70, 141, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.person_id.setFont(font)
        self.person_id.setObjectName("person_id")
        self.depotlink_delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.depotlink_delete_button.setGeometry(QtCore.QRect(480, 20, 101, 28))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.depotlink_delete_button.setFont(font)
        self.depotlink_delete_button.setObjectName("depotlink_delete_button")
        self.depotlink_pid = QtWidgets.QLineEdit(self.centralwidget)
        self.depotlink_pid.setGeometry(QtCore.QRect(340, 20, 141, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.depotlink_pid.setFont(font)
        self.depotlink_pid.setObjectName("depotlink_pid")
        self.depotlink_insert_button = QtWidgets.QPushButton(self.centralwidget)
        self.depotlink_insert_button.setGeometry(QtCore.QRect(376, 50, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.depotlink_insert_button.setFont(font)
        self.depotlink_insert_button.setObjectName("depotlink_insert_button")
        self.depotlink_update_button = QtWidgets.QPushButton(self.centralwidget)
        self.depotlink_update_button.setGeometry(QtCore.QRect(376, 80, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.depotlink_update_button.setFont(font)
        self.depotlink_update_button.setObjectName("depotlink_update_button")
        self.refresh_all_button = QtWidgets.QPushButton(self.centralwidget)
        self.refresh_all_button.setGeometry(QtCore.QRect(530, 90, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.refresh_all_button.setFont(font)
        self.refresh_all_button.setObjectName("refresh_all_button")
        self.agenda_edit_button = QtWidgets.QPushButton(self.centralwidget)
        self.agenda_edit_button.setGeometry(QtCore.QRect(10, 270, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.agenda_edit_button.setFont(font)
        self.agenda_edit_button.setObjectName("agenda_edit_button")
        self.owner_id_edit_button = QtWidgets.QPushButton(self.centralwidget)
        self.owner_id_edit_button.setGeometry(QtCore.QRect(190, 160, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.owner_id_edit_button.setFont(font)
        self.owner_id_edit_button.setObjectName("owner_id_edit_button")
        self.depotlink_edit_button = QtWidgets.QPushButton(self.centralwidget)
        self.depotlink_edit_button.setGeometry(QtCore.QRect(340, 160, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.depotlink_edit_button.setFont(font)
        self.depotlink_edit_button.setObjectName("depotlink_edit_button")
        self.w_intent_table = QtWidgets.QTableWidget(self.centralwidget)
        self.w_intent_table.setGeometry(QtCore.QRect(1180, 260, 371, 431))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.w_intent_table.setFont(font)
        self.w_intent_table.setObjectName("w_intent_table")
        self.w_intent_table.setColumnCount(3)
        self.w_intent_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.w_intent_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_intent_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_intent_table.setHorizontalHeaderItem(2, item)
        self.w_partys_table = QtWidgets.QTableWidget(self.centralwidget)
        self.w_partys_table.setGeometry(QtCore.QRect(1000, 10, 171, 241))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.w_partys_table.setFont(font)
        self.w_partys_table.setObjectName("w_partys_table")
        self.w_partys_table.setColumnCount(3)
        self.w_partys_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.w_partys_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_partys_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_partys_table.setHorizontalHeaderItem(2, item)
        self.w_groups_table = QtWidgets.QTableWidget(self.centralwidget)
        self.w_groups_table.setGeometry(QtCore.QRect(1000, 260, 171, 431))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.w_groups_table.setFont(font)
        self.w_groups_table.setObjectName("w_groups_table")
        self.w_groups_table.setColumnCount(3)
        self.w_groups_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.w_groups_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_groups_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_groups_table.setHorizontalHeaderItem(2, item)
        self.w_ideas_table = QtWidgets.QTableWidget(self.centralwidget)
        self.w_ideas_table.setGeometry(QtCore.QRect(600, 10, 391, 681))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.w_ideas_table.setFont(font)
        self.w_ideas_table.setObjectName("w_ideas_table")
        self.w_ideas_table.setColumnCount(3)
        self.w_ideas_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.w_ideas_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_ideas_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_ideas_table.setHorizontalHeaderItem(2, item)
        self.w_beliefs_table = QtWidgets.QTableWidget(self.centralwidget)
        self.w_beliefs_table.setGeometry(QtCore.QRect(1180, 10, 371, 241))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.w_beliefs_table.setFont(font)
        self.w_beliefs_table.setObjectName("w_beliefs_table")
        self.w_beliefs_table.setColumnCount(3)
        self.w_beliefs_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.w_beliefs_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_beliefs_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_beliefs_table.setHorizontalHeaderItem(2, item)
        self.econ_id_combo = QtWidgets.QComboBox(self.centralwidget)
        self.econ_id_combo.setGeometry(QtCore.QRect(20, 110, 141, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.econ_id_combo.setFont(font)
        self.econ_id_combo.setObjectName("econ_id_combo")
        self.econ_copy_button = QtWidgets.QPushButton(self.centralwidget)
        self.econ_copy_button.setGeometry(QtCore.QRect(100, 80, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.econ_copy_button.setFont(font)
        self.econ_copy_button.setObjectName("econ_copy_button")
        self.depotlink_type_combo = QtWidgets.QComboBox(self.centralwidget)
        self.depotlink_type_combo.setGeometry(QtCore.QRect(376, 110, 141, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.depotlink_type_combo.setFont(font)
        self.depotlink_type_combo.setObjectName("depotlink_type_combo")
        self.econ_load_button = QtWidgets.QPushButton(self.centralwidget)
        self.econ_load_button.setGeometry(QtCore.QRect(100, 140, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.econ_load_button.setFont(font)
        self.econ_load_button.setObjectName("econ_load_button")
        self.depotlink_weight = QtWidgets.QLineEdit(self.centralwidget)
        self.depotlink_weight.setGeometry(QtCore.QRect(460, 140, 61, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.depotlink_weight.setFont(font)
        self.depotlink_weight.setObjectName("depotlink_weight")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(340, 140, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.ignores_table = QtWidgets.QTableWidget(self.centralwidget)
        self.ignores_table.setGeometry(QtCore.QRect(530, 190, 61, 501))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ignores_table.setFont(font)
        self.ignores_table.setObjectName("ignores_table")
        self.ignores_table.setColumnCount(2)
        self.ignores_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.ignores_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ignores_table.setHorizontalHeaderItem(1, item)
        self.show_digests_button = QtWidgets.QPushButton(self.centralwidget)
        self.show_digests_button.setGeometry(QtCore.QRect(530, 120, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.show_digests_button.setFont(font)
        self.show_digests_button.setObjectName("show_digests_button")
        self.show_ignores_button = QtWidgets.QPushButton(self.centralwidget)
        self.show_ignores_button.setGeometry(QtCore.QRect(530, 140, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.show_ignores_button.setFont(font)
        self.show_ignores_button.setObjectName("show_ignores_button")
        self.open_ignore_button = QtWidgets.QPushButton(self.centralwidget)
        self.open_ignore_button.setGeometry(QtCore.QRect(570, 140, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.open_ignore_button.setFont(font)
        self.open_ignore_button.setObjectName("open_ignore_button")
        self.save_ignore_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_ignore_button.setGeometry(QtCore.QRect(570, 160, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.save_ignore_button.setFont(font)
        self.save_ignore_button.setObjectName("save_ignore_button")
        self.set_job_agenda_button = QtWidgets.QPushButton(self.centralwidget)
        self.set_job_agenda_button.setGeometry(QtCore.QRect(190, 640, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.set_job_agenda_button.setFont(font)
        self.set_job_agenda_button.setObjectName("set_job_agenda_button")
        self.reload_jobs_job_agendas_button = QtWidgets.QPushButton(self.centralwidget)
        self.reload_jobs_job_agendas_button.setGeometry(QtCore.QRect(190, 620, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.reload_jobs_job_agendas_button.setFont(font)
        self.reload_jobs_job_agendas_button.setObjectName(
            "reload_jobs_job_agendas_button"
        )
        self.set_jobs_and_reload_srcs_button = QtWidgets.QPushButton(self.centralwidget)
        self.set_jobs_and_reload_srcs_button.setGeometry(
            QtCore.QRect(190, 660, 141, 21)
        )
        font = QtGui.QFont()
        font.setPointSize(8)
        self.set_jobs_and_reload_srcs_button.setFont(font)
        self.set_jobs_and_reload_srcs_button.setObjectName(
            "set_jobs_and_reload_srcs_button"
        )
        self.role_open_button = QtWidgets.QPushButton(self.centralwidget)
        self.role_open_button.setGeometry(QtCore.QRect(530, 50, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.role_open_button.setFont(font)
        self.role_open_button.setObjectName("role_open_button")
        self.role_save_button = QtWidgets.QPushButton(self.centralwidget)
        self.role_save_button.setGeometry(QtCore.QRect(530, 70, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.role_save_button.setFont(font)
        self.role_save_button.setObjectName("role_save_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1557, 21))
        self.menubar.setObjectName("menubar")
        self.file_menu = QtWidgets.QMenu(self.menubar)
        self.file_menu.setObjectName("file_menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.fm_open = QtWidgets.QAction(MainWindow)
        self.fm_open.setCheckable(False)
        self.fm_open.setObjectName("fm_open")
        self.fm_save = QtWidgets.QAction(MainWindow)
        self.fm_save.setObjectName("fm_save")
        self.save_as = QtWidgets.QAction(MainWindow)
        self.save_as.setObjectName("save_as")
        self.fm_new = QtWidgets.QAction(MainWindow)
        self.fm_new.setObjectName("fm_new")
        self.file_menu.addAction(self.fm_new)
        self.file_menu.addAction(self.fm_open)
        self.file_menu.addAction(self.fm_save)
        self.file_menu.addAction(self.save_as)
        self.menubar.addAction(self.file_menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.digests_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Digest"))
        item = self.owner_ids_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "owner_ids"))
        item = self.agendas_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "econ Stories"))
        item = self.depotlinks_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Agendalinks"))
        item = self.depotlinks_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Weight"))
        item = self.depotlinks_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Type"))
        self.econ_delete_button.setText(_translate("MainWindow", "delete "))
        self.econ_insert_button.setText(_translate("MainWindow", "Add new econ"))
        self.econ_update_button.setText(_translate("MainWindow", "Change PID"))
        self.agenda_update_button.setText(_translate("MainWindow", "Change Agenda PID"))
        self.agenda_insert_button.setText(_translate("MainWindow", "Add new Agenda"))
        self.agenda_delete_button.setText(_translate("MainWindow", "Delete"))
        self.owner_id_update_button.setText(
            _translate("MainWindow", "Change owner_id PID")
        )
        self.owner_id_insert_button.setText(
            _translate("MainWindow", "Add new owner_id")
        )
        self.owner_id_delete_button.setText(_translate("MainWindow", "delete owner_id"))
        self.depotlink_delete_button.setText(_translate("MainWindow", "delete Agenda"))
        self.depotlink_insert_button.setText(_translate("MainWindow", "Add new Agenda"))
        self.depotlink_update_button.setText(_translate("MainWindow", "Update Agenda"))
        self.refresh_all_button.setText(_translate("MainWindow", "refresh"))
        self.agenda_edit_button.setText(_translate("MainWindow", "Edit "))
        self.owner_id_edit_button.setText(_translate("MainWindow", "Edit owner_id"))
        self.depotlink_edit_button.setText(_translate("MainWindow", "Edit Agenda"))
        item = self.w_intent_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "owner_ids Agenda"))
        item = self.w_intent_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.w_partys_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "owner_ids Partys"))
        item = self.w_partys_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.w_groups_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "owner_ids Groups"))
        item = self.w_groups_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.w_ideas_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "owner_id Ideas"))
        item = self.w_ideas_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Idea parent_road"))
        item = self.w_beliefs_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Beliefs Base"))
        item = self.w_beliefs_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Beliefs Belief"))
        self.econ_copy_button.setText(_translate("MainWindow", "Copy"))
        self.econ_load_button.setText(_translate("MainWindow", "load"))
        self.label.setText(_translate("MainWindow", "Agendalink Weight:"))
        item = self.ignores_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Ignore"))
        self.show_digests_button.setText(_translate("MainWindow", "digest"))
        self.show_ignores_button.setText(_translate("MainWindow", "ignore"))
        self.open_ignore_button.setText(_translate("MainWindow", "o"))
        self.save_ignore_button.setText(_translate("MainWindow", "s"))
        self.set_job_agenda_button.setText(
            _translate("MainWindow", "output_agenda to jobs_dir")
        )
        self.reload_jobs_job_agendas_button.setText(
            _translate("MainWindow", "refresh_job_agendas")
        )
        self.set_jobs_and_reload_srcs_button.setText(
            _translate("MainWindow", "dest2jobs and refresh")
        )
        self.role_open_button.setText(_translate("MainWindow", "role"))
        self.role_save_button.setText(_translate("MainWindow", "save"))
        self.menubar.setAccessibleName(_translate("MainWindow", "File"))
        self.menubar.setAccessibleDescription(
            _translate("MainWindow", "General Operations")
        )
        self.file_menu.setTitle(_translate("MainWindow", "File"))
        self.fm_open.setText(_translate("MainWindow", "Open"))
        self.fm_save.setText(_translate("MainWindow", "Save"))
        self.save_as.setText(_translate("MainWindow", "Save as..."))
        self.fm_new.setText(_translate("MainWindow", "New"))