from pytest import raises as pytest_raises
from src.a00_data_toolbox.dict_toolbox import get_dict_from_json, x_is_json
from src.a01_rope_logic.rope import default_knot_if_None, to_rope
from src.a03_group_logic.group import awardunit_shop
from src.a03_group_logic.labor import laborunit_shop, partyunit_shop
from src.a04_reason_logic.reason import factunit_shop
from src.a05_plan_logic.healer import healerunit_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_belief_logic.belief_main import (
    beliefunit_shop,
    get_dict_of_belief_from_dict,
    get_from_json as beliefunit_get_from_json,
)
from src.a06_belief_logic.test._util.a06_str import (
    factunits_str,
    kids_str,
    laborunit_str,
    planroot_str,
    reasonunits_str,
    voices_str,
)
from src.a06_belief_logic.test._util.example_beliefs import (
    beliefunit_v001,
    get_beliefunit_laundry_example1,
    get_beliefunit_reason_context_ziet_example,
    get_beliefunit_x1_3levels_1reason_1facts,
)


def test_BeliefUnit_to_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    yao_belief = get_beliefunit_laundry_example1()
    yao_fund_pool = 23000
    yao_belief.fund_pool = yao_fund_pool
    yao_fund_iota = 23
    yao_belief.fund_iota = yao_fund_iota
    belief_tally = 23
    yao_belief.tally = belief_tally
    x_last_pack_id = 77
    yao_belief.set_last_pack_id(x_last_pack_id)

    # WHEN
    belief_dict = yao_belief.to_dict()

    # THEN
    assert belief_dict is not None
    assert str(type(belief_dict)) == "<class 'dict'>"
    assert belief_dict["belief_name"] == yao_belief.belief_name
    assert belief_dict["moment_label"] == yao_belief.moment_label
    assert belief_dict["tally"] == yao_belief.tally
    assert belief_dict["tally"] == belief_tally
    assert belief_dict["fund_pool"] == yao_fund_pool
    assert belief_dict["fund_iota"] == yao_fund_iota
    assert belief_dict["max_tree_traverse"] == yao_belief.max_tree_traverse
    assert belief_dict["knot"] == yao_belief.knot
    assert belief_dict["credor_respect"] == yao_belief.credor_respect
    assert belief_dict["debtor_respect"] == yao_belief.debtor_respect
    assert belief_dict["last_pack_id"] == yao_belief.last_pack_id
    assert len(belief_dict[voices_str()]) == len(yao_belief.voices)
    assert len(belief_dict[voices_str()]) != 12

    x_planroot = yao_belief.planroot
    planroot_dict = belief_dict[planroot_str()]
    assert x_planroot.plan_label == yao_belief.moment_label
    assert planroot_dict["plan_label"] == x_planroot.plan_label
    assert planroot_dict["star"] == x_planroot.star
    assert len(planroot_dict[kids_str()]) == len(x_planroot.kids)


def test_BeliefUnit_to_dict_ReturnsObj_Scenario1_planroot_laborunit():
    # ESTABLISH
    run_str = "runners"
    sue_belief = beliefunit_shop("Sue")
    x_laborunit = laborunit_shop()
    x_laborunit.add_party(party_title=run_str)
    root_rope = to_rope(sue_belief.moment_label)
    sue_belief.edit_plan_attr(root_rope, laborunit=x_laborunit)
    root_plan = sue_belief.get_plan_obj(root_rope)
    x_gogo_want = 5
    x_stop_want = 11
    root_plan.gogo_want = x_gogo_want
    root_plan.stop_want = x_stop_want

    # WHEN
    belief_dict = sue_belief.to_dict()
    planroot_dict = belief_dict.get(planroot_str())

    # THEN
    assert planroot_dict[laborunit_str()] == x_laborunit.to_dict()
    run_partyunit = partyunit_shop(run_str)
    assert planroot_dict[laborunit_str()] == {
        "_partys": {run_str: run_partyunit.to_dict()}
    }
    assert planroot_dict.get("gogo_want") == x_gogo_want
    assert planroot_dict.get("stop_want") == x_stop_want


def test_BeliefUnit_to_dict_ReturnsObj_Scenario2_With_planroot_healerunit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    yao_str = "Yao"
    sue_belief.add_voiceunit(yao_str)
    run_str = ";runners"
    yao_voiceunit = sue_belief.get_voice(yao_str)
    yao_voiceunit.add_membership(run_str)
    run_healerunit = healerunit_shop()
    run_healerunit.set_healer_name(x_healer_name=run_str)
    root_rope = to_rope(sue_belief.moment_label)
    sue_belief.edit_plan_attr(root_rope, healerunit=run_healerunit)

    # WHEN
    belief_dict = sue_belief.to_dict()
    planroot_dict = belief_dict.get(planroot_str())

    # THEN
    assert planroot_dict["healerunit"] == run_healerunit.to_dict()


def test_BeliefUnit_to_dict_ReturnsObj_Scenario3_plankid_LaborUnit():
    # ESTABLISH
    sue_belief = beliefunit_shop("Sue")
    yao_str = "Yao"
    sue_belief.add_voiceunit(yao_str)
    run_str = ";runners"
    yao_voiceunit = sue_belief.get_voice(yao_str)
    yao_voiceunit.add_membership(run_str)

    morn_str = "morning"
    morn_rope = sue_belief.make_l1_rope(morn_str)
    sue_belief.set_l1_plan(planunit_shop(morn_str))
    x_laborunit = laborunit_shop()
    x_laborunit.add_party(party_title=run_str)
    sue_belief.edit_plan_attr(morn_rope, laborunit=x_laborunit)

    # WHEN
    belief_dict = sue_belief.to_dict()
    planroot_dict = belief_dict.get(planroot_str())

    # THEN
    laborunit = "laborunit"

    labor_dict_x = planroot_dict[kids_str()][morn_str][laborunit]
    assert labor_dict_x == x_laborunit.to_dict()
    run_partyunit = partyunit_shop(run_str)
    assert labor_dict_x == {"_partys": {run_str: run_partyunit.to_dict()}}


def test_BeliefUnit_get_json_ReturnsJSON_SimpleExample():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    zia_belief = get_beliefunit_x1_3levels_1reason_1facts()
    x_fund_pool = 66000
    zia_belief.fund_pool = x_fund_pool
    x_fund_iota = 66
    zia_belief.fund_iota = x_fund_iota
    x_respect_bit = 7
    zia_belief.respect_bit = x_respect_bit
    x_penny = 0.3
    zia_belief.penny = x_penny
    override_str = "override"
    yao_str = "Yao"
    run_str = ";runners"
    zia_belief.add_voiceunit(yao_str)
    yao_voiceunit = zia_belief.get_voice(yao_str)
    yao_voiceunit.add_membership(run_str)
    run_healerunit = healerunit_shop({run_str})
    root_rope = to_rope(zia_belief.moment_label)
    zia_belief.edit_plan_attr(root_rope, healerunit=run_healerunit)
    zia_belief.edit_plan_attr(root_rope, problem_bool=True)

    # WHEN
    x_json = zia_belief.get_json()

    # THEN
    assert x_json is not None
    assert True == x_is_json(x_json)
    belief_dict = get_dict_from_json(x_json)

    assert belief_dict["belief_name"] == zia_belief.belief_name
    assert belief_dict["moment_label"] == zia_belief.moment_label
    assert belief_dict["tally"] == zia_belief.tally
    assert belief_dict["fund_pool"] == zia_belief.fund_pool
    assert belief_dict["fund_iota"] == zia_belief.fund_iota
    assert belief_dict["respect_bit"] == zia_belief.respect_bit
    assert belief_dict["penny"] == zia_belief.penny
    assert belief_dict["credor_respect"] == zia_belief.credor_respect
    assert belief_dict["debtor_respect"] == zia_belief.debtor_respect
    # with pytest_raises(Exception) as excinfo:
    #     belief_dict["_credor_respect"]
    # assert str(excinfo.value) == "'_credor_respect'"
    # with pytest_raises(Exception) as excinfo:
    #     belief_dict["_debtor_respect"]
    # assert str(excinfo.value) == "'_debtor_respect'"
    with pytest_raises(Exception) as excinfo:
        belief_dict["last_pack_id"]

    x_planroot = zia_belief.planroot
    planroot_dict = belief_dict.get(planroot_str())

    assert len(planroot_dict[kids_str()]) == len(x_planroot.kids)

    shave_str = "shave"
    shave_dict = planroot_dict[kids_str()][shave_str]
    shave_factunits = shave_dict[factunits_str()]
    print(f"{shave_factunits=}")
    assert len(shave_factunits) == 1
    assert len(shave_factunits) == len(x_planroot.kids[shave_str].factunits)
    planroot_healerunit = planroot_dict["healerunit"]
    print(f"{planroot_healerunit=}")
    assert len(planroot_healerunit) == 1
    assert x_planroot.healerunit.any_healer_name_exists()
    assert x_planroot.problem_bool


def test_BeliefUnit_get_json_ReturnsJSON_BigExample():
    # ESTABLISH
    yao_belief = beliefunit_v001()
    hr_number_str = "hr_number"
    hr_number_rope = yao_belief.make_l1_rope(hr_number_str)
    yao_belief.add_fact(
        fact_context=hr_number_rope,
        fact_state=hr_number_rope,
        fact_lower=0,
        fact_upper=23,
    )
    jour_min_str = "jour_minute"
    jour_min_rope = yao_belief.make_l1_rope(jour_min_str)
    yao_belief.add_fact(
        fact_context=jour_min_rope,
        fact_state=jour_min_rope,
        fact_lower=0,
        fact_upper=59,
    )
    x_factunit = factunit_shop(jour_min_rope, jour_min_rope, 5, 59)
    yao_belief.edit_plan_attr(x_factunit.fact_context, factunit=x_factunit)
    yao_belief.set_max_tree_traverse(2)
    yao_str = "Yao"

    # WHEN
    belief_dict = get_dict_from_json(yao_belief.get_json())

    # THEN
    assert belief_dict["belief_name"] == yao_belief.belief_name
    assert belief_dict["moment_label"] == yao_belief.moment_label
    assert belief_dict["tally"] == yao_belief.tally
    assert belief_dict["max_tree_traverse"] == 2
    assert belief_dict["max_tree_traverse"] == yao_belief.max_tree_traverse
    assert belief_dict["knot"] == yao_belief.knot

    x_planroot = yao_belief.planroot
    planroot_dict = belief_dict.get(planroot_str())
    assert len(planroot_dict[kids_str()]) == len(x_planroot.kids)

    kids_dict = planroot_dict[kids_str()]
    jour_min_dict = kids_dict[jour_min_str]
    jour_min_factunits_dict = jour_min_dict[factunits_str()]
    jour_min_plan_x = yao_belief.get_plan_obj(jour_min_rope)
    print(f"{jour_min_factunits_dict=}")
    assert len(jour_min_factunits_dict) == 1
    assert len(jour_min_factunits_dict) == len(jour_min_plan_x.factunits)

    cont_str = "Freelancing"
    ulti_str = "Ultimate Frisbee"
    cont_rope = yao_belief.make_l1_rope(cont_str)
    ulti_rope = yao_belief.make_l1_rope(ulti_str)
    cont_plan = yao_belief.get_plan_obj(cont_rope)
    ulti_plan = yao_belief.get_plan_obj(ulti_rope)
    cont_reasonunits_dict = planroot_dict[kids_str()][cont_str][reasonunits_str()]
    ulti_reasonunits_dict = planroot_dict[kids_str()][ulti_str][reasonunits_str()]
    assert len(cont_reasonunits_dict) == len(cont_plan.reasonunits)
    assert len(ulti_reasonunits_dict) == len(ulti_plan.reasonunits)

    anna_str = "Anna"
    anna_voiceunit = yao_belief.get_voice(anna_str)
    assert anna_voiceunit.get_membership(";Family").group_cred_points == 6.2
    assert yao_belief.voices is not None
    assert len(yao_belief.voices) == 22


def test_beliefunit_get_from_json_ReturnsObjSimpleExample():
    # ESTABLISH
    zia_belief = get_beliefunit_x1_3levels_1reason_1facts()
    zia_belief.set_max_tree_traverse(23)
    tiger_moment_label = "tiger"
    zia_belief.set_moment_label(tiger_moment_label)
    zia_fund_pool = 80000
    zia_belief.fund_pool = zia_fund_pool
    zia_fund_iota = 8
    zia_belief.fund_iota = zia_fund_iota
    zia_resepect_bit = 5
    zia_belief.respect_bit = zia_resepect_bit
    zia_penny = 2
    zia_belief.penny = zia_penny
    zia_credor_respect = 200
    zia_debtor_respect = 200
    zia_belief.set_credor_respect(zia_credor_respect)
    zia_belief.set_debtor_respect(zia_debtor_respect)
    zia_last_pack_id = 73
    zia_belief.set_last_pack_id(zia_last_pack_id)

    shave_str = "shave"
    shave_rope = zia_belief.make_l1_rope(shave_str)
    shave_plan_y1 = zia_belief.get_plan_obj(shave_rope)
    shave_plan_y1.problem_bool = True
    # print(f"{shave_rope=}")
    # print(f"{json_shave_plan.plan_label=} {json_shave_plan.parent_rope=}")

    sue_str = "Sue"
    zia_belief.add_voiceunit(
        voice_name=sue_str, voice_cred_points=199, voice_debt_points=199
    )
    xio_str = "Xio"
    zia_belief.add_voiceunit(voice_name=xio_str)
    run_str = ";runners"
    sue_voiceunit = zia_belief.get_voice(sue_str)
    xio_voiceunit = zia_belief.get_voice(xio_str)
    sue_voiceunit.add_membership(run_str)
    xio_voiceunit.add_membership(run_str)
    run_laborunit = laborunit_shop()
    run_laborunit.add_party(party_title=run_str)
    root_rope = to_rope(zia_belief.moment_label)
    zia_belief.edit_plan_attr(root_rope, laborunit=run_laborunit)
    xio_laborunit = laborunit_shop()
    xio_laborunit.add_party(party_title=xio_str)
    zia_belief.edit_plan_attr(shave_rope, laborunit=xio_laborunit)
    zia_belief.edit_plan_attr(shave_rope, awardunit=awardunit_shop(xio_str))
    zia_belief.edit_plan_attr(shave_rope, awardunit=awardunit_shop(sue_str))
    zia_belief.edit_plan_attr(root_rope, awardunit=awardunit_shop(sue_str))
    # add healerunit to shave planunit
    run_healerunit = healerunit_shop({run_str})
    zia_belief.edit_plan_attr(shave_rope, healerunit=run_healerunit)
    shave_plan = zia_belief.get_plan_obj(shave_rope)
    zia_gogo_want = 75
    zia_stop_want = 77
    shave_plan.gogo_want = zia_gogo_want
    shave_plan.stop_want = zia_stop_want

    override_str = "override"

    # WHEN
    x_json = zia_belief.get_json()
    assert x_is_json(x_json) is True
    json_belief = beliefunit_get_from_json(x_belief_json=x_json)

    # THEN
    assert str(type(json_belief)).find(".belief_main.BeliefUnit'>") > 0
    assert json_belief.belief_name is not None
    assert json_belief.belief_name == zia_belief.belief_name
    assert json_belief.moment_label == zia_belief.moment_label
    assert json_belief.fund_pool == zia_fund_pool
    assert json_belief.fund_pool == zia_belief.fund_pool
    assert json_belief.fund_iota == zia_fund_iota
    assert json_belief.fund_iota == zia_belief.fund_iota
    assert json_belief.respect_bit == zia_resepect_bit
    assert json_belief.respect_bit == zia_belief.respect_bit
    assert json_belief.penny == zia_penny
    assert json_belief.penny == zia_belief.penny
    assert json_belief.max_tree_traverse == 23
    assert json_belief.max_tree_traverse == zia_belief.max_tree_traverse
    assert json_belief.knot == zia_belief.knot
    assert json_belief.credor_respect == zia_belief.credor_respect
    assert json_belief.debtor_respect == zia_belief.debtor_respect
    assert json_belief.credor_respect == zia_credor_respect
    assert json_belief.debtor_respect == zia_debtor_respect
    assert json_belief.last_pack_id == zia_belief.last_pack_id
    assert json_belief.last_pack_id == zia_last_pack_id

    json_planroot = json_belief.planroot
    assert json_planroot.parent_rope == ""
    assert json_planroot.parent_rope == zia_belief.planroot.parent_rope
    assert json_planroot.reasonunits == {}
    assert json_planroot.laborunit == zia_belief.planroot.laborunit
    assert json_planroot.laborunit == run_laborunit
    assert json_planroot.fund_iota == 8
    assert json_planroot.fund_iota == zia_fund_iota
    assert len(json_planroot.factunits) == 1
    assert len(json_planroot.awardunits) == 1

    assert len(json_belief.planroot.kids) == 2

    sem_jour_str = "sem_jours"
    sem_jour_rope = json_belief.make_l1_rope(sem_jour_str)
    sem_jour_plan_x = json_belief.get_plan_obj(sem_jour_rope)
    assert len(sem_jour_plan_x.kids) == 2

    sun_str = "Sun"
    sun_rope = json_belief.make_rope(sem_jour_rope, sun_str)
    sun_plan = json_belief.get_plan_obj(sun_rope)
    assert sun_plan.star == 20

    json_shave_plan = json_belief.get_plan_obj(shave_rope)
    zia_shave_plan = zia_belief.get_plan_obj(shave_rope)
    assert len(json_shave_plan.reasonunits) == 1
    assert json_shave_plan.laborunit == zia_shave_plan.laborunit
    assert json_shave_plan.laborunit == xio_laborunit
    print(f"{json_shave_plan.healerunit=}")
    assert json_shave_plan.healerunit == zia_shave_plan.healerunit
    assert len(json_shave_plan.awardunits) == 2
    assert len(json_shave_plan.factunits) == 1
    assert zia_shave_plan.problem_bool
    assert json_shave_plan.problem_bool == zia_shave_plan.problem_bool
    assert json_shave_plan.gogo_want == zia_shave_plan.gogo_want
    assert json_shave_plan.stop_want == zia_shave_plan.stop_want


def test_beliefunit_get_from_json_ReturnsPlanRoot():
    # ESTABLISH
    zia_belief = get_beliefunit_x1_3levels_1reason_1facts()
    zia_belief.set_max_tree_traverse(23)
    # root_plan = zia_belief.get_plan_obj(zia_belief.get_plan_obj(zia_belief.moment_label))
    root_plan = zia_belief.planroot
    zia_gogo_want = 75
    zia_stop_want = 77
    root_plan.gogo_want = zia_gogo_want
    root_plan.stop_want = zia_stop_want

    # WHEN
    x_json = zia_belief.get_json()
    assert x_is_json(x_json) is True
    json_belief = beliefunit_get_from_json(x_belief_json=x_json)

    # THEN
    json_planroot = json_belief.get_plan_obj(to_rope(zia_belief.moment_label))
    assert json_planroot.gogo_want == zia_gogo_want
    assert json_planroot.stop_want == zia_stop_want


def test_beliefunit_get_from_json_ReturnsObj_knot_Example():
    # ESTABLISH
    slash_knot = "/"
    before_bob_belief = beliefunit_shop("Bob", knot=slash_knot)
    assert before_bob_belief.knot != default_knot_if_None()

    # WHEN
    bob_json = before_bob_belief.get_json()
    after_bob_belief = beliefunit_get_from_json(bob_json)

    # THEN
    assert after_bob_belief.knot != default_knot_if_None()
    assert after_bob_belief.knot == slash_knot
    assert after_bob_belief.knot == before_bob_belief.knot


def test_beliefunit_get_from_json_ReturnsObj_knot_VoiceExample():
    # ESTABLISH
    slash_knot = "/"
    before_bob_belief = beliefunit_shop("Bob", knot=slash_knot)
    bob_str = ",Bob"
    before_bob_belief.add_voiceunit(bob_str)
    assert before_bob_belief.voice_exists(bob_str)

    # WHEN
    bob_json = before_bob_belief.get_json()
    after_bob_belief = beliefunit_get_from_json(bob_json)

    # THEN
    after_bob_voiceunit = after_bob_belief.get_voice(bob_str)
    assert after_bob_voiceunit.knot == slash_knot


def test_beliefunit_get_from_json_ReturnsObj_knot_GroupExample():
    # ESTABLISH
    slash_knot = "/"
    before_bob_belief = beliefunit_shop("Bob", knot=slash_knot)
    yao_str = "Yao"
    swim_str = f"{slash_knot}Swimmers"
    before_bob_belief.add_voiceunit(yao_str)
    yao_voiceunit = before_bob_belief.get_voice(yao_str)
    yao_voiceunit.add_membership(swim_str)

    # WHEN
    bob_json = before_bob_belief.get_json()
    after_bob_belief = beliefunit_get_from_json(bob_json)

    # THEN
    after_yao_voiceunit = after_bob_belief.get_voice(yao_str)
    assert after_yao_voiceunit.knot == slash_knot


def test_beliefunit_get_from_json_ReturnsObj_Scenario7_planroot_knot_IsApplied():
    # sourcery skip: extract-duplicate-method
    # ESTABLISH
    slash_str = "/"
    run_str = "runners"
    sue_belief = beliefunit_shop("Sue", knot=slash_str)
    root_rope = to_rope(sue_belief.moment_label, slash_str)
    hr_number_str = "hr_number"
    hr_number_rope = sue_belief.make_l1_rope(hr_number_str)
    sue_belief.add_plan(hr_number_rope)
    assert sue_belief.knot == slash_str
    assert sue_belief.get_plan_obj(root_rope).knot == slash_str
    assert sue_belief.get_plan_obj(hr_number_rope).knot == slash_str

    # WHEN
    after_bob_belief = beliefunit_get_from_json(sue_belief.get_json())

    # THEN
    assert after_bob_belief.knot == slash_str
    assert after_bob_belief.get_plan_obj(root_rope).knot == slash_str
    assert after_bob_belief.get_plan_obj(hr_number_rope).knot == slash_str


def test_beliefunit_get_from_json_ExportsBeliefUnit_star():
    # ESTABLISH
    x1_belief = beliefunit_v001()
    x1_belief.tally = 15
    assert x1_belief.tally == 15
    assert x1_belief.planroot.star != x1_belief.tally
    assert x1_belief.planroot.star == 1

    # WHEN
    x2_belief = beliefunit_get_from_json(x1_belief.get_json())

    # THEN
    assert x1_belief.tally == 15
    assert x1_belief.tally == x2_belief.tally
    assert x1_belief.planroot.star == 1
    assert x1_belief.planroot.star == x2_belief.planroot.star
    assert x1_belief.planroot.kids == x2_belief.planroot.kids


def test_get_dict_of_belief_from_dict_ReturnsDictOfBeliefUnits():
    # ESTABLISH
    x1_belief = beliefunit_v001()
    x2_belief = get_beliefunit_x1_3levels_1reason_1facts()
    x3_belief = get_beliefunit_reason_context_ziet_example()
    print(f"{x1_belief.belief_name}")
    print(f"{x2_belief.belief_name}")
    print(f"{x3_belief.belief_name}")

    cn_dict_of_dicts = {
        x1_belief.belief_name: x1_belief.to_dict(),
        x2_belief.belief_name: x2_belief.to_dict(),
        x3_belief.belief_name: x3_belief.to_dict(),
    }

    # WHEN
    ccn_dict_of_obj = get_dict_of_belief_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(x1_belief.belief_name) is not None
    assert ccn_dict_of_obj.get(x2_belief.belief_name) is not None
    assert ccn_dict_of_obj.get(x3_belief.belief_name) is not None

    ccn2_belief = ccn_dict_of_obj.get(x2_belief.belief_name)
    assert ccn2_belief.planroot.plan_label == x2_belief.planroot.plan_label
    assert ccn2_belief.planroot.parent_rope == x2_belief.planroot.parent_rope
    assert ccn2_belief.planroot.fund_iota == x2_belief.planroot.fund_iota
    shave_rope = ccn2_belief.make_l1_rope("shave")
    wk_rope = ccn2_belief.make_l1_rope("sem_jours")
    # assert ccn2_belief.get_plan_obj(shave_rope) == x2_belief.get_plan_obj(shave_rope)
    # assert ccn2_belief.get_plan_obj(wk_rope) == x2_belief.get_plan_obj(wk_rope)
    # assert ccn2_belief.planroot == x2_belief.planroot
    assert ccn2_belief.to_dict() == x2_belief.to_dict()

    ccn_belief3 = ccn_dict_of_obj.get(x3_belief.belief_name)
    assert ccn_belief3.to_dict() == x3_belief.to_dict()

    cc1_plan_root = ccn_dict_of_obj.get(x1_belief.belief_name).planroot
    ccn_belief1 = ccn_dict_of_obj.get(x1_belief.belief_name)
    assert ccn_belief1._plan_dict == x1_belief._plan_dict
    philipa_str = "Philipa"
    ccn_philipa_voiceunit = ccn_belief1.get_voice(philipa_str)
    x1_philipa_voiceunit = x1_belief.get_voice(philipa_str)
    assert ccn_philipa_voiceunit.memberships == x1_philipa_voiceunit.memberships
    assert ccn_belief1 == x1_belief
    assert ccn_dict_of_obj.get(x1_belief.belief_name) == x1_belief
