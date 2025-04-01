from src.f00_instrument.dict_toolbox import x_is_json
from src.f01_road.deal import owner_name_str, fisc_title_str
from src.f01_road.jaar_config import init_vow_id, get_vows_folder
from src.f01_road.road import get_default_fisc_title as root_title
from src.f02_bud.acct import acctunit_shop
from src.f02_bud.bud_tool import bud_acctunit_str
from src.f02_bud.bud import budunit_shop
from src.f04_vow.atom import budatom_shop
from src.f04_vow.atom_config import (
    face_name_str,
    event_int_str,
    credit_belief_str,
    debtit_belief_str,
    acct_name_str,
    atom_insert,
    atom_delete,
    atom_update,
)
from src.f04_vow.delta import buddelta_shop
from src.f04_vow.vow import (
    vowUnit,
    vowunit_shop,
    get_init_vow_id_if_None,
    get_vowunit_from_json,
)
from src.f04_vow.examples.example_atoms import get_atom_example_itemunit_sports
from src.f04_vow.examples.example_deltas import get_buddelta_sue_example
from pytest import raises as pytest_raises


def test_get_vows_folder_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_vows_folder() == "vows"


def test_init_vow_id_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert init_vow_id() == 0


def test_get_init_vow_id_if_None_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_init_vow_id_if_None() == init_vow_id()
    assert get_init_vow_id_if_None(None) == init_vow_id()
    assert get_init_vow_id_if_None(1) == 1


def test_vowUnit_exists():
    # ESTABLISH / WHEN
    x_vowunit = vowUnit()

    # THEN
    assert not x_vowunit.face_name
    assert not x_vowunit.fisc_title
    assert not x_vowunit.owner_name
    assert not x_vowunit._vow_id
    assert not x_vowunit._buddelta
    assert not x_vowunit._delta_start
    assert not x_vowunit._vows_dir
    assert not x_vowunit._atoms_dir
    assert not x_vowunit.event_int


def test_vowunit_shop_ReturnsObjEstablishWithEmptyArgs():
    # ESTABLISH
    bob_str = "Bob"

    # WHEN
    bob_vowunit = vowunit_shop(owner_name=bob_str)

    # THEN
    assert not bob_vowunit.face_name
    assert bob_vowunit.fisc_title == root_title()
    assert bob_vowunit.owner_name == bob_str
    assert bob_vowunit._vow_id == 0
    assert bob_vowunit._buddelta == buddelta_shop()
    assert bob_vowunit._delta_start == 0
    assert not bob_vowunit._vows_dir
    assert not bob_vowunit._atoms_dir
    assert not bob_vowunit.event_int


def test_vowunit_shop_ReturnsObjEstablishWithNonEmptyArgs():
    # ESTABLISH
    bob_str = "Bob"
    bob_vow_id = 13
    sue_str = "Sue"
    bob_buddelta = get_buddelta_sue_example()
    bob_delta_start = 6
    bob_vows_dir = "exampletext7"
    bob_atoms_dir = "exampletext9"
    accord45_str = "accord45"
    accord45_e5_event_int = 5

    # WHEN
    bob_vowunit = vowunit_shop(
        face_name=sue_str,
        owner_name=bob_str,
        fisc_title=accord45_str,
        _vow_id=bob_vow_id,
        _buddelta=bob_buddelta,
        _delta_start=bob_delta_start,
        _vows_dir=bob_vows_dir,
        _atoms_dir=bob_atoms_dir,
        event_int=accord45_e5_event_int,
    )

    # THEN
    assert bob_vowunit.face_name == sue_str
    assert bob_vowunit.owner_name == bob_str
    assert bob_vowunit.fisc_title == accord45_str
    assert bob_vowunit._vow_id == bob_vow_id
    assert bob_vowunit._buddelta == bob_buddelta
    assert bob_vowunit._delta_start == bob_delta_start
    assert bob_vowunit._vows_dir == bob_vows_dir
    assert bob_vowunit._atoms_dir == bob_atoms_dir
    assert bob_vowunit.event_int == accord45_e5_event_int


def test_vowunit_shop_ReturnsObjEstablishWithSomeArgs_v1():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"

    # WHEN
    bob_vowunit = vowunit_shop(owner_name=bob_str, face_name=yao_str)

    # THEN
    assert bob_vowunit.owner_name == bob_str
    assert bob_vowunit.face_name == yao_str


def test_vowUnit_set_face_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_vowunit = vowunit_shop(owner_name=bob_str)
    sue_str = "Sue"
    assert bob_vowunit.face_name is None
    assert bob_vowunit.face_name != sue_str

    # WHEN
    bob_vowunit.set_face(sue_str)

    # THEN
    assert bob_vowunit.face_name == sue_str


def test_vowUnit_del_face_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_vowunit = vowunit_shop(owner_name=bob_str)
    yao_str = "Yao"
    bob_vowunit.set_face(yao_str)
    assert bob_vowunit.face_name == yao_str

    # WHEN
    bob_vowunit.del_face()

    # THEN
    assert bob_vowunit.face_name != yao_str
    assert bob_vowunit.face_name is None


def test_vowUnit_set_buddelta_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_vowunit = vowunit_shop(owner_name=bob_str)
    assert bob_vowunit._buddelta == buddelta_shop()

    # WHEN
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(get_atom_example_itemunit_sports())
    bob_vowunit.set_buddelta(x_buddelta)

    # THEN
    assert bob_vowunit._buddelta == x_buddelta


def test_vowUnit_set_delta_start_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_vowunit = vowunit_shop(bob_str)
    assert bob_vowunit._delta_start == 0

    # WHEN
    x_delta_start = 11
    bob_vowunit.set_delta_start(x_delta_start)

    # THEN
    assert bob_vowunit._delta_start == x_delta_start


def test_vowUnit_budatom_exists_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    x_buddelta = buddelta_shop()
    bob_vowunit = vowunit_shop(owner_name=bob_str)
    bob_vowunit.set_buddelta(x_buddelta)

    # WHEN
    sports_budatom = get_atom_example_itemunit_sports()

    # THEN
    assert bob_vowunit.budatom_exists(sports_budatom) is False

    # WHEN
    x_buddelta.set_budatom(sports_budatom)
    bob_vowunit.set_buddelta(x_buddelta)

    # THEN
    assert bob_vowunit.budatom_exists(sports_budatom)


def test_vowUnit_del_buddelta_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    x_buddelta = buddelta_shop()
    x_buddelta.set_budatom(get_atom_example_itemunit_sports())
    bob_vowunit = vowunit_shop(owner_name=bob_str, _buddelta=x_buddelta)
    assert bob_vowunit._buddelta != buddelta_shop()
    assert bob_vowunit._buddelta == x_buddelta

    # WHEN
    bob_vowunit.del_buddelta()

    # THEN
    assert bob_vowunit._buddelta == buddelta_shop()


def test_vowUnit_get_step_dict_ReturnsObj_Simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    accord45_str = "accord45"
    accord45_e5_int = 5
    bob_vowunit = vowunit_shop(
        fisc_title=accord45_str, owner_name=bob_str, event_int=accord45_e5_int
    )
    bob_vowunit.set_face(sue_str)

    # WHEN
    x_dict = bob_vowunit.get_step_dict()

    # THEN
    assert x_dict.get(fisc_title_str()) is not None
    assert x_dict.get(fisc_title_str()) == accord45_str
    assert x_dict.get(owner_name_str()) is not None
    assert x_dict.get(owner_name_str()) == bob_str
    assert x_dict.get(face_name_str()) is not None
    assert x_dict.get(face_name_str()) == sue_str
    assert x_dict.get(event_int_str()) is not None
    assert x_dict.get(event_int_str()) == accord45_e5_int

    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == buddelta_shop().get_ordered_budatoms()
    assert x_dict.get(delta_str) == {}


def test_vowUnit_get_step_dict_ReturnsObj_WithBudDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_buddelta = get_buddelta_sue_example()
    bob_vowunit = vowunit_shop(bob_str, _buddelta=sue_buddelta)

    # WHEN
    x_dict = bob_vowunit.get_step_dict()

    # THEN
    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == sue_buddelta.get_ordered_budatoms()
    sue_budatoms_dict = x_dict.get(delta_str)
    print(f"{len(sue_buddelta.get_sorted_budatoms())=}")
    print(f"{sue_budatoms_dict.keys()=}")
    # print(f"{sue_budatoms_dict.get(0)=}")
    assert sue_budatoms_dict.get(2) is None
    assert sue_budatoms_dict.get(0) is not None
    assert sue_budatoms_dict.get(1) is not None


def test_vowUnit_get_step_dict_ReturnsObj_delta_start():
    # ESTABLISH
    bob_str = "Bob"
    sue_buddelta = get_buddelta_sue_example()
    x_delta_start = 7
    bob_vowunit = vowunit_shop(
        bob_str, _buddelta=sue_buddelta, _delta_start=x_delta_start
    )

    # WHEN
    step_dict = bob_vowunit.get_step_dict()

    # THEN
    delta_str = "delta"
    assert step_dict.get(delta_str) is not None
    assert step_dict.get(delta_str) == sue_buddelta.get_ordered_budatoms(x_delta_start)
    sue_budatoms_dict = step_dict.get(delta_str)
    print(f"{len(sue_buddelta.get_sorted_budatoms())=}")
    print(f"{sue_budatoms_dict.keys()=}")
    # print(f"{sue_budatoms_dict.get(0)=}")
    assert sue_budatoms_dict.get(x_delta_start + 2) is None
    assert sue_budatoms_dict.get(x_delta_start + 0) is not None
    assert sue_budatoms_dict.get(x_delta_start + 1) is not None


def test_vowUnit_get_serializable_dict_ReturnsObj_Simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    accord45_str = "accord45"
    accord45_e5_int = 5
    bob_vowunit = vowunit_shop(
        fisc_title=accord45_str, owner_name=bob_str, event_int=accord45_e5_int
    )
    bob_vowunit.set_face(sue_str)

    # WHEN
    total_dict = bob_vowunit.get_serializable_dict()

    # THEN
    assert total_dict.get(fisc_title_str()) is not None
    assert total_dict.get(fisc_title_str()) == accord45_str
    assert total_dict.get(owner_name_str()) is not None
    assert total_dict.get(owner_name_str()) == bob_str
    assert total_dict.get(face_name_str()) is not None
    assert total_dict.get(face_name_str()) == sue_str
    assert total_dict.get(event_int_str()) is not None
    assert total_dict.get(event_int_str()) == accord45_e5_int
    delta_str = "delta"
    assert total_dict.get(delta_str) == {}


def test_vowUnit_get_serializable_dict_ReturnsObj_WithBudDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_buddelta = get_buddelta_sue_example()
    bob_vowunit = vowunit_shop(bob_str, _buddelta=sue_buddelta)

    # WHEN
    total_dict = bob_vowunit.get_serializable_dict()

    # THEN
    print(f"{total_dict=}")
    delta_str = "delta"
    assert total_dict.get(delta_str) is not None
    assert total_dict.get(delta_str) == sue_buddelta.get_ordered_dict()


def test_vowUnit_get_json_ReturnsObj_WithBudDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_buddelta = get_buddelta_sue_example()
    bob_vowunit = vowunit_shop(bob_str, _buddelta=sue_buddelta)

    # WHEN
    generated_json = bob_vowunit.get_json()

    # THEN
    assert generated_json
    print(f"{generated_json=}")
    expected_json = """{
  "delta": {
    "0": {
      "crud": "DELETE",
      "dimen": "bud_acctunit",
      "jkeys": {
        "acct_name": "Sue"
      },
      "jvalues": {}
    },
    "1": {
      "crud": "UPDATE",
      "dimen": "budunit",
      "jkeys": {},
      "jvalues": {
        "credor_respect": 77
      }
    }
  },
  "event_int": null,
  "face_name": null,
  "fisc_title": "ZZ",
  "owner_name": "Bob"
}"""
    assert generated_json == expected_json


def test_get_vowunit_from_json_ReturnsObj_WithBudDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_buddelta = get_buddelta_sue_example()
    bob_vowunit = vowunit_shop(bob_str, _buddelta=sue_buddelta, event_int=778)

    # WHEN
    generated_bob_vowunit = get_vowunit_from_json(bob_vowunit.get_json())

    # THEN
    assert generated_bob_vowunit
    assert generated_bob_vowunit.face_name == bob_vowunit.face_name
    assert generated_bob_vowunit.event_int == bob_vowunit.event_int
    assert generated_bob_vowunit.fisc_title == bob_vowunit.fisc_title
    assert generated_bob_vowunit._buddelta == bob_vowunit._buddelta
    assert generated_bob_vowunit == bob_vowunit


def test_vowUnit_get_delta_atom_numbers_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    sue_buddelta = get_buddelta_sue_example()
    x_delta_start = 7
    bob_vowunit = vowunit_shop(bob_str)
    bob_vowunit.set_buddelta(sue_buddelta)
    bob_vowunit.set_delta_start(x_delta_start)
    bob_vowunit.set_face(yao_str)
    x_dict = bob_vowunit.get_step_dict()

    # WHEN
    x_delta_atom_numbers = bob_vowunit.get_delta_atom_numbers(x_dict)
    # THEN
    assert x_delta_atom_numbers == [x_delta_start, x_delta_start + 1]


def test_vowUnit_get_deltametric_dict_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    event5_int = 5550
    sue_buddelta = get_buddelta_sue_example()
    x_delta_start = 7
    bob_vowunit = vowunit_shop(bob_str)
    bob_vowunit.set_buddelta(sue_buddelta)
    bob_vowunit.set_delta_start(x_delta_start)
    bob_vowunit.set_face(yao_str)
    bob_vowunit.event_int = event5_int

    # WHEN
    x_dict = bob_vowunit.get_deltametric_dict()

    # THEN
    assert x_dict.get(owner_name_str()) is not None
    assert x_dict.get(owner_name_str()) == bob_str
    assert x_dict.get(face_name_str()) is not None
    assert x_dict.get(face_name_str()) == yao_str
    assert x_dict.get(event_int_str()) is not None
    assert x_dict.get(event_int_str()) == event5_int

    delta_atom_numbers_str = "delta_atom_numbers"
    assert x_dict.get(delta_atom_numbers_str) is not None
    assert x_dict.get(delta_atom_numbers_str) == [7, 8]

    delta_min_str = "delta_min"
    assert x_dict.get(delta_min_str) is None
    delta_max_str = "delta_max"
    assert x_dict.get(delta_max_str) is None


def test_vowUnit_get_deltametric_json_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    sue_buddelta = get_buddelta_sue_example()
    x_delta_start = 7
    bob_vowunit = vowunit_shop(bob_str)
    bob_vowunit.set_buddelta(sue_buddelta)
    bob_vowunit.set_delta_start(x_delta_start)
    bob_vowunit.set_face(sue_str)
    bob_vowunit.set_face(yao_str)

    # WHEN
    delta_json = bob_vowunit.get_deltametric_json()

    # THEN
    assert x_is_json(delta_json)


def test_vowUnit_add_budatom_CorrectlySets_BudUnit_acctunits():
    # ESTABLISH
    bob_str = "Bob"
    bob_vowunit = vowunit_shop(bob_str)
    bob_credit_belief = 55
    bob_debtit_belief = 66
    bob_acctunit = acctunit_shop(bob_str, bob_credit_belief, bob_debtit_belief)
    cw_str = credit_belief_str()
    dw_str = debtit_belief_str()
    print(f"{bob_acctunit.get_dict()=}")
    bob_required_dict = {acct_name_str(): bob_acctunit.get_dict().get(acct_name_str())}
    bob_optional_dict = {cw_str: bob_acctunit.get_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_acctunit.get_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    assert bob_vowunit._buddelta.budatoms == {}

    # WHEN
    bob_vowunit.add_budatom(
        dimen=bud_acctunit_str(),
        crud_str=atom_insert(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    assert len(bob_vowunit._buddelta.budatoms) == 1
    assert (
        bob_vowunit._buddelta.budatoms.get(atom_insert())
        .get(bud_acctunit_str())
        .get(bob_str)
        is not None
    )


def test_vowUnit_get_edited_bud_ReturnsObj_BudUnit_insert_acct():
    # ESTABLISH
    sue_str = "Sue"
    sue_vowunit = vowunit_shop(sue_str)

    before_sue_budunit = budunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_budunit.add_acctunit(yao_str)
    assert before_sue_budunit.acct_exists(yao_str)
    assert before_sue_budunit.acct_exists(zia_str) is False
    dimen = bud_acctunit_str()
    x_budatom = budatom_shop(dimen, atom_insert())
    x_budatom.set_jkey(acct_name_str(), zia_str)
    x_credit_belief = 55
    x_debtit_belief = 66
    x_budatom.set_jvalue("credit_belief", x_credit_belief)
    x_budatom.set_jvalue("debtit_belief", x_debtit_belief)
    sue_vowunit._buddelta.set_budatom(x_budatom)
    print(f"{sue_vowunit._buddelta.budatoms.keys()=}")

    # WHEN
    after_sue_budunit = sue_vowunit.get_edited_bud(before_sue_budunit)

    # THEN
    yao_acctunit = after_sue_budunit.get_acct(yao_str)
    zia_acctunit = after_sue_budunit.get_acct(zia_str)
    assert yao_acctunit is not None
    assert zia_acctunit is not None
    assert zia_acctunit.credit_belief == x_credit_belief
    assert zia_acctunit.debtit_belief == x_debtit_belief


def test_vowUnit_get_edited_bud_RaisesErrorWhenvowAttrsAndBudAttrsAreNotTheSame():
    # ESTABLISH
    yao_str = "Yao"
    xia_str = "Xia"
    accord23_str = "accord23"
    bob_vowunit = vowunit_shop(yao_str, xia_str, fisc_title=accord23_str)
    sue_str = "Sue"
    accord45_str = "accord45"
    before_sue_budunit = budunit_shop(sue_str, fisc_title=accord45_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_vowunit.get_edited_bud(before_sue_budunit)
    assert str(excinfo.value) == "vow bud conflict accord23 != accord45 or Yao != Sue"


def test_vowUnit_is_empty_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_vowunit = vowunit_shop(bob_str)
    bob_credit_belief = 55
    bob_debtit_belief = 66
    bob_acctunit = acctunit_shop(bob_str, bob_credit_belief, bob_debtit_belief)
    cw_str = credit_belief_str()
    dw_str = debtit_belief_str()
    print(f"{bob_acctunit.get_dict()=}")
    bob_required_dict = {acct_name_str(): bob_acctunit.get_dict().get(acct_name_str())}
    bob_optional_dict = {cw_str: bob_acctunit.get_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_acctunit.get_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    assert bob_vowunit._buddelta.budatoms == {}
    assert bob_vowunit.is_empty()

    # WHEN
    bob_vowunit.add_budatom(
        dimen=bud_acctunit_str(),
        crud_str=atom_insert(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    assert len(bob_vowunit._buddelta.budatoms) == 1
    assert bob_vowunit.is_empty() is False

    # WHEN
    bob_vowunit._buddelta.budatoms = {}

    # THEN
    assert bob_vowunit.is_empty()

    # Test for atom_update operation
    bob_vowunit_update = vowunit_shop(bob_str)
    bob_vowunit_update.add_budatom(
        dimen=bud_acctunit_str(),
        crud_str=atom_update(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )
    assert len(bob_vowunit_update._buddelta.budatoms) == 1
    assert bob_vowunit_update.is_empty() is False

    # Test for atom_delete operation
    bob_vowunit_delete = vowunit_shop(bob_str)
    bob_vowunit_delete.add_budatom(
        dimen=bud_acctunit_str(),
        crud_str=atom_delete(),
        jkeys=bob_required_dict,
        jvalues={},
    )
    assert len(bob_vowunit_delete._buddelta.budatoms) == 1
    assert bob_vowunit_delete.is_empty() is False
