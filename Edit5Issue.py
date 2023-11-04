# command to for converting ui form to python file: pyuic5 ui\culture5IssueUI.ui -o ui\culture5IssueUI.py
import sys
from ui.Culture5IssueUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from pyqt_func import agenda_importance_diplay
from src.agenda.agenda import agendaunit_shop
from src.agenda.group import groupunit_shop
from src.agenda.party import partylink_shop


class Edit5Issue(qtw.QTableWidget, Ui_Form):
    party_selected = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        # self.group_update_button.clicked.connect(self.group_update)
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)
        self.selected_party_handle = None
        self.partyunit_x = None
        self.groupunit_x = None

    def refresh_all(self):
        pass
