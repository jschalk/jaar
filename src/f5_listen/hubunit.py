from src.f0_instrument.file import (
    create_file_path as f_path,
    get_directory_path,
    save_file,
    open_file,
    delete_dir,
    dir_files,
    set_dir,
    get_integer_filenames,
)
from src.f0_instrument.dict_tool import get_empty_set_if_none
from src.f0_instrument.db_tool import sqlite_connection
from src.f1_road.jaar_config import (
    dutys_str,
    jobs_str,
    grades_folder,
    get_rootpart_of_keep_dir,
    treasury_file_name,
    get_gifts_folder,
    get_fiscal_id_if_None,
    get_test_fiscals_dir,
    get_init_gift_id_if_None,
    get_json_filename,
    init_gift_id,
)
from src.f1_road.finance import (
    default_fund_coin_if_none,
    validate_fund_pool,
    default_respect_bit_if_none,
    default_penny_if_none,
    default_money_magnitude_if_none,
    TimeLinePoint,
)
from src.f1_road.finance_tran import (
    PurviewEpisode,
    purviewepisode_shop,
    PurviewLog,
    purviewlog_shop,
    get_purviewepisode_from_json,
)
from src.f1_road.road import (
    OwnerID,
    FiscalID,
    RoadNode,
    RoadUnit,
    rebuild_road,
    get_all_road_nodes,
    validate_roadnode,
    default_road_delimiter_if_none,
)
from src.f2_bud.bud import BudUnit, get_from_json as budunit_get_from_json, budunit_shop
from src.f2_bud.bud_tool import get_bud_settle_acct_net_dict
from src.f4_gift.atom import (
    AtomUnit,
    get_from_json as atomunit_get_from_json,
    modify_bud_with_atomunit,
)
from src.f5_listen.basis_buds import get_default_final_bud
from src.f4_gift.gift import GiftUnit, giftunit_shop, create_giftunit_from_files
from os.path import exists as os_path_exists
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection


class Invalid_voice_Exception(Exception):
    pass


class Invalid_final_Exception(Exception):
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


class calc_timepoint_purview_Exception(Exception):
    pass


def get_keep_dutys_dir(x_keep_dir: str) -> str:
    return f_path(x_keep_dir, dutys_str())


def get_keep_jobs_dir(x_keep_dir: str) -> str:
    return f_path(x_keep_dir, jobs_str())


def get_keep_grades_dir(x_keep_dir: str) -> str:
    return f_path(x_keep_dir, grades_folder())


@dataclass
class HubUnit:
    owner_id: OwnerID = None
    fiscals_dir: str = None
    fiscal_id: str = None
    keep_road: RoadUnit = None
    road_delimiter: str = None
    fund_pool: float = None
    fund_coin: float = None
    respect_bit: float = None
    penny: float = None
    keep_point_magnitude: float = None

    def fiscal_dir(self) -> str:
        return f_path(self.fiscals_dir, self.fiscal_id)

    def owners_dir(self) -> str:
        return f"{self.fiscal_dir()}/owners"

    def owner_dir(self) -> str:
        return f_path(self.owners_dir(), self.owner_id)

    def keeps_dir(self) -> str:
        return f"{self.owner_dir()}/keeps"

    def atoms_dir(self) -> str:
        return f"{self.owner_dir()}/atoms"

    def gifts_dir(self) -> str:
        return f_path(self.owner_dir(), get_gifts_folder())

    def voice_dir(self) -> str:
        return f"{self.owner_dir()}/voice"

    def final_dir(self) -> str:
        return f"{self.owner_dir()}/final"

    def timeline_dir(self) -> str:
        return f"{self.owner_dir()}/timeline"

    def voice_file_name(self) -> str:
        return get_json_filename(self.owner_id)

    def voice_file_path(self) -> str:
        return f_path(self.voice_dir(), self.voice_file_name())

    def final_file_name(self) -> str:
        return get_json_filename(self.owner_id)

    def final_path(self) -> str:
        return f_path(self.final_dir(), self.final_file_name())

    def save_file_voice(self, file_str: str, replace: bool):
        save_file(
            dest_dir=self.voice_dir(),
            file_name=self.voice_file_name(),
            file_str=file_str,
            replace=replace,
        )

    def save_file_final(self, file_str: str, replace: bool):
        save_file(
            dest_dir=self.final_dir(),
            file_name=self.final_file_name(),
            file_str=file_str,
            replace=replace,
        )

    def voice_file_exists(self) -> bool:
        return os_path_exists(self.voice_file_path())

    def final_file_exists(self) -> bool:
        return os_path_exists(self.final_path())

    def open_file_voice(self) -> str:
        return open_file(self.voice_dir(), self.voice_file_name())

    def save_voice_bud(self, x_bud: BudUnit):
        if x_bud._owner_id != self.owner_id:
            raise Invalid_voice_Exception(
                f"BudUnit with owner_id '{x_bud._owner_id}' cannot be saved as owner_id '{self.owner_id}''s voice bud."
            )
        self.save_file_voice(x_bud.get_json(), True)

    def get_voice_bud(self) -> BudUnit:
        if self.voice_file_exists() is False:
            return None
        file_content = self.open_file_voice()
        return budunit_get_from_json(file_content)

    def default_voice_bud(self) -> BudUnit:
        x_budunit = budunit_shop(
            _owner_id=self.owner_id,
            _fiscal_id=self.fiscal_id,
            _road_delimiter=self.road_delimiter,
            fund_pool=self.fund_pool,
            fund_coin=self.fund_coin,
            respect_bit=self.respect_bit,
            penny=self.penny,
        )
        x_budunit._last_gift_id = init_gift_id()
        return x_budunit

    def delete_voice_file(self):
        delete_dir(self.voice_file_path())

    def open_file_final(self) -> str:
        return open_file(self.final_dir(), self.final_file_name())

    def get_max_atom_file_number(self) -> int:
        if not os_path_exists(self.atoms_dir()):
            return None
        atom_files_dict = dir_files(self.atoms_dir(), True, include_files=True)
        atom_filenames = atom_files_dict.keys()
        atom_file_numbers = {int(atom_filename) for atom_filename in atom_filenames}
        return max(atom_file_numbers, default=None)

    def _get_next_atom_file_number(self) -> int:
        max_file_number = self.get_max_atom_file_number()
        return 0 if max_file_number is None else max_file_number + 1

    def atom_file_name(self, atom_number: int) -> str:
        return f"{atom_number}.json"

    def atom_file_path(self, atom_number: int) -> str:
        return f_path(self.atoms_dir(), self.atom_file_name(atom_number))

    def _save_valid_atom_file(self, x_atom: AtomUnit, file_number: int):
        save_file(
            self.atoms_dir(),
            self.atom_file_name(file_number),
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
        x_bud = budunit_shop(self.owner_id, self.fiscal_id)
        if self.atom_file_exists(self.get_max_atom_file_number()):
            x_atom_files = dir_files(self.atoms_dir(), delete_extensions=True)
            sorted_atom_filenames = sorted(list(x_atom_files.keys()))

            for x_atom_filename in sorted_atom_filenames:
                x_file_str = x_atom_files.get(x_atom_filename)
                x_atom = atomunit_get_from_json(x_file_str)
                modify_bud_with_atomunit(x_bud, x_atom)
        return x_bud

    def get_max_gift_file_number(self) -> int:
        if not os_path_exists(self.gifts_dir()):
            return None
        gifts_dir = self.gifts_dir()
        gift_filenames = dir_files(gifts_dir, True, include_files=True).keys()
        gift_file_numbers = {int(filename) for filename in gift_filenames}
        return max(gift_file_numbers, default=None)

    def _get_next_gift_file_number(self) -> int:
        max_file_number = self.get_max_gift_file_number()
        init_gift_id = get_init_gift_id_if_None()
        return init_gift_id if max_file_number is None else max_file_number + 1

    def gift_file_name(self, gift_id: int) -> str:
        return get_json_filename(gift_id)

    def gift_file_path(self, gift_id: int) -> bool:
        gift_filename = self.gift_file_name(gift_id)
        return f_path(self.gifts_dir(), gift_filename)

    def gift_file_exists(self, gift_id: int) -> bool:
        return os_path_exists(self.gift_file_path(gift_id))

    def validate_giftunit(self, x_giftunit: GiftUnit) -> GiftUnit:
        if x_giftunit._atoms_dir != self.atoms_dir():
            x_giftunit._atoms_dir = self.atoms_dir()
        if x_giftunit._gifts_dir != self.gifts_dir():
            x_giftunit._gifts_dir = self.gifts_dir()
        if x_giftunit._gift_id != self._get_next_gift_file_number():
            x_giftunit._gift_id = self._get_next_gift_file_number()
        if x_giftunit.owner_id != self.owner_id:
            x_giftunit.owner_id = self.owner_id
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

        if x_gift._atoms_dir != self.atoms_dir():
            raise SaveGiftFileException(
                f"GiftUnit file cannot be saved because giftunit._atoms_dir is incorrect: {x_gift._atoms_dir}. It must be {self.atoms_dir()}."
            )
        if x_gift._gifts_dir != self.gifts_dir():
            raise SaveGiftFileException(
                f"GiftUnit file cannot be saved because giftunit._gifts_dir is incorrect: {x_gift._gifts_dir}. It must be {self.gifts_dir()}."
            )
        if x_gift.owner_id != self.owner_id:
            raise SaveGiftFileException(
                f"GiftUnit file cannot be saved because giftunit.owner_id is incorrect: {x_gift.owner_id}. It must be {self.owner_id}."
            )
        gift_filename = self.gift_file_name(x_gift._gift_id)
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
            owner_id=self.owner_id,
            _gift_id=self._get_next_gift_file_number(),
            _atoms_dir=self.atoms_dir(),
            _gifts_dir=self.gifts_dir(),
        )

    def create_save_gift_file(self, before_bud: BudUnit, after_bud: BudUnit):
        new_giftunit = self._default_giftunit()
        new_deltaunit = new_giftunit._deltaunit
        new_deltaunit.add_all_different_atomunits(before_bud, after_bud)
        self.save_gift_file(new_giftunit)

    def get_giftunit(self, gift_id: int) -> GiftUnit:
        if self.gift_file_exists(gift_id) is False:
            raise GiftFileMissingException(
                f"GiftUnit file_number {gift_id} does not exist."
            )
        x_gifts_dir = self.gifts_dir()
        x_atoms_dir = self.atoms_dir()
        return create_giftunit_from_files(x_gifts_dir, gift_id, x_atoms_dir)

    def _merge_any_gifts(self, x_bud: BudUnit) -> BudUnit:
        gifts_dir = self.gifts_dir()
        gift_ints = get_integer_filenames(gifts_dir, x_bud._last_gift_id)
        if len(gift_ints) == 0:
            return copy_deepcopy(x_bud)

        for gift_int in gift_ints:
            x_gift = self.get_giftunit(gift_int)
            new_bud = x_gift._deltaunit.get_edited_bud(x_bud)
        return new_bud

    def _create_initial_gift_files_from_default(self):
        x_giftunit = giftunit_shop(
            owner_id=self.owner_id,
            _gift_id=get_init_gift_id_if_None(),
            _gifts_dir=self.gifts_dir(),
            _atoms_dir=self.atoms_dir(),
        )
        x_giftunit._deltaunit.add_all_different_atomunits(
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
        x_giftunit._deltaunit.add_all_different_atomunits(
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

    def timepoint_dir(self, x_timestamp: TimeLinePoint) -> str:
        return f"{self.timeline_dir()}/{x_timestamp}"

    def purview_file_name(self) -> str:
        return "purview.json"

    def purview_file_path(self, x_timestamp: TimeLinePoint) -> str:
        return f_path(self.timepoint_dir(x_timestamp), self.purview_file_name())

    def _save_valid_purview_file(self, x_purview: PurviewEpisode):
        x_purview.calc_magnitude()
        save_file(
            self.timepoint_dir(x_purview.timestamp),
            self.purview_file_name(),
            x_purview.get_json(),
            replace=True,
        )

    def purview_file_exists(self, x_timestamp: TimeLinePoint) -> bool:
        return os_path_exists(self.purview_file_path(x_timestamp))

    def get_purview_file(self, x_timestamp: TimeLinePoint) -> PurviewEpisode:
        if self.purview_file_exists(x_timestamp):
            x_json = open_file(
                self.timepoint_dir(x_timestamp), self.purview_file_name()
            )
            return get_purviewepisode_from_json(x_json)

    def delete_purview_file(self, x_timestamp: TimeLinePoint):
        delete_dir(self.purview_file_path(x_timestamp))

    def get_purviewlog(self) -> PurviewLog:
        x_purviewlog = purviewlog_shop(self.owner_id)
        x_dirs = self._get_timepoint_dirs()
        for x_purview_folder_name in x_dirs:
            x_purviewepisode = self.get_purview_file(x_purview_folder_name)
            x_purviewlog.set_episode(x_purviewepisode)
        return x_purviewlog

    def _get_timepoint_dirs(self) -> list[str]:
        x_dict = dir_files(self.timeline_dir(), include_dirs=True, include_files=False)
        return list(x_dict.keys())

    def budpoint_file_name(self) -> str:
        return "budpoint.json"

    def budpoint_file_path(self, x_timestamp: TimeLinePoint) -> str:
        return f_path(self.timepoint_dir(x_timestamp), self.budpoint_file_name())

    def _save_valid_budpoint_file(
        self, x_timestamp: TimeLinePoint, x_budpoint: BudUnit
    ):
        x_budpoint.settle_bud()
        if x_budpoint._rational is False:
            raise _save_valid_budpoint_Exception(
                "BudPoint could not be saved BudUnit._rational is False"
            )
        save_file(
            self.timepoint_dir(x_timestamp),
            self.budpoint_file_name(),
            x_budpoint.get_json(),
            replace=True,
        )

    def budpoint_file_exists(self, x_timestamp: TimeLinePoint) -> bool:
        return os_path_exists(self.budpoint_file_path(x_timestamp))

    def get_budpoint_file(self, x_timestamp: TimeLinePoint) -> BudUnit:
        if self.budpoint_file_exists(x_timestamp):
            timepoint_dir = self.timepoint_dir(x_timestamp)
            file_content = open_file(timepoint_dir, self.budpoint_file_name())
            return budunit_get_from_json(file_content)

    def delete_budpoint_file(self, x_timestamp: TimeLinePoint):
        delete_dir(self.budpoint_file_path(x_timestamp))

    def calc_timepoint_purview(self, x_timestamp: TimeLinePoint):
        if self.budpoint_file_exists(x_timestamp) is False:
            exception_str = f"Cannot calculate timepoint {x_timestamp} purviews without saved BudPoint file"
            raise calc_timepoint_purview_Exception(exception_str)
        x_budpoint = self.get_budpoint_file(x_timestamp)
        if self.purview_file_exists(x_timestamp):
            x_purviewepisode = self.get_purview_file(x_timestamp)
            x_budpoint.set_fund_pool(x_purviewepisode.amount)
        else:
            x_purviewepisode = purviewepisode_shop(x_timestamp)
        x_net_purviews = get_bud_settle_acct_net_dict(x_budpoint, True)
        x_purviewepisode._net_purviews = x_net_purviews
        self._save_valid_budpoint_file(x_timestamp, x_budpoint)
        self._save_valid_purview_file(x_purviewepisode)

    def calc_timepoint_purviews(self):
        for x_timepoint in self._get_timepoint_dirs():
            self.calc_timepoint_purview(x_timepoint)

    def keep_dir(self) -> str:
        if self.keep_road is None:
            raise _keep_roadMissingException(
                f"HubUnit '{self.owner_id}' cannot save to keep_dir because it does not have keep_road."
            )
        return get_keep_path(self, self.keep_road)

    def create_keep_dir_if_missing(self):
        set_dir(self.keep_dir())

    def owner_file_name(self, owner_id: OwnerID) -> str:
        return get_json_filename(owner_id)

    def treasury_file_name(self) -> str:
        return treasury_file_name()

    def treasury_db_path(self) -> str:
        return f_path(self.keep_dir(), treasury_file_name())

    def duty_path(self, owner_id: OwnerID) -> str:
        return f_path(self.dutys_dir(), self.owner_file_name(owner_id))

    def job_path(self, owner_id: OwnerID) -> str:
        return f"{self.jobs_dir()}/{self.owner_file_name(owner_id)}"

    def grade_path(self, owner_id: OwnerID) -> str:
        return f"{self.grades_dir()}/{self.owner_file_name(owner_id)}"

    def dutys_dir(self) -> str:
        return get_keep_dutys_dir(self.keep_dir())

    def jobs_dir(self) -> str:
        return get_keep_jobs_dir(self.keep_dir())

    def grades_dir(self) -> str:
        return get_keep_grades_dir(self.keep_dir())

    def get_jobs_dir_file_names_list(self) -> list[str]:
        try:
            return list(dir_files(self.jobs_dir(), True).keys())
        except Exception:
            return []

    def save_duty_bud(self, x_bud: BudUnit):
        x_file_name = self.owner_file_name(x_bud._owner_id)
        save_file(self.dutys_dir(), x_file_name, x_bud.get_json())

    def save_job_bud(self, x_bud: BudUnit):
        x_file_name = self.owner_file_name(x_bud._owner_id)
        save_file(self.jobs_dir(), x_file_name, x_bud.get_json())

    def save_final_bud(self, x_bud: BudUnit):
        if x_bud._owner_id != self.owner_id:
            raise Invalid_final_Exception(
                f"BudUnit with owner_id '{x_bud._owner_id}' cannot be saved as owner_id '{self.owner_id}''s final bud."
            )
        self.save_file_final(x_bud.get_json(), True)

    def initialize_final_file(self, voice: BudUnit):
        if self.final_file_exists() is False:
            self.save_final_bud(get_default_final_bud(voice))

    def duty_file_exists(self, owner_id: OwnerID) -> bool:
        return os_path_exists(self.duty_path(owner_id))

    def job_file_exists(self, owner_id: OwnerID) -> bool:
        return os_path_exists(self.job_path(owner_id))

    def get_duty_bud(self, owner_id: OwnerID) -> BudUnit:
        if self.duty_file_exists(owner_id) is False:
            return None
        file_content = open_file(self.dutys_dir(), self.owner_file_name(owner_id))
        return budunit_get_from_json(file_content)

    def get_job_bud(self, owner_id: OwnerID) -> BudUnit:
        if self.job_file_exists(owner_id) is False:
            return None
        file_content = open_file(self.jobs_dir(), self.owner_file_name(owner_id))
        return budunit_get_from_json(file_content)

    def get_final_bud(self) -> BudUnit:
        if self.final_file_exists() is False:
            return None
        file_content = self.open_file_final()
        return budunit_get_from_json(file_content)

    def delete_duty_file(self, owner_id: OwnerID):
        delete_dir(self.duty_path(owner_id))

    def delete_job_file(self, owner_id: OwnerID):
        delete_dir(self.job_path(owner_id))

    def delete_treasury_db_file(self):
        delete_dir(self.treasury_db_path())

    def dw_speaker_bud(self, speaker_id: OwnerID) -> BudUnit:
        speaker_hubunit = hubunit_shop(
            fiscals_dir=self.fiscals_dir,
            fiscal_id=self.fiscal_id,
            owner_id=speaker_id,
            road_delimiter=self.road_delimiter,
            respect_bit=self.respect_bit,
        )
        return speaker_hubunit.get_final_bud()

    def get_perspective_bud(self, speaker: BudUnit) -> BudUnit:
        # get copy of bud without any metrics
        perspective_bud = budunit_get_from_json(speaker.get_json())
        perspective_bud.set_owner_id(self.owner_id)
        perspective_bud.settle_bud()
        return perspective_bud

    def get_dw_perspective_bud(self, speaker_id: OwnerID) -> BudUnit:
        return self.get_perspective_bud(self.dw_speaker_bud(speaker_id))

    def rj_speaker_bud(self, healer_id: OwnerID, speaker_id: OwnerID) -> BudUnit:
        speaker_hubunit = hubunit_shop(
            fiscals_dir=self.fiscals_dir,
            fiscal_id=self.fiscal_id,
            owner_id=healer_id,
            keep_road=self.keep_road,
            road_delimiter=self.road_delimiter,
            respect_bit=self.respect_bit,
        )
        return speaker_hubunit.get_job_bud(speaker_id)

    def rj_perspective_bud(self, healer_id: OwnerID, speaker_id: OwnerID) -> BudUnit:
        speaker_job = self.rj_speaker_bud(healer_id, speaker_id)
        return self.get_perspective_bud(speaker_job)

    def get_keep_roads(self) -> set[RoadUnit]:
        x_voice_bud = self.get_voice_bud()
        x_voice_bud.settle_bud()
        if x_voice_bud._keeps_justified is False:
            x_str = f"Cannot get_keep_roads from '{self.owner_id}' voice bud because 'BudUnit._keeps_justified' is False."
            raise get_keep_roadsException(x_str)
        if x_voice_bud._keeps_buildable is False:
            x_str = f"Cannot get_keep_roads from '{self.owner_id}' voice bud because 'BudUnit._keeps_buildable' is False."
            raise get_keep_roadsException(x_str)
        owner_healer_dict = x_voice_bud._healers_dict.get(self.owner_id)
        if owner_healer_dict is None:
            return get_empty_set_if_none(None)
        keep_roads = x_voice_bud._healers_dict.get(self.owner_id).keys()
        return get_empty_set_if_none(keep_roads)

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
    fiscals_dir: str,
    fiscal_id: FiscalID,
    owner_id: OwnerID = None,
    keep_road: RoadUnit = None,
    road_delimiter: str = None,
    fund_pool: float = None,
    fund_coin: float = None,
    respect_bit: float = None,
    penny: float = None,
    keep_point_magnitude: float = None,
) -> HubUnit:
    fiscals_dir = get_test_fiscals_dir() if fiscals_dir is None else fiscals_dir
    fiscal_id = get_fiscal_id_if_None(fiscal_id)

    return HubUnit(
        fiscals_dir=fiscals_dir,
        fiscal_id=fiscal_id,
        owner_id=validate_roadnode(owner_id, road_delimiter),
        keep_road=keep_road,
        road_delimiter=default_road_delimiter_if_none(road_delimiter),
        fund_pool=validate_fund_pool(fund_pool),
        fund_coin=default_fund_coin_if_none(fund_coin),
        respect_bit=default_respect_bit_if_none(respect_bit),
        penny=default_penny_if_none(penny),
        keep_point_magnitude=default_money_magnitude_if_none(keep_point_magnitude),
    )


def get_keep_path(x_hubunit: HubUnit, x_road: RoadNode) -> str:
    keep_root = get_rootpart_of_keep_dir()
    x_road = rebuild_road(x_road, x_hubunit.fiscal_id, keep_root)
    x_list = get_all_road_nodes(x_road, x_hubunit.road_delimiter)
    return f"{x_hubunit.keeps_dir()}{get_directory_path(x_list=[*x_list])}"
