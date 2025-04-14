from src.a00_data_toolboxs.file_toolbox import (
    create_path,
    get_directory_path,
    save_file,
    open_file,
    delete_dir,
    get_dir_file_strs,
    set_dir,
    get_integer_filenames,
    get_max_file_number,
    get_json_filename,
)
from src.a00_data_toolboxs.dict_toolbox import get_empty_set_if_None
from src.a00_data_toolboxs.db_toolbox import sqlite_connection
from src.a02_finance_toolboxs.finance_config import (
    default_fund_coin_if_None,
    validate_fund_pool,
    default_respect_bit_if_None,
    filter_penny,
    default_money_magnitude_if_None,
    TimeLinePoint,
)
from src.a02_finance_toolboxs.deal import (
    DealUnit,
    dealunit_shop,
    BrokerUnit,
    brokerunit_shop,
    get_dealunit_from_json,
)
from src.a01_word_logic.road import (
    OwnerName,
    FiscTitle,
    TitleUnit,
    RoadUnit,
    rebuild_road,
    get_all_road_titles,
    validate_titleunit,
    default_bridge_if_None,
)
from src.a06_bud_logic.bud import (
    BudUnit,
    get_from_json as budunit_get_from_json,
    budunit_shop,
)
from src.a06_bud_logic.bud_tool import get_acct_agenda_net_ledger
from src.a08_bud_atom_logic.atom import (
    BudAtom,
    get_from_json as budatom_get_from_json,
    modify_bud_with_budatom,
)
from src.a09_pack_logic.pack import (
    get_init_pack_id_if_None,
    init_pack_id,
    PackUnit,
    packunit_shop,
    create_packunit_from_files,
)
from src.f06_listen.basis_buds import get_default_plan
from src.f06_listen.hub_path import treasury_filename
from src.f06_listen.hub_tool import (
    save_gut_file,
    open_gut_file,
    save_plan_file,
    open_plan_file,
    gut_file_exists,
    plan_file_exists,
)
from os.path import exists as os_path_exists
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection


class Invalid_gut_Exception(Exception):
    pass


class Invalid_plan_Exception(Exception):
    pass


class SavepackFileException(Exception):
    pass


class packFileMissingException(Exception):
    pass


class get_keep_roadsException(Exception):
    pass


class _keep_roadMissingException(Exception):
    pass


class _save_valid_budpoint_Exception(Exception):
    pass


class calc_timepoint_deal_Exception(Exception):
    pass


def get_keep_dutys_dir(x_keep_dir: str) -> str:
    return create_path(x_keep_dir, "dutys")


def get_keep_jobs_dir(x_keep_dir: str) -> str:
    return create_path(x_keep_dir, "jobs")


def get_keep_grades_dir(x_keep_dir: str) -> str:
    return create_path(x_keep_dir, "grades")


@dataclass
class HubUnit:
    owner_name: OwnerName = None
    fisc_mstr_dir: str = None
    fisc_title: str = None
    keep_road: RoadUnit = None
    bridge: str = None
    fund_pool: float = None
    fund_coin: float = None
    respect_bit: float = None
    penny: float = None
    keep_point_magnitude: float = None
    _fisc_dir: str = None
    _owners_dir: str = None
    _owner_dir: str = None
    _keeps_dir: str = None
    _atoms_dir: str = None
    _packs_dir: str = None
    _deals_dir: str = None

    def set_dir_attrs(self):
        fiscs_dir = create_path(self.fisc_mstr_dir, "fiscs")
        self._fisc_dir = create_path(fiscs_dir, self.fisc_title)
        self._owners_dir = create_path(self._fisc_dir, "owners")
        self._owner_dir = create_path(self._owners_dir, self.owner_name)
        self._keeps_dir = create_path(self._owner_dir, "keeps")
        self._atoms_dir = create_path(self._owner_dir, "atoms")
        self._packs_dir = create_path(self._owner_dir, "packs")
        self._deals_dir = create_path(self._owner_dir, "deals")

    def default_gut_bud(self) -> BudUnit:
        x_budunit = budunit_shop(
            owner_name=self.owner_name,
            fisc_title=self.fisc_title,
            bridge=self.bridge,
            fund_pool=self.fund_pool,
            fund_coin=self.fund_coin,
            respect_bit=self.respect_bit,
            penny=self.penny,
        )
        x_budunit.last_pack_id = init_pack_id()
        return x_budunit

    # pack methods
    def get_max_atom_file_number(self) -> int:
        return get_max_file_number(self._atoms_dir)

    def _get_next_atom_file_number(self) -> int:
        max_file_number = self.get_max_atom_file_number()
        return 0 if max_file_number is None else max_file_number + 1

    def atom_filename(self, atom_number: int) -> str:
        return f"{atom_number}.json"

    def atom_file_path(self, atom_number: int) -> str:
        return create_path(self._atoms_dir, self.atom_filename(atom_number))

    def _save_valid_atom_file(self, x_atom: BudAtom, file_number: int):
        save_file(
            self._atoms_dir,
            self.atom_filename(file_number),
            x_atom.get_json(),
            replace=False,
        )
        return file_number

    def save_atom_file(self, x_atom: BudAtom):
        x_atom_filename = self._get_next_atom_file_number()
        return self._save_valid_atom_file(x_atom, x_atom_filename)

    def atom_file_exists(self, atom_number: int) -> bool:
        return os_path_exists(self.atom_file_path(atom_number))

    def delete_atom_file(self, atom_number: int):
        delete_dir(self.atom_file_path(atom_number))

    def _get_bud_from_atom_files(self) -> BudUnit:
        x_bud = budunit_shop(self.owner_name, self.fisc_title)
        if self.atom_file_exists(self.get_max_atom_file_number()):
            x_atom_files = get_dir_file_strs(self._atoms_dir, delete_extensions=True)
            sorted_atom_filenames = sorted(list(x_atom_files.keys()))

            for x_atom_filename in sorted_atom_filenames:
                x_file_str = x_atom_files.get(x_atom_filename)
                x_atom = budatom_get_from_json(x_file_str)
                modify_bud_with_budatom(x_bud, x_atom)
        return x_bud

    def get_max_pack_file_number(self) -> int:
        return get_max_file_number(self._packs_dir)

    def _get_next_pack_file_number(self) -> int:
        max_file_number = self.get_max_pack_file_number()
        init_pack_id = get_init_pack_id_if_None()
        return init_pack_id if max_file_number is None else max_file_number + 1

    def pack_filename(self, pack_id: int) -> str:
        return get_json_filename(pack_id)

    def pack_file_path(self, pack_id: int) -> bool:
        pack_filename = self.pack_filename(pack_id)
        return create_path(self._packs_dir, pack_filename)

    def pack_file_exists(self, pack_id: int) -> bool:
        return os_path_exists(self.pack_file_path(pack_id))

    def validate_packunit(self, x_packunit: PackUnit) -> PackUnit:
        if x_packunit._atoms_dir != self._atoms_dir:
            x_packunit._atoms_dir = self._atoms_dir
        if x_packunit._packs_dir != self._packs_dir:
            x_packunit._packs_dir = self._packs_dir
        if x_packunit._pack_id != self._get_next_pack_file_number():
            x_packunit._pack_id = self._get_next_pack_file_number()
        if x_packunit.owner_name != self.owner_name:
            x_packunit.owner_name = self.owner_name
        if x_packunit._delta_start != self._get_next_atom_file_number():
            x_packunit._delta_start = self._get_next_atom_file_number()
        return x_packunit

    def save_pack_file(
        self,
        x_pack: PackUnit,
        replace: bool = True,
        correct_invalid_attrs: bool = True,
    ) -> PackUnit:
        if correct_invalid_attrs:
            x_pack = self.validate_packunit(x_pack)

        if x_pack._atoms_dir != self._atoms_dir:
            raise SavepackFileException(
                f"PackUnit file cannot be saved because packunit._atoms_dir is incorrect: {x_pack._atoms_dir}. It must be {self._atoms_dir}."
            )
        if x_pack._packs_dir != self._packs_dir:
            raise SavepackFileException(
                f"PackUnit file cannot be saved because packunit._packs_dir is incorrect: {x_pack._packs_dir}. It must be {self._packs_dir}."
            )
        if x_pack.owner_name != self.owner_name:
            raise SavepackFileException(
                f"PackUnit file cannot be saved because packunit.owner_name is incorrect: {x_pack.owner_name}. It must be {self.owner_name}."
            )
        pack_filename = self.pack_filename(x_pack._pack_id)
        if not replace and self.pack_file_exists(x_pack._pack_id):
            raise SavepackFileException(
                f"PackUnit file {pack_filename} exists and cannot be saved over."
            )
        x_pack.save_files()
        return x_pack

    def _del_pack_file(self, pack_id: int):
        delete_dir(self.pack_file_path(pack_id))

    def _default_packunit(self) -> PackUnit:
        return packunit_shop(
            owner_name=self.owner_name,
            _pack_id=self._get_next_pack_file_number(),
            _atoms_dir=self._atoms_dir,
            _packs_dir=self._packs_dir,
        )

    def create_save_pack_file(self, before_bud: BudUnit, after_bud: BudUnit):
        new_packunit = self._default_packunit()
        new_buddelta = new_packunit._buddelta
        new_buddelta.add_all_different_budatoms(before_bud, after_bud)
        self.save_pack_file(new_packunit)

    def get_packunit(self, pack_id: int) -> PackUnit:
        if self.pack_file_exists(pack_id) is False:
            raise packFileMissingException(
                f"PackUnit file_number {pack_id} does not exist."
            )
        x_packs_dir = self._packs_dir
        x_atoms_dir = self._atoms_dir
        return create_packunit_from_files(x_packs_dir, pack_id, x_atoms_dir)

    def _merge_any_packs(self, x_bud: BudUnit) -> BudUnit:
        packs_dir = self._packs_dir
        pack_ints = get_integer_filenames(packs_dir, x_bud.last_pack_id)
        if len(pack_ints) == 0:
            return copy_deepcopy(x_bud)

        for pack_int in pack_ints:
            x_pack = self.get_packunit(pack_int)
            new_bud = x_pack._buddelta.get_edited_bud(x_bud)
        return new_bud

    def _create_initial_pack_files_from_default(self):
        x_packunit = packunit_shop(
            owner_name=self.owner_name,
            _pack_id=get_init_pack_id_if_None(),
            _packs_dir=self._packs_dir,
            _atoms_dir=self._atoms_dir,
        )
        x_packunit._buddelta.add_all_different_budatoms(
            before_bud=self.default_gut_bud(),
            after_bud=self.default_gut_bud(),
        )
        x_packunit.save_files()

    def _create_gut_from_packs(self):
        x_bud = self._merge_any_packs(self.default_gut_bud())
        save_gut_file(self.fisc_mstr_dir, x_bud)

    def _create_initial_pack_and_gut_files(self):
        self._create_initial_pack_files_from_default()
        self._create_gut_from_packs()

    def _create_initial_pack_files_from_gut(self):
        x_packunit = self._default_packunit()
        x_packunit._buddelta.add_all_different_budatoms(
            before_bud=self.default_gut_bud(),
            after_bud=open_gut_file(
                self.fisc_mstr_dir, self.fisc_title, self.owner_name
            ),
        )
        x_packunit.save_files()

    def initialize_pack_gut_files(self):
        x_gut_file_exists = gut_file_exists(
            self.fisc_mstr_dir, self.fisc_title, self.owner_name
        )
        pack_file_exists = self.pack_file_exists(init_pack_id())
        if x_gut_file_exists is False and pack_file_exists is False:
            self._create_initial_pack_and_gut_files()
        elif x_gut_file_exists is False and pack_file_exists:
            self._create_gut_from_packs()
        elif x_gut_file_exists and pack_file_exists is False:
            self._create_initial_pack_files_from_gut()

    def append_packs_to_gut_file(self):
        gut_bud = open_gut_file(self.fisc_mstr_dir, self.fisc_title, self.owner_name)
        gut_bud = self._merge_any_packs(gut_bud)
        save_gut_file(self.fisc_mstr_dir, gut_bud)
        return gut_bud

    # Deal methods
    def timepoint_dir(self, x_deal_time: TimeLinePoint) -> str:
        return create_path(self._deals_dir, str(x_deal_time))

    def deal_filename(self) -> str:
        return "dealunit.json"

    def deal_file_path(self, x_deal_time: TimeLinePoint) -> str:
        return create_path(self.timepoint_dir(x_deal_time), self.deal_filename())

    def _save_valid_deal_file(self, x_deal: DealUnit):
        x_deal.calc_magnitude()
        save_file(
            self.timepoint_dir(x_deal.deal_time),
            self.deal_filename(),
            x_deal.get_json(),
            replace=True,
        )

    def deal_file_exists(self, x_deal_time: TimeLinePoint) -> bool:
        return os_path_exists(self.deal_file_path(x_deal_time))

    def get_deal_file(self, x_deal_time: TimeLinePoint) -> DealUnit:
        if self.deal_file_exists(x_deal_time):
            x_json = open_file(self.timepoint_dir(x_deal_time), self.deal_filename())
            return get_dealunit_from_json(x_json)

    def delete_deal_file(self, x_deal_time: TimeLinePoint):
        delete_dir(self.deal_file_path(x_deal_time))

    def get_brokerunit(self) -> BrokerUnit:
        x_brokerunit = brokerunit_shop(self.owner_name)
        x_dirs = self._get_timepoint_dirs()
        for x_deal_folder_name in x_dirs:
            x_dealunit = self.get_deal_file(x_deal_folder_name)
            x_brokerunit.set_deal(x_dealunit)
        return x_brokerunit

    def _get_timepoint_dirs(self) -> list[str]:
        x_dict = get_dir_file_strs(
            self._deals_dir, include_dirs=True, include_files=False
        )
        return list(x_dict.keys())

    def budpoint_filename(self) -> str:
        return "budpoint.json"

    def budpoint_file_path(self, x_deal_time: TimeLinePoint) -> str:
        return create_path(self.timepoint_dir(x_deal_time), self.budpoint_filename())

    def _save_valid_budpoint_file(
        self, x_deal_time: TimeLinePoint, x_budpoint: BudUnit
    ):
        x_budpoint.settle_bud()
        if x_budpoint._rational is False:
            raise _save_valid_budpoint_Exception(
                "BudPoint could not be saved BudUnit._rational is False"
            )
        save_file(
            self.timepoint_dir(x_deal_time),
            self.budpoint_filename(),
            x_budpoint.get_json(),
            replace=True,
        )

    def budpoint_file_exists(self, x_deal_time: TimeLinePoint) -> bool:
        return os_path_exists(self.budpoint_file_path(x_deal_time))

    def get_budpoint_file(self, x_deal_time: TimeLinePoint) -> BudUnit:
        if self.budpoint_file_exists(x_deal_time):
            timepoint_dir = self.timepoint_dir(x_deal_time)
            file_content = open_file(timepoint_dir, self.budpoint_filename())
            return budunit_get_from_json(file_content)

    def delete_budpoint_file(self, x_deal_time: TimeLinePoint):
        delete_dir(self.budpoint_file_path(x_deal_time))

    def calc_timepoint_deal(self, x_deal_time: TimeLinePoint):
        if self.budpoint_file_exists(x_deal_time) is False:
            exception_str = f"Cannot calculate timepoint {x_deal_time} deals without saved BudPoint file"
            raise calc_timepoint_deal_Exception(exception_str)
        x_budpoint = self.get_budpoint_file(x_deal_time)
        if self.deal_file_exists(x_deal_time):
            x_dealunit = self.get_deal_file(x_deal_time)
            x_budpoint.set_fund_pool(x_dealunit.quota)
        else:
            x_dealunit = dealunit_shop(x_deal_time)
        x_dealunit._deal_acct_nets = get_acct_agenda_net_ledger(x_budpoint, True)
        self._save_valid_budpoint_file(x_deal_time, x_budpoint)
        self._save_valid_deal_file(x_dealunit)

    def calc_timepoint_deals(self):
        for x_timepoint in self._get_timepoint_dirs():
            self.calc_timepoint_deal(x_timepoint)

    def keep_dir(self) -> str:
        if self.keep_road is None:
            raise _keep_roadMissingException(
                f"HubUnit '{self.owner_name}' cannot save to keep_dir because it does not have keep_road."
            )
        return get_keep_path(self, self.keep_road)

    def create_keep_dir_if_missing(self):
        set_dir(self.keep_dir())

    def owner_filename(self, owner_name: OwnerName) -> str:
        return get_json_filename(owner_name)

    def treasury_db_path(self) -> str:
        return create_path(self.keep_dir(), treasury_filename())

    def duty_path(self, owner_name: OwnerName) -> str:
        return create_path(self.dutys_dir(), self.owner_filename(owner_name))

    def job_path(self, owner_name: OwnerName) -> str:
        return create_path(self.jobs_dir(), self.owner_filename(owner_name))

    def grade_path(self, owner_name: OwnerName) -> str:
        return create_path(self.grades_dir(), self.owner_filename(owner_name))

    def dutys_dir(self) -> str:
        return get_keep_dutys_dir(self.keep_dir())

    def jobs_dir(self) -> str:
        return get_keep_jobs_dir(self.keep_dir())

    def grades_dir(self) -> str:
        return get_keep_grades_dir(self.keep_dir())

    def get_jobs_dir_filenames_list(self) -> list[str]:
        try:
            return list(get_dir_file_strs(self.jobs_dir(), True).keys())
        except Exception:
            return []

    def save_duty_bud(self, x_bud: BudUnit):
        x_filename = self.owner_filename(x_bud.owner_name)
        save_file(self.dutys_dir(), x_filename, x_bud.get_json())

    def save_job_bud(self, x_bud: BudUnit):
        x_filename = self.owner_filename(x_bud.owner_name)
        save_file(self.jobs_dir(), x_filename, x_bud.get_json())

    def initialize_plan_file(self, gut: BudUnit):
        save_plan_file(self.fisc_mstr_dir, get_default_plan(gut))

    def duty_file_exists(self, owner_name: OwnerName) -> bool:
        return os_path_exists(self.duty_path(owner_name))

    def job_file_exists(self, owner_name: OwnerName) -> bool:
        return os_path_exists(self.job_path(owner_name))

    def get_duty_bud(self, owner_name: OwnerName) -> BudUnit:
        if self.duty_file_exists(owner_name) is False:
            return None
        file_content = open_file(self.dutys_dir(), self.owner_filename(owner_name))
        return budunit_get_from_json(file_content)

    def get_job_bud(self, owner_name: OwnerName) -> BudUnit:
        if self.job_file_exists(owner_name) is False:
            return None
        file_content = open_file(self.jobs_dir(), self.owner_filename(owner_name))
        return budunit_get_from_json(file_content)

    def delete_duty_file(self, owner_name: OwnerName):
        delete_dir(self.duty_path(owner_name))

    def delete_job_file(self, owner_name: OwnerName):
        delete_dir(self.job_path(owner_name))

    def delete_treasury_db_file(self):
        delete_dir(self.treasury_db_path())

    def get_perspective_bud(self, speaker: BudUnit) -> BudUnit:
        # get copy of bud without any metrics
        perspective_bud = budunit_get_from_json(speaker.get_json())
        perspective_bud.set_owner_name(self.owner_name)
        perspective_bud.settle_bud()
        return perspective_bud

    def get_dw_perspective_bud(self, speaker_id: OwnerName) -> BudUnit:
        speaker_plan = open_plan_file(self.fisc_mstr_dir, self.fisc_title, speaker_id)
        return self.get_perspective_bud(speaker_plan)

    def rj_speaker_bud(self, healer_name: OwnerName, speaker_id: OwnerName) -> BudUnit:
        speaker_hubunit = hubunit_shop(
            fisc_mstr_dir=self.fisc_mstr_dir,
            fisc_title=self.fisc_title,
            owner_name=healer_name,
            keep_road=self.keep_road,
            bridge=self.bridge,
            respect_bit=self.respect_bit,
        )
        return speaker_hubunit.get_job_bud(speaker_id)

    def rj_perspective_bud(
        self, healer_name: OwnerName, speaker_id: OwnerName
    ) -> BudUnit:
        speaker_job = self.rj_speaker_bud(healer_name, speaker_id)
        return self.get_perspective_bud(speaker_job)

    def get_keep_roads(self) -> set[RoadUnit]:
        x_gut_bud = open_gut_file(self.fisc_mstr_dir, self.fisc_title, self.owner_name)
        x_gut_bud.settle_bud()
        if x_gut_bud._keeps_justified is False:
            x_str = f"Cannot get_keep_roads from '{self.owner_name}' gut bud because 'BudUnit._keeps_justified' is False."
            raise get_keep_roadsException(x_str)
        if x_gut_bud._keeps_buildable is False:
            x_str = f"Cannot get_keep_roads from '{self.owner_name}' gut bud because 'BudUnit._keeps_buildable' is False."
            raise get_keep_roadsException(x_str)
        owner_healer_dict = x_gut_bud._healers_dict.get(self.owner_name)
        if owner_healer_dict is None:
            return get_empty_set_if_None(None)
        keep_roads = x_gut_bud._healers_dict.get(self.owner_name).keys()
        return get_empty_set_if_None(keep_roads)

    def save_all_gut_dutys(self):
        gut = open_gut_file(self.fisc_mstr_dir, self.fisc_title, self.owner_name)
        for x_keep_road in self.get_keep_roads():
            self.keep_road = x_keep_road
            self.save_duty_bud(gut)
        self.keep_road = None

    def create_treasury_db_file(self):
        self.create_keep_dir_if_missing()
        with sqlite3_connect(self.treasury_db_path()) as conn:
            pass

    def treasury_db_file_exists(self) -> bool:
        return os_path_exists(self.treasury_db_path())

    def treasury_db_file_conn(self) -> Connection:
        if self.keep_road is None:
            raise _keep_roadMissingException(
                f"hubunit cannot connect to treasury_db_file because keep_road is {self.keep_road}"
            )
        if self.treasury_db_file_exists() is False:
            self.create_treasury_db_file()
        return sqlite_connection(self.treasury_db_path())

    def create_gut_treasury_db_files(self):
        for x_keep_road in self.get_keep_roads():
            self.keep_road = x_keep_road
            self.create_treasury_db_file()
        self.keep_road = None


def hubunit_shop(
    fisc_mstr_dir: str,
    fisc_title: FiscTitle,
    owner_name: OwnerName = None,
    keep_road: RoadUnit = None,
    bridge: str = None,
    fund_pool: float = None,
    fund_coin: float = None,
    respect_bit: float = None,
    penny: float = None,
    keep_point_magnitude: float = None,
) -> HubUnit:
    x_hubunit = HubUnit(
        fisc_mstr_dir=fisc_mstr_dir,
        fisc_title=fisc_title,
        owner_name=validate_titleunit(owner_name, bridge),
        keep_road=keep_road,
        bridge=default_bridge_if_None(bridge),
        fund_pool=validate_fund_pool(fund_pool),
        fund_coin=default_fund_coin_if_None(fund_coin),
        respect_bit=default_respect_bit_if_None(respect_bit),
        penny=filter_penny(penny),
        keep_point_magnitude=default_money_magnitude_if_None(keep_point_magnitude),
    )
    x_hubunit.set_dir_attrs()
    return x_hubunit


def get_keep_path(x_hubunit: HubUnit, x_road: TitleUnit) -> str:
    keep_root = "itemroot"
    x_road = rebuild_road(x_road, x_hubunit.fisc_title, keep_root)
    x_list = get_all_road_titles(x_road, x_hubunit.bridge)
    keep_sub_path = get_directory_path(x_list=[*x_list])
    return create_path(x_hubunit._keeps_dir, keep_sub_path)
