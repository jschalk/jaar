# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\dev\reddibrush\ui\EditIdeaunitUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1843, 853)
        Form.setMinimumSize(QtCore.QSize(1492, 0))
        self.label_14 = QtWidgets.QLabel(Form)
        self.label_14.setGeometry(QtCore.QRect(700, 10, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.yo_deescription = QtWidgets.QTextEdit(Form)
        self.yo_deescription.setGeometry(QtCore.QRect(680, 40, 341, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.yo_deescription.setFont(font)
        self.yo_deescription.setObjectName("yo_deescription")
        self.yo_weight = QtWidgets.QTextEdit(Form)
        self.yo_weight.setGeometry(QtCore.QRect(680, 130, 170, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.yo_weight.setFont(font)
        self.yo_weight.setObjectName("yo_weight")
        self.label_1 = QtWidgets.QLabel(Form)
        self.label_1.setGeometry(QtCore.QRect(580, 40, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_1.setFont(font)
        self.label_1.setObjectName("label_1")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(580, 130, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.submit_child_insert = QtWidgets.QPushButton(Form)
        self.submit_child_insert.setGeometry(QtCore.QRect(890, 800, 171, 26))
        self.submit_child_insert.setObjectName("submit_child_insert")
        self.submit_node_update = QtWidgets.QPushButton(Form)
        self.submit_node_update.setGeometry(QtCore.QRect(700, 800, 171, 26))
        self.submit_node_update.setObjectName("submit_node_update")
        self.label_parent_id = QtWidgets.QLabel(Form)
        self.label_parent_id.setGeometry(QtCore.QRect(1050, 0, 381, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_parent_id.setFont(font)
        self.label_parent_id.setObjectName("label_parent_id")
        self.baseideaunit = QtWidgets.QTreeWidget(Form)
        self.baseideaunit.setGeometry(QtCore.QRect(10, 110, 551, 721))
        self.baseideaunit.setIndentation(15)
        self.baseideaunit.setObjectName("baseideaunit")
        self.submit_node_delete = QtWidgets.QPushButton(Form)
        self.submit_node_delete.setGeometry(QtCore.QRect(1080, 800, 91, 26))
        self.submit_node_delete.setObjectName("submit_node_delete")
        self.refresh_button = QtWidgets.QPushButton(Form)
        self.refresh_button.setGeometry(QtCore.QRect(10, 20, 81, 51))
        self.refresh_button.setObjectName("refresh_button")
        self.close_button = QtWidgets.QPushButton(Form)
        self.close_button.setGeometry(QtCore.QRect(1250, 20, 91, 31))
        self.close_button.setObjectName("close_button")
        self.quit_button = QtWidgets.QPushButton(Form)
        self.quit_button.setGeometry(QtCore.QRect(1340, 20, 91, 31))
        self.quit_button.setObjectName("quit_button")
        self.idea2group_table = QtWidgets.QTableWidget(Form)
        self.idea2group_table.setGeometry(QtCore.QRect(1050, 80, 381, 191))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.idea2group_table.setFont(font)
        self.idea2group_table.setObjectName("idea2group_table")
        self.idea2group_table.setColumnCount(3)
        self.idea2group_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.idea2group_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.idea2group_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.idea2group_table.setHorizontalHeaderItem(2, item)
        self.idea2group_delete_button = QtWidgets.QPushButton(Form)
        self.idea2group_delete_button.setGeometry(QtCore.QRect(1440, 80, 131, 28))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.idea2group_delete_button.setFont(font)
        self.idea2group_delete_button.setObjectName("idea2group_delete_button")
        self.idea2group_insert_button = QtWidgets.QPushButton(Form)
        self.idea2group_insert_button.setGeometry(QtCore.QRect(1050, 50, 141, 28))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.idea2group_insert_button.setFont(font)
        self.idea2group_insert_button.setObjectName("idea2group_insert_button")
        self.idea2group_insert_combo = QtWidgets.QComboBox(Form)
        self.idea2group_insert_combo.setGeometry(QtCore.QRect(1200, 50, 231, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.idea2group_insert_combo.setFont(font)
        self.idea2group_insert_combo.setObjectName("idea2group_insert_combo")
        self.cb_rootadmiration = QtWidgets.QCheckBox(Form)
        self.cb_rootadmiration.setGeometry(QtCore.QRect(100, 20, 100, 20))
        self.cb_rootadmiration.setObjectName("cb_rootadmiration")
        self.cb_yo_id = QtWidgets.QCheckBox(Form)
        self.cb_yo_id.setGeometry(QtCore.QRect(100, 40, 100, 20))
        self.cb_yo_id.setObjectName("cb_yo_id")
        self.cb_yo2bd_count = QtWidgets.QCheckBox(Form)
        self.cb_yo2bd_count.setGeometry(QtCore.QRect(100, 60, 100, 20))
        self.cb_yo2bd_count.setObjectName("cb_yo2bd_count")
        self.cb_yo_goal = QtWidgets.QCheckBox(Form)
        self.cb_yo_goal.setGeometry(QtCore.QRect(320, 40, 91, 20))
        self.cb_yo_goal.setObjectName("cb_yo_goal")
        self.cb_yo_insert_allChildren = QtWidgets.QCheckBox(Form)
        self.cb_yo_insert_allChildren.setGeometry(QtCore.QRect(900, 780, 151, 20))
        self.cb_yo_insert_allChildren.setObjectName("cb_yo_insert_allChildren")
        self.hreg_open_hr = QtWidgets.QComboBox(Form)
        self.hreg_open_hr.setGeometry(QtCore.QRect(1610, 280, 73, 22))
        self.hreg_open_hr.setObjectName("hreg_open_hr")
        self.hreg_open_min = QtWidgets.QComboBox(Form)
        self.hreg_open_min.setGeometry(QtCore.QRect(1690, 280, 73, 22))
        self.hreg_open_min.setObjectName("hreg_open_min")
        self.label_37 = QtWidgets.QLabel(Form)
        self.label_37.setGeometry(QtCore.QRect(1610, 260, 55, 16))
        self.label_37.setObjectName("label_37")
        self.label_38 = QtWidgets.QLabel(Form)
        self.label_38.setGeometry(QtCore.QRect(1700, 260, 55, 16))
        self.label_38.setObjectName("label_38")
        self.hreg_length_hr = QtWidgets.QComboBox(Form)
        self.hreg_length_hr.setGeometry(QtCore.QRect(1610, 310, 73, 22))
        self.hreg_length_hr.setObjectName("hreg_length_hr")
        self.hreg_length_min = QtWidgets.QComboBox(Form)
        self.hreg_length_min.setGeometry(QtCore.QRect(1690, 310, 73, 22))
        self.hreg_length_min.setObjectName("hreg_length_min")
        self.cb_yo_goal_current = QtWidgets.QCheckBox(Form)
        self.cb_yo_goal_current.setGeometry(QtCore.QRect(210, 40, 91, 20))
        self.cb_yo_goal_current.setObjectName("cb_yo_goal_current")
        self.cb_yo_action = QtWidgets.QCheckBox(Form)
        self.cb_yo_action.setGeometry(QtCore.QRect(320, 20, 91, 20))
        self.cb_yo_action.setObjectName("cb_yo_action")
        self.yo_action_cb = QtWidgets.QCheckBox(Form)
        self.yo_action_cb.setGeometry(QtCore.QRect(930, 160, 81, 20))
        self.yo_action_cb.setObjectName("yo_action_cb")
        self.cb_yo_complete = QtWidgets.QCheckBox(Form)
        self.cb_yo_complete.setGeometry(QtCore.QRect(210, 20, 91, 20))
        self.cb_yo_complete.setObjectName("cb_yo_complete")
        self.button_hreg_instance = QtWidgets.QPushButton(Form)
        self.button_hreg_instance.setGeometry(QtCore.QRect(1450, 210, 75, 24))
        self.button_hreg_instance.setObjectName("button_hreg_instance")
        self.button_hreg_1hour = QtWidgets.QPushButton(Form)
        self.button_hreg_1hour.setGeometry(QtCore.QRect(1450, 240, 75, 24))
        self.button_hreg_1hour.setObjectName("button_hreg_1hour")
        self.button_hreg_all_day = QtWidgets.QPushButton(Form)
        self.button_hreg_all_day.setGeometry(QtCore.QRect(1450, 180, 75, 24))
        self.button_hreg_all_day.setObjectName("button_hreg_all_day")
        self.cb_yo_prev = QtWidgets.QCheckBox(Form)
        self.cb_yo_prev.setGeometry(QtCore.QRect(210, 60, 101, 20))
        self.cb_yo_prev.setObjectName("cb_yo_prev")
        self.cb_yo_curr = QtWidgets.QCheckBox(Form)
        self.cb_yo_curr.setGeometry(QtCore.QRect(320, 60, 111, 20))
        self.cb_yo_curr.setObjectName("cb_yo_curr")
        self.required_base_combo = QtWidgets.QComboBox(Form)
        self.required_base_combo.setGeometry(QtCore.QRect(620, 370, 701, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.required_base_combo.setFont(font)
        self.required_base_combo.setObjectName("required_base_combo")
        self.required_table = QtWidgets.QTableWidget(Form)
        self.required_table.setGeometry(QtCore.QRect(580, 520, 841, 250))
        self.required_table.setObjectName("required_table")
        self.required_table.setColumnCount(10)
        self.required_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.required_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.required_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.required_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.required_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.required_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.required_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.required_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.required_table.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.required_table.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.required_table.setHorizontalHeaderItem(9, item)
        self.cb_acptfact_count = QtWidgets.QCheckBox(Form)
        self.cb_acptfact_count.setGeometry(QtCore.QRect(430, 20, 121, 20))
        self.cb_acptfact_count.setObjectName("cb_acptfact_count")
        self.cb_required_count = QtWidgets.QCheckBox(Form)
        self.cb_required_count.setGeometry(QtCore.QRect(430, 40, 121, 20))
        self.cb_required_count.setObjectName("cb_required_count")
        self.cb_required_view = QtWidgets.QCheckBox(Form)
        self.cb_required_view.setGeometry(QtCore.QRect(10, 80, 61, 20))
        self.cb_required_view.setObjectName("cb_required_view")
        self.combo_dim_root = QtWidgets.QComboBox(Form)
        self.combo_dim_root.setGeometry(QtCore.QRect(80, 80, 481, 22))
        self.combo_dim_root.setObjectName("combo_dim_root")
        self.prom_l_03 = QtWidgets.QLabel(Form)
        self.prom_l_03.setGeometry(QtCore.QRect(580, 400, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.prom_l_03.setFont(font)
        self.prom_l_03.setObjectName("prom_l_03")
        self.prom_l_02 = QtWidgets.QLabel(Form)
        self.prom_l_02.setGeometry(QtCore.QRect(1480, 820, 311, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.prom_l_02.setFont(font)
        self.prom_l_02.setText("")
        self.prom_l_02.setObjectName("prom_l_02")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(590, 430, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.button_required_upsert = QtWidgets.QPushButton(Form)
        self.button_required_upsert.setGeometry(QtCore.QRect(1330, 430, 91, 81))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.button_required_upsert.setFont(font)
        self.button_required_upsert.setObjectName("button_required_upsert")
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(580, 160, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.yo_begin = QtWidgets.QTextEdit(Form)
        self.yo_begin.setGeometry(QtCore.QRect(680, 160, 170, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.yo_begin.setFont(font)
        self.yo_begin.setObjectName("yo_begin")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(580, 190, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.yo_close = QtWidgets.QTextEdit(Form)
        self.yo_close.setGeometry(QtCore.QRect(680, 190, 170, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.yo_close.setFont(font)
        self.yo_close.setObjectName("yo_close")
        self.label_12 = QtWidgets.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(580, 70, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.yo_pad = QtWidgets.QTextEdit(Form)
        self.yo_pad.setGeometry(QtCore.QRect(680, 70, 341, 51))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.yo_pad.setFont(font)
        self.yo_pad.setObjectName("yo_pad")
        self.create_hreg_button = QtWidgets.QPushButton(Form)
        self.create_hreg_button.setGeometry(QtCore.QRect(580, 790, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.create_hreg_button.setFont(font)
        self.create_hreg_button.setObjectName("create_hreg_button")
        self.required_sufffact_combo = QtWidgets.QComboBox(Form)
        self.required_sufffact_combo.setGeometry(QtCore.QRect(620, 400, 701, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.required_sufffact_combo.setFont(font)
        self.required_sufffact_combo.setObjectName("required_sufffact_combo")
        self.required_sufffact_open = QtWidgets.QTextEdit(Form)
        self.required_sufffact_open.setGeometry(QtCore.QRect(620, 430, 71, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.required_sufffact_open.setFont(font)
        self.required_sufffact_open.setObjectName("required_sufffact_open")
        self.required_sufffact_nigh = QtWidgets.QTextEdit(Form)
        self.required_sufffact_nigh.setGeometry(QtCore.QRect(620, 460, 71, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.required_sufffact_nigh.setFont(font)
        self.required_sufffact_nigh.setObjectName("required_sufffact_nigh")
        self.required_sufffact_divisor = QtWidgets.QTextEdit(Form)
        self.required_sufffact_divisor.setGeometry(QtCore.QRect(620, 490, 71, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.required_sufffact_divisor.setFont(font)
        self.required_sufffact_divisor.setObjectName("required_sufffact_divisor")
        self.label_15 = QtWidgets.QLabel(Form)
        self.label_15.setGeometry(QtCore.QRect(590, 460, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(Form)
        self.label_16.setGeometry(QtCore.QRect(580, 490, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(Form)
        self.label_17.setGeometry(QtCore.QRect(580, 370, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.button_required_delete = QtWidgets.QPushButton(Form)
        self.button_required_delete.setGeometry(QtCore.QRect(1330, 370, 91, 24))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.button_required_delete.setFont(font)
        self.button_required_delete.setObjectName("button_required_delete")
        self.yo_task_status = QtWidgets.QTextEdit(Form)
        self.yo_task_status.setGeometry(QtCore.QRect(930, 130, 91, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.yo_task_status.setFont(font)
        self.yo_task_status.setObjectName("yo_task_status")
        self.label_18 = QtWidgets.QLabel(Form)
        self.label_18.setGeometry(QtCore.QRect(860, 130, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.yo_numor = QtWidgets.QTextEdit(Form)
        self.yo_numor.setGeometry(QtCore.QRect(680, 250, 170, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.yo_numor.setFont(font)
        self.yo_numor.setObjectName("yo_numor")
        self.label_19 = QtWidgets.QLabel(Form)
        self.label_19.setGeometry(QtCore.QRect(580, 250, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(Form)
        self.label_20.setGeometry(QtCore.QRect(580, 310, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.yo_range_source_road = QtWidgets.QComboBox(Form)
        self.yo_range_source_road.setGeometry(QtCore.QRect(680, 340, 611, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.yo_range_source_road.setFont(font)
        self.yo_range_source_road.setObjectName("yo_range_source_road")
        self.label_21 = QtWidgets.QLabel(Form)
        self.label_21.setGeometry(QtCore.QRect(580, 340, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.required_sufffact_open_combo = QtWidgets.QComboBox(Form)
        self.required_sufffact_open_combo.setGeometry(QtCore.QRect(700, 430, 621, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.required_sufffact_open_combo.setFont(font)
        self.required_sufffact_open_combo.setObjectName("required_sufffact_open_combo")
        self.required_sufffact_nigh_combo = QtWidgets.QComboBox(Form)
        self.required_sufffact_nigh_combo.setGeometry(QtCore.QRect(700, 460, 621, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.required_sufffact_nigh_combo.setFont(font)
        self.required_sufffact_nigh_combo.setObjectName("required_sufffact_nigh_combo")
        self.required_sufffact_divisor_combo = QtWidgets.QComboBox(Form)
        self.required_sufffact_divisor_combo.setGeometry(
            QtCore.QRect(700, 490, 621, 26)
        )
        font = QtGui.QFont()
        font.setPointSize(8)
        self.required_sufffact_divisor_combo.setFont(font)
        self.required_sufffact_divisor_combo.setObjectName(
            "required_sufffact_divisor_combo"
        )
        self.yo_numeric_road = QtWidgets.QComboBox(Form)
        self.yo_numeric_road.setGeometry(QtCore.QRect(680, 310, 611, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.yo_numeric_road.setFont(font)
        self.yo_numeric_road.setObjectName("yo_numeric_road")
        self.label_22 = QtWidgets.QLabel(Form)
        self.label_22.setGeometry(QtCore.QRect(580, 280, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.yo_denom = QtWidgets.QTextEdit(Form)
        self.yo_denom.setGeometry(QtCore.QRect(680, 280, 170, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.yo_denom.setFont(font)
        self.yo_denom.setObjectName("yo_denom")
        self.label_23 = QtWidgets.QLabel(Form)
        self.label_23.setGeometry(QtCore.QRect(860, 250, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.yo_reest = QtWidgets.QCheckBox(Form)
        self.yo_reest.setGeometry(QtCore.QRect(930, 250, 81, 20))
        self.yo_reest.setObjectName("yo_reest")
        self.label_24 = QtWidgets.QLabel(Form)
        self.label_24.setGeometry(QtCore.QRect(580, 220, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.yo_addin = QtWidgets.QTextEdit(Form)
        self.yo_addin.setGeometry(QtCore.QRect(680, 220, 170, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.yo_addin.setFont(font)
        self.yo_addin.setObjectName("yo_addin")
        self.button_hreg_base = QtWidgets.QPushButton(Form)
        self.button_hreg_base.setGeometry(QtCore.QRect(1440, 280, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.button_hreg_base.setFont(font)
        self.button_hreg_base.setObjectName("button_hreg_base")
        self.hreg_days_repeat = QtWidgets.QTextEdit(Form)
        self.hreg_days_repeat.setGeometry(QtCore.QRect(1610, 350, 41, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.hreg_days_repeat.setFont(font)
        self.hreg_days_repeat.setObjectName("hreg_days_repeat")
        self.label_25 = QtWidgets.QLabel(Form)
        self.label_25.setGeometry(QtCore.QRect(1530, 350, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.hreg_weeks_repeat = QtWidgets.QTextEdit(Form)
        self.hreg_weeks_repeat.setGeometry(QtCore.QRect(1610, 380, 41, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.hreg_weeks_repeat.setFont(font)
        self.hreg_weeks_repeat.setObjectName("hreg_weeks_repeat")
        self.label_26 = QtWidgets.QLabel(Form)
        self.label_26.setGeometry(QtCore.QRect(1530, 380, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(Form)
        self.label_27.setGeometry(QtCore.QRect(1560, 280, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_27.setFont(font)
        self.label_27.setObjectName("label_27")
        self.label_28 = QtWidgets.QLabel(Form)
        self.label_28.setGeometry(QtCore.QRect(1560, 310, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.hreg_weekday = QtWidgets.QComboBox(Form)
        self.hreg_weekday.setGeometry(QtCore.QRect(1770, 380, 71, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.hreg_weekday.setFont(font)
        self.hreg_weekday.setObjectName("hreg_weekday")
        self.label_29 = QtWidgets.QLabel(Form)
        self.label_29.setGeometry(QtCore.QRect(1660, 380, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.label_31 = QtWidgets.QLabel(Form)
        self.label_31.setGeometry(QtCore.QRect(1530, 410, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_31.setFont(font)
        self.label_31.setObjectName("label_31")
        self.hreg_months_repeat = QtWidgets.QTextEdit(Form)
        self.hreg_months_repeat.setGeometry(QtCore.QRect(1610, 410, 41, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.hreg_months_repeat.setFont(font)
        self.hreg_months_repeat.setObjectName("hreg_months_repeat")
        self.hreg_years_repeat = QtWidgets.QTextEdit(Form)
        self.hreg_years_repeat.setGeometry(QtCore.QRect(1610, 440, 41, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.hreg_years_repeat.setFont(font)
        self.hreg_years_repeat.setObjectName("hreg_years_repeat")
        self.label_32 = QtWidgets.QLabel(Form)
        self.label_32.setGeometry(QtCore.QRect(1530, 440, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_32.setFont(font)
        self.label_32.setObjectName("label_32")
        self.hreg_monthday = QtWidgets.QTextEdit(Form)
        self.hreg_monthday.setGeometry(QtCore.QRect(1720, 410, 51, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.hreg_monthday.setFont(font)
        self.hreg_monthday.setObjectName("hreg_monthday")
        self.label_33 = QtWidgets.QLabel(Form)
        self.label_33.setGeometry(QtCore.QRect(1660, 410, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_33.setFont(font)
        self.label_33.setObjectName("label_33")
        self.label_34 = QtWidgets.QLabel(Form)
        self.label_34.setGeometry(QtCore.QRect(1660, 440, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_34.setFont(font)
        self.label_34.setObjectName("label_34")
        self.hreg_year_month = QtWidgets.QTextEdit(Form)
        self.hreg_year_month.setGeometry(QtCore.QRect(1660, 460, 51, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.hreg_year_month.setFont(font)
        self.hreg_year_month.setObjectName("hreg_year_month")
        self.hreg_year_monthday = QtWidgets.QTextEdit(Form)
        self.hreg_year_monthday.setGeometry(QtCore.QRect(1720, 460, 51, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.hreg_year_monthday.setFont(font)
        self.hreg_year_monthday.setObjectName("hreg_year_monthday")
        self.label_35 = QtWidgets.QLabel(Form)
        self.label_35.setGeometry(QtCore.QRect(1720, 440, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_35.setFont(font)
        self.label_35.setObjectName("label_35")
        self.button_sufffactunit_hreg_update_weeks = QtWidgets.QPushButton(Form)
        self.button_sufffactunit_hreg_update_weeks.setGeometry(
            QtCore.QRect(1530, 490, 291, 24)
        )
        self.button_sufffactunit_hreg_update_weeks.setObjectName(
            "button_sufffactunit_hreg_update_weeks"
        )
        self.hreg_weeks_remainder = QtWidgets.QTextEdit(Form)
        self.hreg_weeks_remainder.setGeometry(QtCore.QRect(1720, 380, 41, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.hreg_weeks_remainder.setFont(font)
        self.hreg_weeks_remainder.setObjectName("hreg_weeks_remainder")
        self.hreg_days_remainder = QtWidgets.QTextEdit(Form)
        self.hreg_days_remainder.setGeometry(QtCore.QRect(1720, 350, 41, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.hreg_days_remainder.setFont(font)
        self.hreg_days_remainder.setObjectName("hreg_days_remainder")
        self.label_30 = QtWidgets.QLabel(Form)
        self.label_30.setGeometry(QtCore.QRect(1660, 350, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.button_sufffactunit_hreg_update_days = QtWidgets.QPushButton(Form)
        self.button_sufffactunit_hreg_update_days.setGeometry(
            QtCore.QRect(1530, 520, 291, 24)
        )
        self.button_sufffactunit_hreg_update_days.setObjectName(
            "button_sufffactunit_hreg_update_days"
        )
        self.yo_problem_bool_cb = QtWidgets.QCheckBox(Form)
        self.yo_problem_bool_cb.setGeometry(QtCore.QRect(930, 190, 81, 20))
        self.yo_problem_bool_cb.setObjectName("yo_problem_bool_cb")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowHandle(_translate("Form", "Form"))
        self.label_14.setText(_translate("Form", "Ideas: Edit or Add Children "))
        self.label_1.setText(_translate("Form", "Description"))
        self.label_4.setText(_translate("Form", "Weight"))
        self.submit_child_insert.setText(_translate("Form", "Add Child"))
        self.submit_node_update.setText(_translate("Form", "Update Node"))
        self.label_parent_id.setText(_translate("Form", "Current Node ID:"))
        self.baseideaunit.headerItem().setText(0, _translate("Form", "ideaunit"))
        self.submit_node_delete.setText(_translate("Form", "Delete Node"))
        self.refresh_button.setText(_translate("Form", "Refresh"))
        self.close_button.setText(_translate("Form", "Close"))
        self.quit_button.setText(_translate("Form", "Quit App"))
        item = self.idea2group_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Group_ID"))
        item = self.idea2group_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Group"))
        item = self.idea2group_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Party Count"))
        self.idea2group_delete_button.setText(_translate("Form", "De-link Group"))
        self.idea2group_insert_button.setText(_translate("Form", "Add Group to Idea"))
        self.cb_rootadmiration.setText(_translate("Form", "root admiration"))
        self.cb_yo_id.setText(_translate("Form", "uid"))
        self.cb_yo2bd_count.setText(_translate("Form", "Group count"))
        self.cb_yo_goal.setText(_translate("Form", "lf goal"))
        self.cb_yo_insert_allChildren.setText(
            _translate("Form", "New node gets all children")
        )
        self.label_37.setText(_translate("Form", "Hour"))
        self.label_38.setText(_translate("Form", "Min"))
        self.cb_yo_goal_current.setText(_translate("Form", "Agenda"))
        self.cb_yo_action.setText(_translate("Form", "Act"))
        self.yo_action_cb.setText(_translate("Form", "Action"))
        self.cb_yo_complete.setText(_translate("Form", "Complete"))
        self.button_hreg_instance.setText(_translate("Form", "Instant"))
        self.button_hreg_1hour.setText(_translate("Form", "1 hour"))
        self.button_hreg_all_day.setText(_translate("Form", "All Day"))
        self.cb_yo_prev.setText(_translate("Form", "Previous Time"))
        self.cb_yo_curr.setText(_translate("Form", "Current Time"))
        item = self.required_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Required Base"))
        item = self.required_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "SuffFact"))
        item = self.required_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Base"))
        item = self.required_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Need"))
        item = self.required_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Open"))
        item = self.required_table.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Nigh"))
        item = self.required_table.horizontalHeaderItem(6)
        item.setText(_translate("Form", "Divisor"))
        item = self.required_table.horizontalHeaderItem(7)
        item.setText(_translate("Form", "empty"))
        item = self.required_table.horizontalHeaderItem(8)
        item.setText(_translate("Form", "Limt_status"))
        item = self.required_table.horizontalHeaderItem(9)
        item.setText(_translate("Form", "SuffFact_status"))
        self.cb_acptfact_count.setText(_translate("Form", "Idea Required"))
        self.cb_required_count.setText(_translate("Form", "Required Count"))
        self.cb_required_view.setText(_translate("Form", "Required:"))
        self.prom_l_03.setText(_translate("Form", "AcptFact"))
        self.label_9.setText(_translate("Form", "Open"))
        self.button_required_upsert.setText(_translate("Form", "Required Update"))
        self.label_10.setText(_translate("Form", "Begin"))
        self.label_11.setText(_translate("Form", "Close"))
        self.label_12.setText(_translate("Form", "Walk"))
        self.create_hreg_button.setText(_translate("Form", "create hreg"))
        self.label_15.setText(_translate("Form", "Nigh"))
        self.label_16.setText(_translate("Form", "Divisor"))
        self.label_17.setText(_translate("Form", "Base"))
        self.button_required_delete.setText(_translate("Form", "Required Del"))
        self.label_18.setText(_translate("Form", "Task Status:"))
        self.label_19.setText(_translate("Form", "Numorator"))
        self.label_20.setText(_translate("Form", "Numeric Source"))
        self.label_21.setText(_translate("Form", "Special Road"))
        self.label_22.setText(_translate("Form", "Denominator"))
        self.label_23.setText(_translate("Form", "Remainder:"))
        self.yo_reest.setText(_translate("Form", "reest"))
        self.label_24.setText(_translate("Form", "Addin"))
        self.button_hreg_base.setText(_translate("Form", "hregtime"))
        self.label_25.setText(_translate("Form", "Every x days"))
        self.label_26.setText(_translate("Form", "Every x weeks"))
        self.label_27.setText(_translate("Form", "Open"))
        self.label_28.setText(_translate("Form", "Length"))
        self.label_29.setText(_translate("Form", "Starting..."))
        self.label_31.setText(_translate("Form", "Every x months"))
        self.label_32.setText(_translate("Form", "Every x years"))
        self.label_33.setText(_translate("Form", "Monthday:"))
        self.label_34.setText(_translate("Form", "Month:"))
        self.label_35.setText(_translate("Form", "Monthday:"))
        self.button_sufffactunit_hreg_update_weeks.setText(
            _translate("Form", "apply sufffactunit_hregtime")
        )
        self.label_30.setText(_translate("Form", "Starting..."))
        self.button_sufffactunit_hreg_update_days.setText(
            _translate("Form", "apply sufffactunit_hregtime_days")
        )
        self.yo_problem_bool_cb.setText(_translate("Form", "Problem"))
