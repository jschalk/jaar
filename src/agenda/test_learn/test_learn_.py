from src.agenda.party import partyunit_shop
from src.agenda.learn import (
    LearnUnit,
    learnunit_shop,
    grainunit_shop,
    grain_update,
    grain_insert,
    grain_delete,
)
from src.agenda.examples.example_learns import (
    get_sue_personroad,
    get_sue_learnunit_example1,
)
from pytest import raises as pytest_raises


def test_LearnUnit_exists():
    # GIVEN / WHEN
    x_learnunit = LearnUnit()

    # THEN
    assert x_learnunit.agenda_road is None
    assert x_learnunit.grainunits is None


def test_learnunit_shop_ReturnsCorrectObj():
    # GIVEN
    sue_road = get_sue_personroad()

    # WHEN
    sue_learnunit = learnunit_shop(sue_road)

    # THEN
    assert sue_learnunit.agenda_road == sue_road
    assert sue_learnunit.grainunits == {}


def test_LearnUnit_set_grainunit_CorrectlySets_AgendaUnitSimpleAttrs():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_learnunit = learnunit_shop(sue_road)
    attribute_value = 55
    category = "AgendaUnit_weight"
    required_args = {category: attribute_value}
    agenda_weight_grainunit = grainunit_shop(
        category, grain_update(), required_args=required_args
    )
    assert sue_learnunit.grainunits == {}
    assert agenda_weight_grainunit.grain_order is None

    # WHEN
    sue_learnunit.set_grainunit(agenda_weight_grainunit)

    # THEN
    assert len(sue_learnunit.grainunits) == 1
    x_update_dict = sue_learnunit.grainunits.get(grain_update())
    # print(f"{x_update_dict=}")
    x_category_grainunit = x_update_dict.get(category)
    print(f"{x_category_grainunit=}")
    assert x_category_grainunit == agenda_weight_grainunit
    assert agenda_weight_grainunit.grain_order != None


def test_LearnUnit_set_grainunit_RaisesErrorWhen_is_valid_IsFalse():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_learnunit = learnunit_shop(sue_road)
    x_category = "AgendaUnit_weight"
    agenda_weight_grainunit = grainunit_shop(x_category, grain_update())

    # WHEN
    with pytest_raises(Exception) as excinfo:
        sue_learnunit.set_grainunit(agenda_weight_grainunit)
    assert (
        str(excinfo.value)
        == f"""'{x_category}' UPDATE GrainUnit is invalid
x_grainunit.is_locator_valid()=True
x_grainunit.is_required_args_valid()=False
x_grainunit.is_optional_args_valid()=True"""
    )


def test_LearnUnit_get_grain_ReturnsCorrectObj():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_learnunit = learnunit_shop(sue_road)
    AgendaUnit_weight_value = 55
    AgendaUnit_weight_text = "AgendaUnit_weight"
    AgendaUnit_weight_grainunit = grainunit_shop(AgendaUnit_weight_text, grain_update())
    AgendaUnit_weight_grainunit.set_required_arg(
        x_key=AgendaUnit_weight_text, x_value=AgendaUnit_weight_value
    )
    sue_learnunit.set_grainunit(AgendaUnit_weight_grainunit)

    # WHEN
    gen_grainunit = sue_learnunit.get_grainunit(
        grain_update(), category=AgendaUnit_weight_text, locator_values=[]
    )

    # THEN
    assert gen_grainunit == AgendaUnit_weight_grainunit


def test_LearnUnit_add_grainunit_CorrectlySets_AgendaUnitSimpleAttrs():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_learnunit = learnunit_shop(sue_road)
    assert sue_learnunit.grainunits == {}

    # WHEN
    AgendaUnit_weight_value = 55
    AgendaUnit_weight_text = "AgendaUnit_weight"
    required_args = {AgendaUnit_weight_text: AgendaUnit_weight_value}
    sue_learnunit.add_grainunit(
        AgendaUnit_weight_text, grain_update(), None, required_args
    )

    # THEN
    assert len(sue_learnunit.grainunits) == 1
    x_update_dict = sue_learnunit.grainunits.get(grain_update())
    x_grainunit = x_update_dict.get(AgendaUnit_weight_text)
    assert x_grainunit != None
    assert x_grainunit.category == AgendaUnit_weight_text


def test_LearnUnit_add_grainunit_CorrectlySets_AgendaUnit_partyunits():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_learnunit = learnunit_shop(sue_road)
    assert sue_learnunit.grainunits == {}

    # WHEN
    party_id_text = "party_id"
    bob_text = "Bob"
    bob_locator_dict = {party_id_text: bob_text}
    bob_creditor_weight = 55
    bob_debtor_weight = 66
    bob_partyunit = partyunit_shop(
        bob_text,
        bob_creditor_weight,
        bob_debtor_weight,
        depotlink_type="assignment",
    )
    party_id_text = "party_id"
    cw_text = "creditor_weight"
    dw_text = "debtor_weight"
    print(f"{bob_partyunit.get_dict()=}")
    bob_required_dict = {party_id_text: bob_partyunit.get_dict().get(party_id_text)}
    bob_optional_dict = {cw_text: bob_partyunit.get_dict().get(cw_text)}
    bob_optional_dict[dw_text] = bob_partyunit.get_dict().get(dw_text)
    print(f"{bob_required_dict=}")
    partyunit_text = "partyunit"
    sue_learnunit.add_grainunit(
        category=partyunit_text,
        crud_text=grain_insert(),
        locator=bob_locator_dict,
        required_args=bob_required_dict,
        optional_args=bob_optional_dict,
    )
    # THEN
    assert len(sue_learnunit.grainunits) == 1
    bob_locator_key = f"{partyunit_text} {bob_text}"
    assert (
        sue_learnunit.grainunits.get(grain_insert()).get(partyunit_text).get(bob_text)
        != None
    )


def test_LearnUnit_add_grainunit_CorrectlySets_AgendaUnit_max_tree_traverse():
    # GIVEN
    sue_learnunit = learnunit_shop(get_sue_personroad())
    assert sue_learnunit.grainunits == {}

    # WHEN
    weight_value = 55
    weight_name = "AgendaUnit_weight"
    required_args = {weight_name: weight_value}
    weight_grainunit = grainunit_shop(weight_name, grain_update(), None, required_args)
    sue_learnunit.set_grainunit(weight_grainunit)
    # THEN
    assert len(sue_learnunit.grainunits.get(grain_update()).keys()) == 1
    assert weight_grainunit == sue_learnunit.grainunits.get(grain_update()).get(
        weight_name
    )

    # WHEN
    new2_value = 66
    x_attribute = "_max_tree_traverse"
    required_args = {x_attribute: new2_value}
    x_grainunit = grainunit_shop(x_attribute, grain_update(), None, required_args)
    sue_learnunit.set_grainunit(x_grainunit)
    # THEN
    print(f"{sue_learnunit.grainunits.keys()=}")
    print(f"{sue_learnunit.grainunits.get(grain_update()).keys()=}")
    # print(f"{get_all_nondictionary_objs(sue_learnunit.grainunits).get(grain_update())=}")
    assert len(sue_learnunit.grainunits.get(grain_update()).keys()) == 2
    assert x_grainunit == sue_learnunit.grainunits.get(grain_update()).get(x_attribute)

    # WHEN
    new3_value = 77
    x_attribute = "_party_creditor_pool"
    required_args = {x_attribute: new3_value}
    x_grainunit = grainunit_shop(x_attribute, grain_update(), None, required_args)
    sue_learnunit.set_grainunit(x_grainunit)
    # THEN
    assert len(sue_learnunit.grainunits.get(grain_update()).keys()) == 3
    assert x_grainunit == sue_learnunit.grainunits.get(grain_update()).get(x_attribute)

    # WHEN
    new4_value = 88
    x_attribute = "_party_debtor_pool"
    required_args = {x_attribute: new4_value}
    x_grainunit = grainunit_shop(x_attribute, grain_update(), None, required_args)
    sue_learnunit.set_grainunit(x_grainunit)
    # THEN
    assert len(sue_learnunit.grainunits.get(grain_update()).keys()) == 4
    assert x_grainunit == sue_learnunit.grainunits.get(grain_update()).get(x_attribute)

    # WHEN
    new5_value = "override"
    x_attribute = "_meld_strategy"
    required_args = {x_attribute: new5_value}
    x_grainunit = grainunit_shop(x_attribute, grain_update(), None, required_args)
    sue_learnunit.set_grainunit(x_grainunit)
    # THEN
    assert len(sue_learnunit.grainunits.get(grain_update()).keys()) == 5
    assert x_grainunit == sue_learnunit.grainunits.get(grain_update()).get(x_attribute)


def test_LearnUnit_get_grain_order_grainunit_dict_ReturnsCorrectObj():
    # GIVEN
    sue_learnunit = get_sue_learnunit_example1()
    assert len(sue_learnunit.grainunits.get(grain_update()).keys()) == 5
    assert sue_learnunit.grainunits.get(grain_insert()) is None
    assert len(sue_learnunit.grainunits.get(grain_delete()).keys()) == 1

    # WHEN
    sue_grain_order_dict = sue_learnunit.get_grain_order_grainunit_dict()

    # THEN
    assert len(sue_grain_order_dict) == 2
    print(f"{sue_grain_order_dict.keys()=}")
    print(f"{sue_grain_order_dict.get(grain_update())=}")
    assert len(sue_grain_order_dict.get(grain_update())) == 5
    assert len(sue_grain_order_dict.get(grain_delete())) == 1