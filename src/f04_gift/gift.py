from src.f00_instrument.file import save_file, open_file, create_path
from src.f00_instrument.dict_toolbox import get_json_from_dict, get_dict_from_json
from src.f01_road.jaar_config import get_init_gift_id_if_None, get_json_filename
from src.f01_road.road import (
    FaceName,
    OwnerName,
    FiscalTitle,
    get_default_fiscal_title,
)
from src.f04_gift.atom import AtomUnit, get_from_json as atomunit_get_from_json
from src.f04_gift.delta import (
    DeltaUnit,
    deltaunit_shop,
    get_deltaunit_from_ordered_dict,
)
from dataclasses import dataclass
from os.path import exists as os_path_exists


@dataclass
class GiftUnit:
    face_name: FaceName = None
    fiscal_title: FiscalTitle = None
    owner_name: OwnerName = None
    _gift_id: int = None
    _deltaunit: DeltaUnit = None
    _delta_start: int = None
    _gifts_dir: str = None
    _atoms_dir: str = None
    event_int: int = None

    def set_face(self, x_face_name: FaceName):
        self.face_name = x_face_name

    def del_face(self):
        self.face_name = None

    def set_deltaunit(self, x_deltaunit: DeltaUnit):
        self._deltaunit = x_deltaunit

    def del_deltaunit(self):
        self._deltaunit = deltaunit_shop()

    def set_delta_start(self, x_delta_start: int):
        self._delta_start = get_init_gift_id_if_None(x_delta_start)

    def atomunit_exists(self, x_atomunit: AtomUnit):
        return self._deltaunit.atomunit_exists(x_atomunit)

    def get_step_dict(self) -> dict[str, any]:
        return {
            "face_name": self.face_name,
            "fiscal_title": self.fiscal_title,
            "owner_name": self.owner_name,
            "event_int": self.event_int,
            "delta": self._deltaunit.get_ordered_atomunits(self._delta_start),
        }

    def get_serializable_dict(self) -> dict[str, dict]:
        total_dict = self.get_step_dict()
        total_dict["delta"] = self._deltaunit.get_ordered_dict()
        return total_dict

    def get_json(self) -> str:
        return get_json_from_dict(self.get_serializable_dict())

    def get_delta_atom_numbers(self, giftunit_dict: list[str]) -> int:
        delta_dict = giftunit_dict.get("delta")
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

    def _save_atom_file(self, atom_number: int, x_atom: AtomUnit):
        x_filename = self._get_num_filename(atom_number)
        save_file(self._atoms_dir, x_filename, x_atom.get_json())

    def atom_file_exists(self, atom_number: int) -> bool:
        x_filename = self._get_num_filename(atom_number)
        return os_path_exists(create_path(self._atoms_dir, x_filename))

    def _open_atom_file(self, atom_number: int) -> AtomUnit:
        x_json = open_file(self._atoms_dir, self._get_num_filename(atom_number))
        return atomunit_get_from_json(x_json)

    def _save_gift_file(self):
        x_filename = self._get_num_filename(self._gift_id)
        save_file(self._gifts_dir, x_filename, self.get_deltametric_json())

    def gift_file_exists(self) -> bool:
        x_filename = self._get_num_filename(self._gift_id)
        return os_path_exists(create_path(self._gifts_dir, x_filename))

    def _save_atom_files(self):
        step_dict = self.get_step_dict()
        ordered_atomunits = step_dict.get("delta")
        for order_int, atomunit in ordered_atomunits.items():
            self._save_atom_file(order_int, atomunit)

    def save_files(self):
        self._save_gift_file()
        self._save_atom_files()

    def _create_deltaunit_from_atom_files(self, atom_number_list: list) -> DeltaUnit:
        x_deltaunit = deltaunit_shop()
        for atom_number in atom_number_list:
            x_atomunit = self._open_atom_file(atom_number)
            x_deltaunit.set_atomunit(x_atomunit)
        self._deltaunit = x_deltaunit


def giftunit_shop(
    owner_name: OwnerName,
    face_name: FaceName = None,
    fiscal_title: FiscalTitle = None,
    _gift_id: int = None,
    _deltaunit: DeltaUnit = None,
    _delta_start: int = None,
    _gifts_dir: str = None,
    _atoms_dir: str = None,
    event_int: int = None,
) -> GiftUnit:
    _deltaunit = deltaunit_shop() if _deltaunit is None else _deltaunit
    fiscal_title = get_default_fiscal_title() if fiscal_title is None else fiscal_title
    x_giftunit = GiftUnit(
        face_name=face_name,
        owner_name=owner_name,
        fiscal_title=fiscal_title,
        _gift_id=get_init_gift_id_if_None(_gift_id),
        _deltaunit=_deltaunit,
        _gifts_dir=_gifts_dir,
        _atoms_dir=_atoms_dir,
        event_int=event_int,
    )
    x_giftunit.set_delta_start(_delta_start)
    return x_giftunit


def create_giftunit_from_files(
    gifts_dir: str,
    gift_id: str,
    atoms_dir: str,
) -> GiftUnit:
    gift_filename = get_json_filename(gift_id)
    gift_dict = get_dict_from_json(open_file(gifts_dir, gift_filename))
    x_owner_name = gift_dict.get("owner_name")
    x_fiscal_title = gift_dict.get("fiscal_title")
    x_face_name = gift_dict.get("face_name")
    delta_atom_numbers_list = gift_dict.get("delta_atom_numbers")
    x_giftunit = giftunit_shop(
        face_name=x_face_name,
        owner_name=x_owner_name,
        fiscal_title=x_fiscal_title,
        _gift_id=gift_id,
        _atoms_dir=atoms_dir,
    )
    x_giftunit._create_deltaunit_from_atom_files(delta_atom_numbers_list)
    return x_giftunit


def get_giftunit_from_json(x_json: str) -> GiftUnit:
    gift_dict = get_dict_from_json(x_json)
    if gift_dict.get("event_int") is None:
        x_event_int = None
    else:
        x_event_int = int(gift_dict.get("event_int"))
    x_giftunit = giftunit_shop(
        face_name=gift_dict.get("face_name"),
        owner_name=gift_dict.get("owner_name"),
        fiscal_title=gift_dict.get("fiscal_title"),
        _gift_id=gift_dict.get("gift_id"),
        _atoms_dir=gift_dict.get("atoms_dir"),
        event_int=x_event_int,
    )
    x_deltaunit = get_deltaunit_from_ordered_dict(gift_dict.get("delta"))
    x_giftunit.set_deltaunit(x_deltaunit)
    return x_giftunit
