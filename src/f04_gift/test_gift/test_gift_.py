from src.f00_instrument.dict_toolbox import x_is_json
from src.f01_road.deal import owner_name_str, fisc_title_str
from src.f01_road.jaar_config import init_gift_id, get_gifts_folder
from src.f01_road.road import get_default_fisc_title as root_title
from src.f02_bud.acct import acctunit_shop
from src.f02_bud.bud_tool import bud_acctunit_str
from src.f02_bud.bud import budunit_shop
from src.f04_gift.atom import atomunit_shop
from src.f04_gift.atom_config import (
    face_name_str,
    event_int_str,
    credit_belief_str,
    debtit_belief_str,
    acct_name_str,
    atom_insert,
    atom_delete,
    atom_update,
)
from src.f04_gift.delta import buddelta_shop
from src.f04_gift.gift import (
    GiftUnit,
    giftunit_shop,
    get_init_gift_id_if_None,
    get_giftunit_from_json,
)
from src.f04_gift.examples.example_atoms import get_atom_example_itemunit_sports
from src.f04_gift.examples.example_deltas import get_buddelta_sue_example
from pytest import raises as pytest_raises


def test_get_gifts_folder_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_gifts_folder() == "gifts"


def test_init_gift_id_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert init_gift_id() == 0


def test_get_init_gift_id_if_None_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_init_gift_id_if_None() == init_gift_id()
    assert get_init_gift_id_if_None(None) == init_gift_id()
    assert get_init_gift_id_if_None(1) == 1


def test_GiftUnit_exists():
    # ESTABLISH / WHEN
    x_giftunit = GiftUnit()

    # THEN
    assert not x_giftunit.face_name
    assert not x_giftunit.fisc_title
    assert not x_giftunit.owner_name
    assert not x_giftunit._gift_id
    assert not x_giftunit._buddelta
    assert not x_giftunit._delta_start
    assert not x_giftunit._gifts_dir
    assert not x_giftunit._atoms_dir
    assert not x_giftunit.event_int


def test_giftunit_shop_ReturnsObjEstablishWithEmptyArgs():
    # ESTABLISH
    bob_str = "Bob"

    # WHEN
    bob_giftunit = giftunit_shop(owner_name=bob_str)

    # THEN
    assert not bob_giftunit.face_name
    assert bob_giftunit.fisc_title == root_title()
    assert bob_giftunit.owner_name == bob_str
    assert bob_giftunit._gift_id == 0
    assert bob_giftunit._buddelta == buddelta_shop()
    assert bob_giftunit._delta_start == 0
    assert not bob_giftunit._gifts_dir
    assert not bob_giftunit._atoms_dir
    assert not bob_giftunit.event_int


def test_giftunit_shop_ReturnsObjEstablishWithNonEmptyArgs():
    # ESTABLISH
    bob_str = "Bob"
    bob_gift_id = 13
    sue_str = "Sue"
    bob_buddelta = get_buddelta_sue_example()
    bob_delta_start = 6
    bob_gifts_dir = "exampletext7"
    bob_atoms_dir = "exampletext9"
    accord45_str = "accord45"
    accord45_e5_event_int = 5

    # WHEN
    bob_giftunit = giftunit_shop(
        face_name=sue_str,
        owner_name=bob_str,
        fisc_title=accord45_str,
        _gift_id=bob_gift_id,
        _buddelta=bob_buddelta,
        _delta_start=bob_delta_start,
        _gifts_dir=bob_gifts_dir,
        _atoms_dir=bob_atoms_dir,
        event_int=accord45_e5_event_int,
    )

    # THEN
    assert bob_giftunit.face_name == sue_str
    assert bob_giftunit.owner_name == bob_str
    assert bob_giftunit.fisc_title == accord45_str
    assert bob_giftunit._gift_id == bob_gift_id
    assert bob_giftunit._buddelta == bob_buddelta
    assert bob_giftunit._delta_start == bob_delta_start
    assert bob_giftunit._gifts_dir == bob_gifts_dir
    assert bob_giftunit._atoms_dir == bob_atoms_dir
    assert bob_giftunit.event_int == accord45_e5_event_int


def test_giftunit_shop_ReturnsObjEstablishWithSomeArgs_v1():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"

    # WHEN
    bob_giftunit = giftunit_shop(owner_name=bob_str, face_name=yao_str)

    # THEN
    assert bob_giftunit.owner_name == bob_str
    assert bob_giftunit.face_name == yao_str


def test_GiftUnit_set_face_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_giftunit = giftunit_shop(owner_name=bob_str)
    sue_str = "Sue"
    assert bob_giftunit.face_name is None
    assert bob_giftunit.face_name != sue_str

    # WHEN
    bob_giftunit.set_face(sue_str)

    # THEN
    assert bob_giftunit.face_name == sue_str


def test_GiftUnit_del_face_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_giftunit = giftunit_shop(owner_name=bob_str)
    yao_str = "Yao"
    bob_giftunit.set_face(yao_str)
    assert bob_giftunit.face_name == yao_str

    # WHEN
    bob_giftunit.del_face()

    # THEN
    assert bob_giftunit.face_name != yao_str
    assert bob_giftunit.face_name is None


def test_GiftUnit_set_buddelta_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_giftunit = giftunit_shop(owner_name=bob_str)
    assert bob_giftunit._buddelta == buddelta_shop()

    # WHEN
    x_buddelta = buddelta_shop()
    x_buddelta.set_atomunit(get_atom_example_itemunit_sports())
    bob_giftunit.set_buddelta(x_buddelta)

    # THEN
    assert bob_giftunit._buddelta == x_buddelta


def test_GiftUnit_set_delta_start_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_giftunit = giftunit_shop(bob_str)
    assert bob_giftunit._delta_start == 0

    # WHEN
    x_delta_start = 11
    bob_giftunit.set_delta_start(x_delta_start)

    # THEN
    assert bob_giftunit._delta_start == x_delta_start


def test_GiftUnit_atomunit_exists_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    x_buddelta = buddelta_shop()
    bob_giftunit = giftunit_shop(owner_name=bob_str)
    bob_giftunit.set_buddelta(x_buddelta)

    # WHEN
    sports_atomunit = get_atom_example_itemunit_sports()

    # THEN
    assert bob_giftunit.atomunit_exists(sports_atomunit) is False

    # WHEN
    x_buddelta.set_atomunit(sports_atomunit)
    bob_giftunit.set_buddelta(x_buddelta)

    # THEN
    assert bob_giftunit.atomunit_exists(sports_atomunit)


def test_GiftUnit_del_buddelta_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    x_buddelta = buddelta_shop()
    x_buddelta.set_atomunit(get_atom_example_itemunit_sports())
    bob_giftunit = giftunit_shop(owner_name=bob_str, _buddelta=x_buddelta)
    assert bob_giftunit._buddelta != buddelta_shop()
    assert bob_giftunit._buddelta == x_buddelta

    # WHEN
    bob_giftunit.del_buddelta()

    # THEN
    assert bob_giftunit._buddelta == buddelta_shop()


def test_GiftUnit_get_step_dict_ReturnsObj_Simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    accord45_str = "accord45"
    accord45_e5_int = 5
    bob_giftunit = giftunit_shop(
        fisc_title=accord45_str, owner_name=bob_str, event_int=accord45_e5_int
    )
    bob_giftunit.set_face(sue_str)

    # WHEN
    x_dict = bob_giftunit.get_step_dict()

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
    assert x_dict.get(delta_str) == buddelta_shop().get_ordered_atomunits()
    assert x_dict.get(delta_str) == {}


def test_GiftUnit_get_step_dict_ReturnsObj_WithBudDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_buddelta = get_buddelta_sue_example()
    bob_giftunit = giftunit_shop(bob_str, _buddelta=sue_buddelta)

    # WHEN
    x_dict = bob_giftunit.get_step_dict()

    # THEN
    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == sue_buddelta.get_ordered_atomunits()
    sue_atomunits_dict = x_dict.get(delta_str)
    print(f"{len(sue_buddelta.get_sorted_atomunits())=}")
    print(f"{sue_atomunits_dict.keys()=}")
    # print(f"{sue_atomunits_dict.get(0)=}")
    assert sue_atomunits_dict.get(2) is None
    assert sue_atomunits_dict.get(0) is not None
    assert sue_atomunits_dict.get(1) is not None


def test_GiftUnit_get_step_dict_ReturnsObj_delta_start():
    # ESTABLISH
    bob_str = "Bob"
    sue_buddelta = get_buddelta_sue_example()
    x_delta_start = 7
    bob_giftunit = giftunit_shop(
        bob_str, _buddelta=sue_buddelta, _delta_start=x_delta_start
    )

    # WHEN
    step_dict = bob_giftunit.get_step_dict()

    # THEN
    delta_str = "delta"
    assert step_dict.get(delta_str) is not None
    assert step_dict.get(delta_str) == sue_buddelta.get_ordered_atomunits(x_delta_start)
    sue_atomunits_dict = step_dict.get(delta_str)
    print(f"{len(sue_buddelta.get_sorted_atomunits())=}")
    print(f"{sue_atomunits_dict.keys()=}")
    # print(f"{sue_atomunits_dict.get(0)=}")
    assert sue_atomunits_dict.get(x_delta_start + 2) is None
    assert sue_atomunits_dict.get(x_delta_start + 0) is not None
    assert sue_atomunits_dict.get(x_delta_start + 1) is not None


def test_GiftUnit_get_serializable_dict_ReturnsObj_Simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    accord45_str = "accord45"
    accord45_e5_int = 5
    bob_giftunit = giftunit_shop(
        fisc_title=accord45_str, owner_name=bob_str, event_int=accord45_e5_int
    )
    bob_giftunit.set_face(sue_str)

    # WHEN
    total_dict = bob_giftunit.get_serializable_dict()

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


def test_GiftUnit_get_serializable_dict_ReturnsObj_WithBudDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_buddelta = get_buddelta_sue_example()
    bob_giftunit = giftunit_shop(bob_str, _buddelta=sue_buddelta)

    # WHEN
    total_dict = bob_giftunit.get_serializable_dict()

    # THEN
    print(f"{total_dict=}")
    delta_str = "delta"
    assert total_dict.get(delta_str) is not None
    assert total_dict.get(delta_str) == sue_buddelta.get_ordered_dict()


def test_GiftUnit_get_json_ReturnsObj_WithBudDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_buddelta = get_buddelta_sue_example()
    bob_giftunit = giftunit_shop(bob_str, _buddelta=sue_buddelta)

    # WHEN
    generated_json = bob_giftunit.get_json()

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


def test_get_giftunit_from_json_ReturnsObj_WithBudDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_buddelta = get_buddelta_sue_example()
    bob_giftunit = giftunit_shop(bob_str, _buddelta=sue_buddelta, event_int=778)

    # WHEN
    generated_bob_giftunit = get_giftunit_from_json(bob_giftunit.get_json())

    # THEN
    assert generated_bob_giftunit
    assert generated_bob_giftunit.face_name == bob_giftunit.face_name
    assert generated_bob_giftunit.event_int == bob_giftunit.event_int
    assert generated_bob_giftunit.fisc_title == bob_giftunit.fisc_title
    assert generated_bob_giftunit._buddelta == bob_giftunit._buddelta
    assert generated_bob_giftunit == bob_giftunit


def test_GiftUnit_get_delta_atom_numbers_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    sue_buddelta = get_buddelta_sue_example()
    x_delta_start = 7
    bob_giftunit = giftunit_shop(bob_str)
    bob_giftunit.set_buddelta(sue_buddelta)
    bob_giftunit.set_delta_start(x_delta_start)
    bob_giftunit.set_face(yao_str)
    x_dict = bob_giftunit.get_step_dict()

    # WHEN
    x_delta_atom_numbers = bob_giftunit.get_delta_atom_numbers(x_dict)
    # THEN
    assert x_delta_atom_numbers == [x_delta_start, x_delta_start + 1]


def test_GiftUnit_get_deltametric_dict_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    event5_int = 5550
    sue_buddelta = get_buddelta_sue_example()
    x_delta_start = 7
    bob_giftunit = giftunit_shop(bob_str)
    bob_giftunit.set_buddelta(sue_buddelta)
    bob_giftunit.set_delta_start(x_delta_start)
    bob_giftunit.set_face(yao_str)
    bob_giftunit.event_int = event5_int

    # WHEN
    x_dict = bob_giftunit.get_deltametric_dict()

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


def test_GiftUnit_get_deltametric_json_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    sue_buddelta = get_buddelta_sue_example()
    x_delta_start = 7
    bob_giftunit = giftunit_shop(bob_str)
    bob_giftunit.set_buddelta(sue_buddelta)
    bob_giftunit.set_delta_start(x_delta_start)
    bob_giftunit.set_face(sue_str)
    bob_giftunit.set_face(yao_str)

    # WHEN
    delta_json = bob_giftunit.get_deltametric_json()

    # THEN
    assert x_is_json(delta_json)


def test_GiftUnit_add_atomunit_CorrectlySets_BudUnit_acctunits():
    # ESTABLISH
    bob_str = "Bob"
    bob_giftunit = giftunit_shop(bob_str)
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
    assert bob_giftunit._buddelta.atomunits == {}

    # WHEN
    bob_giftunit.add_atomunit(
        dimen=bud_acctunit_str(),
        crud_str=atom_insert(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    assert len(bob_giftunit._buddelta.atomunits) == 1
    assert (
        bob_giftunit._buddelta.atomunits.get(atom_insert())
        .get(bud_acctunit_str())
        .get(bob_str)
        is not None
    )


def test_GiftUnit_get_edited_bud_ReturnsObj_BudUnit_insert_acct():
    # ESTABLISH
    sue_str = "Sue"
    sue_giftunit = giftunit_shop(sue_str)

    before_sue_budunit = budunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_budunit.add_acctunit(yao_str)
    assert before_sue_budunit.acct_exists(yao_str)
    assert before_sue_budunit.acct_exists(zia_str) is False
    dimen = bud_acctunit_str()
    x_atomunit = atomunit_shop(dimen, atom_insert())
    x_atomunit.set_jkey(acct_name_str(), zia_str)
    x_credit_belief = 55
    x_debtit_belief = 66
    x_atomunit.set_jvalue("credit_belief", x_credit_belief)
    x_atomunit.set_jvalue("debtit_belief", x_debtit_belief)
    sue_giftunit._buddelta.set_atomunit(x_atomunit)
    print(f"{sue_giftunit._buddelta.atomunits.keys()=}")

    # WHEN
    after_sue_budunit = sue_giftunit.get_edited_bud(before_sue_budunit)

    # THEN
    yao_acctunit = after_sue_budunit.get_acct(yao_str)
    zia_acctunit = after_sue_budunit.get_acct(zia_str)
    assert yao_acctunit is not None
    assert zia_acctunit is not None
    assert zia_acctunit.credit_belief == x_credit_belief
    assert zia_acctunit.debtit_belief == x_debtit_belief


def test_GiftUnit_get_edited_bud_RaisesErrorWhenGiftAttrsAndBudAttrsAreNotTheSame():
    # ESTABLISH
    yao_str = "Yao"
    xia_str = "Xia"
    accord23_str = "accord23"
    bob_giftunit = giftunit_shop(yao_str, xia_str, fisc_title=accord23_str)
    sue_str = "Sue"
    accord45_str = "accord45"
    before_sue_budunit = budunit_shop(sue_str, fisc_title=accord45_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_giftunit.get_edited_bud(before_sue_budunit)
    assert str(excinfo.value) == "gift bud conflict accord23 != accord45 or Yao != Sue"


def test_GiftUnit_is_empty_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_giftunit = giftunit_shop(bob_str)
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
    assert bob_giftunit._buddelta.atomunits == {}
    assert bob_giftunit.is_empty()

    # WHEN
    bob_giftunit.add_atomunit(
        dimen=bud_acctunit_str(),
        crud_str=atom_insert(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    assert len(bob_giftunit._buddelta.atomunits) == 1
    assert bob_giftunit.is_empty() is False

    # WHEN
    bob_giftunit._buddelta.atomunits = {}

    # THEN
    assert bob_giftunit.is_empty()

    # Test for atom_update operation
    bob_giftunit_update = giftunit_shop(bob_str)
    bob_giftunit_update.add_atomunit(
        dimen=bud_acctunit_str(),
        crud_str=atom_update(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )
    assert len(bob_giftunit_update._buddelta.atomunits) == 1
    assert bob_giftunit_update.is_empty() is False

    # Test for atom_delete operation
    bob_giftunit_delete = giftunit_shop(bob_str)
    bob_giftunit_delete.add_atomunit(
        dimen=bud_acctunit_str(),
        crud_str=atom_delete(),
        jkeys=bob_required_dict,
        jvalues={},
    )
    assert len(bob_giftunit_delete._buddelta.atomunits) == 1
    assert bob_giftunit_delete.is_empty() is False
