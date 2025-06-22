from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from os.path import exists as os_path_exists
from sqlite3 import Connection, connect as sqlite3_connect
from src.a00_data_toolbox.db_toolbox import sqlite_connection
from src.a00_data_toolbox.dict_toolbox import get_empty_set_if_None
from src.a00_data_toolbox.file_toolbox import (
    create_path,
    delete_dir,
    get_dir_file_strs,
    get_directory_path,
    get_integer_filenames,
    get_json_filename,
    get_max_file_number,
    open_file,
    open_json,
    save_file,
    save_json,
    set_dir,
)
from src.a01_term_logic.rope import (
    get_all_rope_labels,
    rebuild_rope,
    validate_labelterm,
)
from src.a01_term_logic.term import (
    BeliefLabel,
    LabelTerm,
    OwnerName,
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
from src.a06_plan_logic.plan import (
    PlanUnit,
    get_from_json as planunit_get_from_json,
    planunit_shop,
)
from src.a08_plan_atom_logic.atom import (
    PlanAtom,
    get_from_json as planatom_get_from_json,
    modify_plan_with_planatom,
)
from src.a09_pack_logic.pack import (
    PackUnit,
    create_packunit_from_files,
    get_init_pack_id_if_None,
    init_pack_id,
    packunit_shop,
)
from src.a12_hub_toolbox.basis_plans import get_default_job
from src.a12_hub_toolbox.hub_path import (
    create_atoms_dir_path,
    create_keeps_dir_path,
    create_packs_dir_path,
    treasury_filename,
)
from src.a12_hub_toolbox.hub_tool import (
    gut_file_exists,
    open_gut_file,
    open_job_file,
    save_gut_file,
    save_job_file,
)


class SavePackFileException(Exception):
    pass


class PackFileMissingException(Exception):
    pass


class get_keep_ropesException(Exception):
    pass


class _keep_ropeMissingException(Exception):
    pass


def get_keep_dutys_dir(x_keep_dir: str) -> str:
    return create_path(x_keep_dir, "dutys")


def get_keep_visions_dir(x_keep_dir: str) -> str:
    return create_path(x_keep_dir, "visions")


def get_keep_grades_dir(x_keep_dir: str) -> str:
    return create_path(x_keep_dir, "grades")


@dataclass
class HubUnit:
    owner_name: OwnerName = None
    belief_mstr_dir: str = None
    belief_label: str = None
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
        mstr_dir = self.belief_mstr_dir
        belief_label = self.belief_label
        owner_name = self.owner_name
        self._keeps_dir = create_keeps_dir_path(mstr_dir, belief_label, owner_name)
        self._atoms_dir = create_atoms_dir_path(mstr_dir, belief_label, owner_name)
        self._packs_dir = create_packs_dir_path(mstr_dir, belief_label, owner_name)

    def default_gut_plan(self) -> PlanUnit:
        x_planunit = planunit_shop(
            owner_name=self.owner_name,
            belief_label=self.belief_label,
            knot=self.knot,
            fund_pool=self.fund_pool,
            fund_iota=self.fund_iota,
            respect_bit=self.respect_bit,
            penny=self.penny,
        )
        x_planunit.last_pack_id = init_pack_id()
        return x_planunit

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

    def _save_valid_atom_file(self, x_atom: PlanAtom, file_number: int):
        save_file(
            self._atoms_dir,
            self.atom_filename(file_number),
            x_atom.get_json(),
            replace=False,
        )
        return file_number

    def save_atom_file(self, x_atom: PlanAtom):
        x_atom_filename = self._get_next_atom_file_number()
        return self._save_valid_atom_file(x_atom, x_atom_filename)

    def atom_file_exists(self, atom_number: int) -> bool:
        return os_path_exists(self.atom_file_path(atom_number))

    def delete_atom_file(self, atom_number: int):
        delete_dir(self.atom_file_path(atom_number))

    def _get_plan_from_atom_files(self) -> PlanUnit:
        x_plan = planunit_shop(self.owner_name, self.belief_label)
        if self.atom_file_exists(self.get_max_atom_file_number()):
            x_atom_files = get_dir_file_strs(self._atoms_dir, delete_extensions=True)
            sorted_atom_filenames = sorted(list(x_atom_files.keys()))

            for x_atom_filename in sorted_atom_filenames:
                x_file_str = x_atom_files.get(x_atom_filename)
                x_atom = planatom_get_from_json(x_file_str)
                modify_plan_with_planatom(x_plan, x_atom)
        return x_plan

    def get_max_pack_file_number(self) -> int:
        return get_max_file_number(self._packs_dir)

    def _get_next_pack_file_number(self) -> int:
        max_file_number = self.get_max_pack_file_number()
        init_pack_id = get_init_pack_id_if_None()
        return init_pack_id if max_file_number is None else max_file_number + 1

    def pack_filename(self, pack_id: int) -> str:
        return get_json_filename(pack_id)

    def pack_file_path(self, pack_id: int) -> str:
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
            raise SavePackFileException(
                f"PackUnit file cannot be saved because packunit._atoms_dir is incorrect: {x_pack._atoms_dir}. It must be {self._atoms_dir}."
            )
        if x_pack._packs_dir != self._packs_dir:
            raise SavePackFileException(
                f"PackUnit file cannot be saved because packunit._packs_dir is incorrect: {x_pack._packs_dir}. It must be {self._packs_dir}."
            )
        if x_pack.owner_name != self.owner_name:
            raise SavePackFileException(
                f"PackUnit file cannot be saved because packunit.owner_name is incorrect: {x_pack.owner_name}. It must be {self.owner_name}."
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
            owner_name=self.owner_name,
            _pack_id=self._get_next_pack_file_number(),
            _atoms_dir=self._atoms_dir,
            _packs_dir=self._packs_dir,
        )

    def create_save_pack_file(self, before_plan: PlanUnit, after_plan: PlanUnit):
        new_packunit = self._default_packunit()
        new_plandelta = new_packunit._plandelta
        new_plandelta.add_all_different_planatoms(before_plan, after_plan)
        self.save_pack_file(new_packunit)

    def get_packunit(self, pack_id: int) -> PackUnit:
        if self.pack_file_exists(pack_id) is False:
            raise PackFileMissingException(
                f"PackUnit file_number {pack_id} does not exist."
            )
        x_packs_dir = self._packs_dir
        x_atoms_dir = self._atoms_dir
        return create_packunit_from_files(x_packs_dir, pack_id, x_atoms_dir)

    def _merge_any_packs(self, x_plan: PlanUnit) -> PlanUnit:
        packs_dir = self._packs_dir
        pack_ints = get_integer_filenames(packs_dir, x_plan.last_pack_id)
        if len(pack_ints) == 0:
            return copy_deepcopy(x_plan)

        for pack_int in pack_ints:
            x_pack = self.get_packunit(pack_int)
            new_plan = x_pack._plandelta.get_edited_plan(x_plan)
        return new_plan

    def _create_initial_pack_files_from_default(self):
        x_packunit = packunit_shop(
            owner_name=self.owner_name,
            _pack_id=get_init_pack_id_if_None(),
            _packs_dir=self._packs_dir,
            _atoms_dir=self._atoms_dir,
        )
        x_packunit._plandelta.add_all_different_planatoms(
            before_plan=self.default_gut_plan(),
            after_plan=self.default_gut_plan(),
        )
        x_packunit.save_files()

    def _create_gut_from_packs(self):
        x_plan = self._merge_any_packs(self.default_gut_plan())
        save_gut_file(self.belief_mstr_dir, x_plan)

    def _create_initial_pack_and_gut_files(self):
        self._create_initial_pack_files_from_default()
        self._create_gut_from_packs()

    def _create_initial_pack_files_from_gut(self):
        x_packunit = self._default_packunit()
        x_packunit._plandelta.add_all_different_planatoms(
            before_plan=self.default_gut_plan(),
            after_plan=open_gut_file(
                self.belief_mstr_dir, self.belief_label, self.owner_name
            ),
        )
        x_packunit.save_files()

    def initialize_pack_gut_files(self):
        x_gut_file_exists = gut_file_exists(
            self.belief_mstr_dir, self.belief_label, self.owner_name
        )
        pack_file_exists = self.pack_file_exists(init_pack_id())
        if x_gut_file_exists is False and pack_file_exists is False:
            self._create_initial_pack_and_gut_files()
        elif x_gut_file_exists is False and pack_file_exists:
            self._create_gut_from_packs()
        elif x_gut_file_exists and pack_file_exists is False:
            self._create_initial_pack_files_from_gut()

    def append_packs_to_gut_file(self) -> PlanUnit:
        gut_plan = open_gut_file(
            self.belief_mstr_dir, self.belief_label, self.owner_name
        )
        gut_plan = self._merge_any_packs(gut_plan)
        save_gut_file(self.belief_mstr_dir, gut_plan)
        return gut_plan

    # keep management
    def keep_dir(self) -> str:
        if self.keep_rope is None:
            raise _keep_ropeMissingException(
                f"HubUnit '{self.owner_name}' cannot save to keep_dir because it does not have keep_rope."
            )
        return get_keep_path(self, self.keep_rope)

    def create_keep_dir_if_missing(self):
        set_dir(self.keep_dir())

    def treasury_db_path(self) -> str:
        return create_path(self.keep_dir(), treasury_filename())

    def duty_path(self, owner_name: OwnerName) -> str:
        return create_path(self.dutys_dir(), get_json_filename(owner_name))

    def vision_path(self, owner_name: OwnerName) -> str:
        return create_path(self.visions_dir(), get_json_filename(owner_name))

    def grade_path(self, owner_name: OwnerName) -> str:
        return create_path(self.grades_dir(), get_json_filename(owner_name))

    def dutys_dir(self) -> str:
        return get_keep_dutys_dir(self.keep_dir())

    def visions_dir(self) -> str:
        return get_keep_visions_dir(self.keep_dir())

    def grades_dir(self) -> str:
        return get_keep_grades_dir(self.keep_dir())

    def get_visions_dir_filenames_list(self) -> list[str]:
        try:
            return list(get_dir_file_strs(self.visions_dir(), True).keys())
        except Exception:
            return []

    def save_duty_plan(self, x_plan: PlanUnit) -> None:
        x_filename = get_json_filename(x_plan.owner_name)
        save_file(self.dutys_dir(), x_filename, x_plan.get_json())

    def save_vision_plan(self, x_plan: PlanUnit) -> None:
        x_filename = get_json_filename(x_plan.owner_name)
        save_file(self.visions_dir(), x_filename, x_plan.get_json())

    def initialize_job_file(self, gut: PlanUnit) -> None:
        save_job_file(self.belief_mstr_dir, get_default_job(gut))

    def duty_file_exists(self, owner_name: OwnerName) -> bool:
        return os_path_exists(self.duty_path(owner_name))

    def vision_file_exists(self, owner_name: OwnerName) -> bool:
        return os_path_exists(self.vision_path(owner_name))

    def get_duty_plan(self, owner_name: OwnerName) -> PlanUnit:
        if self.duty_file_exists(owner_name) is False:
            return None
        file_content = open_file(self.dutys_dir(), get_json_filename(owner_name))
        return planunit_get_from_json(file_content)

    def get_vision_plan(self, owner_name: OwnerName) -> PlanUnit:
        if self.vision_file_exists(owner_name) is False:
            return None
        file_content = open_file(self.visions_dir(), get_json_filename(owner_name))
        return planunit_get_from_json(file_content)

    def delete_duty_file(self, owner_name: OwnerName) -> None:
        delete_dir(self.duty_path(owner_name))

    def delete_vision_file(self, owner_name: OwnerName) -> None:
        delete_dir(self.vision_path(owner_name))

    def delete_treasury_db_file(self) -> None:
        delete_dir(self.treasury_db_path())

    def get_perspective_plan(self, speaker: PlanUnit) -> PlanUnit:
        # get copy of plan without any metrics
        perspective_plan = planunit_get_from_json(speaker.get_json())
        perspective_plan.set_owner_name(self.owner_name)
        perspective_plan.settle_plan()
        return perspective_plan

    def get_dw_perspective_plan(self, speaker_id: OwnerName) -> PlanUnit:
        speaker_job = open_job_file(self.belief_mstr_dir, self.belief_label, speaker_id)
        return self.get_perspective_plan(speaker_job)

    def rj_speaker_plan(
        self, healer_name: OwnerName, speaker_id: OwnerName
    ) -> PlanUnit:
        speaker_hubunit = hubunit_shop(
            belief_mstr_dir=self.belief_mstr_dir,
            belief_label=self.belief_label,
            owner_name=healer_name,
            keep_rope=self.keep_rope,
            knot=self.knot,
            respect_bit=self.respect_bit,
        )
        return speaker_hubunit.get_vision_plan(speaker_id)

    def rj_perspective_plan(
        self, healer_name: OwnerName, speaker_id: OwnerName
    ) -> PlanUnit:
        speaker_vision = self.rj_speaker_plan(healer_name, speaker_id)
        return self.get_perspective_plan(speaker_vision)

    def get_keep_ropes(self) -> set[RopeTerm]:
        x_gut_plan = open_gut_file(
            self.belief_mstr_dir, self.belief_label, self.owner_name
        )
        x_gut_plan.settle_plan()
        if x_gut_plan._keeps_justified is False:
            x_str = f"Cannot get_keep_ropes from '{self.owner_name}' gut plan because 'PlanUnit._keeps_justified' is False."
            raise get_keep_ropesException(x_str)
        if x_gut_plan._keeps_buildable is False:
            x_str = f"Cannot get_keep_ropes from '{self.owner_name}' gut plan because 'PlanUnit._keeps_buildable' is False."
            raise get_keep_ropesException(x_str)
        owner_healer_dict = x_gut_plan._healers_dict.get(self.owner_name)
        if owner_healer_dict is None:
            return get_empty_set_if_None()
        keep_ropes = x_gut_plan._healers_dict.get(self.owner_name).keys()
        return get_empty_set_if_None(keep_ropes)

    def save_all_gut_dutys(self):
        gut = open_gut_file(self.belief_mstr_dir, self.belief_label, self.owner_name)
        for x_keep_rope in self.get_keep_ropes():
            self.keep_rope = x_keep_rope
            self.save_duty_plan(gut)
        self.keep_rope = None

    def create_treasury_db_file(self) -> None:
        self.create_keep_dir_if_missing()
        db_path = self.treasury_db_path()
        conn = sqlite3_connect(db_path)
        conn.close()

    def treasury_db_file_exists(self) -> bool:
        return os_path_exists(self.treasury_db_path())

    def treasury_db_file_conn(self) -> Connection:
        if self.keep_rope is None:
            raise _keep_ropeMissingException(
                f"hubunit cannot connect to treasury_db_file because keep_rope is {self.keep_rope}"
            )
        if self.treasury_db_file_exists() is False:
            self.create_treasury_db_file()
        return sqlite_connection(self.treasury_db_path())

    def create_gut_treasury_db_files(self):
        for x_keep_rope in self.get_keep_ropes():
            self.keep_rope = x_keep_rope
            self.create_treasury_db_file()
        self.keep_rope = None


def hubunit_shop(
    belief_mstr_dir: str,
    belief_label: BeliefLabel,
    owner_name: OwnerName = None,
    keep_rope: RopeTerm = None,
    knot: str = None,
    fund_pool: float = None,
    fund_iota: float = None,
    respect_bit: float = None,
    penny: float = None,
    keep_point_magnitude: float = None,
) -> HubUnit:
    x_hubunit = HubUnit(
        belief_mstr_dir=belief_mstr_dir,
        belief_label=belief_label,
        owner_name=validate_labelterm(owner_name, knot),
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


def get_keep_path(x_hubunit: HubUnit, x_rope: LabelTerm) -> str:
    keep_root = "conceptroot"
    x_rope = rebuild_rope(x_rope, x_hubunit.belief_label, keep_root)
    x_list = get_all_rope_labels(x_rope, x_hubunit.knot)
    keep_sub_path = get_directory_path(x_list=[*x_list])
    return create_path(x_hubunit._keeps_dir, keep_sub_path)
