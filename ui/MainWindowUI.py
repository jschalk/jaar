# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\MainWindowUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual modifications made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1693, 878)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.editmain_button = QtWidgets.QPushButton(self.centralwidget)
        self.editmain_button.setGeometry(QtCore.QRect(390, 270, 201, 30))
        self.editmain_button.setObjectName("editmain_button")
        self.belief_open_lower_spec1 = QtWidgets.QPushButton(self.centralwidget)
        self.belief_open_lower_spec1.setGeometry(QtCore.QRect(200, 190, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.belief_open_lower_spec1.setFont(font)
        self.belief_open_lower_spec1.setObjectName("belief_open_lower_spec1")
        self.belief_nigh_now = QtWidgets.QPushButton(self.centralwidget)
        self.belief_nigh_now.setGeometry(QtCore.QRect(30, 170, 281, 21))
        self.belief_nigh_now.setObjectName("belief_nigh_now")
        self.intent_task_complete = QtWidgets.QPushButton(self.centralwidget)
        self.intent_task_complete.setGeometry(QtCore.QRect(30, 270, 221, 30))
        self.intent_task_complete.setObjectName("intent_task_complete")
        self.root_datetime_prev_l = QtWidgets.QLabel(self.centralwidget)
        self.root_datetime_prev_l.setGeometry(QtCore.QRect(30, 50, 971, 51))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.root_datetime_prev_l.setFont(font)
        self.root_datetime_prev_l.setObjectName("root_datetime_prev_l")
        self.root_datetime_now_l = QtWidgets.QLabel(self.centralwidget)
        self.root_datetime_now_l.setGeometry(QtCore.QRect(30, 120, 981, 51))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.root_datetime_now_l.setFont(font)
        self.root_datetime_now_l.setObjectName("root_datetime_now_l")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 100, 141, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 30, 181, 16))
        self.label_3.setObjectName("label_3")
        self.label_intent_label_header = QtWidgets.QLabel(self.centralwidget)
        self.label_intent_label_header.setGeometry(QtCore.QRect(30, 340, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_intent_label_header.setFont(font)
        self.label_intent_label_header.setObjectName("label_intent_label_header")
        self.root_datetime_view = QtWidgets.QPushButton(self.centralwidget)
        self.root_datetime_view.setGeometry(QtCore.QRect(590, 170, 151, 41))
        self.root_datetime_view.setObjectName("root_datetime_view")
        self.loubby_button = QtWidgets.QPushButton(self.centralwidget)
        self.loubby_button.setGeometry(QtCore.QRect(380, 810, 201, 24))
        self.loubby_button.setObjectName("loubby_button")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(130, 840, 331, 16))
        self.label_7.setObjectName("label_7")
        self.cb_update_now_repeat = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_update_now_repeat.setGeometry(QtCore.QRect(30, 220, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.cb_update_now_repeat.setFont(font)
        self.cb_update_now_repeat.setObjectName("cb_update_now_repeat")
        self.label_time_display = QtWidgets.QLabel(self.centralwidget)
        self.label_time_display.setGeometry(QtCore.QRect(30, 210, 261, 16))
        self.label_time_display.setObjectName("label_time_display")
        self.edit_intent_button = QtWidgets.QPushButton(self.centralwidget)
        self.edit_intent_button.setGeometry(QtCore.QRect(250, 270, 141, 30))
        self.edit_intent_button.setObjectName("edit_intent_button")
        self.beliefs_table = QtWidgets.QTableWidget(self.centralwidget)
        self.beliefs_table.setGeometry(QtCore.QRect(1270, 390, 391, 461))
        self.beliefs_table.setObjectName("beliefs_table")
        self.beliefs_table.setColumnCount(6)
        self.beliefs_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.beliefs_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.beliefs_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.beliefs_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.beliefs_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.beliefs_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.beliefs_table.setHorizontalHeaderItem(5, item)
        self.agenda_l = QtWidgets.QLabel(self.centralwidget)
        self.agenda_l.setGeometry(QtCore.QRect(30, 10, 91, 16))
        self.agenda_l.setObjectName("agenda_l")
        self.agenda_label_update_button = QtWidgets.QPushButton(self.centralwidget)
        self.agenda_label_update_button.setGeometry(QtCore.QRect(310, 10, 101, 21))
        self.agenda_label_update_button.setObjectName("agenda_label_update_button")
        self.agenda_owner_id = QtWidgets.QLineEdit(self.centralwidget)
        self.agenda_owner_id.setGeometry(QtCore.QRect(100, 10, 201, 22))
        self.agenda_owner_id.setObjectName("agenda_owner_id")
        self.label_intent_day_header = QtWidgets.QLabel(self.centralwidget)
        self.label_intent_day_header.setGeometry(QtCore.QRect(30, 500, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_intent_day_header.setFont(font)
        self.label_intent_day_header.setObjectName("label_intent_day_header")
        self.label_intent_time_header = QtWidgets.QLabel(self.centralwidget)
        self.label_intent_time_header.setGeometry(QtCore.QRect(30, 560, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_intent_time_header.setFont(font)
        self.label_intent_time_header.setObjectName("label_intent_time_header")
        self.label_intent_end_header = QtWidgets.QLabel(self.centralwidget)
        self.label_intent_end_header.setGeometry(QtCore.QRect(30, 610, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_intent_end_header.setFont(font)
        self.label_intent_end_header.setObjectName("label_intent_end_header")
        self.label_intent_agenda_importance_header1 = QtWidgets.QLabel(
            self.centralwidget
        )
        self.label_intent_agenda_importance_header1.setGeometry(
            QtCore.QRect(30, 640, 91, 31)
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_intent_agenda_importance_header1.setFont(font)
        self.label_intent_agenda_importance_header1.setObjectName(
            "label_intent_agenda_importance_header1"
        )
        self.label_intent_family_header1 = QtWidgets.QLabel(self.centralwidget)
        self.label_intent_family_header1.setGeometry(QtCore.QRect(30, 700, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_intent_family_header1.setFont(font)
        self.label_intent_family_header1.setObjectName("label_intent_family_header1")
        self.label_intent_road_header = QtWidgets.QLabel(self.centralwidget)
        self.label_intent_road_header.setGeometry(QtCore.QRect(30, 320, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_intent_road_header.setFont(font)
        self.label_intent_road_header.setObjectName("label_intent_road_header")
        self.label_intent_label_data = QtWidgets.QLabel(self.centralwidget)
        self.label_intent_label_data.setGeometry(QtCore.QRect(150, 340, 861, 71))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label_intent_label_data.setFont(font)
        self.label_intent_label_data.setText("")
        self.label_intent_label_data.setWordWrap(True)
        self.label_intent_label_data.setObjectName("label_intent_label_data")
        self.label_intent_family_header2 = QtWidgets.QLabel(self.centralwidget)
        self.label_intent_family_header2.setGeometry(QtCore.QRect(30, 720, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_intent_family_header2.setFont(font)
        self.label_intent_family_header2.setObjectName("label_intent_family_header2")
        self.label_intent_agenda_importance_header2 = QtWidgets.QLabel(
            self.centralwidget
        )
        self.label_intent_agenda_importance_header2.setGeometry(
            QtCore.QRect(30, 660, 101, 31)
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_intent_agenda_importance_header2.setFont(font)
        self.label_intent_agenda_importance_header2.setObjectName(
            "label_intent_agenda_importance_header2"
        )
        self.label_intent_road_data = QtWidgets.QLabel(self.centralwidget)
        self.label_intent_road_data.setGeometry(QtCore.QRect(80, 330, 561, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_intent_road_data.setFont(font)
        self.label_intent_road_data.setObjectName("label_intent_road_data")
        self.label_intent_family_data = QtWidgets.QLabel(self.centralwidget)
        self.label_intent_family_data.setGeometry(QtCore.QRect(130, 710, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_intent_family_data.setFont(font)
        self.label_intent_family_data.setObjectName("label_intent_family_data")
        self.label_intent_agenda_importance_data = QtWidgets.QLabel(self.centralwidget)
        self.label_intent_agenda_importance_data.setGeometry(
            QtCore.QRect(130, 650, 221, 41)
        )
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_intent_agenda_importance_data.setFont(font)
        self.label_intent_agenda_importance_data.setObjectName(
            "label_intent_agenda_importance_data"
        )
        self.label_intent_end_data = QtWidgets.QLabel(self.centralwidget)
        self.label_intent_end_data.setGeometry(QtCore.QRect(130, 610, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_intent_end_data.setFont(font)
        self.label_intent_end_data.setObjectName("label_intent_end_data")
        self.label_intent_time_data = QtWidgets.QLabel(self.centralwidget)
        self.label_intent_time_data.setGeometry(QtCore.QRect(130, 560, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_intent_time_data.setFont(font)
        self.label_intent_time_data.setObjectName("label_intent_time_data")
        self.label_intent_day_data = QtWidgets.QLabel(self.centralwidget)
        self.label_intent_day_data.setGeometry(QtCore.QRect(130, 500, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_intent_day_data.setFont(font)
        self.label_intent_day_data.setObjectName("label_intent_day_data")
        self.update_now_time = QtWidgets.QComboBox(self.centralwidget)
        self.update_now_time.setGeometry(QtCore.QRect(280, 230, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.update_now_time.setFont(font)
        self.update_now_time.setObjectName("update_now_time")
        self.belief_open_soft_spec1 = QtWidgets.QPushButton(self.centralwidget)
        self.belief_open_soft_spec1.setGeometry(QtCore.QRect(380, 190, 211, 21))
        self.belief_open_soft_spec1.setObjectName("belief_open_soft_spec1")
        self.intent_states = QtWidgets.QTableWidget(self.centralwidget)
        self.intent_states.setGeometry(QtCore.QRect(1020, 30, 641, 351))
        self.intent_states.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.intent_states.setObjectName("intent_states")
        self.intent_states.setColumnCount(8)
        self.intent_states.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.intent_states.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.intent_states.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.intent_states.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.intent_states.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.intent_states.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.intent_states.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.intent_states.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.intent_states.setHorizontalHeaderItem(7, item)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(430, 840, 331, 20))
        self.label_8.setObjectName("label_8")
        self.belief_open_5daysago = QtWidgets.QPushButton(self.centralwidget)
        self.belief_open_5daysago.setGeometry(QtCore.QRect(30, 190, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.belief_open_5daysago.setFont(font)
        self.belief_open_5daysago.setObjectName("belief_open_5daysago")
        self.label_last_label = QtWidgets.QLabel(self.centralwidget)
        self.label_last_label.setGeometry(QtCore.QRect(120, 300, 891, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_last_label.setFont(font)
        self.label_last_label.setText("")
        self.label_last_label.setObjectName("label_last_label")
        self.label_last_burb = QtWidgets.QLabel(self.centralwidget)
        self.label_last_burb.setGeometry(QtCore.QRect(30, 300, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_last_burb.setFont(font)
        self.label_last_burb.setObjectName("label_last_burb")
        self.operating_file_path_l = QtWidgets.QLabel(self.centralwidget)
        self.operating_file_path_l.setGeometry(QtCore.QRect(540, 10, 471, 20))
        self.operating_file_path_l.setText("")
        self.operating_file_path_l.setObjectName("operating_file_path_l")
        self.save_close_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_close_button.setGeometry(QtCore.QRect(420, 10, 111, 21))
        self.save_close_button.setObjectName("save_close_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1693, 21))
        self.menubar.setObjectName("menubar")
        self.file_menu = QtWidgets.QMenu(self.menubar)
        self.file_menu.setTitle("")
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
        MainWindow.setProperty("windowkind", _translate("MainWindow", "MainWindow"))
        self.editmain_button.setText(
            _translate("MainWindow", "Agendas /  Party /  dimension")
        )
        self.belief_open_lower_spec1.setText(
            _translate("MainWindow", "set minutes next midnight")
        )
        self.belief_nigh_now.setText(_translate("MainWindow", "Update nigh to Now"))
        self.intent_task_complete.setText(_translate("MainWindow", "Complete pledge"))
        self.root_datetime_prev_l.setText(_translate("MainWindow", "Past:"))
        self.root_datetime_now_l.setText(_translate("MainWindow", "Now:"))
        self.label_2.setText(_translate("MainWindow", "What is your present?"))
        self.label_3.setText(
            _translate("MainWindow", "When is the past you have not let go?")
        )
        self.label_intent_label_header.setText(_translate("MainWindow", "Label"))
        self.root_datetime_view.setText(
            _translate("MainWindow", "Manuparty modification")
        )
        self.loubby_button.setText(_translate("MainWindow", "Request Someone"))
        self.label_7.setText(
            _translate("MainWindow", "Who you are right now. What's missing...")
        )
        self.cb_update_now_repeat.setText(_translate("MainWindow", "Update now per"))
        self.label_time_display.setText(_translate("MainWindow", "Current Time:"))
        self.edit_intent_button.setText(_translate("MainWindow", "view current intent"))
        item = self.beliefs_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "BeliefBase"))
        item = self.beliefs_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "BeliefPick"))
        item = self.beliefs_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Base"))
        item = self.beliefs_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Pick"))
        item = self.beliefs_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Open"))
        item = self.beliefs_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Close"))
        self.agenda_l.setText(_translate("MainWindow", "AGENDA: "))
        self.agenda_label_update_button.setText(_translate("MainWindow", "Update"))
        self.label_intent_day_header.setText(_translate("MainWindow", "Day:"))
        self.label_intent_time_header.setText(_translate("MainWindow", "Time:"))
        self.label_intent_end_header.setText(_translate("MainWindow", "End:"))
        self.label_intent_agenda_importance_header1.setText(
            _translate("MainWindow", "root_relative")
        )
        self.label_intent_family_header1.setText(_translate("MainWindow", "Agenda"))
        self.label_intent_road_header.setText(_translate("MainWindow", "RoadUnit:"))
        self.label_intent_family_header2.setText(_translate("MainWindow", "Family:"))
        self.label_intent_agenda_importance_header2.setText(
            _translate("MainWindow", "weight:")
        )
        self.label_intent_road_data.setText(_translate("MainWindow", "Fact_id:"))
        self.label_intent_family_data.setText(_translate("MainWindow", "Agenda"))
        self.label_intent_agenda_importance_data.setText(
            _translate("MainWindow", "weight:")
        )
        self.label_intent_end_data.setText(_translate("MainWindow", "End:"))
        self.label_intent_time_data.setText(_translate("MainWindow", "Time:"))
        self.label_intent_day_data.setText(_translate("MainWindow", "Day:"))
        self.belief_open_soft_spec1.setText(
            _translate("MainWindow", '"Soft" moving up the past')
        )
        item = self.intent_states.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "admiration"))
        item = self.intent_states.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "label"))
        item = self.intent_states.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "agenda_importance"))
        item = self.intent_states.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "fact_road"))
        item = self.intent_states.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "fact_percent"))
        item = self.intent_states.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "jaja_open"))
        item = self.intent_states.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "jaja_nigh"))
        item = self.intent_states.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "range_source_road"))
        self.label_8.setText(
            _translate("MainWindow", "Things you pledged to be right now")
        )
        self.belief_open_5daysago.setText(
            _translate("MainWindow", "Set open 5 days ago")
        )
        self.label_last_burb.setText(_translate("MainWindow", "Last Complete:"))
        self.save_close_button.setText(_translate("MainWindow", "Save And Close"))
        self.menubar.setAccessibleDescription(
            _translate("MainWindow", "General Operations")
        )
        self.menubar.setProperty("accessiblePID", _translate("MainWindow", "File"))
        self.file_menu.setProperty("kind", _translate("MainWindow", "File"))
        self.fm_open.setText(_translate("MainWindow", "Open"))
        self.fm_save.setText(_translate("MainWindow", "Save"))
        self.save_as.setText(_translate("MainWindow", "Save as..."))
        self.fm_new.setText(_translate("MainWindow", "New"))
