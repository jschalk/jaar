from src._instrument.file import (
    create_file_path as f_path,
    get_directory_path,
    save_file,
    open_file,
    delete_dir,
    dir_files,
    set_dir,
    get_integer_filenames,
)
from src._instrument.python_tool import get_empty_set_if_none
from src._instrument.db_tool import sqlite_connection
from src._road.jaar_config import (
    dutys_str,
    jobs_str,
    grades_folder,
    get_rootpart_of_econ_dir,
    treasury_file_name,
    get_gifts_folder,
    get_fiscal_id_if_None,
    get_test_fiscals_dir,
    get_init_gift_id_if_None,
    get_json_filename,
    init_gift_id,
)
from src._road.finance import (
    default_fund_coin_if_none,
    validate_fund_pool,
    default_bit_if_none,
    default_penny_if_none,
    default_money_magnitude_if_none,
)
from src._road.road import (
    OwnerID,
    FiscalID,
    RoadNode,
    RoadUnit,
    rebuild_road,
    get_all_road_nodes,
    validate_roadnode,
    default_road_delimiter_if_none,
)
from src.bud.bud import (
    BudUnit,
    get_from_json as budunit_get_from_json,
    budunit_shop,
)
from src.delta.atom import (
    AtomUnit,
    get_from_json as atomunit_get_from_json,
    modify_bud_with_atomunit,
)
from src.d_listen.basis_buds import get_default_action_bud
from src.delta.gift import GiftUnit, giftunit_shop, create_giftunit_from_files
from os.path import exists as os_path_exists
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection


class Invalid_voice_Exception(Exception):
    pass


class Invalid_action_Exception(Exception):
    pass


class SaveGiftFileException(Exception):
    pass


class GiftFileMissingException(Exception):
    pass


class get_econ_roadsException(Exception):
    pass


class _econ_roadMissingException(Exception):
    pass


def get_econ_dutys_dir(x_econ_dir: str) -> str:
    return f_path(x_econ_dir, dutys_str())


def get_econ_jobs_dir(x_econ_dir: str) -> str:
    return f_path(x_econ_dir, jobs_str())


def get_econ_grades_dir(x_econ_dir: str) -> str:
    return f_path(x_econ_dir, grades_folder())


@dataclass
class HubUnit:
    owner_id: OwnerID = None
    fiscals_dir: str = None
    fiscal_id: str = None
    econ_road: RoadUnit = None
    road_delimiter: str = None
    fund_pool: float = None
    fund_coin: float = None
    bit: float = None
    penny: float = None
    econ_money_magnitude: float = None

    def fiscal_dir(self) -> str:
        return f_path(self.fiscals_dir, self.fiscal_id)

    def owners_dir(self) -> str:
        return f"{self.fiscal_dir()}/owners"

    def owner_dir(self) -> str:
        return f_path(self.owners_dir(), self.owner_id)

    def econs_dir(self) -> str:
        return f"{self.owner_dir()}/econs"

    def atoms_dir(self) -> str:
        return f"{self.owner_dir()}/atoms"

    def gifts_dir(self) -> str:
        return f_path(self.owner_dir(), get_gifts_folder())

    def voice_dir(self) -> str:
        return f"{self.owner_dir()}/voice"

    def action_dir(self) -> str:
        return f"{self.owner_dir()}/action"

    def voice_file_name(self) -> str:
        return get_json_filename(self.owner_id)

    def voice_file_path(self) -> str:
        return f_path(self.voice_dir(), self.voice_file_name())

    def action_file_name(self) -> str:
        return get_json_filename(self.owner_id)

    def action_path(self) -> str:
        return f_path(self.action_dir(), self.action_file_name())

    def save_file_voice(self, file_str: str, replace: bool):
        save_file(
            dest_dir=self.voice_dir(),
            file_name=self.voice_file_name(),
            file_str=file_str,
            replace=replace,
        )

    def save_file_action(self, file_str: str, replace: bool):
        save_file(
            dest_dir=self.action_dir(),
            file_name=self.action_file_name(),
            file_str=file_str,
            replace=replace,
        )

    def voice_file_exists(self) -> bool:
        return os_path_exists(self.voice_file_path())

    def action_file_exists(self) -> bool:
        return os_path_exists(self.action_path())

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
            bit=self.bit,
            penny=self.penny,
        )
        x_budunit._last_gift_id = init_gift_id()
        return x_budunit

    def delete_voice_file(self):
        delete_dir(self.voice_file_path())

    def open_file_action(self) -> str:
        return open_file(self.action_dir(), self.action_file_name())

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
                f"GiftUnit file {gift_filename} already exists and cannot be saved over."
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

    def econ_dir(self) -> str:
        if self.econ_road is None:
            raise _econ_roadMissingException(
                f"HubUnit '{self.owner_id}' cannot save to econ_dir because it does not have econ_road."
            )
        return get_econ_path(self, self.econ_road)

    def create_econ_dir_if_missing(self):
        set_dir(self.econ_dir())

    def owner_file_name(self, owner_id: OwnerID) -> str:
        return get_json_filename(owner_id)

    def treasury_file_name(self) -> str:
        return treasury_file_name()

    def treasury_db_path(self) -> str:
        return f_path(self.econ_dir(), treasury_file_name())

    def duty_path(self, owner_id: OwnerID) -> str:
        return f_path(self.dutys_dir(), self.owner_file_name(owner_id))

    def job_path(self, owner_id: OwnerID) -> str:
        return f"{self.jobs_dir()}/{self.owner_file_name(owner_id)}"

    def grade_path(self, owner_id: OwnerID) -> str:
        return f"{self.grades_dir()}/{self.owner_file_name(owner_id)}"

    def dutys_dir(self) -> str:
        return get_econ_dutys_dir(self.econ_dir())

    def jobs_dir(self) -> str:
        return get_econ_jobs_dir(self.econ_dir())

    def grades_dir(self) -> str:
        return get_econ_grades_dir(self.econ_dir())

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

    def save_action_bud(self, x_bud: BudUnit):
        if x_bud._owner_id != self.owner_id:
            raise Invalid_action_Exception(
                f"BudUnit with owner_id '{x_bud._owner_id}' cannot be saved as owner_id '{self.owner_id}''s action bud."
            )
        self.save_file_action(x_bud.get_json(), True)

    def initialize_action_file(self, voice: BudUnit):
        if self.action_file_exists() is False:
            self.save_action_bud(get_default_action_bud(voice))

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

    def get_action_bud(self) -> BudUnit:
        if self.action_file_exists() is False:
            return None
        file_content = self.open_file_action()
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
            bit=self.bit,
        )
        return speaker_hubunit.get_action_bud()

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
            econ_road=self.econ_road,
            road_delimiter=self.road_delimiter,
            bit=self.bit,
        )
        return speaker_hubunit.get_job_bud(speaker_id)

    def rj_perspective_bud(self, healer_id: OwnerID, speaker_id: OwnerID) -> BudUnit:
        speaker_job = self.rj_speaker_bud(healer_id, speaker_id)
        return self.get_perspective_bud(speaker_job)

    def get_econ_roads(self) -> set[RoadUnit]:
        x_voice_bud = self.get_voice_bud()
        x_voice_bud.settle_bud()
        if x_voice_bud._econs_justified is False:
            x_str = f"Cannot get_econ_roads from '{self.owner_id}' voice bud because 'BudUnit._econs_justified' is False."
            raise get_econ_roadsException(x_str)
        if x_voice_bud._econs_buildable is False:
            x_str = f"Cannot get_econ_roads from '{self.owner_id}' voice bud because 'BudUnit._econs_buildable' is False."
            raise get_econ_roadsException(x_str)
        owner_healer_dict = x_voice_bud._healers_dict.get(self.owner_id)
        if owner_healer_dict is None:
            return get_empty_set_if_none(None)
        econ_roads = x_voice_bud._healers_dict.get(self.owner_id).keys()
        return get_empty_set_if_none(econ_roads)

    def save_all_voice_dutys(self):
        voice = self.get_voice_bud()
        for x_econ_road in self.get_econ_roads():
            self.econ_road = x_econ_road
            self.save_duty_bud(voice)
        self.econ_road = None

    def create_treasury_db_file(self):
        self.create_econ_dir_if_missing()
        with sqlite3_connect(self.treasury_db_path()) as conn:
            pass

    def treasury_db_file_exists(self) -> bool:
        return os_path_exists(self.treasury_db_path())

    def treasury_db_file_conn(self) -> Connection:
        if self.econ_road is None:
            raise _econ_roadMissingException(
                f"hubunit cannot connect to treasury_db_file because econ_road is {self.econ_road}"
            )
        if self.treasury_db_file_exists() is False:
            self.create_treasury_db_file()
        return sqlite_connection(self.treasury_db_path())

    def create_voice_treasury_db_files(self):
        for x_econ_road in self.get_econ_roads():
            self.econ_road = x_econ_road
            self.create_treasury_db_file()
        self.econ_road = None


def hubunit_shop(
    fiscals_dir: str,
    fiscal_id: FiscalID,
    owner_id: OwnerID = None,
    econ_road: RoadUnit = None,
    road_delimiter: str = None,
    fund_pool: float = None,
    fund_coin: float = None,
    bit: float = None,
    penny: float = None,
    econ_money_magnitude: float = None,
) -> HubUnit:
    fiscals_dir = get_test_fiscals_dir() if fiscals_dir is None else fiscals_dir
    fiscal_id = get_fiscal_id_if_None(fiscal_id)

    return HubUnit(
        fiscals_dir=fiscals_dir,
        fiscal_id=fiscal_id,
        owner_id=validate_roadnode(owner_id, road_delimiter),
        econ_road=econ_road,
        road_delimiter=default_road_delimiter_if_none(road_delimiter),
        fund_pool=validate_fund_pool(fund_pool),
        fund_coin=default_fund_coin_if_none(fund_coin),
        bit=default_bit_if_none(bit),
        penny=default_penny_if_none(penny),
        econ_money_magnitude=default_money_magnitude_if_none(econ_money_magnitude),
    )


def get_econ_path(x_hubunit: HubUnit, x_road: RoadNode) -> str:
    econ_root = get_rootpart_of_econ_dir()
    x_road = rebuild_road(x_road, x_hubunit.fiscal_id, econ_root)
    x_list = get_all_road_nodes(x_road, x_hubunit.road_delimiter)
    return f"{x_hubunit.econs_dir()}{get_directory_path(x_list=[*x_list])}"
