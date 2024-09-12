from src._instrument.file import save_file, open_file, create_file_path
from src._instrument.python_tool import get_json_from_dict, get_dict_from_json
from src._road.jaar_config import get_init_gift_id_if_None, get_json_filename
from src._road.road import OwnerID, FiscalID, get_default_fiscal_id_roadnode
from src.gift.atom_config import fiscal_id_str, owner_id_str
from src.gift.atom import AtomUnit, get_from_json as atomunit_get_from_json
from src.gift.change import ChangeUnit, changeunit_shop
from dataclasses import dataclass
from os.path import exists as os_path_exists


@dataclass
class GiftUnit:
    fiscal_id: FiscalID = None
    owner_id: OwnerID = None
    _gift_id: int = None
    _face_id: OwnerID = None
    _changeunit: ChangeUnit = None
    _change_start: int = None
    _gifts_dir: str = None
    _atoms_dir: str = None

    def set_face(self, x_face_id: OwnerID):
        self._face_id = x_face_id

    def del_face(self):
        self._face_id = None

    def set_changeunit(self, x_changeunit: ChangeUnit):
        self._changeunit = x_changeunit

    def del_changeunit(self):
        self._changeunit = changeunit_shop()

    def set_change_start(self, x_change_start: int):
        self._change_start = get_init_gift_id_if_None(x_change_start)

    def atomunit_exists(self, x_atomunit: AtomUnit):
        return self._changeunit.atomunit_exists(x_atomunit)

    def get_step_dict(self) -> dict[str, any]:
        return {
            fiscal_id_str(): self.fiscal_id,
            owner_id_str(): self.owner_id,
            "face_id": self._face_id,
            "change": self._changeunit.get_ordered_atomunits(self._change_start),
        }

    def get_change_atom_numbers(self, giftunit_dict: list[str]) -> int:
        change_dict = giftunit_dict.get("change")
        return list(change_dict.keys())

    def get_changemetric_dict(self) -> dict:
        x_dict = self.get_step_dict()
        return {
            owner_id_str(): x_dict.get(owner_id_str()),
            "face_id": x_dict.get("face_id"),
            "change_atom_numbers": self.get_change_atom_numbers(x_dict),
        }

    def get_changemetric_json(self) -> str:
        return get_json_from_dict(self.get_changemetric_dict())

    def _get_num_filename(self, x_number: int) -> str:
        return get_json_filename(x_number)

    def _save_atom_file(self, atom_number: int, x_atom: AtomUnit):
        x_filename = self._get_num_filename(atom_number)
        save_file(self._atoms_dir, x_filename, x_atom.get_json())

    def atom_file_exists(self, atom_number: int) -> bool:
        x_filename = self._get_num_filename(atom_number)
        return os_path_exists(create_file_path(self._atoms_dir, x_filename))

    def _open_atom_file(self, atom_number: int) -> AtomUnit:
        x_json = open_file(self._atoms_dir, self._get_num_filename(atom_number))
        return atomunit_get_from_json(x_json)

    def _save_gift_file(self):
        x_filename = self._get_num_filename(self._gift_id)
        save_file(self._gifts_dir, x_filename, self.get_changemetric_json())

    def gift_file_exists(self) -> bool:
        x_filename = self._get_num_filename(self._gift_id)
        return os_path_exists(create_file_path(self._gifts_dir, x_filename))

    def _save_atom_files(self):
        step_dict = self.get_step_dict()
        ordered_atomunits = step_dict.get("change")
        for order_int, atomunit in ordered_atomunits.items():
            self._save_atom_file(order_int, atomunit)

    def save_files(self):
        self._save_gift_file()
        self._save_atom_files()

    def _create_changeunit_from_atom_files(self, atom_number_list: list) -> ChangeUnit:
        x_changeunit = changeunit_shop()
        for atom_number in atom_number_list:
            x_atomunit = self._open_atom_file(atom_number)
            x_changeunit.set_atomunit(x_atomunit)
        self._changeunit = x_changeunit


def giftunit_shop(
    owner_id: OwnerID,
    fiscal_id: FiscalID = None,
    _gift_id: int = None,
    _face_id: OwnerID = None,
    _changeunit: ChangeUnit = None,
    _change_start: int = None,
    _gifts_dir: str = None,
    _atoms_dir: str = None,
):
    _changeunit = changeunit_shop() if _changeunit is None else _changeunit
    fiscal_id = get_default_fiscal_id_roadnode() if fiscal_id is None else fiscal_id
    x_giftunit = GiftUnit(
        fiscal_id=fiscal_id,
        owner_id=owner_id,
        _gift_id=get_init_gift_id_if_None(_gift_id),
        _face_id=_face_id,
        _changeunit=_changeunit,
        _gifts_dir=_gifts_dir,
        _atoms_dir=_atoms_dir,
    )
    x_giftunit.set_change_start(_change_start)
    return x_giftunit


def create_giftunit_from_files(
    gifts_dir: str,
    gift_id: str,
    atoms_dir: str,
) -> GiftUnit:
    gift_filename = get_json_filename(gift_id)
    gift_dict = get_dict_from_json(open_file(gifts_dir, gift_filename))
    x_owner_id = gift_dict.get(owner_id_str())
    x_fiscal_id = gift_dict.get(fiscal_id_str())
    x_face_id = gift_dict.get("face_id")
    change_atom_numbers_list = gift_dict.get("change_atom_numbers")
    x_giftunit = giftunit_shop(
        owner_id=x_owner_id,
        fiscal_id=x_fiscal_id,
        _gift_id=gift_id,
        _face_id=x_face_id,
        _atoms_dir=atoms_dir,
    )
    x_giftunit._create_changeunit_from_atom_files(change_atom_numbers_list)
    return x_giftunit
