from src.a01_rope_logic.term import GroupTitle
from src.a03_group_logic._ref.a03_terms import party_title_str, solo_str
from src.a03_group_logic.labor import (
    laborunit_get_from_dict,
    laborunit_shop,
    partyunit_get_from_dict,
    partyunit_shop,
)


def test_PartyUnit_to_dict_ReturnsObj_Scenario0_solo_IsTrue():
    # ESTABLISH
    bob_str = "Bob"
    bob_solo_bool = True
    x_partyunit = partyunit_shop(bob_str, solo=bob_solo_bool)

    # WHEN
    party_dict = x_partyunit.to_dict()

    # THEN
    assert party_dict
    assert party_dict.get(party_title_str()) == bob_str
    assert party_dict.get(solo_str()) == bob_solo_bool
    assert set(party_dict.keys()) == {party_title_str(), solo_str()}


def test_PartyUnit_to_dict_ReturnsObj_Scenario1_solo_IsFalse():
    # ESTABLISH
    bob_str = "Bob"
    x_partyunit = partyunit_shop(bob_str, solo=False)

    # WHEN
    party_dict = x_partyunit.to_dict()

    # THEN
    assert party_dict
    assert party_dict.get(party_title_str()) == bob_str
    assert set(party_dict.keys()) == {party_title_str()}


def test_partyunit_get_from_dict_ReturnsObj_Scenario0_solo_KeyExists():
    # ESTABLISH
    bob_str = "Bob"
    bob_solo_bool = True
    expected_bob_partyunit = partyunit_shop(bob_str, solo=bob_solo_bool)
    bob_party_dict = expected_bob_partyunit.to_dict()

    # WHEN
    gen_bob_party = partyunit_get_from_dict(bob_party_dict)

    # THEN
    assert gen_bob_party == expected_bob_partyunit


def test_partyunit_get_from_dict_ReturnsObj_Scenario1_solo_KeyDoesNotExist():
    # ESTABLISH
    bob_str = "Bob"
    bob_solo_bool = False
    expected_bob_partyunit = partyunit_shop(bob_str, solo=bob_solo_bool)
    bob_party_dict = expected_bob_partyunit.to_dict()
    assert set(bob_party_dict.keys()) == {party_title_str()}

    # WHEN
    gen_bob_party = partyunit_get_from_dict(bob_party_dict)

    # THEN
    assert gen_bob_party.solo == False
    assert gen_bob_party == expected_bob_partyunit


def test_LaborUnit_to_dict_ReturnsDictWithSingle_partyunit():
    # ESTABLISH
    bob_party_title = GroupTitle("Bob")
    bob_partyunit = partyunit_shop(bob_party_title)
    x_partys = {bob_party_title: bob_partyunit}
    x_laborunit = laborunit_shop(_partys=x_partys)

    # WHEN
    obj_dict = x_laborunit.to_dict()

    # THEN
    assert obj_dict is not None
    example_dict = {"_partys": {bob_party_title: bob_partyunit.to_dict()}}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_laborunit_get_from_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    xio_str = "Xio"
    run_str = ";runners"
    expected_laborunit = laborunit_shop()
    expected_laborunit.add_party(run_str, True)
    expected_laborunit.add_party(xio_str, False)
    run_partyunit = expected_laborunit.get_partyunit(run_str)
    xio_partyunit = expected_laborunit.get_partyunit(xio_str)
    src_laborunit_dict = {
        "_partys": {
            run_str: run_partyunit.to_dict(),
            xio_str: xio_partyunit.to_dict(),
        }
    }

    # WHEN
    gen_laborunit = laborunit_get_from_dict(src_laborunit_dict)

    # THEN
    assert gen_laborunit == expected_laborunit
