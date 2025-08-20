from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from os.path import exists as os_path_exists
from src.a00_data_toolbox.dict_toolbox import get_empty_set_if_None
from src.a00_data_toolbox.file_toolbox import (
    create_path,
    delete_dir,
    get_dir_file_strs,
    get_integer_filenames,
    get_json_filename,
    get_max_file_number,
    open_file,
    save_file,
    save_json,
)
from src.a01_term_logic.rope import validate_labelterm
from src.a01_term_logic.term import (
    BelieverName,
    CoinLabel,
    RopeTerm,
    default_knot_if_None,
)
from src.a02_finance_logic.finance_config import (
    default_fund_iota_if_None,
    default_money_magnitude_if_None,
    default_RespectBit_if_None,
    filter_penny,
    validate_fund_pool,
)
from src.a06_believer_logic.believer_main import (
    BelieverUnit,
    believerunit_shop,
    get_from_json as believerunit_get_from_json,
)
from src.a08_believer_atom_logic.atom_main import (
    BelieverAtom,
    get_from_json as believeratom_get_from_json,
    modify_believer_with_believeratom,
)
from src.a09_pack_logic.pack import (
    PackUnit,
    create_packunit_from_files,
    get_init_pack_id_if_None,
    init_pack_id,
    packunit_shop,
)
from src.a12_hub_toolbox.a12_path import (
    create_atoms_dir_path,
    create_keep_duty_path,
    create_keep_grades_path,
    create_keep_visions_path,
    create_keeps_dir_path,
    create_packs_dir_path,
    create_treasury_db_path,
)
from src.a12_hub_toolbox.hub_tool import (
    gut_file_exists,
    open_gut_file,
    open_job_file,
    save_gut_file,
)
from src.a12_hub_toolbox.keep_tool import create_treasury_db_file, save_duty_believer


class SavePackFileException(Exception):
    pass


class PackFileMissingException(Exception):
    pass


class get_keep_ropesException(Exception):
    pass


@dataclass
class HubUnit:
    believer_name: BelieverName = None
    coin_mstr_dir: str = None
    coin_label: str = None
    keep_rope: RopeTerm = None
    knot: str = None
    fund_pool: float = None
    fund_iota: float = None
    respect_bit: float = None
    penny: float = None
    keep_point_magnitude: float = None
    _keeps_dir: str = None
    _atoms_dir: str = None
    _packs_dir: str = None

    def set_dir_attrs(self):
        mstr_dir = self.coin_mstr_dir
        coin_label = self.coin_label
        believer_name = self.believer_name
        self._keeps_dir = create_keeps_dir_path(mstr_dir, coin_label, believer_name)
        self._atoms_dir = create_atoms_dir_path(mstr_dir, coin_label, believer_name)
        self._packs_dir = create_packs_dir_path(mstr_dir, coin_label, believer_name)

    def default_gut_believer(self) -> BelieverUnit:
        x_believerunit = believerunit_shop(
            believer_name=self.believer_name,
            coin_label=self.coin_label,
            knot=self.knot,
            fund_pool=self.fund_pool,
            fund_iota=self.fund_iota,
            respect_bit=self.respect_bit,
            penny=self.penny,
        )
        x_believerunit.last_pack_id = init_pack_id()
        return x_believerunit

    # pack methods
    def get_max_atom_file_number(self) -> int:
        return get_max_file_number(self._atoms_dir)

    def _get_next_atom_file_number(self) -> int:
        max_file_number = self.get_max_atom_file_number()
        return 0 if max_file_number is None else max_file_number + 1

    def atom_filename(self, atom_number: int) -> str:
        return f"{atom_number}.json"

    def atom_file_path(self, atom_number: int) -> str:
        "Returns path: _atoms_dir/atom_number.json"
        return create_path(self._atoms_dir, self.atom_filename(atom_number))

    def _save_valid_atom_file(self, x_atom: BelieverAtom, file_number: int):
        save_file(
            self._atoms_dir,
            self.atom_filename(file_number),
            x_atom.get_json(),
            replace=False,
        )
        return file_number

    def save_atom_file(self, x_atom: BelieverAtom):
        x_atom_filename = self._get_next_atom_file_number()
        return self._save_valid_atom_file(x_atom, x_atom_filename)

    def atom_file_exists(self, atom_number: int) -> bool:
        return os_path_exists(self.atom_file_path(atom_number))

    def delete_atom_file(self, atom_number: int):
        delete_dir(self.atom_file_path(atom_number))

    def _get_believer_from_atom_files(self) -> BelieverUnit:
        x_believer = believerunit_shop(self.believer_name, self.coin_label)
        if self.atom_file_exists(self.get_max_atom_file_number()):
            x_atom_files = get_dir_file_strs(self._atoms_dir, delete_extensions=True)
            sorted_atom_filenames = sorted(list(x_atom_files.keys()))

            for x_atom_filename in sorted_atom_filenames:
                x_file_str = x_atom_files.get(x_atom_filename)
                x_atom = believeratom_get_from_json(x_file_str)
                modify_believer_with_believeratom(x_believer, x_atom)
        return x_believer

    def get_max_pack_file_number(self) -> int:
        return get_max_file_number(self._packs_dir)

    def _get_next_pack_file_number(self) -> int:
        max_file_number = self.get_max_pack_file_number()
        init_pack_id = get_init_pack_id_if_None()
        return init_pack_id if max_file_number is None else max_file_number + 1

    def pack_filename(self, pack_id: int) -> str:
        return get_json_filename(pack_id)

    def pack_file_path(self, pack_id: int) -> str:
        """Returns path: _packs/pack_id.json"""

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
        if x_packunit.believer_name != self.believer_name:
            x_packunit.believer_name = self.believer_name
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
            raise SavePackFileException(
                f"PackUnit file cannot be saved because packunit._atoms_dir is incorrect: {x_pack._atoms_dir}. It must be {self._atoms_dir}."
            )
        if x_pack._packs_dir != self._packs_dir:
            raise SavePackFileException(
                f"PackUnit file cannot be saved because packunit._packs_dir is incorrect: {x_pack._packs_dir}. It must be {self._packs_dir}."
            )
        if x_pack.believer_name != self.believer_name:
            raise SavePackFileException(
                f"PackUnit file cannot be saved because packunit.believer_name is incorrect: {x_pack.believer_name}. It must be {self.believer_name}."
            )
        pack_filename = self.pack_filename(x_pack._pack_id)
        if not replace and self.pack_file_exists(x_pack._pack_id):
            raise SavePackFileException(
                f"PackUnit file {pack_filename} exists and cannot be saved over."
            )
        x_pack.save_files()
        return x_pack

    def _del_pack_file(self, pack_id: int):
        delete_dir(self.pack_file_path(pack_id))

    def _default_packunit(self) -> PackUnit:
        return packunit_shop(
            believer_name=self.believer_name,
            _pack_id=self._get_next_pack_file_number(),
            _atoms_dir=self._atoms_dir,
            _packs_dir=self._packs_dir,
        )

    def create_save_pack_file(
        self, before_believer: BelieverUnit, after_believer: BelieverUnit
    ):
        new_packunit = self._default_packunit()
        new_believerdelta = new_packunit._believerdelta
        new_believerdelta.add_all_different_believeratoms(
            before_believer, after_believer
        )
        self.save_pack_file(new_packunit)

    def get_packunit(self, pack_id: int) -> PackUnit:
        if self.pack_file_exists(pack_id) is False:
            raise PackFileMissingException(
                f"PackUnit file_number {pack_id} does not exist."
            )
        x_packs_dir = self._packs_dir
        x_atoms_dir = self._atoms_dir
        return create_packunit_from_files(x_packs_dir, pack_id, x_atoms_dir)

    def _merge_any_packs(self, x_believer: BelieverUnit) -> BelieverUnit:
        packs_dir = self._packs_dir
        pack_ints = get_integer_filenames(packs_dir, x_believer.last_pack_id)
        if len(pack_ints) == 0:
            return copy_deepcopy(x_believer)

        for pack_int in pack_ints:
            x_pack = self.get_packunit(pack_int)
            new_believer = x_pack._believerdelta.get_edited_believer(x_believer)
        return new_believer

    def _create_initial_pack_files_from_default(self):
        x_packunit = packunit_shop(
            believer_name=self.believer_name,
            _pack_id=get_init_pack_id_if_None(),
            _packs_dir=self._packs_dir,
            _atoms_dir=self._atoms_dir,
        )
        x_packunit._believerdelta.add_all_different_believeratoms(
            before_believer=self.default_gut_believer(),
            after_believer=self.default_gut_believer(),
        )
        x_packunit.save_files()

    def _create_gut_from_packs(self):
        x_believer = self._merge_any_packs(self.default_gut_believer())
        save_gut_file(self.coin_mstr_dir, x_believer)

    def _create_initial_pack_and_gut_files(self):
        self._create_initial_pack_files_from_default()
        self._create_gut_from_packs()

    def _create_initial_pack_files_from_gut(self):
        x_packunit = self._default_packunit()
        x_packunit._believerdelta.add_all_different_believeratoms(
            before_believer=self.default_gut_believer(),
            after_believer=open_gut_file(
                self.coin_mstr_dir, self.coin_label, self.believer_name
            ),
        )
        x_packunit.save_files()

    def initialize_pack_gut_files(self):
        x_gut_file_exists = gut_file_exists(
            self.coin_mstr_dir, self.coin_label, self.believer_name
        )
        pack_file_exists = self.pack_file_exists(init_pack_id())
        if x_gut_file_exists is False and pack_file_exists is False:
            self._create_initial_pack_and_gut_files()
        elif x_gut_file_exists is False and pack_file_exists:
            self._create_gut_from_packs()
        elif x_gut_file_exists and pack_file_exists is False:
            self._create_initial_pack_files_from_gut()

    def append_packs_to_gut_file(self) -> BelieverUnit:
        gut_believer = open_gut_file(
            self.coin_mstr_dir, self.coin_label, self.believer_name
        )
        gut_believer = self._merge_any_packs(gut_believer)
        save_gut_file(self.coin_mstr_dir, gut_believer)
        return gut_believer

    # keep management
    def vision_path(self, believer_name: BelieverName) -> str:
        "Returns path: visions_path/believer_name.json"

        return create_path(self.visions_path(), get_json_filename(believer_name))

    def grade_path(self, believer_name: BelieverName) -> str:
        "Returns path: grades_path/believer_name.json"

        return create_path(self.grades_path(), get_json_filename(believer_name))

    def visions_path(self) -> str:
        return create_keep_visions_path(
            coin_mstr_dir=self.coin_mstr_dir,
            believer_name=self.believer_name,
            coin_label=self.coin_label,
            keep_rope=self.keep_rope,
            knot=self.knot,
        )

    def grades_path(self) -> str:
        return create_keep_grades_path(
            coin_mstr_dir=self.coin_mstr_dir,
            believer_name=self.believer_name,
            coin_label=self.coin_label,
            keep_rope=self.keep_rope,
            knot=self.knot,
        )

    def get_visions_path_filenames_list(self) -> list[str]:
        try:
            return list(get_dir_file_strs(self.visions_path(), True).keys())
        except Exception:
            return []

    def save_vision_believer(self, x_believer: BelieverUnit) -> None:
        x_filename = get_json_filename(x_believer.believer_name)
        save_file(self.visions_path(), x_filename, x_believer.get_json())

    def vision_file_exists(self, believer_name: BelieverName) -> bool:
        return os_path_exists(self.vision_path(believer_name))

    def get_vision_believer(self, believer_name: BelieverName) -> BelieverUnit:
        if self.vision_file_exists(believer_name) is False:
            return None
        file_content = open_file(self.visions_path(), get_json_filename(believer_name))
        return believerunit_get_from_json(file_content)

    def get_perspective_believer(self, speaker: BelieverUnit) -> BelieverUnit:
        # get copy of believer without any metrics
        perspective_believer = believerunit_get_from_json(speaker.get_json())
        perspective_believer.set_believer_name(self.believer_name)
        perspective_believer.settle_believer()
        return perspective_believer

    def get_dw_perspective_believer(self, speaker_id: BelieverName) -> BelieverUnit:
        speaker_job = open_job_file(self.coin_mstr_dir, self.coin_label, speaker_id)
        return self.get_perspective_believer(speaker_job)

    def rj_speaker_believer(
        self, healer_name: BelieverName, speaker_id: BelieverName
    ) -> BelieverUnit:
        speaker_hubunit = hubunit_shop(
            coin_mstr_dir=self.coin_mstr_dir,
            coin_label=self.coin_label,
            believer_name=healer_name,
            keep_rope=self.keep_rope,
            knot=self.knot,
            respect_bit=self.respect_bit,
        )
        return speaker_hubunit.get_vision_believer(speaker_id)

    def rj_perspective_believer(
        self, healer_name: BelieverName, speaker_id: BelieverName
    ) -> BelieverUnit:
        speaker_vision = self.rj_speaker_believer(healer_name, speaker_id)
        return self.get_perspective_believer(speaker_vision)

    def get_keep_ropes(self) -> set[RopeTerm]:
        x_gut_believer = open_gut_file(
            self.coin_mstr_dir, self.coin_label, self.believer_name
        )
        x_gut_believer.settle_believer()
        if x_gut_believer._keeps_justified is False:
            x_str = f"Cannot get_keep_ropes from '{self.believer_name}' gut believer because 'BelieverUnit._keeps_justified' is False."
            raise get_keep_ropesException(x_str)
        if x_gut_believer._keeps_buildable is False:
            x_str = f"Cannot get_keep_ropes from '{self.believer_name}' gut believer because 'BelieverUnit._keeps_buildable' is False."
            raise get_keep_ropesException(x_str)
        believer_healer_dict = x_gut_believer._healers_dict.get(self.believer_name)
        if believer_healer_dict is None:
            return get_empty_set_if_None()
        keep_ropes = x_gut_believer._healers_dict.get(self.believer_name).keys()
        return get_empty_set_if_None(keep_ropes)

    def save_all_gut_dutys(self):
        gut = open_gut_file(self.coin_mstr_dir, self.coin_label, self.believer_name)
        for x_keep_rope in self.get_keep_ropes():
            self.keep_rope = x_keep_rope
            save_duty_believer(
                coin_mstr_dir=self.coin_mstr_dir,
                believer_name=self.believer_name,
                coin_label=self.coin_label,
                keep_rope=self.keep_rope,
                knot=self.knot,
                duty_believer=gut,
            )
        self.keep_rope = None

    def create_gut_treasury_db_files(self):
        for x_keep_rope in self.get_keep_ropes():
            create_treasury_db_file(
                self.coin_mstr_dir,
                self.believer_name,
                self.coin_label,
                x_keep_rope,
                self.knot,
            )
        self.keep_rope = None


def hubunit_shop(
    coin_mstr_dir: str,
    coin_label: CoinLabel,
    believer_name: BelieverName = None,
    keep_rope: RopeTerm = None,
    knot: str = None,
    fund_pool: float = None,
    fund_iota: float = None,
    respect_bit: float = None,
    penny: float = None,
    keep_point_magnitude: float = None,
) -> HubUnit:
    x_hubunit = HubUnit(
        coin_mstr_dir=coin_mstr_dir,
        coin_label=coin_label,
        believer_name=validate_labelterm(believer_name, knot),
        keep_rope=keep_rope,
        knot=default_knot_if_None(knot),
        fund_pool=validate_fund_pool(fund_pool),
        fund_iota=default_fund_iota_if_None(fund_iota),
        respect_bit=default_RespectBit_if_None(respect_bit),
        penny=filter_penny(penny),
        keep_point_magnitude=default_money_magnitude_if_None(keep_point_magnitude),
    )
    x_hubunit.set_dir_attrs()
    return x_hubunit
