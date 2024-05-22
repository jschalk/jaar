# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1682, 914)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(730, 365, 55, 16))
        self.label.setObjectName("label")
        self.settings_button = QtWidgets.QPushButton(self.centralwidget)
        self.settings_button.setGeometry(QtCore.QRect(720, 335, 93, 28))
        self.settings_button.setObjectName("settings_button")
        self.editmain_button = QtWidgets.QPushButton(self.centralwidget)
        self.editmain_button.setGeometry(QtCore.QRect(390, 270, 201, 30))
        self.editmain_button.setObjectName("editmain_button")
        self.root_datetime_prev_update = QtWidgets.QPushButton(self.centralwidget)
        self.root_datetime_prev_update.setGeometry(QtCore.QRect(30, 190, 281, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.root_datetime_prev_update.setFont(font)
        self.root_datetime_prev_update.setObjectName("root_datetime_prev_update")
        self.root_datetime_now_update = QtWidgets.QPushButton(self.centralwidget)
        self.root_datetime_now_update.setGeometry(QtCore.QRect(30, 170, 281, 21))
        self.root_datetime_now_update.setObjectName("root_datetime_now_update")
        self.intent_task_complete = QtWidgets.QPushButton(self.centralwidget)
        self.intent_task_complete.setGeometry(QtCore.QRect(30, 270, 221, 30))
        self.intent_task_complete.setObjectName("intent_task_complete")
        self.root_datetime_prev_l = QtWidgets.QLabel(self.centralwidget)
        self.root_datetime_prev_l.setGeometry(QtCore.QRect(30, 50, 1161, 51))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.root_datetime_prev_l.setFont(font)
        self.root_datetime_prev_l.setObjectName("root_datetime_prev_l")
        self.root_datetime_now_l = QtWidgets.QLabel(self.centralwidget)
        self.root_datetime_now_l.setGeometry(QtCore.QRect(30, 120, 1161, 51))
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
        self.label_intent_deescription_header = QtWidgets.QLabel(self.centralwidget)
        self.label_intent_deescription_header.setGeometry(
            QtCore.QRect(30, 310, 141, 41)
        )
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_intent_deescription_header.setFont(font)
        self.label_intent_deescription_header.setObjectName(
            "label_intent_deescription_header"
        )
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(470, 400, 141, 20))
        self.label_5.setObjectName("label_5")
        self.root_datetime_view = QtWidgets.QPushButton(self.centralwidget)
        self.root_datetime_view.setGeometry(QtCore.QRect(590, 170, 151, 41))
        self.root_datetime_view.setObjectName("root_datetime_view")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(720, 315, 93, 21))
        self.pushButton_2.setObjectName("pushButton_2")
        self.loubby_button = QtWidgets.QPushButton(self.centralwidget)
        self.loubby_button.setGeometry(QtCore.QRect(600, 270, 201, 24))
        self.loubby_button.setObjectName("loubby_button")
        self.completeness_status = QtWidgets.QTableWidget(self.centralwidget)
        self.completeness_status.setGeometry(QtCore.QRect(850, 210, 331, 181))
        self.completeness_status.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.completeness_status.setObjectName("completeness_status")
        self.completeness_status.setColumnCount(8)
        self.completeness_status.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.completeness_status.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.completeness_status.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.completeness_status.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.completeness_status.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.completeness_status.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.completeness_status.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.completeness_status.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.completeness_status.setHorizontalHeaderItem(7, item)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(860, 180, 331, 16))
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
        self.now_intent = QtWidgets.QPushButton(self.centralwidget)
        self.now_intent.setGeometry(QtCore.QRect(250, 270, 141, 30))
        self.now_intent.setObjectName("now_intent")
        self.beliefs_table = QtWidgets.QTableWidget(self.centralwidget)
        self.beliefs_table.setGeometry(QtCore.QRect(380, 480, 821, 331))
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
        self.label_intent_idea_id_header = QtWidgets.QLabel(self.centralwidget)
        self.label_intent_idea_id_header.setGeometry(QtCore.QRect(30, 750, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_intent_idea_id_header.setFont(font)
        self.label_intent_idea_id_header.setObjectName("label_intent_idea_id_header")
        self.label_intent_deescription_data = QtWidgets.QLabel(self.centralwidget)
        self.label_intent_deescription_data.setGeometry(QtCore.QRect(80, 350, 681, 71))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label_intent_deescription_data.setFont(font)
        self.label_intent_deescription_data.setText("")
        self.label_intent_deescription_data.setWordWrap(True)
        self.label_intent_deescription_data.setObjectName(
            "label_intent_deescription_data"
        )
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
        self.label_intent_idea_id_data = QtWidgets.QLabel(self.centralwidget)
        self.label_intent_idea_id_data.setGeometry(QtCore.QRect(130, 750, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_intent_idea_id_data.setFont(font)
        self.label_intent_idea_id_data.setObjectName("label_intent_idea_id_data")
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
        self.belief_base_update_combo = QtWidgets.QComboBox(self.centralwidget)
        self.belief_base_update_combo.setGeometry(QtCore.QRect(460, 420, 421, 26))
        self.belief_base_update_combo.setObjectName("belief_base_update_combo")
        self.root_datetime_prev_upd_soft = QtWidgets.QPushButton(self.centralwidget)
        self.root_datetime_prev_upd_soft.setGeometry(QtCore.QRect(310, 190, 281, 21))
        self.root_datetime_prev_upd_soft.setObjectName("root_datetime_prev_upd_soft")
        self.intent_states = QtWidgets.QTableWidget(self.centralwidget)
        self.intent_states.setGeometry(QtCore.QRect(1290, 30, 381, 621))
        self.intent_states.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.intent_states.setObjectName("intent_states")
        self.intent_states.setColumnCount(5)
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
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(1300, 10, 331, 20))
        self.label_8.setObjectName("label_8")
        self.belief_belief_update_combo = QtWidgets.QComboBox(self.centralwidget)
        self.belief_belief_update_combo.setGeometry(QtCore.QRect(460, 450, 421, 26))
        self.belief_belief_update_combo.setObjectName("belief_belief_update_combo")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(370, 420, 81, 20))
        self.label_6.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_6.setObjectName("label_6")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(370, 450, 81, 20))
        self.label_9.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_9.setObjectName("label_9")
        self.belief_open = QtWidgets.QLineEdit(self.centralwidget)
        self.belief_open.setGeometry(QtCore.QRect(900, 440, 71, 31))
        self.belief_open.setObjectName("belief_open")
        self.belief_nigh = QtWidgets.QLineEdit(self.centralwidget)
        self.belief_nigh.setGeometry(QtCore.QRect(980, 440, 71, 31))
        self.belief_nigh.setObjectName("belief_nigh")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(900, 420, 71, 20))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(980, 420, 71, 20))
        self.label_11.setObjectName("label_11")
        self.belief_update_button = QtWidgets.QPushButton(self.centralwidget)
        self.belief_update_button.setGeometry(QtCore.QRect(1070, 420, 131, 30))
        self.belief_update_button.setObjectName("belief_update_button")
        self.belief_delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.belief_delete_button.setGeometry(QtCore.QRect(1070, 450, 131, 30))
        self.belief_delete_button.setObjectName("belief_delete_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1682, 26))
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
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.settings_button.setText(_translate("MainWindow", "Settings"))
        self.editmain_button.setText(
            _translate("MainWindow", "Agendas /  Party /  dimension")
        )
        self.root_datetime_prev_update.setText(
            _translate("MainWindow", "Update Lowerbound DateTime to next midnight")
        )
        self.root_datetime_now_update.setText(
            _translate("MainWindow", "Update Present DateTime to Now")
        )
        self.intent_task_complete.setText(_translate("MainWindow", "Complete Promise"))
        self.root_datetime_prev_l.setText(_translate("MainWindow", "Past:"))
        self.root_datetime_now_l.setText(_translate("MainWindow", "Now:"))
        self.label_2.setText(_translate("MainWindow", "What is your present?"))
        self.label_3.setText(
            _translate("MainWindow", "When is the past you have not let go?")
        )
        self.label_intent_deescription_header.setText(
            _translate("MainWindow", "Description")
        )
        self.label_5.setText(_translate("MainWindow", "Change where I am:"))
        self.root_datetime_view.setText(_translate("MainWindow", "Manuparty change"))
        self.pushButton_2.setText(_translate("MainWindow", "Manuparty change"))
        self.loubby_button.setText(_translate("MainWindow", "Request Someone"))
        item = self.completeness_status.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.completeness_status.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Promise Kept"))
        item = self.completeness_status.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Root Relative Weight"))
        item = self.completeness_status.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Completeness %"))
        item = self.completeness_status.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Complete %"))
        item = self.completeness_status.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Incomplete %"))
        item = self.completeness_status.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Node Type"))
        item = self.completeness_status.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Incomplete Weight"))
        self.label_7.setText(
            _translate("MainWindow", "Who you are right now. What's missing...")
        )
        self.cb_update_now_repeat.setText(_translate("MainWindow", "Update now per"))
        self.label_time_display.setText(_translate("MainWindow", "Current Time:"))
        self.now_intent.setText(_translate("MainWindow", "view current intent"))
        item = self.beliefs_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "BeliefBase"))
        item = self.beliefs_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "BeliefSelect"))
        item = self.beliefs_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Base"))
        item = self.beliefs_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Belief"))
        item = self.beliefs_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Open"))
        item = self.beliefs_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Close"))
        self.agenda_l.setText(_translate("MainWindow", "Agenda: "))
        self.agenda_label_update_button.setText(_translate("MainWindow", "Update"))
        self.label_intent_day_header.setText(_translate("MainWindow", "Day:"))
        self.label_intent_time_header.setText(_translate("MainWindow", "Time:"))
        self.label_intent_end_header.setText(_translate("MainWindow", "End:"))
        self.label_intent_agenda_importance_header1.setText(
            _translate("MainWindow", "root_relative")
        )
        self.label_intent_family_header1.setText(_translate("MainWindow", "Agenda"))
        self.label_intent_idea_id_header.setText(_translate("MainWindow", "Idea_id:"))
        self.label_intent_family_header2.setText(_translate("MainWindow", "Family:"))
        self.label_intent_agenda_importance_header2.setText(
            _translate("MainWindow", "weight:")
        )
        self.label_intent_idea_id_data.setText(_translate("MainWindow", "Idea_id:"))
        self.label_intent_family_data.setText(_translate("MainWindow", "Agenda"))
        self.label_intent_agenda_importance_data.setText(
            _translate("MainWindow", "weight:")
        )
        self.label_intent_end_data.setText(_translate("MainWindow", "End:"))
        self.label_intent_time_data.setText(_translate("MainWindow", "Time:"))
        self.label_intent_day_data.setText(_translate("MainWindow", "Day:"))
        self.root_datetime_prev_upd_soft.setText(
            _translate("MainWindow", '"Soft" moving up the past')
        )
        item = self.intent_states.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.intent_states.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.intent_states.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.intent_states.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.intent_states.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "New Column"))
        self.label_8.setText(
            _translate("MainWindow", "Things you promised to be right now")
        )
        self.label_6.setText(_translate("MainWindow", "Belief Base:"))
        self.label_9.setText(_translate("MainWindow", "Belief Belief:"))
        self.label_10.setText(_translate("MainWindow", "Open"))
        self.label_11.setText(_translate("MainWindow", "Nigh"))
        self.belief_update_button.setText(_translate("MainWindow", "Set Belief"))
        self.belief_delete_button.setText(_translate("MainWindow", "Del Belief"))
        self.menubar.setAccessibleName(_translate("MainWindow", "File"))
        self.menubar.setAccessibleDescription(
            _translate("MainWindow", "General Operations")
        )
        self.file_menu.setTitle(_translate("MainWindow", "File"))
        self.fm_open.setText(_translate("MainWindow", "Open"))
        self.fm_save.setText(_translate("MainWindow", "Save"))
        self.save_as.setText(_translate("MainWindow", "Save as..."))
        self.fm_new.setText(_translate("MainWindow", "New"))
