# # command to for converting ui form to python file: pyuic5 ui\CureMainUI.ui -o ui\CureMainUI.py
from ui.CureMainUI import Ui_MainWindow
from Edit5Issue import Edit5Issue
from EditMain import EditMainView
from PyQt5 import QtCore as qtc
from src.pact.pact import (
    PactUnit,
    get_from_json as get_pact_from_json,
)
from sys import argv as sys_argv, exit as sys_exit
from PyQt5.QtWidgets import (
    QTableWidgetItem as qtw1,
    QApplication,
    QMainWindow,
)
from src.cure.cure import cureunit_shop
from src.cure.examples.cure_env_kit import (
    create_example_cures_list,
    setup_test_example_environment,
    create_example_cure,
    delete_dir_example_cure,
    rename_example_cure,
    get_test_cures_dir,
)

from src.pact.party import get_depotlink_types
from src.pact.x_func import (
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)
from pyqt_func import pact_importance_diplay


class MainApp(QApplication):
    """The main application object"""

    def __init__(self, argv):
        super().__init__(argv)

        self.main_window = MainWindow()
        self.main_window.show()

        # create editmain instance
        self.editmain_view = EditMainView()
        # create slot for making editmain visible
        self.main_window.open_editmain.connect(self.editmain_show)

        # create instance
        self.edit5issue_view = Edit5Issue()
        # create slot for making visible
        self.main_window.open_edit5issue.connect(self.edit5issue_show)

    def editmain_show(self):
        if self.main_window.ignore_pact_x is None:
            self.main_window.isol = self.main_window.healer_x._admin.open_isol_pact()
            self.editmain_view.pact_x = self.main_window.isol
        else:
            self.editmain_view.pact_x = self.main_window.ignore_pact_x
        self.editmain_view.refresh_all()
        self.editmain_view.show()

    def edit5issue_show(self):
        if self.main_window.healer_x != None:
            self.edit5issue_view.healer_x = self.main_window.healer_x
            self.edit5issue_view.refresh_all()
            self.edit5issue_view.show()


class MainWindow(QMainWindow, Ui_MainWindow):
    """The main application window"""

    open_editmain = qtc.pyqtSignal(bool)
    open_edit5issue = qtc.pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        # signals for opening windows
        self.refresh_all_button.clicked.connect(self.refresh_all)
        self.cure_insert_button.clicked.connect(self.cure_insert)
        self.cure_load_button.clicked.connect(self.cure_load_from_file)
        self.cure_update_button.clicked.connect(self.cure_update_title)
        self.cure_delete_button.clicked.connect(self.cure_delete)
        self.pact_insert_button.clicked.connect(self.pact_insert)
        self.pact_update_button.clicked.connect(self.pact_update_title)
        self.pact_delete_button.clicked.connect(self.pact_delete)
        self.pacts_table.itemClicked.connect(self.pacts_table_select)
        self.healer_insert_button.clicked.connect(self.healer_insert)
        self.healer_update_button.clicked.connect(self.healer_update_title)
        self.healer_delete_button.clicked.connect(self.healer_delete)
        self.healers_table.itemClicked.connect(self.healers_table_select)
        self.reload_all_src_pacts_button.clicked.connect(self.reload_all_src_pacts)
        self.set_public_pact_button.clicked.connect(self.save_output_pact_to_public())
        self.set_public_and_reload_srcs_button.clicked.connect(
            self.set_public_and_reload_srcs
        )
        self.ignores_table.itemClicked.connect(self.ignores_table_select)
        self.open_ignore_button.clicked.connect(self.open_editmain)
        self.save_ignore_button.clicked.connect(self.ignore_pact_file_update)
        self.ignores_table.setHidden(True)
        self.show_ignores_button.clicked.connect(self.show_ignores_table)
        self.show_digests_button.clicked.connect(self.show_digests_table)
        self.isol_open_button.clicked.connect(self.open_editmain)
        self.isol_save_button.clicked.connect(self.save_isol)

        self.depotlink_insert_button.clicked.connect(self.depotlink_insert)
        self.depotlink_update_button.clicked.connect(self.depotlink_update)
        self.depotlink_delete_button.clicked.connect(self.depotlink_delete)
        self.depotlinks_table.itemClicked.connect(self.depotlinks_table_select)
        self.five_issue_button.clicked.connect(self.open_edit5issue)

        self.cure_x = None
        self.healer_x = None
        self.ignore_pact_x = None
        setup_test_example_environment()
        first_env = "ex5"
        self.cure_x = cureunit_shop(title=first_env, cures_dir=get_test_cures_dir())
        self.refresh_cure()
        self.cure_handle_combo_refresh()
        self.cure_handle_combo.setCurrentText(first_env)
        self._healer_load(healer_title="ernie")

    def save_isol(self):
        if self.isol != None:
            self.healer_x._admin.save_isol_pact(self.isol)
        self.refresh_healer()

    def reload_all_src_pacts(self):
        if self.cure_x != None:
            self.cure_x.reload_all_healers_src_pactunits()

    def set_public_and_reload_srcs(self):
        self.save_output_pact_to_public()
        self.reload_all_src_pacts()

    def save_output_pact_to_public(self):
        if self.healer_x != None:
            self.healer_x.save_output_pact_to_public()
        self.refresh_cure()

    def cure_load_from_file(self):
        cure_selected = self.cure_handle_combo.currentText()
        self.cure_x = cureunit_shop(title=cure_selected, cures_dir=get_test_cures_dir())
        self.cure_x.create_dirs_if_null(in_memory_bank=False)
        self.cure_handle.setText(cure_selected)
        self.refresh_cure()

    def pacts_table_select(self):
        self.pact_healer.setText(
            self.pacts_table.item(self.pacts_table.currentRow(), 0).text()
        )
        if self.healers_table.currentRow() != -1:
            selected_healer = self.healers_table.item(
                self.healers_table.currentRow(), 0
            ).text()
            selected_pact = self.pacts_table.item(
                self.pacts_table.currentRow(), 0
            ).text()
            self.depotlink_title.setText(f"{selected_healer} - {selected_pact}")

    def healers_table_select(self):
        healer_x_title = self.healers_table.item(
            self.healers_table.currentRow(), 0
        ).text()
        self._healer_load(healer_title=healer_x_title)

    def _healer_load(self, healer_title: str):
        self.cure_x.create_healerunit_from_public(title=healer_title)
        self.healer_x = self.cure_x._healerunits.get(healer_title)
        self.healer_title.setText(self.healer_x._admin.title)
        self.refresh_healer()

    def depotlinks_table_select(self):
        self.depotlink_title.setText(
            self.depotlinks_table.item(self.depotlinks_table.currentRow(), 0).text()
        )
        self.depotlink_type_combo.setCurrentText(
            self.depotlinks_table.item(self.depotlinks_table.currentRow(), 1).text()
        )
        self.depotlink_weight.setText(
            self.depotlinks_table.item(self.depotlinks_table.currentRow(), 2).text()
        )

    def ignores_table_select(self):
        ignore_pact_healer = self.ignores_table.item(
            self.ignores_table.currentRow(), 0
        ).text()
        # self.ignore_pact_x = self.cure_x.get_public_pact(
        self.ignore_pact_x = self.cure_x.get_pact_from_ignores_dir(
            healer_title=self.healer_x._admin.title, _healer=ignore_pact_healer
        )
        self.edit_pact = self.ignore_pact_x

    def ignore_pact_file_update(self):
        self.cure_x.set_ignore_pact_file(
            healer_title=self.healer_x._admin.title, pact_obj=self.ignore_pact_x
        )
        self.refresh_healer()

    def show_ignores_table(self):
        self.ignores_table.setHidden(False)
        self.digests_table.setHidden(True)

    def show_digests_table(self):
        self.ignores_table.setHidden(True)
        self.digests_table.setHidden(False)

    def cure_insert(self):
        create_example_cure(cure_handle=self.cure_handle.text())
        self.cure_handle_combo_refresh()

    def cure_update_title(self):
        rename_example_cure(cure_obj=self.cure_x, new_title=self.cure_handle.text())
        self.cure_handle_combo_refresh()

    def cure_delete(self):
        delete_dir_example_cure(cure_obj=self.cure_x)
        self.cure_x = None
        self.cure_handle_combo_refresh()
        self.refresh_cure()

    def pact_insert(self):
        self.cure_x.save_public_pact(pact_x=PactUnit(_healer=self.pact_healer.text()))
        self.refresh_cure()

    def pact_update_title(self):
        currently_selected = self.pacts_table.item(
            self.pacts_table.currentRow(), 0
        ).text()
        typed_in = self.pact_healer.text()
        if currently_selected != typed_in:
            self.cure_x.rename_public_pact(
                old_label=currently_selected, new_label=typed_in
            )
            self.refresh_cure()

    def pact_delete(self):
        self.cure_x.del_public_pact(
            pact_x_label=self.pacts_table.item(self.pacts_table.currentRow(), 0).text()
        )
        self.refresh_cure()

    def healer_insert(self):
        self.cure_x.create_new_healerunit(healer_title=self.healer_title.text())
        self.refresh_healers()

    def healer_update_title(self):
        currently_selected = self.healers_table.item(
            self.healers_table.currentRow(), 0
        ).text()
        typed_in = self.healer_title.text()
        if currently_selected != typed_in:
            self.cure_x.rename_healerunit(
                old_label=currently_selected, new_label=typed_in
            )
            self.refresh_healers()

    def healer_delete(self):
        self.cure_x.del_healer_dir(
            healer_title=self.healers_table.item(
                self.healers_table.currentRow(), 0
            ).text()
        )
        self.refresh_healers()

    def depotlink_insert(self):
        pact_healer = self.pacts_table.item(self.pacts_table.currentRow(), 0).text()
        if self.healer_x != None:
            pact_json = x_func_open_file(
                dest_dir=self.healer_x._admin._pacts_public_dir,
                file_title=f"{pact_healer}.json",
            )
            pact_x = get_pact_from_json(pact_json)
            self.healer_x.set_depot_pact(
                pact_x=pact_x,
                depotlink_type=self.depotlink_type_combo.currentText(),
                depotlink_weight=self.depotlink_weight.text(),
            )
            self.cure_x.save_healer_file(healer_title=self.healer_x._admin.title)
        self.refresh_healer()

    def depotlink_update(self):
        healer_title_x = self.healer_x._admin.title
        self.cure_x.update_depotlink(
            healer_title=healer_title_x,
            partytitle=self.depotlink_title.text(),
            depotlink_type=self.depotlink_type_combo.currentText(),
            creditor_weight=self.depotlink_weight.text(),
            debtor_weight=self.depotlink_weight.text(),
        )
        self.cure_x.save_healer_file(healer_title=healer_title_x)
        self.refresh_healer()

    def depotlink_delete(self):
        healer_title_x = self.healer_x._admin.title
        self.cure_x.del_depotlink(
            healer_title=healer_title_x, pactunit_healer=self.depotlink_title.text()
        )
        self.cure_x.save_healer_file(healer_title=healer_title_x)
        self.refresh_healer()

    def get_pact_healer_list(self):
        pacts_list = []
        for file_title in self.get_public_dir_file_titles_list():
            pact_json = x_func_open_file(
                dest_dir=self.get_public_dir(), file_title=file_title
            )
            pacts_list.append(get_pact_from_json(cx_json=pact_json))
        return pacts_list

    def get_healer_title_list(self):
        healers_healer_list = []
        if self.cure_x != None:
            healers_healer_list.extend(
                [healer_dir] for healer_dir in self.cure_x.get_healer_dir_paths_list()
            )
        return healers_healer_list

    def get_depotlink_list(self):
        depotlinks_list = []
        if self.healer_x != None:
            for cl_val in self.healer_x._depotlinks.values():
                depotlink_row = [
                    cl_val.pact_healer,
                    cl_val.depotlink_type,
                    str(cl_val.weight),
                ]
                depotlinks_list.append(depotlink_row)
        return depotlinks_list

    def get_digests_list(self):
        x_list = []
        if self.healer_x != None:
            digest_file_list = x_func_dir_files(
                dir_path=self.healer_x_admin._pacts_digest_dir,
                remove_extensions=True,
                include_dirs=False,
                include_files=True,
            )
            x_list.extend([file] for file in digest_file_list)
        return x_list

    def get_ignores_list(self):
        x_list = []
        if self.healer_x != None:
            digest_file_list = x_func_dir_files(
                dir_path=self.healer_x._admin._pacts_ignore_dir,
                remove_extensions=True,
                include_dirs=False,
                include_files=True,
            )
            x_list.extend([file] for file in digest_file_list)
        return x_list

    def get_p_ideas_list(self):
        x_list = []
        if self.healer_output_pact != None:
            idea_list = self.healer_output_pact.get_idea_tree_ordered_road_list()

            for idea_road in idea_list:
                idea_obj = self.healer_output_pact.get_idea_kid(idea_road)

                if idea_obj._pad.find("time") != 3:
                    x_list.append(
                        [
                            pact_importance_diplay(idea_obj._pact_importance),
                            idea_road,
                            len(idea_obj._balancelinks),
                        ]
                    )

        return x_list

    def get_p_partys_list(self):
        x_list = []
        if self.healer_output_pact != None:
            x_list.extend(
                [
                    f"{pact_importance_diplay(partyunit._pact_credit)}/{pact_importance_diplay(partyunit._pact_debt)}",
                    partyunit.title,
                    f"{partyunit.creditor_weight}/{partyunit.debtor_weight}",
                ]
                for partyunit in self.healer_output_pact._partys.values()
            )
        return x_list

    def get_p_groups_list(self):
        x_list = []
        if self.healer_output_pact != None:
            x_list.extend(
                [
                    f"{pact_importance_diplay(groupunit._pact_debt)}/{pact_importance_diplay(groupunit._pact_credit)}",
                    groupunit.brand,
                    len(groupunit._partys),
                ]
                for groupunit in self.healer_output_pact._groups.values()
            )
        return x_list

    def get_p_acptfacts_list(self):
        x_list = []
        if self.healer_output_pact != None:
            for (
                acptfactunit
            ) in self.healer_output_pact._idearoot._acptfactunits.values():
                open_nigh = ""
                if acptfactunit.open is None and acptfactunit.nigh is None:
                    open_nigh = ""
                else:
                    open_nigh = f"{acptfactunit.open}-{acptfactunit.nigh}"

                x_list.append(
                    [
                        acptfactunit.base,
                        acptfactunit.pick.replace(acptfactunit.base, ""),
                        open_nigh,
                    ]
                )
        return x_list

    def get_p_agenda_list(self):
        x_list = []
        if self.healer_output_pact != None:
            agenda_list = self.healer_output_pact.get_agenda_items()
            agenda_list.sort(key=lambda x: x._pact_importance, reverse=True)
            x_list.extend(
                [
                    pact_importance_diplay(agenda_item._pact_importance),
                    agenda_item._label,
                    agenda_item._pad,
                ]
                for agenda_item in agenda_list
            )
        return x_list

    def refresh_all(self):
        self.refresh_cure()

    def _sub_refresh_healers_table(self):
        self.refresh_x(
            self.healers_table, ["Healers Table"], self.get_healer_title_list()
        )

    def _sub_refresh_depotlinks_table(self):
        depotlink_types = list(get_depotlink_types())
        depotlink_types.insert(0, "")
        self.depotlink_type_combo.clear()
        self.depotlink_type_combo.addItems(depotlink_types)
        self.depotlink_type_combo.setCurrentText("")
        column_header = ""
        if self.healer_x is None:
            column_header = "Pactlinks Table"
        elif self.healer_x != None:
            column_header = f"'{self.healer_x._admin.title}' Pactlinks"
        self.refresh_x(
            self.depotlinks_table,
            [column_header, "Link Type", "Weight"],
            self.get_depotlink_list(),
        )

    def _sub_refresh_digests_table(self):
        self.refresh_x(self.digests_table, ["digests_table"], self.get_digests_list())

    def _sub_refresh_ignores_table(self):
        ignores_list = self.get_ignores_list()
        if len(ignores_list) >= 0:
            column_headers = [
                f"Ignores Table ({len(ignores_list)})",
            ]
        self.refresh_x(self.ignores_table, column_headers, ignores_list)

    def _sub_refresh_p_ideas_table(self):
        p_ideas_list = self.get_p_ideas_list()
        if len(p_ideas_list) >= 0:
            column_headers = [
                "pact_importance",
                f"Ideas Table ({len(p_ideas_list)})",
                "balancelinks",
            ]
        else:
            column_headers = [
                "pact_importance",
                "Ideas Table",
                "balancelinks",
            ]

        self.w_ideas_table.setObjectName("Ideas Table")
        self.w_ideas_table.setColumnHidden(0, False)
        self.w_ideas_table.setColumnHidden(1, False)
        self.w_ideas_table.setColumnHidden(2, False)
        self.refresh_x(
            table_x=self.w_ideas_table,
            column_header=column_headers,
            populate_list=p_ideas_list,
            column_width=[50, 300, 50],
        )

    def _sub_refresh_p_partys_table(self):
        p_partys_list = self.get_p_partys_list()
        column_headers = [
            "pact_debt/pact_credit",
            f"Partys ({len(p_partys_list)})",
            "creditor_weight/debtor_weight",
        ]

        self.refresh_x(
            table_x=self.w_partys_table,
            column_header=column_headers,
            populate_list=p_partys_list,
            column_width=[50, 300, 50],
        )

    def _sub_refresh_p_groups_table(self):
        p_groups_list = self.get_p_groups_list()
        column_headers = [
            "pact_debt/pact_credit",
            f"groups ({len(p_groups_list)})",
            "Partys",
        ]

        self.refresh_x(
            table_x=self.w_groups_table,
            column_header=column_headers,
            populate_list=p_groups_list,
            column_width=[50, 300, 100],
        )

    def _sub_refresh_p_acptfacts_table(self):
        p_acptfacts_list = self.get_p_acptfacts_list()
        column_headers = [f"Bases ({len(p_acptfacts_list)})", "AcptFacts", "Open-Nigh"]

        self.refresh_x(
            table_x=self.w_acptfacts_table,
            column_header=column_headers,
            populate_list=p_acptfacts_list,
            column_width=[200, 100, 200],
        )

    def _sub_refresh_p_agenda_table(self):
        p_agenda_list = self.get_p_agenda_list()
        column_headers = [
            "pact_importance",
            f"Agenda ({len(p_agenda_list)})",
            "Idea Walk",
        ]

        self.refresh_x(
            table_x=self.w_agenda_table,
            column_header=column_headers,
            populate_list=p_agenda_list,
            column_width=[50, 200, 300],
        )

    def cure_handle_combo_refresh(self):
        self.cure_handle_combo.clear()
        self.cure_handle_combo.addItems(create_example_cures_list())

    def refresh_healers(self):
        self.healer_x = None
        self._sub_refresh_healers_table()
        self.refresh_healer()

    def refresh_healer(self):
        self._sub_refresh_depotlinks_table()
        self._sub_refresh_digests_table()
        self._sub_refresh_ignores_table()
        self.healer_output_pact = None
        if self.healer_x != None:
            self.healer_output_pact = self.healer_x._admin.get_remelded_output_pact()
        self._sub_refresh_p_ideas_table()
        self._sub_refresh_p_partys_table()
        self._sub_refresh_p_groups_table()
        self._sub_refresh_p_acptfacts_table()
        self._sub_refresh_p_agenda_table()

    def refresh_cure(self):
        self.refresh_x(self.pacts_table, ["Pacts Table"], self.get_pact_healer_list())
        self.refresh_healers()

    def refresh_x(
        self,
        table_x,
        column_header: list[str],
        populate_list: list[any],
        column_width: list[int] = None,
    ):
        table_x.setObjectName(column_header[0])
        if column_width is None:
            table_x.setColumnWidth(0, 150)
            table_x.setColumnHidden(0, False)
        else:
            table_x.setColumnWidth(0, column_width[0])
            table_x.setColumnWidth(1, column_width[1])
            table_x.setColumnWidth(2, column_width[2])

        table_x.clear()
        table_x.setHorizontalHeaderLabels(column_header)
        table_x.verticalHeader().setVisible(False)
        table_x.setRowCount(0)
        for row, list_x in enumerate(populate_list):
            table_x.setRowCount(row + 1)
            table_x.setRowHeight(row, 9)
            if len(list_x) == 3:
                table_x.setHorizontalHeaderLabels(column_header)
                table_x.setItem(row, 0, qtw1(str(list_x[0])))
                table_x.setItem(row, 1, qtw1(str(list_x[1])))
                table_x.setItem(row, 2, qtw1(str(list_x[2])))
            elif len(list_x) == 1:
                table_x.setItem(row, 0, qtw1(list_x[0]))


if __title__ == "__main__":
    app = MainApp(sys_argv)
    sys_exit(app.exec())
