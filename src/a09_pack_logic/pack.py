from src.a00_data_toolbox.file_toolbox import (
    save_file,
    open_file,
    open_json,
    create_path,
    get_json_filename,
)
from src.a00_data_toolbox.dict_toolbox import get_json_from_dict, get_dict_from_json
from src.a01_term_logic.way import (
    FaceName,
    OwnerName,
    FiscLabel,
    get_default_fisc_label,
)
from src.a06_bud_logic.bud import BudUnit
from src.a08_bud_atom_logic.atom import BudAtom, get_from_json as budatom_get_from_json
from src.a09_pack_logic.delta import (
    BudDelta,
    buddelta_shop,
    get_buddelta_from_ordered_dict,
)
from dataclasses import dataclass
from os.path import exists as os_path_exists


class pack_bud_conflict_Exception(Exception):
    pass


def init_pack_id() -> int:
    return 0


def get_init_pack_id_if_None(x_pack_id: int = None) -> int:
    return init_pack_id() if x_pack_id is None else x_pack_id


@dataclass
class PackUnit:
    face_name: FaceName = None
    fisc_label: FiscLabel = None
    owner_name: OwnerName = None
    _pack_id: int = None
    _buddelta: BudDelta = None
    _delta_start: int = None
    _packs_dir: str = None
    _atoms_dir: str = None
    event_int: int = None
    """Represents a per fisc_label/event_int BudDelta for a owner_name"""

    def set_face(self, x_face_name: FaceName):
        self.face_name = x_face_name

    def del_face(self):
        self.face_name = None

    def set_buddelta(self, x_buddelta: BudDelta):
        self._buddelta = x_buddelta

    def del_buddelta(self):
        self._buddelta = buddelta_shop()

    def set_delta_start(self, x_delta_start: int):
        self._delta_start = get_init_pack_id_if_None(x_delta_start)

    def budatom_exists(self, x_budatom: BudAtom):
        return self._buddelta.budatom_exists(x_budatom)

    def get_step_dict(self) -> dict[str, any]:
        return {
            "face_name": self.face_name,
            "fisc_label": self.fisc_label,
            "owner_name": self.owner_name,
            "event_int": self.event_int,
            "delta": self._buddelta.get_ordered_budatoms(self._delta_start),
        }

    def get_serializable_dict(self) -> dict[str, dict]:
        total_dict = self.get_step_dict()
        total_dict["delta"] = self._buddelta.get_ordered_dict()
        return total_dict

    def get_json(self) -> str:
        return get_json_from_dict(self.get_serializable_dict())

    def get_delta_atom_numbers(self, packunit_dict: list[str]) -> int:
        delta_dict = packunit_dict.get("delta")
        return list(delta_dict.keys())

    def get_deltametric_dict(self) -> dict:
        x_dict = self.get_step_dict()
        return {
            "owner_name": x_dict.get("owner_name"),
            "face_name": x_dict.get("face_name"),
            "event_int": x_dict.get("event_int"),
            "delta_atom_numbers": self.get_delta_atom_numbers(x_dict),
        }

    def get_deltametric_json(self) -> str:
        return get_json_from_dict(self.get_deltametric_dict())

    def _get_num_filename(self, x_number: int) -> str:
        return get_json_filename(x_number)

    def _save_atom_file(self, atom_number: int, x_atom: BudAtom):
        x_filename = self._get_num_filename(atom_number)
        save_file(self._atoms_dir, x_filename, x_atom.get_json())

    def atom_file_exists(self, atom_number: int) -> bool:
        x_filename = self._get_num_filename(atom_number)
        return os_path_exists(create_path(self._atoms_dir, x_filename))

    def _open_atom_file(self, atom_number: int) -> BudAtom:
        x_json = open_file(self._atoms_dir, self._get_num_filename(atom_number))
        return budatom_get_from_json(x_json)

    def _save_pack_file(self):
        x_filename = self._get_num_filename(self._pack_id)
        save_file(self._packs_dir, x_filename, self.get_deltametric_json())

    def pack_file_exists(self) -> bool:
        x_filename = self._get_num_filename(self._pack_id)
        return os_path_exists(create_path(self._packs_dir, x_filename))

    def _save_atom_files(self):
        step_dict = self.get_step_dict()
        ordered_budatoms = step_dict.get("delta")
        for order_int, budatom in ordered_budatoms.items():
            self._save_atom_file(order_int, budatom)

    def save_files(self):
        self._save_pack_file()
        self._save_atom_files()

    def _create_buddelta_from_atom_files(self, atom_number_list: list) -> BudDelta:
        x_buddelta = buddelta_shop()
        for atom_number in atom_number_list:
            x_budatom = self._open_atom_file(atom_number)
            x_buddelta.set_budatom(x_budatom)
        self._buddelta = x_buddelta

    def add_budatom(
        self,
        dimen: str,
        crud_str: str,
        jkeys: dict[str, str] = None,
        jvalues: dict[str, str] = None,
    ):
        self._buddelta.add_budatom(dimen, crud_str, jkeys=jkeys, jvalues=jvalues)

    def get_edited_bud(self, before_bud: BudUnit) -> BudUnit:
        if (
            self.fisc_label != before_bud.fisc_label
            or self.owner_name != before_bud.owner_name
        ):
            raise pack_bud_conflict_Exception(
                f"pack bud conflict {self.fisc_label} != {before_bud.fisc_label} or {self.owner_name} != {before_bud.owner_name}"
            )
        return self._buddelta.get_edited_bud(before_bud)

    def is_empty(self) -> bool:
        return self._buddelta.is_empty()


def packunit_shop(
    owner_name: OwnerName,
    face_name: FaceName = None,
    fisc_label: FiscLabel = None,
    _pack_id: int = None,
    _buddelta: BudDelta = None,
    _delta_start: int = None,
    _packs_dir: str = None,
    _atoms_dir: str = None,
    event_int: int = None,
) -> PackUnit:
    _buddelta = buddelta_shop() if _buddelta is None else _buddelta
    fisc_label = get_default_fisc_label() if fisc_label is None else fisc_label
    x_packunit = PackUnit(
        face_name=face_name,
        owner_name=owner_name,
        fisc_label=fisc_label,
        _pack_id=get_init_pack_id_if_None(_pack_id),
        _buddelta=_buddelta,
        _packs_dir=_packs_dir,
        _atoms_dir=_atoms_dir,
        event_int=event_int,
    )
    x_packunit.set_delta_start(_delta_start)
    return x_packunit


def create_packunit_from_files(
    packs_dir: str,
    pack_id: str,
    atoms_dir: str,
) -> PackUnit:
    pack_filename = get_json_filename(pack_id)
    pack_dict = open_json(packs_dir, pack_filename)
    x_owner_name = pack_dict.get("owner_name")
    x_fisc_label = pack_dict.get("fisc_label")
    x_face_name = pack_dict.get("face_name")
    delta_atom_numbers_list = pack_dict.get("delta_atom_numbers")
    x_packunit = packunit_shop(
        face_name=x_face_name,
        owner_name=x_owner_name,
        fisc_label=x_fisc_label,
        _pack_id=pack_id,
        _atoms_dir=atoms_dir,
    )
    x_packunit._create_buddelta_from_atom_files(delta_atom_numbers_list)
    return x_packunit


def get_packunit_from_json(x_json: str) -> PackUnit:
    pack_dict = get_dict_from_json(x_json)
    if pack_dict.get("event_int") is None:
        x_event_int = None
    else:
        x_event_int = int(pack_dict.get("event_int"))
    x_packunit = packunit_shop(
        face_name=pack_dict.get("face_name"),
        owner_name=pack_dict.get("owner_name"),
        fisc_label=pack_dict.get("fisc_label"),
        _pack_id=pack_dict.get("pack_id"),
        _atoms_dir=pack_dict.get("atoms_dir"),
        event_int=x_event_int,
    )
    x_buddelta = get_buddelta_from_ordered_dict(pack_dict.get("delta"))
    x_packunit.set_buddelta(x_buddelta)
    return x_packunit
