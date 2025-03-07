from src.f00_instrument.file import (
    create_path as f_path,
    get_directory_path,
    save_file,
    open_file,
    delete_dir,
    get_dir_file_strs,
    set_dir,
    get_integer_filenames,
    get_max_file_number,
)
from src.f00_instrument.dict_toolbox import get_empty_set_if_None
from src.f00_instrument.db_toolbox import sqlite_connection
from src.f01_road.jaar_config import (
    grades_folder,
    get_rootpart_of_keep_dir,
    treasury_filename,
    get_gifts_folder,
    get_init_gift_id_if_None,
    get_json_filename,
    init_gift_id,
)
from src.f01_road.finance import (
    default_fund_coin_if_None,
    validate_fund_pool,
    default_respect_bit_if_None,
    filter_penny,
    default_money_magnitude_if_None,
    TimeLinePoint,
)
from src.f01_road.deal import (
    DealUnit,
    dealunit_shop,
    BrokerUnit,
    brokerunit_shop,
    get_dealunit_from_json,
)
from src.f01_road.road import (
    OwnerName,
    FiscTitle,
    TitleUnit,
    RoadUnit,
    rebuild_road,
    get_all_road_titles,
    validate_titleunit,
    default_bridge_if_None,
)
from src.f02_bud.bud import (
    BudUnit,
    get_from_json as budunit_get_from_json,
    budunit_shop,
)
from src.f02_bud.bud_tool import get_acct_agenda_net_ledger
from src.f04_gift.atom import (
    AtomUnit,
    get_from_json as atomunit_get_from_json,
    modify_bud_with_atomunit,
)
from src.f05_listen.basis_buds import get_default_forecast_bud
from src.f04_gift.gift import GiftUnit, giftunit_shop, create_giftunit_from_files
from os.path import exists as os_path_exists
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection


class Invalid_voice_Exception(Exception):
    pass


class Invalid_forecast_Exception(Exception):
    pass


class SaveGiftFileException(Exception):
    pass


class GiftFileMissingException(Exception):
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
    return f_path(x_keep_dir, "dutys")


def get_keep_jobs_dir(x_keep_dir: str) -> str:
    return f_path(x_keep_dir, "jobs")


def get_keep_grades_dir(x_keep_dir: str) -> str:
    return f_path(x_keep_dir, grades_folder())


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
    _gifts_dir: str = None
    _voice_dir: str = None
    _forecast_dir: str = None
    _deals_dir: str = None
    _voice_filename: str = None
    _voice_path: str = None
    _forecast_filename: str = None
    _forecast_path: str = None

    def set_dir_attrs(self):
        fiscs_dir = f_path(self.fisc_mstr_dir, "fiscs")
        self._fisc_dir = f_path(fiscs_dir, self.fisc_title)
        self._owners_dir = f_path(self._fisc_dir, "owners")
        self._owner_dir = f_path(self._owners_dir, self.owner_name)
        self._keeps_dir = f_path(self._owner_dir, "keeps")
        self._atoms_dir = f_path(self._owner_dir, "atoms")
        self._gifts_dir = f_path(self._owner_dir, get_gifts_folder())
        self._voice_dir = f_path(self._owner_dir, "voice")
        self._forecast_dir = f_path(self._owner_dir, "forecast")
        self._deals_dir = f_path(self._owner_dir, "deals")
        self._voice_filename = get_json_filename(self.owner_name)
        self._voice_path = f_path(self._voice_dir, self._voice_filename)
        self._forecast_filename = get_json_filename(self.owner_name)
        self._forecast_path = f_path(self._forecast_dir, self._forecast_filename)

    def save_file_voice(self, file_str: str, replace: bool):
        save_file(
            dest_dir=self._voice_dir,
            filename=self._voice_filename,
            file_str=file_str,
            replace=replace,
        )

    def save_file_forecast(self, file_str: str, replace: bool):
        save_file(
            dest_dir=self._forecast_dir,
            filename=self._forecast_filename,
            file_str=file_str,
            replace=replace,
        )

    def voice_file_exists(self) -> bool:
        return os_path_exists(self._voice_path)

    def forecast_file_exists(self) -> bool:
        return os_path_exists(self._forecast_path)

    def open_file_voice(self) -> str:
        return open_file(self._voice_dir, self._voice_filename)

    def save_voice_bud(self, x_bud: BudUnit):
        if x_bud.owner_name != self.owner_name:
            raise Invalid_voice_Exception(
                f"BudUnit with owner_name '{x_bud.owner_name}' cannot be saved as owner_name '{self.owner_name}''s voice bud."
            )
        self.save_file_voice(x_bud.get_json(), True)

    def get_voice_bud(self) -> BudUnit:
        if self.voice_file_exists() is False:
            return None
        return budunit_get_from_json(self.open_file_voice())

    def default_voice_bud(self) -> BudUnit:
        x_budunit = budunit_shop(
            owner_name=self.owner_name,
            fisc_title=self.fisc_title,
            bridge=self.bridge,
            fund_pool=self.fund_pool,
            fund_coin=self.fund_coin,
            respect_bit=self.respect_bit,
            penny=self.penny,
        )
        x_budunit.last_gift_id = init_gift_id()
        return x_budunit

    def delete_voice_file(self):
        delete_dir(self._voice_path)

    def open_file_forecast(self) -> str:
        return open_file(self._forecast_dir, self._forecast_filename)

    # Gift methods
    def get_max_atom_file_number(self) -> int:
        return get_max_file_number(self._atoms_dir)

    def _get_next_atom_file_number(self) -> int:
        max_file_number = self.get_max_atom_file_number()
        return 0 if max_file_number is None else max_file_number + 1

    def atom_filename(self, atom_number: int) -> str:
        return f"{atom_number}.json"

    def atom_file_path(self, atom_number: int) -> str:
        return f_path(self._atoms_dir, self.atom_filename(atom_number))

    def _save_valid_atom_file(self, x_atom: AtomUnit, file_number: int):
        save_file(
            self._atoms_dir,
            self.atom_filename(file_number),
            x_atom.get_json(),
            replace=False,
        )
        return file_number

    def save_atom_file(self, x_atom: AtomUnit):
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
                x_atom = atomunit_get_from_json(x_file_str)
                modify_bud_with_atomunit(x_bud, x_atom)
        return x_bud

    def get_max_gift_file_number(self) -> int:
        return get_max_file_number(self._gifts_dir)

    def _get_next_gift_file_number(self) -> int:
        max_file_number = self.get_max_gift_file_number()
        init_gift_id = get_init_gift_id_if_None()
        return init_gift_id if max_file_number is None else max_file_number + 1

    def gift_filename(self, gift_id: int) -> str:
        return get_json_filename(gift_id)

    def gift_file_path(self, gift_id: int) -> bool:
        gift_filename = self.gift_filename(gift_id)
        return f_path(self._gifts_dir, gift_filename)

    def gift_file_exists(self, gift_id: int) -> bool:
        return os_path_exists(self.gift_file_path(gift_id))

    def validate_giftunit(self, x_giftunit: GiftUnit) -> GiftUnit:
        if x_giftunit._atoms_dir != self._atoms_dir:
            x_giftunit._atoms_dir = self._atoms_dir
        if x_giftunit._gifts_dir != self._gifts_dir:
            x_giftunit._gifts_dir = self._gifts_dir
        if x_giftunit._gift_id != self._get_next_gift_file_number():
            x_giftunit._gift_id = self._get_next_gift_file_number()
        if x_giftunit.owner_name != self.owner_name:
            x_giftunit.owner_name = self.owner_name
        if x_giftunit._delta_start != self._get_next_atom_file_number():
            x_giftunit._delta_start = self._get_next_atom_file_number()
        return x_giftunit

    def save_gift_file(
        self,
        x_gift: GiftUnit,
        replace: bool = True,
        correct_invalid_attrs: bool = True,
    ) -> GiftUnit:
        if correct_invalid_attrs:
            x_gift = self.validate_giftunit(x_gift)

        if x_gift._atoms_dir != self._atoms_dir:
            raise SaveGiftFileException(
                f"GiftUnit file cannot be saved because giftunit._atoms_dir is incorrect: {x_gift._atoms_dir}. It must be {self._atoms_dir}."
            )
        if x_gift._gifts_dir != self._gifts_dir:
            raise SaveGiftFileException(
                f"GiftUnit file cannot be saved because giftunit._gifts_dir is incorrect: {x_gift._gifts_dir}. It must be {self._gifts_dir}."
            )
        if x_gift.owner_name != self.owner_name:
            raise SaveGiftFileException(
                f"GiftUnit file cannot be saved because giftunit.owner_name is incorrect: {x_gift.owner_name}. It must be {self.owner_name}."
            )
        gift_filename = self.gift_filename(x_gift._gift_id)
        if not replace and self.gift_file_exists(x_gift._gift_id):
            raise SaveGiftFileException(
                f"GiftUnit file {gift_filename} exists and cannot be saved over."
            )
        x_gift.save_files()
        return x_gift

    def _del_gift_file(self, gift_id: int):
        delete_dir(self.gift_file_path(gift_id))

    def _default_giftunit(self) -> GiftUnit:
        return giftunit_shop(
            owner_name=self.owner_name,
            _gift_id=self._get_next_gift_file_number(),
            _atoms_dir=self._atoms_dir,
            _gifts_dir=self._gifts_dir,
        )

    def create_save_gift_file(self, before_bud: BudUnit, after_bud: BudUnit):
        new_giftunit = self._default_giftunit()
        new_buddelta = new_giftunit._buddelta
        new_buddelta.add_all_different_atomunits(before_bud, after_bud)
        self.save_gift_file(new_giftunit)

    def get_giftunit(self, gift_id: int) -> GiftUnit:
        if self.gift_file_exists(gift_id) is False:
            raise GiftFileMissingException(
                f"GiftUnit file_number {gift_id} does not exist."
            )
        x_gifts_dir = self._gifts_dir
        x_atoms_dir = self._atoms_dir
        return create_giftunit_from_files(x_gifts_dir, gift_id, x_atoms_dir)

    def _merge_any_gifts(self, x_bud: BudUnit) -> BudUnit:
        gifts_dir = self._gifts_dir
        gift_ints = get_integer_filenames(gifts_dir, x_bud.last_gift_id)
        if len(gift_ints) == 0:
            return copy_deepcopy(x_bud)

        for gift_int in gift_ints:
            x_gift = self.get_giftunit(gift_int)
            new_bud = x_gift._buddelta.get_edited_bud(x_bud)
        return new_bud

    def _create_initial_gift_files_from_default(self):
        x_giftunit = giftunit_shop(
            owner_name=self.owner_name,
            _gift_id=get_init_gift_id_if_None(),
            _gifts_dir=self._gifts_dir,
            _atoms_dir=self._atoms_dir,
        )
        x_giftunit._buddelta.add_all_different_atomunits(
            before_bud=self.default_voice_bud(),
            after_bud=self.default_voice_bud(),
        )
        x_giftunit.save_files()

    def _create_voice_from_gifts(self):
        x_bud = self._merge_any_gifts(self.default_voice_bud())
        self.save_voice_bud(x_bud)

    def _create_initial_gift_and_voice_files(self):
        self._create_initial_gift_files_from_default()
        self._create_voice_from_gifts()

    def _create_initial_gift_files_from_voice(self):
        x_giftunit = self._default_giftunit()
        x_giftunit._buddelta.add_all_different_atomunits(
            before_bud=self.default_voice_bud(),
            after_bud=self.get_voice_bud(),
        )
        x_giftunit.save_files()

    def initialize_gift_voice_files(self):
        x_voice_file_exists = self.voice_file_exists()
        gift_file_exists = self.gift_file_exists(init_gift_id())
        if x_voice_file_exists is False and gift_file_exists is False:
            self._create_initial_gift_and_voice_files()
        elif x_voice_file_exists is False and gift_file_exists:
            self._create_voice_from_gifts()
        elif x_voice_file_exists and gift_file_exists is False:
            self._create_initial_gift_files_from_voice()

    def append_gifts_to_voice_file(self):
        voice_bud = self.get_voice_bud()
        voice_bud = self._merge_any_gifts(voice_bud)
        self.save_voice_bud(voice_bud)
        return self.get_voice_bud()

    # Deal methods
    def timepoint_dir(self, x_time_int: TimeLinePoint) -> str:
        return f_path(self._deals_dir, str(x_time_int))

    def deal_filename(self) -> str:
        return "dealunit.json"

    def deal_file_path(self, x_time_int: TimeLinePoint) -> str:
        return f_path(self.timepoint_dir(x_time_int), self.deal_filename())

    def _save_valid_deal_file(self, x_deal: DealUnit):
        x_deal.calc_magnitude()
        save_file(
            self.timepoint_dir(x_deal.time_int),
            self.deal_filename(),
            x_deal.get_json(),
            replace=True,
        )

    def deal_file_exists(self, x_time_int: TimeLinePoint) -> bool:
        return os_path_exists(self.deal_file_path(x_time_int))

    def get_deal_file(self, x_time_int: TimeLinePoint) -> DealUnit:
        if self.deal_file_exists(x_time_int):
            x_json = open_file(self.timepoint_dir(x_time_int), self.deal_filename())
            return get_dealunit_from_json(x_json)

    def delete_deal_file(self, x_time_int: TimeLinePoint):
        delete_dir(self.deal_file_path(x_time_int))

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

    def budpoint_file_path(self, x_time_int: TimeLinePoint) -> str:
        return f_path(self.timepoint_dir(x_time_int), self.budpoint_filename())

    def _save_valid_budpoint_file(self, x_time_int: TimeLinePoint, x_budpoint: BudUnit):
        x_budpoint.settle_bud()
        if x_budpoint._rational is False:
            raise _save_valid_budpoint_Exception(
                "BudPoint could not be saved BudUnit._rational is False"
            )
        save_file(
            self.timepoint_dir(x_time_int),
            self.budpoint_filename(),
            x_budpoint.get_json(),
            replace=True,
        )

    def budpoint_file_exists(self, x_time_int: TimeLinePoint) -> bool:
        return os_path_exists(self.budpoint_file_path(x_time_int))

    def get_budpoint_file(self, x_time_int: TimeLinePoint) -> BudUnit:
        if self.budpoint_file_exists(x_time_int):
            timepoint_dir = self.timepoint_dir(x_time_int)
            file_content = open_file(timepoint_dir, self.budpoint_filename())
            return budunit_get_from_json(file_content)

    def delete_budpoint_file(self, x_time_int: TimeLinePoint):
        delete_dir(self.budpoint_file_path(x_time_int))

    def calc_timepoint_deal(self, x_time_int: TimeLinePoint):
        if self.budpoint_file_exists(x_time_int) is False:
            exception_str = f"Cannot calculate timepoint {x_time_int} deals without saved BudPoint file"
            raise calc_timepoint_deal_Exception(exception_str)
        x_budpoint = self.get_budpoint_file(x_time_int)
        if self.deal_file_exists(x_time_int):
            x_dealunit = self.get_deal_file(x_time_int)
            x_budpoint.set_fund_pool(x_dealunit.quota)
        else:
            x_dealunit = dealunit_shop(x_time_int)
        x_dealunit._deal_acct_nets = get_acct_agenda_net_ledger(x_budpoint, True)
        self._save_valid_budpoint_file(x_time_int, x_budpoint)
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

    def treasury_filename(self) -> str:
        return treasury_filename()

    def treasury_db_path(self) -> str:
        return f_path(self.keep_dir(), treasury_filename())

    def duty_path(self, owner_name: OwnerName) -> str:
        return f_path(self.dutys_dir(), self.owner_filename(owner_name))

    def job_path(self, owner_name: OwnerName) -> str:
        return f_path(self.jobs_dir(), self.owner_filename(owner_name))

    def grade_path(self, owner_name: OwnerName) -> str:
        return f_path(self.grades_dir(), self.owner_filename(owner_name))

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

    def save_forecast_bud(self, x_bud: BudUnit):
        if x_bud.owner_name != self.owner_name:
            raise Invalid_forecast_Exception(
                f"BudUnit with owner_name '{x_bud.owner_name}' cannot be saved as owner_name '{self.owner_name}''s forecast bud."
            )
        self.save_file_forecast(x_bud.get_json(), True)

    def initialize_forecast_file(self, voice: BudUnit):
        if self.forecast_file_exists() is False:
            self.save_forecast_bud(get_default_forecast_bud(voice))

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

    def get_forecast_bud(self) -> BudUnit:
        if self.forecast_file_exists() is False:
            return None
        file_content = self.open_file_forecast()
        return budunit_get_from_json(file_content)

    def delete_duty_file(self, owner_name: OwnerName):
        delete_dir(self.duty_path(owner_name))

    def delete_job_file(self, owner_name: OwnerName):
        delete_dir(self.job_path(owner_name))

    def delete_treasury_db_file(self):
        delete_dir(self.treasury_db_path())

    def dw_speaker_bud(self, speaker_id: OwnerName) -> BudUnit:
        speaker_hubunit = hubunit_shop(
            fisc_mstr_dir=self.fisc_mstr_dir,
            fisc_title=self.fisc_title,
            owner_name=speaker_id,
            bridge=self.bridge,
            respect_bit=self.respect_bit,
        )
        return speaker_hubunit.get_forecast_bud()

    def get_perspective_bud(self, speaker: BudUnit) -> BudUnit:
        # get copy of bud without any metrics
        perspective_bud = budunit_get_from_json(speaker.get_json())
        perspective_bud.set_owner_name(self.owner_name)
        perspective_bud.settle_bud()
        return perspective_bud

    def get_dw_perspective_bud(self, speaker_id: OwnerName) -> BudUnit:
        return self.get_perspective_bud(self.dw_speaker_bud(speaker_id))

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
        x_voice_bud = self.get_voice_bud()
        x_voice_bud.settle_bud()
        if x_voice_bud._keeps_justified is False:
            x_str = f"Cannot get_keep_roads from '{self.owner_name}' voice bud because 'BudUnit._keeps_justified' is False."
            raise get_keep_roadsException(x_str)
        if x_voice_bud._keeps_buildable is False:
            x_str = f"Cannot get_keep_roads from '{self.owner_name}' voice bud because 'BudUnit._keeps_buildable' is False."
            raise get_keep_roadsException(x_str)
        owner_healer_dict = x_voice_bud._healers_dict.get(self.owner_name)
        if owner_healer_dict is None:
            return get_empty_set_if_None(None)
        keep_roads = x_voice_bud._healers_dict.get(self.owner_name).keys()
        return get_empty_set_if_None(keep_roads)

    def save_all_voice_dutys(self):
        voice = self.get_voice_bud()
        for x_keep_road in self.get_keep_roads():
            self.keep_road = x_keep_road
            self.save_duty_bud(voice)
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

    def create_voice_treasury_db_files(self):
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
    keep_root = get_rootpart_of_keep_dir()
    x_road = rebuild_road(x_road, x_hubunit.fisc_title, keep_root)
    x_list = get_all_road_titles(x_road, x_hubunit.bridge)
    keep_sub_path = get_directory_path(x_list=[*x_list])
    return f_path(x_hubunit._keeps_dir, keep_sub_path)
