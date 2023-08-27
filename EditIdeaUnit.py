# command to for converting ui form to python file: pyuic5 ui\EditIdeaUnitUI.ui -o ui\EditIdeaUnitUI.py
import sys
from src.agent.idea import IdeaKid, IdeaAttrHolder
from ui.EditIdeaUnitUI import Ui_Form
from PyQt5 import QtWidgets as qtw, QtCore
from PyQt5.QtWidgets import QTableWidgetItem as qtw1, QTableWidget as qtw0
from src.agent.hreg_time import SuffFactUnitHregTime
from src.agent.group import GroupLink, GroupName
from src.agent.required import Road
from src.agent.hreg_time import get_24hr, get_60min
from src.pyqt5_tools.pyqt_func import (
    num2str,
    bool_val,
    str2float,
    get_pyqttree,
    emptystr,
    lw_diplay,
    emptystring_returns_none,
)


class EditIdeaUnit(qtw0, Ui_Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.refresh_button.clicked.connect(self.refresh_tree)
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)

        self.baseideaunit.itemClicked.connect(self.yo_tree_item_selected)
        self.baseideaunit.itemActivated.connect(self.yo_tree_item_expanded)
        self.submit_node_update.clicked.connect(self.idea_update)
        self.submit_node_delete.clicked.connect(self.idea_delete)
        self.submit_child_insert.clicked.connect(self.idea_insert)
        self.submit_duty_insert.clicked.connect(self.idea_duty_insert)

        self.cb_rootrank.stateChanged.connect(self.refresh_tree)
        self.cb_yo_id.stateChanged.connect(self.refresh_tree)
        self.cb_yo_agenda.stateChanged.connect(self.refresh_tree)
        self.cb_yo_action.stateChanged.connect(self.refresh_tree)
        self.cb_yo_complete.stateChanged.connect(self.refresh_tree)
        self.cb_yo_acptfactunit_time.stateChanged.connect(self.refresh_tree)
        self.cb_yo_acptfactunit_count.stateChanged.connect(self.refresh_tree)
        self.cb_yo_acptfactheir_count.stateChanged.connect(self.refresh_tree)
        self.cb_requiredheir_count.stateChanged.connect(self.refresh_tree)
        self.cb_required_count.stateChanged.connect(self.refresh_tree)
        self.cb_required_view.stateChanged.connect(self.refresh_tree)
        self.cb_acptfactheir_view.stateChanged.connect(self.refresh_tree)
        self.cb_yo2bd_count.stateChanged.connect(self.refresh_tree)
        self.combo_dim_root.currentTextChanged.connect(self.refresh_tree)

        self.idea2group_table.itemClicked.connect(self.idea2group_table_select)
        self.idea2group_delete_button.clicked.connect(self.idea2group_delete)
        self.idea2group_insert_button.clicked.connect(self.idea2group_update)
        self.required_table.itemClicked.connect(self.required_table_select)
        self.required_base_combo.currentTextChanged.connect(
            self.required_sufffact_combo_load
        )
        self.required_sufffact_combo.currentTextChanged.connect(
            self.required_sufffact_xxxx_combo_load
        )
        self.required_sufffact_open_combo.currentTextChanged.connect(
            self.required_sufffact_open_combo_select
        )
        self.required_sufffact_nigh_combo.currentTextChanged.connect(
            self.required_sufffact_nigh_combo_select
        )
        self.required_sufffact_divisor_combo.currentTextChanged.connect(
            self.required_sufffact_divisor_combo_select
        )
        self.button_required_upsert.clicked.connect(self.required_upsert)
        self.button_required_delete.clicked.connect(self.required_delete)
        self.button_sufffactunit_hreg_update_days.clicked.connect(
            self.sufffactunit_hreg_update_days
        )
        self.button_sufffactunit_hreg_update_weeks.clicked.connect(
            self.sufffactunit_hreg_update_weeks
        )
        self.button_hreg_base.clicked.connect(self.set_base_to_hregtime)
        self.create_hreg_button.clicked.connect(self.add_hreg_to_agent)
        self.button_view_requiredheirs.clicked.connect(self.toogle_requiredheir_tables)
        self.requiredheir_table_hidden = True

        self.yo_tree_item_setHidden(setHiddenBool=True)
        self.show
        self.yo_x = None

    def toogle_requiredheir_tables(self):
        self.requiredheir_table_hidden = self.requiredheir_table_hidden == False
        self.requiredheir_table.setHidden(self.requiredheir_table_hidden)

    def set_base_to_hregtime(self):
        self.required_base_combo.setCurrentText("Myagent,time,jajatime")

    def add_hreg_to_agent(self):
        self.agent_x.set_time_hreg_ideas(c400_count=7)
        self.refresh_tree()

    def yo_tree_item_setHidden(self, setHiddenBool):
        if type(setHiddenBool) is not bool:
            raise Exception("input varible is not boolen")

        self.label_parent_id.setHidden(setHiddenBool)
        self.button_hreg_instance.setHidden(setHiddenBool)
        self.button_hreg_1hour.setHidden(setHiddenBool)
        self.button_hreg_all_day.setHidden(setHiddenBool)
        self.cb_yo_insert_allChildren.setHidden(setHiddenBool)
        self.label_1.setHidden(setHiddenBool)
        self.label_4.setHidden(setHiddenBool)
        self.label_10.setHidden(setHiddenBool)
        self.label_11.setHidden(setHiddenBool)
        self.label_12.setHidden(setHiddenBool)
        self.label_14.setHidden(setHiddenBool)
        self.label_18.setHidden(setHiddenBool)
        self.label_19.setHidden(setHiddenBool)
        self.label_20.setHidden(setHiddenBool)
        self.label_21.setHidden(setHiddenBool)
        self.label_22.setHidden(setHiddenBool)
        self.label_23.setHidden(setHiddenBool)
        self.label_24.setHidden(setHiddenBool)
        self.prom_label_02.setHidden(setHiddenBool)
        self.prom_label_03.setHidden(setHiddenBool)
        self.yo_action_cb.setHidden(setHiddenBool)
        self.yo_problem_bool_cb.setHidden(setHiddenBool)
        self.yo_description.setHidden(setHiddenBool)
        self.yo_walk.setHidden(setHiddenBool)
        self.yo_weight.setHidden(setHiddenBool)
        self.yo_begin.setHidden(setHiddenBool)
        self.yo_addin.setHidden(setHiddenBool)
        self.yo_numor.setHidden(setHiddenBool)
        self.yo_denom.setHidden(setHiddenBool)
        self.yo_reest.setHidden(setHiddenBool)
        self.yo_special_road.setHidden(setHiddenBool)
        self.yo_numeric_road.setHidden(setHiddenBool)
        self.yo_close.setHidden(setHiddenBool)
        self.yo_task_status.setHidden(setHiddenBool)
        self.yo_active_status.setHidden(setHiddenBool)
        self.hreg_open_hr.setHidden(setHiddenBool)
        self.hreg_open_min.setHidden(setHiddenBool)
        self.hreg_length_hr.setHidden(setHiddenBool)
        self.hreg_length_min.setHidden(setHiddenBool)
        self.submit_child_insert.setHidden(setHiddenBool)
        self.idea2group_table.setHidden(setHiddenBool)
        self.idea2group_table.clear()
        self.idea2group_table.setRowCount(1)
        self.idea2group_insert_combo.setHidden(setHiddenBool)
        self.idea2group_delete_button.setHidden(setHiddenBool)
        self.idea2group_insert_button.setHidden(setHiddenBool)
        self.requiredheir_table.setHidden(True)
        self.required_table.setHidden(setHiddenBool)
        self.required_base_combo.setHidden(setHiddenBool)
        self.required_sufffact_combo.setHidden(setHiddenBool)
        self.required_sufffact_open_combo.setHidden(setHiddenBool)
        self.required_sufffact_nigh_combo.setHidden(setHiddenBool)
        self.required_sufffact_divisor_combo.setHidden(setHiddenBool)
        self.required_sufffact_open.setHidden(setHiddenBool)
        self.required_sufffact_nigh.setHidden(setHiddenBool)
        self.required_sufffact_divisor.setHidden(setHiddenBool)
        self.label_9.setHidden(setHiddenBool)
        self.label_15.setHidden(setHiddenBool)
        self.label_16.setHidden(setHiddenBool)
        self.label_17.setHidden(setHiddenBool)
        self.button_required_upsert.setHidden(setHiddenBool)
        self.button_sufffactunit_hreg_update_days.setHidden(setHiddenBool)
        self.button_sufffactunit_hreg_update_weeks.setHidden(setHiddenBool)
        self.button_required_delete.setHidden(setHiddenBool)
        self.button_hreg_base.setHidden(setHiddenBool)
        self.submit_child_insert.setHidden(setHiddenBool)
        self.submit_node_update.setHidden(setHiddenBool)
        self.submit_node_delete.setHidden(setHiddenBool)
        self.hreg_open_hr.clear()
        self.hreg_open_hr.addItems(get_24hr())
        self.hreg_open_hr.setCurrentText("")
        self.hreg_open_min.clear()
        self.hreg_open_min.addItems(get_60min())
        self.hreg_open_min.setCurrentText("")
        self.hreg_length_hr.clear()
        self.hreg_length_hr.addItems(get_24hr())
        self.hreg_length_hr.setCurrentText("")
        self.hreg_length_min.clear()
        self.hreg_length_min.addItems(get_60min())
        self.hreg_length_min.setCurrentText("")
        self.hreg_weekday.clear()
        self.hreg_weekday.addItems(
            [
                "",
                "Sunday",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
            ]
        )
        self.hreg_weeks_repeat.setText("")
        self.hreg_weeks_remainder.setText("")
        self.label_parent_id.setText("Current Node ID : ")
        self.prom_label_02.setText("")
        self.yo_action_cb.setChecked(False)
        self.yo_description.setText("")
        self.idea_desc_on_populate = ""
        self.yo_weight.setText("")
        # self.required_base_combo.setText("")
        # self.required_sufffact_combo.setText("")
        self.required_sufffact_open.setText("")
        self.required_sufffact_nigh.setText("")
        self.required_sufffact_divisor.setText("")

        self.required_table.setRowCount(0)
        self.required_base_combo.clear()
        self.required_sufffact_combo.clear()
        self.required_sufffact_open_combo.clear()
        self.required_sufffact_nigh_combo.clear()
        self.required_sufffact_divisor_combo.clear()
        self.idea2group_insert_combo.clear()

        if setHiddenBool == False:
            self.yo_x_populate()

    def yo_x_populate(self):
        self.label_parent_id.setText(f"Current Node road : {self.yo_x._walk}")
        self.yo_description.setText(self.yo_x._desc)
        # self.idea_desc_on_populate = self.yo_x._desc
        self.yo_walk.setText(self.yo_x._walk)
        self.yo_weight.setText(num2str(self.yo_x._weight))
        self.yo_begin.setText(num2str(self.yo_x._begin))
        self.yo_special_road.clear()
        self.yo_numeric_road.clear()
        if f"{type(self.yo_x)}" != "<class 'lw.agent.AgentUnit'>":
            self.populate_idea_kid_actions()
        self.yo_close.setText(num2str(self.yo_x._close))
        self.yo_action_cb.setChecked(self.yo_x.promise)
        self.yo_problem_bool_cb.setChecked(self.yo_x._problem_bool)
        self.yo_task_status.setText(str(self.yo_x._task))
        self.yo_active_status.setText(str(self.yo_x._active_status))
        self.submit_child_insert.setText(f"Add child {self.yo_x._desc:8}")
        self.required_table_load()
        self.requiredheir_table_load()
        self.required_base_combo_load()
        self.idea2group_table_load()
        self.idea2group_insert_combo_load()
        if self.combo_dim_root.currentText() == "":
            self.combo_dim_root.addItems(list(self.agent_x.get_required_bases()))

    def populate_idea_kid_actions(self):
        self.yo_addin.setText(num2str(self.yo_x._addin))
        self.yo_numor.setText(num2str(self.yo_x._numor))
        self.yo_denom.setText(num2str(self.yo_x._denom))
        self.yo_reest.setChecked(bool_val(self.yo_x._reest))
        idea_road_list = self.agent_x.get_idea_tree_ordered_road_list()
        idea_road_list.append("")
        self.yo_special_road.addItems(idea_road_list)
        self.yo_special_road.setCurrentText(self.yo_x._special_road)
        self.yo_numeric_road.addItems(idea_road_list)
        self.yo_numeric_road.setCurrentText(self.yo_x._numeric_road)

    def yo_tree_item_selected(self):
        idea_desc = self.baseideaunit.currentItem().data(2, 10)
        idea_walk = self.baseideaunit.currentItem().data(2, 11)
        if idea_walk not in ("", None):
            self.yo_x = self.agent_x.get_idea_kid(road=f"{idea_walk},{idea_desc}")
        else:
            self.yo_x = self.agent_x._idearoot
        self.yo_tree_item_setHidden(setHiddenBool=False)

    def yo_tree_item_expanded(self):
        root = self.baseideaunit.invisibleRootItem()
        self.idea_tree_set_is_expanded(root)

    def required_base_combo_load(self):
        # create list of all idea roads (road+desc)
        self.required_base_combo.clear()
        self.required_base_combo.addItems([""])
        self.required_base_combo.addItems(
            self.agent_x.get_idea_tree_ordered_road_list()
        )

    def required_sufffact_combo_load(self):
        self.required_sufffact_combo.clear()
        self.required_sufffact_combo.addItems([""])
        self.required_sufffact_combo.addItems(
            self.agent_x.get_heir_road_list(
                src_road=self.required_base_combo.currentText()
            )
        )

    def required_sufffact_xxxx_combo_load(self):
        filtered_list = []
        if self.required_sufffact_combo.currentText() not in [self.agent_x._desc, ""]:
            sufffact_idea = self.agent_x.get_idea_kid(
                road=self.required_sufffact_combo.currentText()
            )
            if sufffact_idea._special_road != None:
                filtered_list = self.agent_x.get_heir_road_list(
                    sufffact_idea._special_road
                )
        self.required_sufffact_open_combo.clear()
        self.required_sufffact_nigh_combo.clear()
        self.required_sufffact_divisor_combo.clear()
        self.required_sufffact_open_combo.addItems(filtered_list)
        self.required_sufffact_nigh_combo.addItems(filtered_list)
        self.required_sufffact_divisor_combo.addItems(filtered_list)
        self.set_sufffact_open_combo()
        self.set_sufffact_nigh_combo()
        self.set_sufffact_divisor_combo()

    def required_sufffact_open_combo_select(self):
        self.required_sufffact_open.setText("")
        self.required_sufffact_nigh.setText("")
        self.required_sufffact_divisor.setText("")

        if self.required_sufffact_open_combo.currentText() not in [
            self.agent_x._desc,
            "",
        ]:
            self.required_sufffact_open_combo_sel_actions()

    def required_sufffact_open_combo_sel_actions(self):
        open_idea_x = self.agent_x.get_idea_kid(
            road=self.required_sufffact_open_combo.currentText()
        )
        if open_idea_x._begin != None:
            self.required_sufffact_open.setText(str(open_idea_x._begin))
        if open_idea_x._close != None:
            self.required_sufffact_nigh.setText(str(open_idea_x._close))
        if open_idea_x._addin != None:
            self.required_sufffact_divisor.setText(str(open_idea_x._addin))
        if open_idea_x._numor != None:
            self.required_sufffact_divisor.setText(str(open_idea_x._numor))
        if open_idea_x._denom != None:
            self.required_sufffact_divisor.setText(str(open_idea_x._denom))
        if open_idea_x._reest != None:
            self.required_sufffact_divisor.setText(str(open_idea_x._reest))

    def numeric_road_combo_select(self):
        if self.required_sufffact_open_combo.currentText() not in [
            self.agent_x._desc,
            "",
        ]:
            open_idea_x = self.agent_x.get_idea_kid(
                road=self.required_sufffact_open_combo.currentText()
            )
            # nigh_idea_x = self.agent_x.get_idea_kid(
            #     road=self.required_sufffact_nigh_combo.currentText()
            # )
            # divisor_idea_x = self.agent_x.get_idea_kid(
            #     road=self.required_sufffact_divisor_combo.currentText()
            # )
            # if open_idea_x._begin != None:
            #     self.required_sufffact_open.setText(str(open_idea_x._begin))
            # if open_idea_x._close != None:
            #     self.required_sufffact_nigh.setText(str(open_idea_x._close))

    def set_sufffact_open_combo(self):
        if (
            self.required_sufffact_open_combo.currentText()
            not in [
                self.agent_x._desc,
                "",
            ]
            and self.required_sufffact_open.toPlainText() != ""
        ):
            open_idea_x = self.agent_x.get_idea_kid(
                road=self.required_sufffact_open_combo.currentText()
            )
            open_int = str2float(self.required_sufffact_open.toPlainText())
            open_kids = open_idea_x.get_kids_in_range(begin=open_int, close=open_int)
            if len(open_kids) == 1:
                idea_x = open_kids[0]
                self.required_sufffact_open_combo.setCurrentText(
                    f"{idea_x._walk},{idea_x._desc}"
                )

    def set_sufffact_nigh_combo(self):
        if (
            self.required_sufffact_nigh_combo.currentText()
            not in [
                self.agent_x._desc,
                "",
            ]
            and self.required_sufffact_nigh.toPlainText() != ""
        ):
            nigh_idea_x = self.agent_x.get_idea_kid(
                road=self.required_sufffact_nigh_combo.currentText()
            )
            nigh_int = int(self.required_sufffact_nigh.toPlainText())
            nigh_kids = nigh_idea_x.get_kids_in_range(begin=nigh_int, close=nigh_int)
            if len(nigh_kids) == 1:
                idea_x = nigh_kids[0]
                self.required_sufffact_nigh_combo.setCurrentText(
                    f"{idea_x._walk},{idea_x._desc}"
                )

    def set_sufffact_divisor_combo(self):
        if (
            self.required_sufffact_divisor_combo.currentText()
            not in [
                self.agent_x._desc,
                "",
            ]
            and self.required_sufffact_divisor.toPlainText() != ""
        ):
            divisor_idea_x = self.agent_x.get_idea_kid(
                road=self.required_sufffact_divisor_combo.currentText()
            )
            divisor_int = int(self.required_sufffact_divisor.toPlainText())
            divisor_kids = divisor_idea_x.get_kids_in_range(
                begin=divisor_int, close=divisor_int
            )
            if len(divisor_kids) == 1:
                idea_x = divisor_kids[0]
                self.required_sufffact_divisor_combo.setCurrentText(
                    f"{idea_x._walk},{idea_x._desc}"
                )

    def required_sufffact_nigh_combo_select(self):
        self.required_sufffact_nigh.setText("")
        if self.required_sufffact_nigh_combo.currentText() not in [
            self.agent_x._desc,
            "",
        ]:
            nigh_idea_x = self.agent_x.get_idea_kid(
                road=self.required_sufffact_nigh_combo.currentText()
            )
            if nigh_idea_x._close != None:
                self.required_sufffact_nigh.setText(str(nigh_idea_x._close))

    def required_sufffact_divisor_combo_select(self):
        self.required_sufffact_divisor.setText("")
        if self.required_sufffact_divisor_combo.currentText() not in [
            self.agent_x._desc,
            "",
        ]:
            divisor_idea_x = self.agent_x.get_idea_kid(
                road=self.required_sufffact_divisor_combo.currentText()
            )
            if divisor_idea_x._denom != None:
                self.required_sufffact_divisor.setText(str(divisor_idea_x._denom))

    def required_table_load(self):
        self.required_table.clear()
        row = 0
        for required in self.yo_x._requiredunits.values():
            requiredheir = self.yo_x._requiredheirs.get(required.base)
            for sufffact in required.sufffacts.values():
                required_text = required.base.replace(f"{self.agent_x._desc}", "")
                required_text = required_text[1:]
                sufffact_text = sufffact.need.replace(required.base, "")
                sufffact_text = sufffact_text[1:]
                sufffact_open = sufffact.open
                sufffact_nigh = sufffact.nigh
                if required_text == "time,jajatime":
                    sufffact_open = self.agent_x.get_jajatime_repeating_readable_text(
                        open=sufffact.open, nigh=sufffact.nigh, divisor=sufffact.divisor
                    )
                    sufffact_nigh = ""
                    sufffact_text = f"{sufffact_open}"

                elif sufffact.divisor != None:
                    sufffact_text = f"{sufffact_text}  Open-Nigh {sufffact_open}-{sufffact.nigh} Divisor {sufffact.divisor}"
                elif sufffact.open != None:
                    sufffact_text = (
                        f"{sufffact_text}  Open-Nigh {sufffact.open}-{sufffact.nigh}"
                    )
                else:
                    sufffact_text = f"{sufffact_text}"

                self.required_table.setRowCount(row + 1)
                self.required_table.setItem(row, 0, qtw1(required_text))
                self.required_table.setItem(row, 1, qtw1(sufffact_text))
                self.required_table.setItem(row, 2, qtw1(required.base))
                self.required_table.setItem(row, 3, qtw1(sufffact.need))
                self.required_table.setItem(row, 4, qtw1(num2str(sufffact.open)))
                self.required_table.setItem(row, 5, qtw1(num2str(sufffact.nigh)))
                self.required_table.setItem(row, 6, qtw1(num2str(sufffact.divisor)))
                self.required_table.setItem(row, 7, qtw1(f"{requiredheir._task}"))
                self.required_table.setItem(row, 8, qtw1(f"{requiredheir._status}"))
                self.required_table.setItem(row, 9, qtw1(str(sufffact._status)))
                self.required_table.setItem(row, 10, qtw1(str(sufffact._task)))
                row += 1

        self.required_table.horizontalHeaderVisible = False
        self.required_table.verticalHeaderVisible = False
        self.required_table.setColumnWidth(0, 300)
        self.required_table.setColumnWidth(1, 400)
        self.required_table.setColumnWidth(2, 30)
        self.required_table.setColumnWidth(3, 30)
        self.required_table.setColumnWidth(4, 30)
        self.required_table.setColumnWidth(5, 30)
        self.required_table.setColumnWidth(6, 60)
        self.required_table.setColumnWidth(7, 60)
        self.required_table.setColumnWidth(8, 60)
        self.required_table.setColumnWidth(9, 60)
        self.required_table.setColumnWidth(10, 60)
        self.required_table.setColumnHidden(0, False)
        self.required_table.setColumnHidden(1, False)
        self.required_table.setColumnHidden(2, True)
        self.required_table.setColumnHidden(3, True)
        self.required_table.setColumnHidden(4, True)
        self.required_table.setColumnHidden(5, True)
        self.required_table.setColumnHidden(6, False)
        self.required_table.setColumnHidden(7, False)
        self.required_table.setColumnHidden(8, False)
        self.required_table.setColumnHidden(9, False)
        self.required_table.setColumnHidden(10, False)
        self.required_table.setHorizontalHeaderLabels(
            [
                "Required",
                "SuffFact",
                "Base",
                "Need",
                "Open",
                "Nigh",
                "Divisor",
                "LimTask",
                "LimStatus",
                "sufffactstatus",
                "SuffFactTask",
            ]
        )

    def requiredheir_table_load(self):
        self.requiredheir_table.clear()
        row = 0
        for requiredheir in self.yo_x._requiredheirs.values():
            for sufffact in requiredheir.sufffacts.values():
                requiredheir_text = requiredheir.base.replace(
                    f"{self.agent_x._desc}", ""
                )
                requiredheir_text = requiredheir_text[1:]
                sufffact_text = sufffact.need.replace(requiredheir.base, "")
                sufffact_text = sufffact_text[1:]
                sufffact_open = sufffact.open
                sufffact_nigh = sufffact.nigh
                if requiredheir_text == "time,jajatime":
                    sufffact_open = self.agent_x.get_jajatime_repeating_readable_text(
                        open=sufffact.open, nigh=sufffact.nigh, divisor=sufffact.divisor
                    )
                    sufffact_nigh = ""
                    sufffact_text = f"{sufffact_open}"

                elif sufffact.divisor != None:
                    sufffact_text = f"{sufffact_text}  Open-Nigh {sufffact_open}-{sufffact.nigh} Divisor {sufffact.divisor}"
                elif sufffact.open != None:
                    sufffact_text = (
                        f"{sufffact_text}  Open-Nigh {sufffact.open}-{sufffact.nigh}"
                    )
                else:
                    sufffact_text = f"{sufffact_text}"

                sufffact_text += f"{type(requiredheir)}"

                self.requiredheir_table.setRowCount(row + 1)
                self.requiredheir_table.setItem(row, 0, qtw1(requiredheir_text))
                self.requiredheir_table.setItem(row, 1, qtw1(sufffact_text))
                self.requiredheir_table.setItem(row, 2, qtw1(requiredheir.base))
                self.requiredheir_table.setItem(row, 3, qtw1(sufffact.need))
                self.requiredheir_table.setItem(row, 4, qtw1(num2str(sufffact.open)))
                self.requiredheir_table.setItem(row, 5, qtw1(num2str(sufffact.nigh)))
                self.requiredheir_table.setItem(row, 6, qtw1(num2str(sufffact.divisor)))
                self.requiredheir_table.setItem(row, 7, qtw1(f"{requiredheir._task}"))
                self.requiredheir_table.setItem(row, 8, qtw1(f"{requiredheir._status}"))
                self.requiredheir_table.setItem(row, 9, qtw1(str(sufffact._status)))
                self.requiredheir_table.setItem(row, 10, qtw1(str(sufffact._task)))
                row += 1

        self.requiredheir_table.horizontalHeaderVisible = False
        self.requiredheir_table.verticalHeaderVisible = False
        self.requiredheir_table.setColumnWidth(0, 300)
        self.requiredheir_table.setColumnWidth(1, 400)
        self.requiredheir_table.setColumnWidth(2, 30)
        self.requiredheir_table.setColumnWidth(3, 30)
        self.requiredheir_table.setColumnWidth(4, 30)
        self.requiredheir_table.setColumnWidth(5, 30)
        self.requiredheir_table.setColumnWidth(6, 60)
        self.requiredheir_table.setColumnWidth(7, 60)
        self.requiredheir_table.setColumnWidth(8, 60)
        self.requiredheir_table.setColumnWidth(9, 60)
        self.requiredheir_table.setColumnWidth(10, 60)
        self.requiredheir_table.setColumnHidden(0, False)
        self.requiredheir_table.setColumnHidden(1, False)
        self.requiredheir_table.setColumnHidden(2, True)
        self.requiredheir_table.setColumnHidden(3, True)
        self.requiredheir_table.setColumnHidden(4, True)
        self.requiredheir_table.setColumnHidden(5, True)
        self.requiredheir_table.setColumnHidden(6, False)
        self.requiredheir_table.setColumnHidden(7, False)
        self.requiredheir_table.setColumnHidden(8, False)
        self.requiredheir_table.setColumnHidden(9, False)
        self.requiredheir_table.setColumnHidden(10, False)
        self.requiredheir_table.setHorizontalHeaderLabels(
            [
                "Requiredheir",
                "SuffFact",
                "Base",
                "Need",
                "Open",
                "Nigh",
                "Divisor",
                "LimTask",
                "LimStatus",
                "sufffactstatus",
                "SuffFactTask",
            ]
        )

    def sufffactunit_hreg_update_weeks(self):
        self.hreg_days_repeat.setText("")
        self.hreg_days_remainder.setText("")

        if self.hreg_length_hr.currentText() == "":
            self.hreg_length_hr.setCurrentText("0")
        if self.hreg_length_min.currentText() == "":
            self.hreg_length_min.setCurrentText("0")
        if self.hreg_open_hr.currentText() == "":
            self.hreg_open_hr.setCurrentText("0")
        if self.hreg_open_min.currentText() == "":
            self.hreg_open_min.setCurrentText("0")
        if self.hreg_weekday.currentText() == "":
            self.hreg_weekday.setCurrentText("Saturday")
        if self.hreg_weeks_repeat.toPlainText() == "":
            self.hreg_weeks_repeat.setText("1")
        if self.hreg_weeks_remainder.toPlainText() == "":
            self.hreg_weeks_remainder.setText("0")

        hu = SuffFactUnitHregTime()
        event_minutes = (int(self.hreg_length_hr.currentText()) * 60) + int(
            self.hreg_length_min.currentText()
        )
        hu.set_weekly_event(
            every_x_weeks=int(self.hreg_weeks_repeat.toPlainText()),
            remainder_weeks=int(self.hreg_weeks_remainder.toPlainText()),
            weekday=self.hreg_weekday.currentText(),
            start_hr=int(self.hreg_open_hr.currentText()),
            start_minute=int(self.hreg_open_min.currentText()),
            event_minutes=event_minutes,
        )
        self.required_sufffact_open.setText(str(hu.jajatime_open))
        self.required_sufffact_nigh.setText(str(hu.jajatime_nigh))
        self.required_sufffact_divisor.setText(str(hu.jajatime_divisor))

    def sufffactunit_hreg_update_days(self):
        self.hreg_weekday.setCurrentText("")
        self.hreg_weeks_repeat.setText("")
        self.hreg_weeks_remainder.setText("")

        if self.hreg_length_hr.currentText() == "":
            self.hreg_length_hr.setCurrentText("0")
        if self.hreg_length_min.currentText() == "":
            self.hreg_length_min.setCurrentText("0")
        if self.hreg_open_hr.currentText() == "":
            self.hreg_open_hr.setCurrentText("0")
        if self.hreg_open_min.currentText() == "":
            self.hreg_open_min.setCurrentText("0")
        if self.hreg_days_repeat.toPlainText() == "":
            self.hreg_days_repeat.setText("1")
        if self.hreg_days_remainder.toPlainText() == "":
            self.hreg_days_remainder.setText("0")

        hu = SuffFactUnitHregTime()
        event_minutes = (int(self.hreg_length_hr.currentText()) * 60) + int(
            self.hreg_length_min.currentText()
        )
        hu.set_days_event(
            every_x_days=float(self.hreg_days_repeat.toPlainText()),
            remainder_days=float(self.hreg_days_remainder.toPlainText()),
            start_hr=int(self.hreg_open_hr.currentText()),
            start_minute=int(self.hreg_open_min.currentText()),
            event_minutes=event_minutes,
        )
        self.required_sufffact_open.setText(str(hu.jajatime_open))
        self.required_sufffact_nigh.setText(str(hu.jajatime_nigh))
        self.required_sufffact_divisor.setText(str(hu.jajatime_divisor))

    def required_upsert(self):
        if (
            self.required_base_combo.currentText() != ""
            and self.required_sufffact_combo.currentText() != ""
        ):
            base_x = self.required_base_combo.currentText()
            sufffact_x = self.required_sufffact_combo.currentText()
            open_x = str2float(self.required_sufffact_open.toPlainText())
            nigh_x = str2float(self.required_sufffact_nigh.toPlainText())
            divisor_x = str2float(self.required_sufffact_divisor.toPlainText())
            idea_desc = self.baseideaunit.currentItem().data(2, 10)
            idea_walk = self.baseideaunit.currentItem().data(2, 11)
            self.agent_x.edit_idea_attr(
                road=f"{idea_walk},{idea_desc}",
                required_base=base_x,
                required_sufffact=sufffact_x,
                required_sufffact_open=open_x,
                required_sufffact_nigh=nigh_x,
                required_sufffact_divisor=divisor_x,
            )

            # self.yo_x.set_required_sufffact(
            #     base=base_x,
            #     need=sufffact_x,
            #     open=open_x,
            #     nigh=nigh_x,
            #     divisor=divisor_x,
            # )
            self.agent_x.get_idea_list()
            self.required_table_load()

    def required_delete(self):
        if (
            self.required_base_combo.currentText() != ""
            and self.required_sufffact_combo.currentText() != ""
        ):
            self.yo_x.del_requiredunit_sufffact(
                base=self.required_base_combo.currentText(),
                need=self.required_sufffact_combo.currentText(),
            )
            self.required_table_load()

    def idea2group_table_select(self):
        self.idea2group_delete_button.setText(
            f"""Remove {self.idea2group_table.item(self.idea2group_table.currentRow(), 1).text()}"""
        )

    def idea2group_table_load(self):
        # idea2group_table is qtw.QTableWidget()
        self.idea2group_table.clear()
        self.idea2group_table.sortItems(1, QtCore.Qt.AscendingOrder)
        self.idea2group_table.horizontalHeaderVisible = False
        self.idea2group_table.verticalHeaderVisible = False
        self.idea2group_table.setColumnWidth(0, 150)
        self.idea2group_table.setColumnHidden(1, True)
        self.idea2group_table.setColumnWidth(1, 50)
        self.idea2group_table.setColumnWidth(2, 70)
        self.idea2group_table.setHorizontalHeaderLabels(
            ["Group display", "group_name", "LW Force"]
        )
        # print(f"{self.yo_x._grouplinks=}")
        # print(f"{self.yo_x._groupheirs=}")
        grouplinks_list = list(self.yo_x._grouplinks.values())
        grouplinks_list.sort(key=lambda x: x.name, reverse=False)
        groupheirs_list = list(self.yo_x._groupheirs.values())
        groupheirs_list.sort(key=lambda x: x.name, reverse=False)
        # print(f"{grouplinks_list=}")
        # print(f"{groupheirs_list=}")

        for row, groupheir in enumerate(groupheirs_list, start=1):
            self.idea2group_table.setRowCount(row)
            x_text = f"  Heir: {groupheir.name}"
            for grouplink in grouplinks_list:
                if grouplink.name == groupheir.name:
                    x_text = f"{groupheir.name}"
            self.idea2group_table.setItem(row - 1, 0, qtw1(x_text))
            self.idea2group_table.setItem(row - 1, 1, qtw1(groupheir.name))
            self.idea2group_table.setItem(
                row - 1,
                2,
                qtw1(lw_diplay(groupheir._agent_credit)),
            )

        self.idea2group_table.sortItems(1, QtCore.Qt.AscendingOrder)

    def idea2group_insert_combo_load(self):
        # groupunits_list = list(self.agent_x._groupunits.values())
        groupunits_names_list = []
        for groupunit in self.agent_x._groups.values():
            group_already_selected = any(
                groupunit.name == grouplink.name
                for grouplink in self.yo_x._grouplinks.values()
            )
            if not group_already_selected:
                groupunits_names_list.append(groupunit.name)
        groupunits_names_list.sort(key=lambda x: x.lower(), reverse=False)

        self.idea2group_insert_combo.clear()
        self.idea2group_insert_combo.addItems(groupunits_names_list)

    def idea2group_update(self):
        bd_name_new = self.idea2group_insert_combo.currentText()
        if bd_name_new == "":
            raise Exception("bd_name is empty, idea2bd cannot be updated")
        grouplink_new = GroupLink(name=GroupName(bd_name_new), weight=1)
        self.agent_x.edit_idea_attr(
            road=f"{self.yo_x._walk},{self.yo_x._desc}", grouplink=grouplink_new
        )
        self.idea2group_insert_combo_load()
        self.idea2group_table_load()

    def idea2group_delete(self):
        delete_group_name = ""
        if self.idea2group_table.currentRow() != None:
            delete_group_name = self.idea2group_table.item(
                self.idea2group_table.currentRow(), 1
            ).text()
            self.agent_x.edit_idea_attr(
                road=f"{self.yo_x._walk},{self.yo_x._desc}",
                grouplink_del=delete_group_name,
            )
            self.idea2group_insert_combo_load()
            self.idea2group_table_load()

    def idea_delete(self):
        self.agent_x.del_idea_kid(road=f"{self.yo_x._walk},{self.yo_x._desc}")
        self.baseideaunit.clear()
        self.refresh_tree(disable_is_expanded=True)

    def idea_edit_nonroad_data(self, idea_road):
        self.agent_x.edit_idea_attr(
            road=idea_road,
            weight=float(self.yo_weight.toPlainText()),
            begin=str2float(self.yo_begin.toPlainText()),
            close=str2float(self.yo_close.toPlainText()),
            addin=str2float(self.yo_addin.toPlainText()),
            numor=str2float(self.yo_numor.toPlainText()),
            denom=str2float(self.yo_denom.toPlainText()),
            reest=self.yo_reest.checkState() == 2,
            special_road=emptystr(self.yo_special_road.currentText()),
            numeric_road=emptystr(self.yo_numeric_road.currentText()),
            promise=(self.yo_action_cb.checkState() == 2),
            problem_bool=(self.yo_problem_bool_cb.checkState() == 2),
            required_base=None,
            required_sufffact=None,
            required_sufffact_open=None,
            required_sufffact_nigh=None,
            required_sufffact_divisor=None,
            required_del_sufffact_base=None,
            required_del_sufffact_need=None,
            uid=None,
            required=None,
            descendant_promise_count=None,
            all_member_credit=None,
            all_member_debt=None,
            grouplink=None,
            is_expanded=None,
        )

    def idea_edit_road(self, idea_road):
        self.agent_x.edit_idea_desc(
            old_road=idea_road,
            new_desc=self.yo_description.toPlainText(),
        )

        # update hierarchical data
        self.refresh_tree(disable_is_expanded=True)
        self.yo_tree_item_setHidden(setHiddenBool=True)

    def idea_update(self):
        idea_road = None
        if self.yo_x._walk not in (None, ""):
            idea_road = Road(f"{self.yo_x._walk},{self.yo_x._desc}")
        else:
            idea_road = Road(f"{self.yo_x._desc}")
        self.idea_edit_nonroad_data(idea_road=idea_road)
        # if (
        #     self.idea_desc_on_populate != self.yo_description.toPlainText()
        #     and self.idea_desc_on_populate != ""
        #     and self.idea_desc_on_populate != None
        # ):
        #     self.idea_edit_road()
        if self.yo_x._desc != self.yo_description.toPlainText():
            self.idea_edit_road(idea_road=idea_road)

    def idea_duty_insert(self):
        new_walk = f"{self.yo_x._desc}"
        if self.yo_x._walk not in ("", None):
            new_walk = f"{self.yo_x._walk},{self.yo_x._desc}"
        new_road = f"{new_walk},{self.yo_description.toPlainText()}"
        self.idea_insert()

        # add done/not_done children
        not_done_text = "not done"
        self.agent_x.add_idea(
            idea_kid=IdeaKid(_desc=not_done_text),
            walk=new_road,
        )
        done_text = "done"
        self.agent_x.add_idea(
            idea_kid=IdeaKid(_desc=done_text),
            walk=new_road,
        )
        # set required to "not done"
        self.agent_x.edit_idea_attr(
            road=new_road,
            required_base=new_road,
            required_sufffact=f"{new_road},{not_done_text}",
        )
        self.agent_x.set_acptfact(
            base=new_road,
            pick=f"{new_road},{not_done_text}",
        )
        self.refresh_tree()

    def idea_insert(self):
        new_idea = IdeaKid(_desc=self.yo_description.toPlainText())
        idea_attr_x = IdeaAttrHolder(
            weight=float(self.yo_weight.toPlainText()),
            begin=str2float(self.yo_begin.toPlainText()),
            close=str2float(self.yo_close.toPlainText()),
            addin=str2float(self.yo_addin.toPlainText()),
            numor=str2float(self.yo_numor.toPlainText()),
            denom=str2float(self.yo_denom.toPlainText()),
            reest=self.yo_reest.checkState() == 2,
            special_road=emptystring_returns_none(self.yo_special_road.currentText()),
            numeric_road=emptystring_returns_none(self.yo_numeric_road.currentText()),
            promise=(self.yo_action_cb.checkState() == 2),
            uid=None,
            required=None,
            required_base=None,
            required_sufffact=None,
            required_sufffact_open=None,
            required_sufffact_nigh=None,
            required_sufffact_divisor=None,
            required_del_sufffact_base=None,
            required_del_sufffact_need=None,
            descendant_promise_count=None,
            all_member_credit=None,
            all_member_debt=None,
            grouplink=None,
            grouplink_del=None,
            is_expanded=None,
            problem_bool=None,
            on_meld_weight_action=None,
        )
        new_idea._set_idea_attr(idea_attr=idea_attr_x)
        new_idea.set_kids_empty_if_null()
        take_parent_children_bool = self.cb_yo_insert_allChildren.checkState() == 2
        new_walk = f"{self.yo_x._desc}"
        if self.yo_x._walk not in ("", None):
            new_walk = f"{self.yo_x._walk},{self.yo_x._desc}"
        self.agent_x.add_idea(
            idea_kid=new_idea,
            walk=new_walk,
        )
        self.refresh_tree()

    def refresh_tree(self, disable_is_expanded: bool = False):
        root_percent_flag = self.cb_rootrank.checkState() == 2
        yo_id_flag = self.cb_yo_id.checkState() == 2
        yo_agenda_flag = self.cb_yo_agenda.checkState() == 2
        yo_action_flag = self.cb_yo_action.checkState() == 2
        yo2bd_count_flag = self.cb_yo2bd_count.checkState() == 2
        # yo2bd_spec1_flag = self.yo2bd_spec1_flag.checkState() == 2
        yo_complete_flag = self.cb_yo_complete.checkState() == 2
        yo_acptfactunit_time_flag = self.cb_yo_acptfactunit_time.checkState() == 2
        yo_acptfactunit_count_flag = self.cb_yo_acptfactunit_count.checkState() == 2
        yo_acptfactheir_count_flag = self.cb_yo_acptfactheir_count.checkState() == 2
        requiredheir_count_flag = self.cb_requiredheir_count.checkState() == 2
        required_count_flag = self.cb_required_count.checkState() == 2
        required_view_flag = self.cb_required_view.checkState() == 2
        required_view_base = self.combo_dim_root.currentText()
        acptfactheir_view_flag = self.cb_acptfactheir_view.checkState() == 2

        # root = self.baseideaunit.invisibleRootItem()
        # self.yo_tree_isExpanded(node=root, level=1)
        root = self.baseideaunit.invisibleRootItem()
        if not disable_is_expanded:
            self.idea_tree_set_is_expanded(root)

        tree_root = get_pyqttree(
            idearoot=self.agent_x._idearoot,
            yo_agenda_flag=yo_agenda_flag,
            yo_action_flag=yo_action_flag,
            yo_acptfactunit_time_flag=yo_acptfactunit_time_flag,
            yo_acptfactunit_count_flag=yo_acptfactunit_count_flag,
            yo_acptfactheir_count_flag=yo_acptfactheir_count_flag,
            yo_complete_flag=yo_complete_flag,
            yo2bd_count_flag=yo2bd_count_flag,
            requiredheir_count_flag=requiredheir_count_flag,
            required_count_flag=required_count_flag,
            required_view_flag=required_view_flag,
            required_view_name=required_view_base,
            acptfactheir_view_flag=acptfactheir_view_flag,
            root_percent_flag=root_percent_flag,
            src_agent=self.agent_x,
        )

        self.baseideaunit.clear()
        self.baseideaunit.insertTopLevelItems(0, [tree_root])

        root = self.baseideaunit.invisibleRootItem()
        self.pyqt_tree_setExpanded(root)
        # self.yo_tree_item_setHidden(setHiddenBool=True)

    # expand to depth set by agent
    def pyqt_tree_setExpanded(self, root):
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            item.setExpanded(item.data(2, 20))
            self.pyqt_tree_setExpanded(item)

    def idea_tree_set_is_expanded(self, root):
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            desc_x = item.data(2, 10)
            road_x = item.data(2, 11)
            is_expanded = item.isExpanded()
            # print(f"{road_x},{desc_x}")
            _road = f"{desc_x}" if road_x in ("", None) else f"{road_x},{desc_x}"
            # print(f"road={road_x},{desc_x}")
            # print(f"{_road=}")

            self.agent_x.edit_idea_attr(road=_road, is_expanded=is_expanded)
            self.idea_tree_set_is_expanded(item)

    def required_table_select(self):
        self.required_base_combo_load()
        self.required_base_combo.setCurrentText(
            self.required_table.item(self.required_table.currentRow(), 2).text()
        )
        self.required_sufffact_combo.setCurrentText(
            self.required_table.item(self.required_table.currentRow(), 3).text()
        )
        self.required_sufffact_open.setText(
            self.required_table.item(self.required_table.currentRow(), 4).text()
        )
        self.required_sufffact_nigh.setText(
            self.required_table.item(self.required_table.currentRow(), 5).text()
        )
        self.required_sufffact_divisor.setText(
            self.required_table.item(self.required_table.currentRow(), 6).text()
        )

        if self.required_sufffact_divisor.toPlainText() != "":
            if float(self.required_sufffact_divisor.toPlainText()) % 10080 == 0:
                self.set_weeks_repeat_sufffactunit_hregtime()
            elif float(self.required_sufffact_divisor.toPlainText()) % 1440 == 0:
                self.set_days_repeat_sufffactunit_hregtime()

    def set_days_repeat_sufffactunit_hregtime(self):
        days_minutes = float(self.required_sufffact_open.toPlainText())
        day_minutes = days_minutes % 1440
        days_repeat = float(self.required_sufffact_divisor.toPlainText()) / 1440
        self.hreg_days_repeat.setText(str(int(days_repeat)))

        days_remainder = (days_minutes - day_minutes) / 1440
        self.hreg_days_remainder.setText(str(int(days_remainder)))

        event_minute = day_minutes % 60
        self.hreg_open_min.setCurrentText(str(int(event_minute)))

        event_hour = (day_minutes - event_minute) / 60
        self.hreg_open_hr.setCurrentText(str(int(event_hour)))

    def set_weeks_repeat_sufffactunit_hregtime(self):
        self.hreg_weeks_repeat.setText(
            str(int(float(self.required_sufffact_divisor.toPlainText()) / 1440))
        )

        week_extra_min = float(self.required_sufffact_open.toPlainText()) % 10080
        week_remainder = (
            float(self.required_sufffact_open.toPlainText()) - week_extra_min
        ) / 10080
        self.hreg_weeks_remainder.setText(str(int(week_remainder)))

        day_minutes_extra = week_extra_min % 1440
        days_extra = (week_extra_min - day_minutes_extra) / 1440
        if days_extra == 0:
            self.hreg_weekday.setCurrentText("Saturday")
        elif days_extra == 1:
            self.hreg_weekday.setCurrentText("Sunday")
        elif days_extra == 2:
            self.hreg_weekday.setCurrentText("Monday")
        elif days_extra == 3:
            self.hreg_weekday.setCurrentText("Tuesday")
        elif days_extra == 4:
            self.hreg_weekday.setCurrentText("Wednesday")
        elif days_extra == 5:
            self.hreg_weekday.setCurrentText("Thursday")
        elif days_extra == 6:
            self.hreg_weekday.setCurrentText("Friday")

        event_minute = day_minutes_extra % 60

        self.hreg_open_min.setCurrentText(str(int(event_minute)))
        event_hour = (day_minutes_extra - event_minute) / 60
        self.hreg_open_hr.setCurrentText(str(int(event_hour)))

        days_extra = week_extra_min - 0

    def set_weeks_repeat_sufffactunit_hregtime(self):
        self.hreg_weeks_repeat.setText(
            str(int(float(self.required_sufffact_divisor.toPlainText()) / 10080))
        )

        week_extra_min = float(self.required_sufffact_open.toPlainText()) % 10080
        week_remainder = (
            float(self.required_sufffact_open.toPlainText()) - week_extra_min
        ) / 10080
        self.hreg_weeks_remainder.setText(str(int(week_remainder)))

        day_minutes_extra = week_extra_min % 1440
        days_extra = (week_extra_min - day_minutes_extra) / 1440
        if days_extra == 0:
            self.hreg_weekday.setCurrentText("Saturday")
        elif days_extra == 1:
            self.hreg_weekday.setCurrentText("Sunday")
        elif days_extra == 2:
            self.hreg_weekday.setCurrentText("Monday")
        elif days_extra == 3:
            self.hreg_weekday.setCurrentText("Tuesday")
        elif days_extra == 4:
            self.hreg_weekday.setCurrentText("Wednesday")
        elif days_extra == 5:
            self.hreg_weekday.setCurrentText("Thursday")
        elif days_extra == 6:
            self.hreg_weekday.setCurrentText("Friday")

        event_minute = day_minutes_extra % 60

        self.hreg_open_min.setCurrentText(str(int(event_minute)))
        event_hour = (day_minutes_extra - event_minute) / 60
        self.hreg_open_hr.setCurrentText(str(int(event_hour)))

        days_extra = week_extra_min - 0
