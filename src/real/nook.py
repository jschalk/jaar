from src._instrument.file import (
    save_file,
    open_file,
    set_dir,
    delete_dir,
    dir_files,
    get_integer_filenames,
)
from src._road.finance import default_planck_if_none
from src._road.road import (
    default_road_delimiter_if_none,
    PersonID,
    RealID,
    validate_roadnode,
    RoadUnit,
)
from src.agenda.group import GroupID
from src.agenda.agenda import (
    AgendaUnit,
    agendaunit_shop,
    get_from_json as agendaunit_get_from_json,
    duty_str,
    work_str,
)
from src.agenda.atom import (
    AgendaAtom,
    get_from_json as agendaatom_get_from_json,
    change_agenda_with_agendaatom,
)
from src.agenda.pledge import create_pledge
from src.econ.econ import EconUnit
from src.real.gift import (
    GiftUnit,
    giftunit_shop,
    get_json_filename as giftunit_get_json_filename,
    create_giftunit_from_files,
    init_gift_id,
    get_init_gift_id_if_None,
    get_gifts_folder,
)
from src.real.examples.real_env_kit import get_test_reals_dir, get_test_real_id
from dataclasses import dataclass
from os.path import exists as os_path_exists
from copy import deepcopy as copy_deepcopy


class Invalid_duty_Exception(Exception):
    pass


class Invalid_work_Exception(Exception):
    pass


class SaveGiftFileException(Exception):
    pass


class GiftFileMissingException(Exception):
    pass


@dataclass
class NookUnit:
    person_id: PersonID = None
    real_dir: str = None
    reals_dir: str = None
    real_id: str = None
    persons_dir: str = None
    person_dir: str = None
    _econs_dir: str = None
    _atoms_dir: str = None
    _gifts_dir: str = None
    _duty_obj: AgendaUnit = None
    _duty_file_name: str = None
    _duty_path: str = None
    _work_obj: AgendaUnit = None
    _work_file_name: str = None
    _work_path: str = None
    _econ_objs: dict[RoadUnit:EconUnit] = None
    _road_delimiter: str = None
    _planck: float = None


def nookunit_shop(
    x_reals_dir: str,
    x_real_id: RealID,
    x_person_id: PersonID,
    x_road_delimiter: str = None,
    x_planck: float = None,
) -> NookUnit:
    x_planck = default_planck_if_none(x_planck)
    if x_reals_dir is None:
        x_reals_dir = get_test_reals_dir()
    if x_real_id is None:
        x_real_id = get_test_real_id()
    x_road_delimiter = default_road_delimiter_if_none(x_road_delimiter)
    x_real_dir = f"{x_reals_dir}/{x_real_id}"
    x_persons_dir = f"{x_real_dir}/persons"
    x_person_id = validate_roadnode(x_person_id, x_road_delimiter)
    x_person_dir = f"{x_persons_dir}/{x_person_id}"
    x_econs_dir = f"{x_person_dir}/econs"
    x_atoms_dir = f"{x_person_dir}/atoms"
    x_gifts_dir = f"{x_person_dir}/{get_gifts_folder()}"
    x_duty_file_name = f"{duty_str()}.json"
    x_duty_path = f"{x_person_dir}/{x_duty_file_name}"
    x_work_file_name = f"{work_str()}.json"
    x_work_path = f"{x_person_dir}/{x_work_file_name}"

    return NookUnit(
        person_id=x_person_id,
        real_id=x_real_id,
        real_dir=x_real_dir,
        reals_dir=x_reals_dir,
        persons_dir=x_persons_dir,
        person_dir=x_person_dir,
        _econs_dir=x_econs_dir,
        _atoms_dir=x_atoms_dir,
        _gifts_dir=x_gifts_dir,
        _duty_file_name=x_duty_file_name,
        _duty_path=x_duty_path,
        _work_file_name=x_work_file_name,
        _work_path=x_work_path,
        _road_delimiter=x_road_delimiter,
        _planck=x_planck,
    )


def duty_file_exists(nookunit: NookUnit) -> bool:
    return os_path_exists(nookunit._duty_path)


def work_file_exists(nookunit: NookUnit) -> bool:
    return os_path_exists(nookunit._work_path)


def nookunit_save_atom_file(x_nookunit: NookUnit, x_atom: AgendaAtom):
    x_filename = _get_next_atom_file_number(x_nookunit)
    return _save_valid_atom_file(x_nookunit, x_atom, x_filename)


def _save_valid_atom_file(x_nookunit: NookUnit, x_atom: AgendaAtom, file_number: int):
    save_file(x_nookunit._atoms_dir, f"{file_number}.json", x_atom.get_json())
    return file_number


def nookunit_atom_file_exists(x_nookunit, filename: int) -> bool:
    return os_path_exists(f"{x_nookunit._atoms_dir}/{filename}.json")


def _delete_atom_file(x_nookunit: NookUnit, filename: int):
    delete_dir(f"{x_nookunit._atoms_dir}/{filename}.json")


def _get_agenda_from_atom_files(x_nookunit: NookUnit) -> AgendaUnit:
    x_agenda = agendaunit_shop(x_nookunit.person_id, x_nookunit.real_id)
    x_atom_files = dir_files(x_nookunit._atoms_dir, delete_extensions=True)
    sorted_atom_filenames = sorted(list(x_atom_files.keys()))

    for x_atom_filename in sorted_atom_filenames:
        x_file_text = x_atom_files.get(x_atom_filename)
        x_atom = agendaatom_get_from_json(x_file_text)
        change_agenda_with_agendaatom(x_agenda, x_atom)
    return x_agenda


def _get_max_atom_file_number(x_nookunit: NookUnit) -> int:
    if not os_path_exists(x_nookunit._atoms_dir):
        return None
    atom_files_dict = dir_files(x_nookunit._atoms_dir, True, include_files=True)
    atom_filenames = atom_files_dict.keys()
    atom_file_numbers = {int(atom_filename) for atom_filename in atom_filenames}
    return max(atom_file_numbers, default=None)


def _get_next_atom_file_number(x_nookunit: NookUnit) -> str:
    max_file_number = _get_max_atom_file_number(x_nookunit)
    return 0 if max_file_number is None else max_file_number + 1


def giftunit_file_exists(x_nookunit: NookUnit, gift_id: int) -> bool:
    gift_filename = giftunit_get_json_filename(gift_id)
    return os_path_exists(f"{x_nookunit._gifts_dir}/{gift_filename}")


def initialize_work_file(x_nookunit):
    if work_file_exists(x_nookunit) == False:
        default_work_agenda = agendaunit_shop(
            x_nookunit.person_id,
            x_nookunit.real_id,
            x_nookunit._road_delimiter,
            x_nookunit._planck,
        )
        _save_work_file(x_nookunit, default_work_agenda)


def _save_work_file(x_nookunit: NookUnit, x_agenda: AgendaUnit, replace: bool = True):
    if x_agenda._owner_id != x_nookunit.person_id:
        raise Invalid_work_Exception(
            f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{x_nookunit.person_id}''s work agenda."
        )
    if replace in {True, False}:
        save_file(
            dest_dir=x_nookunit.person_dir,
            file_name=x_nookunit._work_file_name,
            file_text=x_agenda.get_json(),
            replace=replace,
        )


def _get_empty_agenda(x_nookunit: NookUnit) -> AgendaUnit:
    empty_agenda = agendaunit_shop(x_nookunit.person_id, x_nookunit.real_id)
    empty_agenda._last_gift_id = init_gift_id()
    return empty_agenda


def save_duty_file(x_nookunit: NookUnit, x_agenda: AgendaUnit, replace: bool = True):
    if x_agenda._owner_id != x_nookunit.person_id:
        raise Invalid_duty_Exception(
            f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{x_nookunit.person_id}''s duty agenda."
        )
    if replace in {True, False}:
        save_file(
            dest_dir=x_nookunit.person_dir,
            file_name=x_nookunit._duty_file_name,
            file_text=x_agenda.get_json(),
            replace=replace,
        )


def get_duty_file_agenda(x_nookunit: NookUnit) -> AgendaUnit:
    duty_json = open_file(
        dest_dir=x_nookunit.person_dir, file_name=x_nookunit._duty_file_name
    )
    return agendaunit_get_from_json(duty_json)


def giftunit_file_exists(x_nookunit: NookUnit, gift_id: int) -> bool:
    gift_filename = giftunit_get_json_filename(gift_id)
    return os_path_exists(f"{x_nookunit._gifts_dir}/{gift_filename}")


def get_max_gift_file_number(x_nookunit: NookUnit) -> int:
    if not os_path_exists(x_nookunit._gifts_dir):
        return None
    gift_filenames = dir_files(x_nookunit._gifts_dir, True, include_files=True).keys()
    gift_file_numbers = {int(gift_filename) for gift_filename in gift_filenames}
    return max(gift_file_numbers, default=None)


def _get_next_gift_file_number(x_nookunit: NookUnit) -> int:
    max_file_number = get_max_gift_file_number(x_nookunit)
    init_gift_id = get_init_gift_id_if_None()
    return init_gift_id if max_file_number is None else max_file_number + 1


def _create_initial_gift_from_duty(x_nookunit: NookUnit):
    x_giftunit = giftunit_shop(
        _giver=x_nookunit.person_id,
        _gift_id=get_init_gift_id_if_None(),
        _gifts_dir=x_nookunit._gifts_dir,
        _atoms_dir=x_nookunit._atoms_dir,
    )
    x_giftunit._bookunit.add_all_different_agendaatoms(
        before_agenda=_get_empty_agenda(x_nookunit),
        after_agenda=get_duty_file_agenda(x_nookunit),
    )
    x_giftunit.save_files()


def get_giftunit(x_nookunit: NookUnit, file_number: int) -> GiftUnit:
    if giftunit_file_exists(x_nookunit, file_number) == False:
        raise GiftFileMissingException(
            f"GiftUnit file_number {file_number} does not exist."
        )
    x_gifts_dir = x_nookunit._gifts_dir
    x_atoms_dir = x_nookunit._atoms_dir
    return create_giftunit_from_files(x_gifts_dir, file_number, x_atoms_dir)


def _merge_gifts_into_agenda(x_nookunit: NookUnit, x_agenda: AgendaUnit) -> AgendaUnit:
    gift_ints = get_integer_filenames(x_nookunit._gifts_dir, x_agenda._last_gift_id)
    for gift_int in gift_ints:
        x_gift = get_giftunit(x_nookunit, gift_int)
        new_agenda = x_gift._bookunit.get_edited_agenda(x_agenda)

        update_text = "UPDATE"
        x_gift._bookunit.agendaatoms.get(update_text)
    return new_agenda


def _create_duty_from_gifts(x_nookunit):
    save_duty_file(
        x_nookunit,
        _merge_gifts_into_agenda(x_nookunit, _get_empty_agenda(x_nookunit)),
    )


def _create_initial_gift_and_duty_files(x_nookunit: NookUnit):
    default_duty_agenda = agendaunit_shop(
        x_nookunit.person_id,
        x_nookunit.real_id,
        x_nookunit._road_delimiter,
        x_nookunit._planck,
    )
    x_giftunit = giftunit_shop(
        _giver=x_nookunit.person_id,
        _gift_id=get_init_gift_id_if_None(),
        _gifts_dir=x_nookunit._gifts_dir,
        _atoms_dir=x_nookunit._atoms_dir,
    )
    x_giftunit._bookunit.add_all_different_agendaatoms(
        before_agenda=_get_empty_agenda(x_nookunit),
        after_agenda=default_duty_agenda,
    )
    x_giftunit.save_files()
    _create_duty_from_gifts(x_nookunit)


def initialize_gift_and_duty_files(x_nookunit):
    x_duty_file_exists = duty_file_exists(x_nookunit)
    gift_file_exists = giftunit_file_exists(x_nookunit, init_gift_id())
    if x_duty_file_exists == False and gift_file_exists == False:
        _create_initial_gift_and_duty_files(x_nookunit)
    elif x_duty_file_exists == False and gift_file_exists:
        _create_duty_from_gifts(x_nookunit)
    elif x_duty_file_exists and gift_file_exists == False:
        _create_initial_gift_from_duty(x_nookunit)


def nookunit_create_core_dir_and_files(x_nookunit: NookUnit):
    set_dir(x_nookunit.real_dir)
    set_dir(x_nookunit.persons_dir)
    set_dir(x_nookunit.person_dir)
    set_dir(x_nookunit._econs_dir)
    set_dir(x_nookunit._atoms_dir)
    set_dir(x_nookunit._gifts_dir)
    initialize_gift_and_duty_files(x_nookunit)
    initialize_work_file(x_nookunit)


def get_work_file_agenda(x_nookunit: NookUnit) -> AgendaUnit:
    work_json = open_file(
        dest_dir=x_nookunit.person_dir, file_name=x_nookunit._work_file_name
    )
    return agendaunit_get_from_json(work_json)


def append_gifts_to_duty_file(x_nookunit: NookUnit) -> AgendaUnit:
    duty_agenda = get_duty_file_agenda(x_nookunit)
    duty_agenda = _merge_gifts_into_agenda(x_nookunit, duty_agenda)
    save_duty_file(x_nookunit, duty_agenda)
    return get_duty_file_agenda(x_nookunit)


def _get_next_atom_file_number(x_nookunit: NookUnit) -> str:
    max_file_number = _get_max_atom_file_number(x_nookunit)
    return 0 if max_file_number is None else max_file_number + 1


def _get_max_atom_file_number(x_nookunit: NookUnit) -> int:
    if not os_path_exists(x_nookunit._atoms_dir):
        return None
    atom_files_dict = dir_files(x_nookunit._atoms_dir, True, include_files=True)
    atom_filenames = atom_files_dict.keys()
    atom_file_numbers = {int(atom_filename) for atom_filename in atom_filenames}
    return max(atom_file_numbers, default=None)


def validate_giftunit(x_nookunit: NookUnit, x_giftunit: GiftUnit) -> GiftUnit:
    if x_giftunit._atoms_dir != x_nookunit._atoms_dir:
        x_giftunit._atoms_dir = x_nookunit._atoms_dir
    if x_giftunit._gifts_dir != x_nookunit._gifts_dir:
        x_giftunit._gifts_dir = x_nookunit._gifts_dir
    if x_giftunit._gift_id != _get_next_gift_file_number(x_nookunit):
        x_giftunit._gift_id = _get_next_gift_file_number(x_nookunit)
    if x_giftunit._giver != x_nookunit.person_id:
        x_giftunit._giver = x_nookunit.person_id
    if x_giftunit._book_start != _get_next_atom_file_number(x_nookunit):
        x_giftunit._book_start = _get_next_atom_file_number(x_nookunit)
    return x_giftunit


def save_giftunit_file(
    x_nookunit: NookUnit,
    x_gift: GiftUnit,
    replace: bool = True,
    change_invalid_attrs: bool = True,
) -> GiftUnit:
    if change_invalid_attrs:
        x_gift = validate_giftunit(x_nookunit, x_gift)

    if x_gift._atoms_dir != x_nookunit._atoms_dir:
        raise SaveGiftFileException(
            f"GiftUnit file cannot be saved because giftunit._atoms_dir is incorrect: {x_gift._atoms_dir}. It must be {x_nookunit._atoms_dir}."
        )
    if x_gift._gifts_dir != x_nookunit._gifts_dir:
        raise SaveGiftFileException(
            f"GiftUnit file cannot be saved because giftunit._gifts_dir is incorrect: {x_gift._gifts_dir}. It must be {x_nookunit._gifts_dir}."
        )
    if x_gift._giver != x_nookunit.person_id:
        raise SaveGiftFileException(
            f"GiftUnit file cannot be saved because giftunit._giver is incorrect: {x_gift._giver}. It must be {x_nookunit.person_id}."
        )
    gift_filename = giftunit_get_json_filename(x_gift._gift_id)
    if not replace and giftunit_file_exists(x_nookunit, x_gift._gift_id):
        raise SaveGiftFileException(
            f"GiftUnit file {gift_filename} already exists and cannot be saved over."
        )
    x_gift.save_files()
    return x_gift


def _create_new_giftunit(x_nookunit: NookUnit) -> GiftUnit:
    return giftunit_shop(
        _giver=x_nookunit.person_id,
        _gift_id=_get_next_gift_file_number(x_nookunit),
        _atoms_dir=x_nookunit._atoms_dir,
        _gifts_dir=x_nookunit._gifts_dir,
    )


def create_save_giftunit(
    x_nookunit: NookUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    new_giftunit = _create_new_giftunit(x_nookunit)
    new_giftunit._bookunit.add_all_different_agendaatoms(before_agenda, after_agenda)
    save_giftunit_file(x_nookunit, new_giftunit)


def add_pledge_gift(x_nookunit, pledge_road: RoadUnit, x_suffgroup: GroupID = None):
    duty_agenda = get_duty_file_agenda(x_nookunit)
    old_duty_agenda = copy_deepcopy(duty_agenda)
    create_pledge(duty_agenda, pledge_road, x_suffgroup)
    next_giftunit = _create_new_giftunit(x_nookunit)
    next_giftunit._bookunit.add_all_different_agendaatoms(old_duty_agenda, duty_agenda)
    next_giftunit.save_files()
    append_gifts_to_duty_file(x_nookunit)


def del_giftunit_file(x_nookunit: NookUnit, file_number: int):
    delete_dir(f"{x_nookunit._gifts_dir}/{giftunit_get_json_filename(file_number)}")
