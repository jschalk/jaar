from dataclasses import dataclass
from os.path import exists as os_path_exists
from src.a00_data_toolbox.dict_toolbox import get_dict_from_json, get_json_from_dict
from src.a00_data_toolbox.file_toolbox import (
    create_path,
    get_json_filename,
    open_file,
    open_json,
    save_file,
)
from src.a01_rope_logic.term import BeliefName, FaceName, MomentLabel
from src.a05_plan_logic.plan import get_default_moment_label
from src.a06_belief_logic.belief_main import BeliefUnit
from src.a08_belief_atom_logic.atom_main import (
    BeliefAtom,
    get_from_json as beliefatom_get_from_json,
)
from src.a09_pack_logic.delta import (
    BeliefDelta,
    beliefdelta_shop,
    get_beliefdelta_from_ordered_dict,
)


class pack_belief_conflict_Exception(Exception):
    pass


def init_pack_id() -> int:
    return 0


def get_init_pack_id_if_None(x_pack_id: int = None) -> int:
    return init_pack_id() if x_pack_id is None else x_pack_id


@dataclass
class PackUnit:
    face_name: FaceName = None
    moment_label: MomentLabel = None
    belief_name: BeliefName = None
    _pack_id: int = None
    _beliefdelta: BeliefDelta = None
    _delta_start: int = None
    _packs_dir: str = None
    _atoms_dir: str = None
    event_int: int = None
    """Represents a per moment_label/event_int BeliefDelta for a belief_name"""

    def set_face(self, x_face_name: FaceName):
        self.face_name = x_face_name

    def del_face(self):
        self.face_name = None

    def set_beliefdelta(self, x_beliefdelta: BeliefDelta):
        self._beliefdelta = x_beliefdelta

    def del_beliefdelta(self):
        self._beliefdelta = beliefdelta_shop()

    def set_delta_start(self, x_delta_start: int):
        self._delta_start = get_init_pack_id_if_None(x_delta_start)

    def beliefatom_exists(self, x_beliefatom: BeliefAtom):
        return self._beliefdelta.beliefatom_exists(x_beliefatom)

    def get_step_dict(self) -> dict[str, any]:
        return {
            "face_name": self.face_name,
            "moment_label": self.moment_label,
            "belief_name": self.belief_name,
            "event_int": self.event_int,
            "delta": self._beliefdelta.get_ordered_beliefatoms(self._delta_start),
        }

    def get_serializable_dict(self) -> dict[str, dict]:
        total_dict = self.get_step_dict()
        total_dict["delta"] = self._beliefdelta.get_ordered_dict()
        return total_dict

    def get_json(self) -> str:
        return get_json_from_dict(self.get_serializable_dict())

    def get_delta_atom_numbers(self, packunit_dict: list[str]) -> int:
        delta_dict = packunit_dict.get("delta")
        return list(delta_dict.keys())

    def get_deltametric_dict(self) -> dict:
        x_dict = self.get_step_dict()
        return {
            "belief_name": x_dict.get("belief_name"),
            "face_name": x_dict.get("face_name"),
            "event_int": x_dict.get("event_int"),
            "delta_atom_numbers": self.get_delta_atom_numbers(x_dict),
        }

    def get_deltametric_json(self) -> str:
        return get_json_from_dict(self.get_deltametric_dict())

    def _get_num_filename(self, x_number: int) -> str:
        return get_json_filename(x_number)

    def _save_atom_file(self, atom_number: int, x_atom: BeliefAtom):
        x_filename = self._get_num_filename(atom_number)
        save_file(self._atoms_dir, x_filename, x_atom.get_json())

    def atom_file_exists(self, atom_number: int) -> bool:
        x_filename = self._get_num_filename(atom_number)
        return os_path_exists(create_path(self._atoms_dir, x_filename))

    def _open_atom_file(self, atom_number: int) -> BeliefAtom:
        x_json = open_file(self._atoms_dir, self._get_num_filename(atom_number))
        return beliefatom_get_from_json(x_json)

    def _save_pack_file(self):
        x_filename = self._get_num_filename(self._pack_id)
        save_file(self._packs_dir, x_filename, self.get_deltametric_json())

    def pack_file_exists(self) -> bool:
        x_filename = self._get_num_filename(self._pack_id)
        return os_path_exists(create_path(self._packs_dir, x_filename))

    def _save_atom_files(self):
        step_dict = self.get_step_dict()
        ordered_beliefatoms = step_dict.get("delta")
        for order_int, beliefatom in ordered_beliefatoms.items():
            self._save_atom_file(order_int, beliefatom)

    def save_files(self):
        self._save_pack_file()
        self._save_atom_files()

    def _create_beliefdelta_from_atom_files(
        self, atom_number_list: list
    ) -> BeliefDelta:
        x_beliefdelta = beliefdelta_shop()
        for atom_number in atom_number_list:
            x_beliefatom = self._open_atom_file(atom_number)
            x_beliefdelta.set_beliefatom(x_beliefatom)
        self._beliefdelta = x_beliefdelta

    def add_beliefatom(
        self,
        dimen: str,
        crud_str: str,
        jkeys: dict[str, str] = None,
        jvalues: dict[str, str] = None,
    ):
        self._beliefdelta.add_beliefatom(dimen, crud_str, jkeys=jkeys, jvalues=jvalues)

    def get_edited_belief(self, before_belief: BeliefUnit) -> BeliefUnit:
        if (
            self.moment_label != before_belief.moment_label
            or self.belief_name != before_belief.belief_name
        ):
            raise pack_belief_conflict_Exception(
                f"pack belief conflict {self.moment_label} != {before_belief.moment_label} or {self.belief_name} != {before_belief.belief_name}"
            )
        return self._beliefdelta.get_edited_belief(before_belief)

    def is_empty(self) -> bool:
        return self._beliefdelta.is_empty()


def packunit_shop(
    belief_name: BeliefName,
    face_name: FaceName = None,
    moment_label: MomentLabel = None,
    _pack_id: int = None,
    _beliefdelta: BeliefDelta = None,
    _delta_start: int = None,
    _packs_dir: str = None,
    _atoms_dir: str = None,
    event_int: int = None,
) -> PackUnit:
    _beliefdelta = beliefdelta_shop() if _beliefdelta is None else _beliefdelta
    moment_label = get_default_moment_label() if moment_label is None else moment_label
    x_packunit = PackUnit(
        face_name=face_name,
        belief_name=belief_name,
        moment_label=moment_label,
        _pack_id=get_init_pack_id_if_None(_pack_id),
        _beliefdelta=_beliefdelta,
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
    x_belief_name = pack_dict.get("belief_name")
    x_moment_label = pack_dict.get("moment_label")
    x_face_name = pack_dict.get("face_name")
    delta_atom_numbers_list = pack_dict.get("delta_atom_numbers")
    x_packunit = packunit_shop(
        face_name=x_face_name,
        belief_name=x_belief_name,
        moment_label=x_moment_label,
        _pack_id=pack_id,
        _atoms_dir=atoms_dir,
    )
    x_packunit._create_beliefdelta_from_atom_files(delta_atom_numbers_list)
    return x_packunit


def get_packunit_from_json(x_json: str) -> PackUnit:
    pack_dict = get_dict_from_json(x_json)
    if pack_dict.get("event_int") is None:
        x_event_int = None
    else:
        x_event_int = int(pack_dict.get("event_int"))
    x_packunit = packunit_shop(
        face_name=pack_dict.get("face_name"),
        belief_name=pack_dict.get("belief_name"),
        moment_label=pack_dict.get("moment_label"),
        _pack_id=pack_dict.get("pack_id"),
        _atoms_dir=pack_dict.get("atoms_dir"),
        event_int=x_event_int,
    )
    x_beliefdelta = get_beliefdelta_from_ordered_dict(pack_dict.get("delta"))
    x_packunit.set_beliefdelta(x_beliefdelta)
    return x_packunit
