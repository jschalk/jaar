from src.f00_instrument.file import save_file, open_file, open_json, create_path
from src.f00_instrument.dict_toolbox import get_json_from_dict, get_dict_from_json
from src.f01_road.jaar_config import get_init_vow_id_if_None, get_json_filename
from src.f01_road.road import (
    FaceName,
    OwnerName,
    FiscTitle,
    get_default_fisc_title,
)
from src.f02_bud.bud import BudUnit
from src.f04_vow.atom import BudAtom, get_from_json as budatom_get_from_json
from src.f04_vow.delta import (
    BudDelta,
    buddelta_shop,
    get_buddelta_from_ordered_dict,
)
from dataclasses import dataclass
from os.path import exists as os_path_exists


class vow_bud_conflict_Exception(Exception):
    pass


@dataclass
class vowUnit:
    face_name: FaceName = None
    fisc_title: FiscTitle = None
    owner_name: OwnerName = None
    _vow_id: int = None
    _buddelta: BudDelta = None
    _delta_start: int = None
    _vows_dir: str = None
    _atoms_dir: str = None
    event_int: int = None

    def set_face(self, x_face_name: FaceName):
        self.face_name = x_face_name

    def del_face(self):
        self.face_name = None

    def set_buddelta(self, x_buddelta: BudDelta):
        self._buddelta = x_buddelta

    def del_buddelta(self):
        self._buddelta = buddelta_shop()

    def set_delta_start(self, x_delta_start: int):
        self._delta_start = get_init_vow_id_if_None(x_delta_start)

    def budatom_exists(self, x_budatom: BudAtom):
        return self._buddelta.budatom_exists(x_budatom)

    def get_step_dict(self) -> dict[str, any]:
        return {
            "face_name": self.face_name,
            "fisc_title": self.fisc_title,
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

    def get_delta_atom_numbers(self, vowunit_dict: list[str]) -> int:
        delta_dict = vowunit_dict.get("delta")
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

    def _save_vow_file(self):
        x_filename = self._get_num_filename(self._vow_id)
        save_file(self._vows_dir, x_filename, self.get_deltametric_json())

    def vow_file_exists(self) -> bool:
        x_filename = self._get_num_filename(self._vow_id)
        return os_path_exists(create_path(self._vows_dir, x_filename))

    def _save_atom_files(self):
        step_dict = self.get_step_dict()
        ordered_budatoms = step_dict.get("delta")
        for order_int, budatom in ordered_budatoms.items():
            self._save_atom_file(order_int, budatom)

    def save_files(self):
        self._save_vow_file()
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
            self.fisc_title != before_bud.fisc_title
            or self.owner_name != before_bud.owner_name
        ):
            raise vow_bud_conflict_Exception(
                f"vow bud conflict {self.fisc_title} != {before_bud.fisc_title} or {self.owner_name} != {before_bud.owner_name}"
            )
        return self._buddelta.get_edited_bud(before_bud)

    def is_empty(self) -> bool:
        return self._buddelta.is_empty()


def vowunit_shop(
    owner_name: OwnerName,
    face_name: FaceName = None,
    fisc_title: FiscTitle = None,
    _vow_id: int = None,
    _buddelta: BudDelta = None,
    _delta_start: int = None,
    _vows_dir: str = None,
    _atoms_dir: str = None,
    event_int: int = None,
) -> vowUnit:
    _buddelta = buddelta_shop() if _buddelta is None else _buddelta
    fisc_title = get_default_fisc_title() if fisc_title is None else fisc_title
    x_vowunit = vowUnit(
        face_name=face_name,
        owner_name=owner_name,
        fisc_title=fisc_title,
        _vow_id=get_init_vow_id_if_None(_vow_id),
        _buddelta=_buddelta,
        _vows_dir=_vows_dir,
        _atoms_dir=_atoms_dir,
        event_int=event_int,
    )
    x_vowunit.set_delta_start(_delta_start)
    return x_vowunit


def create_vowunit_from_files(
    vows_dir: str,
    vow_id: str,
    atoms_dir: str,
) -> vowUnit:
    vow_filename = get_json_filename(vow_id)
    vow_dict = open_json(vows_dir, vow_filename)
    x_owner_name = vow_dict.get("owner_name")
    x_fisc_title = vow_dict.get("fisc_title")
    x_face_name = vow_dict.get("face_name")
    delta_atom_numbers_list = vow_dict.get("delta_atom_numbers")
    x_vowunit = vowunit_shop(
        face_name=x_face_name,
        owner_name=x_owner_name,
        fisc_title=x_fisc_title,
        _vow_id=vow_id,
        _atoms_dir=atoms_dir,
    )
    x_vowunit._create_buddelta_from_atom_files(delta_atom_numbers_list)
    return x_vowunit


def get_vowunit_from_json(x_json: str) -> vowUnit:
    vow_dict = get_dict_from_json(x_json)
    if vow_dict.get("event_int") is None:
        x_event_int = None
    else:
        x_event_int = int(vow_dict.get("event_int"))
    x_vowunit = vowunit_shop(
        face_name=vow_dict.get("face_name"),
        owner_name=vow_dict.get("owner_name"),
        fisc_title=vow_dict.get("fisc_title"),
        _vow_id=vow_dict.get("vow_id"),
        _atoms_dir=vow_dict.get("atoms_dir"),
        event_int=x_event_int,
    )
    x_buddelta = get_buddelta_from_ordered_dict(vow_dict.get("delta"))
    x_vowunit.set_buddelta(x_buddelta)
    return x_vowunit
