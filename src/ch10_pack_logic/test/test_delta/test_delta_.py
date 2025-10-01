from pytest import raises as pytest_raises
from src.ch01_data_toolbox.dict_toolbox import x_is_json
from src.ch02_rope_logic.rope import create_rope, to_rope
from src.ch04_voice_logic.voice import voiceunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch09_belief_atom_logic.atom_main import beliefatom_shop
from src.ch10_pack_logic._ref.ch10_keywords import Ch10Keywords as wx
from src.ch10_pack_logic.delta import (
    BeliefDelta,
    belief_built_from_delta_is_valid,
    beliefdelta_shop,
    get_beliefdelta_from_ordered_dict,
)
from src.ch10_pack_logic.test._util.ch10_examples import get_beliefdelta_example1


def test_BeliefDelta_Exists():
    # ESTABLISH / WHEN
    x_beliefdelta = BeliefDelta()

    # THEN
    assert x_beliefdelta.beliefatoms is None
    assert x_beliefdelta._belief_build_validated is None


def test_beliefdelta_shop_ReturnsObj():
    # ESTABLISH / WHEN
    ex1_beliefdelta = beliefdelta_shop()

    # THEN
    assert ex1_beliefdelta.beliefatoms == {}
    assert ex1_beliefdelta._belief_build_validated is False


def test_BeliefDelta_set_beliefatom_Sets_BeliefUnitSimpleAttrs():
    # ESTABLISH
    ex1_beliefdelta = beliefdelta_shop()
    attribute_value = 55
    dimen = wx.beliefunit
    opt1_arg = "tally"
    jvalues = {opt1_arg: attribute_value}
    jkeys = {}
    belief_star_beliefatom = beliefatom_shop(
        dimen,
        wx.UPDATE,
        jkeys=jkeys,
        jvalues=jvalues,
    )
    assert ex1_beliefdelta.beliefatoms == {}
    assert belief_star_beliefatom.atom_order is None

    # WHEN
    ex1_beliefdelta.set_beliefatom(belief_star_beliefatom)

    # THEN
    assert len(ex1_beliefdelta.beliefatoms) == 1
    x_update_dict = ex1_beliefdelta.beliefatoms.get(wx.UPDATE)
    # print(f"{x_update_dict=}")
    x_dimen_beliefatom = x_update_dict.get(dimen)
    print(f"{x_dimen_beliefatom=}")
    assert x_dimen_beliefatom == belief_star_beliefatom
    assert belief_star_beliefatom.atom_order is not None


def test_BeliefDelta_set_beliefatom_RaisesErrorWhen_is_valid_IsFalse():
    # ESTABLISH
    ex1_beliefdelta = beliefdelta_shop()
    x_dimen = wx.belief_voiceunit
    belief_star_beliefatom = beliefatom_shop(x_dimen, wx.UPDATE)

    # WHEN
    with pytest_raises(Exception) as excinfo:
        ex1_beliefdelta.set_beliefatom(belief_star_beliefatom)

    # THEN
    exception_str = f"""'{x_dimen}' UPDATE BeliefAtom is invalid
                x_beliefatom.is_jkeys_valid()=False
                x_beliefatom.is_jvalues_valid()=True"""
    assert str(excinfo.value) == exception_str


def test_ChangUnit_beliefatom_exists_ReturnsObj_belief_voiceunit_str():
    # ESTABLISH
    bob_str = "Bob"
    x_beliefdelta = beliefdelta_shop()
    bob_beliefatom = beliefatom_shop(wx.belief_voiceunit, wx.INSERT)
    bob_beliefatom.set_arg(wx.voice_name, bob_str)
    assert not x_beliefdelta.beliefatom_exists(bob_beliefatom)

    # WHEN
    x_beliefdelta.set_beliefatom(bob_beliefatom)

    # THEN
    assert x_beliefdelta.beliefatom_exists(bob_beliefatom)


def test_ChangUnit_beliefatom_exists_ReturnsObj_belief_voice_membership_str():
    # ESTABLISH
    bob_str = "Bob"
    iowa_str = ";Iowa"
    x_beliefdelta = beliefdelta_shop()
    bob_iowa_beliefatom = beliefatom_shop(wx.belief_voice_membership, wx.INSERT)
    bob_iowa_beliefatom.set_arg(wx.group_title, iowa_str)
    bob_iowa_beliefatom.set_arg(wx.voice_name, bob_str)
    assert not x_beliefdelta.beliefatom_exists(bob_iowa_beliefatom)

    # WHEN
    x_beliefdelta.set_beliefatom(bob_iowa_beliefatom)

    # THEN
    assert x_beliefdelta.beliefatom_exists(bob_iowa_beliefatom)


def test_BeliefDelta_get_atom_ReturnsObj():
    # ESTABLISH
    ex1_beliefdelta = beliefdelta_shop()
    opt_arg1 = "tally"
    opt_value = 55
    beliefunit_beliefatom = beliefatom_shop(wx.beliefunit, wx.UPDATE)
    beliefunit_beliefatom.set_jvalue(x_key=opt_arg1, x_value=opt_value)
    ex1_beliefdelta.set_beliefatom(beliefunit_beliefatom)

    # WHEN
    gen_beliefatom = ex1_beliefdelta.get_beliefatom(
        wx.UPDATE, dimen=wx.beliefunit, jkeys=[]
    )

    # THEN
    assert gen_beliefatom == beliefunit_beliefatom


def test_BeliefDelta_add_beliefatom_Sets_BeliefUnitSimpleAttrs():
    # ESTABLISH
    ex1_beliefdelta = beliefdelta_shop()
    assert ex1_beliefdelta.beliefatoms == {}

    # WHEN
    op2_arg = "tally"
    op2_value = 55
    jkeys = {}
    jvalues = {op2_arg: op2_value}
    ex1_beliefdelta.add_beliefatom(
        wx.beliefunit,
        wx.UPDATE,
        jkeys,
        jvalues=jvalues,
    )

    # THEN
    assert len(ex1_beliefdelta.beliefatoms) == 1
    x_update_dict = ex1_beliefdelta.beliefatoms.get(wx.UPDATE)
    x_beliefatom = x_update_dict.get(wx.beliefunit)
    assert x_beliefatom is not None
    assert x_beliefatom.dimen == wx.beliefunit


def test_BeliefDelta_add_beliefatom_Sets_BeliefUnit_voiceunits():
    # ESTABLISH
    ex1_beliefdelta = beliefdelta_shop()
    assert ex1_beliefdelta.beliefatoms == {}

    # WHEN
    bob_str = "Bob"
    bob_voice_cred_points = 55
    bob_voice_debt_points = 66
    bob_voiceunit = voiceunit_shop(
        bob_str, bob_voice_cred_points, bob_voice_debt_points
    )
    cw_str = wx.voice_cred_points
    dw_str = wx.voice_debt_points
    print(f"{bob_voiceunit.to_dict()=}")
    bob_required_dict = {wx.voice_name: bob_voiceunit.to_dict().get(wx.voice_name)}
    bob_optional_dict = {cw_str: bob_voiceunit.to_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_voiceunit.to_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    voiceunit_str = wx.belief_voiceunit
    ex1_beliefdelta.add_beliefatom(
        dimen=voiceunit_str,
        crud_str=wx.INSERT,
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )
    # THEN
    assert len(ex1_beliefdelta.beliefatoms) == 1
    assert (
        ex1_beliefdelta.beliefatoms.get(wx.INSERT).get(voiceunit_str).get(bob_str)
        is not None
    )


def test_BeliefDelta_get_crud_beliefatoms_list_ReturnsObj():
    # ESTABLISH
    ex1_beliefdelta = get_beliefdelta_example1()
    assert len(ex1_beliefdelta.beliefatoms.get(wx.UPDATE).keys()) == 1
    assert ex1_beliefdelta.beliefatoms.get(wx.INSERT) is None
    assert len(ex1_beliefdelta.beliefatoms.get(wx.DELETE).keys()) == 1

    # WHEN
    sue_atom_order_dict = ex1_beliefdelta._get_crud_beliefatoms_list()

    # THEN
    assert len(sue_atom_order_dict) == 2
    print(f"{sue_atom_order_dict.keys()=}")
    # print(f"{sue_atom_order_dict.get(wx.UPDATE)=}")
    assert len(sue_atom_order_dict.get(wx.UPDATE)) == 1
    assert len(sue_atom_order_dict.get(wx.DELETE)) == 1
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_BeliefDelta_get_dimen_sorted_beliefatoms_list_ReturnsObj_Scenario0_rope():
    # ESTABLISH
    ex1_beliefdelta = get_beliefdelta_example1()
    update_dict = ex1_beliefdelta.beliefatoms.get(wx.UPDATE)
    assert len(update_dict.keys()) == 1
    print(f"{update_dict.keys()=}")
    assert ex1_beliefdelta.beliefatoms.get(wx.INSERT) is None
    delete_dict = ex1_beliefdelta.beliefatoms.get(wx.DELETE)
    assert len(delete_dict.keys()) == 1

    # WHEN
    sue_atoms_list = ex1_beliefdelta.get_dimen_sorted_beliefatoms_list()

    # THEN
    assert len(sue_atoms_list) == 2
    assert sue_atoms_list[0] == update_dict.get(wx.beliefunit)
    z_atom = sue_atoms_list[1]
    print(f"{z_atom=}")
    print(delete_dict.get(wx.belief_voiceunit).keys())
    zia_voiceunit_delete = delete_dict.get(wx.belief_voiceunit).get("Zia")
    assert sue_atoms_list[1] == zia_voiceunit_delete


# def test_BeliefDelta_add_beliefatom_Sets_BeliefUnit_max_tree_traverse():
#     # ESTABLISH
#     ex1_beliefdelta = beliefdelta_shop(get_sue_rope())
#     assert ex1_beliefdelta.beliefatoms == {}

#     # WHEN
#     opt2_value = 55
#     dimen = wx.beliefunit
#     opt2_arg = "star"
#     star_beliefatom = beliefatom_shop(dimen, wx.UPDATE)
#     star_beliefatom.set_jvalue(opt2_arg, opt2_value)
#     ex1_beliefdelta.set_beliefatom(star_beliefatom)
#     # THEN
#     assert len(ex1_beliefdelta.beliefatoms.get(wx.UPDATE).keys()) == 1
#     sue_beliefunit_dict = ex1_beliefdelta.beliefatoms.get(wx.UPDATE)
#     sue_star_beliefatom = sue_beliefunit_dict.get(dimen)
#     print(f"{sue_star_beliefatom=}")
#     assert star_beliefatom == sue_star_beliefatom

#     # WHEN
#     new2_value = 66
#     x_attribute = "max_tree_traverse"
#     jkeys = {x_attribute: new2_value}
#     x_beliefatom = beliefatom_shop(x_attribute, wx.UPDATE, None, jkeys)
#     ex1_beliefdelta.set_beliefatom(x_beliefatom)
#     # THEN
#     print(f"{ex1_beliefdelta.beliefatoms.keys()=}")
#     print(f"{ex1_beliefdelta.beliefatoms.get(wx.UPDATE).keys()=}")
#     assert len(ex1_beliefdelta.beliefatoms.get(wx.UPDATE).keys()) == 2
#     assert x_beliefatom == ex1_beliefdelta.beliefatoms.get(wx.UPDATE).get(x_attribute)

#     # WHEN
#     new3_value = 77
#     x_attribute = "credor_respect"
#     jkeys = {x_attribute: new3_value}
#     x_beliefatom = beliefatom_shop(x_attribute, wx.UPDATE, None, jkeys)
#     ex1_beliefdelta.set_beliefatom(x_beliefatom)
#     # THEN
#     assert len(ex1_beliefdelta.beliefatoms.get(wx.UPDATE).keys()) == 3
#     assert x_beliefatom == ex1_beliefdelta.beliefatoms.get(wx.UPDATE).get(x_attribute)

#     # WHEN
#     new4_value = 88
#     x_attribute = "debtor_respect"
#     jkeys = {x_attribute: new4_value}
#     x_beliefatom = beliefatom_shop(x_attribute, wx.UPDATE, None, jkeys)
#     ex1_beliefdelta.set_beliefatom(x_beliefatom)
#     # THEN
#     assert len(ex1_beliefdelta.beliefatoms.get(wx.UPDATE).keys()) == 4
#     assert x_beliefatom == ex1_beliefdelta.beliefatoms.get(wx.UPDATE).get(x_attribute)


def test_BeliefDelta_get_sorted_beliefatoms_ReturnsObj():
    # ESTABLISH
    ex1_beliefdelta = get_beliefdelta_example1()
    update_dict = ex1_beliefdelta.beliefatoms.get(wx.UPDATE)
    assert len(update_dict.keys()) == 1
    assert update_dict.get(wx.beliefunit) is not None
    print(f"atom_order 28 {ex1_beliefdelta.beliefatoms.get(wx.UPDATE).keys()=}")
    delete_dict = ex1_beliefdelta.beliefatoms.get(wx.DELETE)
    assert len(delete_dict.keys()) == 1
    assert delete_dict.get(wx.belief_voiceunit) is not None
    print(f"atom_order 26 {ex1_beliefdelta.beliefatoms.get(wx.DELETE).keys()=}")

    # WHEN
    sue_atom_order_list = ex1_beliefdelta.get_sorted_beliefatoms()

    # THEN
    assert len(sue_atom_order_list) == 2
    print(delete_dict.get(wx.belief_voiceunit).keys())
    zia_voiceunit_delete = delete_dict.get(wx.belief_voiceunit).get("Zia")
    # for beliefatom in sue_atom_order_list:
    #     print(f"{beliefatom.atom_order=}")
    assert sue_atom_order_list[0] == zia_voiceunit_delete
    assert sue_atom_order_list[1] == update_dict.get(wx.beliefunit)
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_BeliefDelta_get_sorted_beliefatoms_ReturnsObj_PlanUnitsSorted():
    # ESTABLISH
    x_moment_label = "Amy23"
    root_rope = to_rope(x_moment_label)
    sports_str = "sports"
    sports_rope = create_rope(x_moment_label, sports_str)
    knee_str = "knee"
    knee_rope = create_rope(x_moment_label, knee_str)
    x_dimen = wx.belief_planunit
    sports_insert_planunit_beliefatom = beliefatom_shop(x_dimen, wx.INSERT)
    sports_insert_planunit_beliefatom.set_jkey(wx.plan_rope, sports_rope)
    knee_insert_planunit_beliefatom = beliefatom_shop(x_dimen, wx.INSERT)
    knee_insert_planunit_beliefatom.set_jkey(wx.plan_rope, knee_rope)
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(knee_insert_planunit_beliefatom)
    x_beliefdelta.set_beliefatom(sports_insert_planunit_beliefatom)

    # WHEN
    x_atom_order_list = x_beliefdelta.get_sorted_beliefatoms()

    # THEN
    assert len(x_atom_order_list) == 2
    # for beliefatom in x_atom_order_list:
    #     print(f"{beliefatom.jkeys=}")
    assert x_atom_order_list[0] == knee_insert_planunit_beliefatom
    assert x_atom_order_list[1] == sports_insert_planunit_beliefatom
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_BeliefDelta_get_sorted_beliefatoms_ReturnsObj_Rope_Sorted():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    x_moment_label = "Amy23"
    sports_str = "sports"
    sports_rope = create_rope(x_moment_label, sports_str)
    knee_str = "knee"
    knee_rope = create_rope(sports_rope, knee_str)
    x_dimen = wx.belief_plan_awardunit
    swimmers_str = ",Swimmers"
    sports_awardunit_beliefatom = beliefatom_shop(x_dimen, wx.INSERT)
    sports_awardunit_beliefatom.set_jkey(wx.awardee_title, swimmers_str)
    sports_awardunit_beliefatom.set_jkey(wx.plan_rope, sports_rope)
    knee_awardunit_beliefatom = beliefatom_shop(x_dimen, wx.INSERT)
    knee_awardunit_beliefatom.set_jkey(wx.awardee_title, swimmers_str)
    knee_awardunit_beliefatom.set_jkey(wx.plan_rope, knee_rope)
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(knee_awardunit_beliefatom)
    x_beliefdelta.set_beliefatom(sports_awardunit_beliefatom)

    # WHEN
    x_atom_order_list = x_beliefdelta.get_sorted_beliefatoms()

    # THEN
    assert len(x_atom_order_list) == 2
    # for beliefatom in x_atom_order_list:
    #     print(f"{beliefatom.jkeys=}")
    assert x_atom_order_list[0] == sports_awardunit_beliefatom
    assert x_atom_order_list[1] == knee_awardunit_beliefatom
    # for crud_str, atom_list in sue_atom_order_dict.items():
    #     print(f"{crud_str=}")
    #     print(f"{len(atom_list)=}")
    #     for x_atom in atom_list:
    #         print(f"{x_atom.dimen=}")


def test_belief_built_from_delta_is_valid_ReturnsObjEstablishWithNoBelief_scenario1():
    # ESTABLISH
    sue_beliefdelta = beliefdelta_shop()

    x_beliefatom = beliefatom_shop(wx.beliefunit, wx.UPDATE)
    x_attribute = "credor_respect"
    x_beliefatom.set_jvalue(x_attribute, 100)
    sue_beliefdelta.set_beliefatom(x_beliefatom)

    dimen = wx.belief_voiceunit
    zia_str = "Zia"
    x_beliefatom = beliefatom_shop(dimen, wx.INSERT)
    x_beliefatom.set_arg(wx.voice_name, zia_str)
    x_beliefatom.set_arg(wx.voice_cred_points, "70 is the number")
    sue_beliefdelta.set_beliefatom(x_beliefatom)
    print(f"{sue_beliefdelta=}")

    # WHEN / THEN
    assert belief_built_from_delta_is_valid(sue_beliefdelta) is False


def test_belief_built_from_delta_is_valid_ReturnsObjEstablishWithNoBelief_scenario2():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    sue_beliefdelta = beliefdelta_shop()
    dimen = wx.belief_voiceunit
    # WHEN
    yao_str = "Yao"
    x_beliefatom = beliefatom_shop(dimen, wx.INSERT)
    x_beliefatom.set_arg(wx.voice_name, yao_str)
    x_beliefatom.set_arg(wx.voice_cred_points, 30)
    sue_beliefdelta.set_beliefatom(x_beliefatom)

    # THEN
    assert belief_built_from_delta_is_valid(sue_beliefdelta)

    # WHEN
    bob_str = "Bob"
    x_beliefatom = beliefatom_shop(dimen, wx.INSERT)
    x_beliefatom.set_arg(wx.voice_name, bob_str)
    x_beliefatom.set_arg(wx.voice_cred_points, "70 is the number")
    sue_beliefdelta.set_beliefatom(x_beliefatom)

    # THEN
    assert belief_built_from_delta_is_valid(sue_beliefdelta) is False


def test_BeliefDelta_get_ordered_beliefatoms_ReturnsObj_EstablishWithNoStartingNumber():
    # sourcery skip: extract-duplicate-method, inline-immediately-returned-variable, move-assign-in-block
    # ESTABLISH
    sue_beliefdelta = beliefdelta_shop()
    pool_beliefatom = beliefatom_shop(wx.beliefunit, wx.UPDATE)
    pool_attribute = "credor_respect"
    pool_beliefatom.set_jvalue(pool_attribute, 100)
    sue_beliefdelta.set_beliefatom(pool_beliefatom)
    dimen = wx.belief_voiceunit
    zia_str = "Zia"
    zia_beliefatom = beliefatom_shop(dimen, wx.INSERT)
    zia_beliefatom.set_arg(wx.voice_name, zia_str)
    zia_beliefatom.set_arg(wx.voice_cred_points, 70)
    sue_beliefdelta.set_beliefatom(zia_beliefatom)
    sue_belief = beliefunit_shop("Sue")
    sue_belief.set_credor_respect(100)
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, wx.INSERT)
    yao_beliefatom.set_arg(wx.voice_name, yao_str)
    yao_beliefatom.set_arg(wx.voice_cred_points, 30)
    sue_beliefdelta.set_beliefatom(yao_beliefatom)

    sue_belief = beliefunit_shop("Sue")
    assert belief_built_from_delta_is_valid(sue_beliefdelta, sue_belief)

    # WHEN
    beliefdelta_dict = sue_beliefdelta.get_ordered_beliefatoms()

    # THEN
    # delta_zia = beliefdelta_dict.get(0)
    # delta_yao = beliefdelta_dict.get(1)
    # delta_pool = beliefdelta_dict.get(2)
    # assert delta_zia == zia_beliefatom
    # assert delta_yao == yao_beliefatom
    # assert delta_pool == pool_beliefatom
    assert beliefdelta_dict.get(0) == zia_beliefatom
    assert beliefdelta_dict.get(1) == yao_beliefatom
    assert beliefdelta_dict.get(2) == pool_beliefatom


def test_BeliefDelta_get_ordered_beliefatoms_ReturnsObj_EstablishWithStartingNumber():
    # sourcery skip: extract-duplicate-method, inline-immediately-returned-variable, move-assign-in-block
    # ESTABLISH
    sue_beliefdelta = beliefdelta_shop()
    pool_beliefatom = beliefatom_shop(wx.beliefunit, wx.UPDATE)
    pool_attribute = "credor_respect"
    pool_beliefatom.set_jvalue(pool_attribute, 100)
    sue_beliefdelta.set_beliefatom(pool_beliefatom)
    dimen = wx.belief_voiceunit
    zia_str = "Zia"
    zia_beliefatom = beliefatom_shop(dimen, wx.INSERT)
    zia_beliefatom.set_arg(wx.voice_name, zia_str)
    zia_beliefatom.set_arg(wx.voice_cred_points, 70)
    sue_beliefdelta.set_beliefatom(zia_beliefatom)
    sue_belief = beliefunit_shop("Sue")
    sue_belief.set_credor_respect(100)
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, wx.INSERT)
    yao_beliefatom.set_arg(wx.voice_name, yao_str)
    yao_beliefatom.set_arg(wx.voice_cred_points, 30)
    sue_beliefdelta.set_beliefatom(yao_beliefatom)

    sue_belief = beliefunit_shop("Sue")
    assert belief_built_from_delta_is_valid(sue_beliefdelta, sue_belief)

    # WHEN
    beliefdelta_dict = sue_beliefdelta.get_ordered_beliefatoms(5)

    # THEN
    # delta_zia = beliefdelta_dict.get(0)
    # delta_yao = beliefdelta_dict.get(1)
    # delta_pool = beliefdelta_dict.get(2)
    # assert delta_zia == zia_beliefatom
    # assert delta_yao == yao_beliefatom
    # assert delta_pool == pool_beliefatom
    assert beliefdelta_dict.get(5) == zia_beliefatom
    assert beliefdelta_dict.get(6) == yao_beliefatom
    assert beliefdelta_dict.get(7) == pool_beliefatom


def test_BeliefDelta_get_ordered_dict_ReturnsObj_EstablishWithStartingNumber():
    # sourcery skip: extract-duplicate-method, inline-immediately-returned-variable, move-assign-in-block
    # ESTABLISH
    sue_beliefdelta = beliefdelta_shop()
    pool_beliefatom = beliefatom_shop(wx.beliefunit, wx.UPDATE)
    pool_attribute = "credor_respect"
    pool_beliefatom.set_jvalue(pool_attribute, 100)
    sue_beliefdelta.set_beliefatom(pool_beliefatom)
    dimen = wx.belief_voiceunit
    zia_str = "Zia"
    zia_beliefatom = beliefatom_shop(dimen, wx.INSERT)
    zia_beliefatom.set_arg(wx.voice_name, zia_str)
    zia_beliefatom.set_arg(wx.voice_cred_points, 70)
    sue_beliefdelta.set_beliefatom(zia_beliefatom)
    sue_belief = beliefunit_shop("Sue")
    sue_belief.set_credor_respect(100)
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, wx.INSERT)
    yao_beliefatom.set_arg(wx.voice_name, yao_str)
    yao_beliefatom.set_arg(wx.voice_cred_points, 30)
    sue_beliefdelta.set_beliefatom(yao_beliefatom)

    sue_belief = beliefunit_shop("Sue")
    assert belief_built_from_delta_is_valid(sue_beliefdelta, sue_belief)

    # WHEN
    beliefdelta_dict = sue_beliefdelta.get_ordered_dict(5)

    # THEN
    # delta_zia = beliefdelta_dict.get(0)
    # delta_yao = beliefdelta_dict.get(1)
    # delta_pool = beliefdelta_dict.get(2)
    # assert delta_zia == zia_beliefatom
    # assert delta_yao == yao_beliefatom
    # assert delta_pool == pool_beliefatom
    assert beliefdelta_dict.get(5) == zia_beliefatom.to_dict()
    assert beliefdelta_dict.get(6) == yao_beliefatom.to_dict()
    assert beliefdelta_dict.get(7) == pool_beliefatom.to_dict()


def test_get_beliefdelta_from_ordered_dict_ReturnsObj():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    expected_beliefdelta = beliefdelta_shop()
    pool_beliefatom = beliefatom_shop(wx.beliefunit, wx.UPDATE)
    pool_attribute = "credor_respect"
    pool_beliefatom.set_jvalue(pool_attribute, 100)
    expected_beliefdelta.set_beliefatom(pool_beliefatom)
    dimen = wx.belief_voiceunit
    zia_str = "Zia"
    zia_beliefatom = beliefatom_shop(dimen, wx.INSERT)
    zia_beliefatom.set_arg(wx.voice_name, zia_str)
    zia_beliefatom.set_arg(wx.voice_cred_points, 70)
    expected_beliefdelta.set_beliefatom(zia_beliefatom)
    sue_belief = beliefunit_shop("Sue")
    sue_belief.set_credor_respect(100)
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, wx.INSERT)
    yao_beliefatom.set_arg(wx.voice_name, yao_str)
    yao_beliefatom.set_arg(wx.voice_cred_points, 30)
    expected_beliefdelta.set_beliefatom(yao_beliefatom)
    beliefdelta_dict = expected_beliefdelta.get_ordered_dict(5)

    # WHEN
    generated_beliefdelta = get_beliefdelta_from_ordered_dict(beliefdelta_dict)

    # THEN
    # delta_zia = beliefdelta_dict.get(0)
    # delta_yao = beliefdelta_dict.get(1)
    # delta_pool = beliefdelta_dict.get(2)
    # assert delta_zia == zia_beliefatom
    # assert delta_yao == yao_beliefatom
    # assert delta_pool == pool_beliefatom
    # assert beliefdelta_dict.get(5) == zia_beliefatom.to_dict()
    # assert beliefdelta_dict.get(6) == yao_beliefatom.to_dict()
    # assert beliefdelta_dict.get(7) == pool_beliefatom.to_dict()
    assert generated_beliefdelta == expected_beliefdelta


def test_BeliefDelta_get_json_ReturnsObj():
    # sourcery skip: extract-duplicate-method, inline-variable
    # ESTABLISH
    sue_beliefdelta = beliefdelta_shop()
    pool_beliefatom = beliefatom_shop(wx.beliefunit, wx.UPDATE)
    pool_attribute = "credor_respect"
    pool_beliefatom.set_jvalue(pool_attribute, 100)
    sue_beliefdelta.set_beliefatom(pool_beliefatom)
    dimen = wx.belief_voiceunit
    zia_str = "Zia"
    zia_beliefatom = beliefatom_shop(dimen, wx.INSERT)
    zia_beliefatom.set_arg(wx.voice_name, zia_str)
    zia_beliefatom.set_arg(wx.voice_cred_points, 70)
    sue_beliefdelta.set_beliefatom(zia_beliefatom)
    yao_str = "Yao"
    yao_beliefatom = beliefatom_shop(dimen, wx.INSERT)
    yao_beliefatom.set_arg(wx.voice_name, yao_str)
    yao_beliefatom.set_arg(wx.voice_cred_points, 30)
    sue_beliefdelta.set_beliefatom(yao_beliefatom)

    # WHEN
    delta_start_int = 5
    beliefdelta_json = sue_beliefdelta.get_json(delta_start_int)

    # THEN
    assert x_is_json(beliefdelta_json)


def test_BeliefDelta_beliefatom_exists_ReturnsObj():
    # ESTABLISH
    x_beliefdelta = beliefdelta_shop()

    # WHEN / THEN
    dimen = wx.belief_voiceunit
    zia_str = "Zia"
    zia_beliefatom = beliefatom_shop(dimen, wx.INSERT)
    zia_beliefatom.set_arg(wx.voice_name, zia_str)
    zia_beliefatom.set_arg(wx.voice_cred_points, 70)
    assert x_beliefdelta.beliefatom_exists(zia_beliefatom) is False

    # WHEN
    x_beliefdelta.set_beliefatom(zia_beliefatom)

    # THEN
    assert x_beliefdelta.beliefatom_exists(zia_beliefatom)


def test_BeliefDelta_is_empty_ReturnsObj():
    # ESTABLISH
    x_beliefdelta = beliefdelta_shop()

    # WHEN / THEN
    dimen = wx.belief_voiceunit
    zia_str = "Zia"
    zia_beliefatom = beliefatom_shop(dimen, wx.INSERT)
    zia_beliefatom.set_arg(wx.voice_name, zia_str)
    zia_beliefatom.set_arg(wx.voice_cred_points, 70)
    assert x_beliefdelta.is_empty()

    # WHEN
    x_beliefdelta.set_beliefatom(zia_beliefatom)

    # THEN
    assert x_beliefdelta.is_empty() is False
