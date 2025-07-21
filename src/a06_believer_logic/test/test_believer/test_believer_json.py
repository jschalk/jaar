from pytest import raises as pytest_raises
from src.a00_data_toolbox.dict_toolbox import get_dict_from_json, x_is_json
from src.a01_term_logic.rope import default_knot_if_None, to_rope
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_labor import laborunit_shop
from src.a04_reason_logic.reason_plan import factunit_shop
from src.a05_plan_logic.healer import healerlink_shop
from src.a05_plan_logic.plan import planunit_shop
from src.a06_believer_logic.believer import (
    believerunit_shop,
    get_dict_of_believer_from_dict,
    get_from_json as believerunit_get_from_json,
)
from src.a06_believer_logic.test._util.example_believers import (
    believerunit_v001,
    get_believerunit_r_context_time_example,
    get_believerunit_x1_3levels_1reason_1facts,
)


def test_BelieverUnit_get_dict_ReturnsObj_Scenario1_large_json():
    # ESTABLISH
    yao_believer = believerunit_v001()
    hr_number_str = "hr_number"
    hr_number_rope = yao_believer.make_l1_rope(hr_number_str)
    hr_number_plan = yao_believer.get_plan_obj(hr_number_rope)
    yao_believer.add_fact(
        f_context=hr_number_rope, f_state=hr_number_rope, f_lower=0, f_upper=23
    )
    time_minute = yao_believer.make_l1_rope("jour_minute")
    yao_believer.add_fact(
        f_context=time_minute, f_state=time_minute, f_lower=0, f_upper=1440
    )
    yao_str = "Yao"
    yao_fund_pool = 23000
    yao_believer.fund_pool = yao_fund_pool
    yao_fund_iota = 23
    yao_believer.fund_iota = yao_fund_iota
    believer_tally = 23
    yao_believer.tally = believer_tally
    x_credor_respect = 22
    x_debtor_respect = 44
    yao_believer.set_credor_respect(x_credor_respect)
    yao_believer.set_debtor_respect(x_debtor_respect)
    override_str = "override"
    x_last_pack_id = 77
    yao_believer.set_last_pack_id(x_last_pack_id)

    # WHEN
    believer_dict = yao_believer.get_dict()

    # THEN
    assert believer_dict is not None
    assert str(type(believer_dict)) == "<class 'dict'>"
    assert believer_dict["believer_name"] == yao_believer.believer_name
    assert believer_dict["belief_label"] == yao_believer.belief_label
    assert believer_dict["tally"] == yao_believer.tally
    assert believer_dict["tally"] == believer_tally
    assert believer_dict["fund_pool"] == yao_fund_pool
    assert believer_dict["fund_iota"] == yao_fund_iota
    assert believer_dict["max_tree_traverse"] == yao_believer.max_tree_traverse
    assert believer_dict["knot"] == yao_believer.knot
    assert believer_dict["credor_respect"] == yao_believer.credor_respect
    assert believer_dict["debtor_respect"] == yao_believer.debtor_respect
    assert believer_dict["last_pack_id"] == yao_believer.last_pack_id
    assert len(believer_dict["partners"]) == len(yao_believer.partners)
    assert len(believer_dict["partners"]) != 12
    assert believer_dict.get("_groups") is None

    x_planroot = yao_believer.planroot
    planroot_dict = believer_dict["planroot"]
    _kids = "_kids"
    assert x_planroot.plan_label == yao_believer.belief_label
    assert planroot_dict["plan_label"] == x_planroot.plan_label
    assert planroot_dict["mass"] == x_planroot.mass
    assert len(planroot_dict[_kids]) == len(x_planroot._kids)


def test_BelieverUnit_get_dict_ReturnsObj_Scenario2_planroot_laborunit():
    # ESTABLISH
    run_str = "runners"
    sue_believer = believerunit_shop("Sue")
    x_laborunit = laborunit_shop()
    x_laborunit.set_laborlink(labor_title=run_str)
    root_rope = to_rope(sue_believer.belief_label)
    sue_believer.edit_plan_attr(root_rope, laborunit=x_laborunit)
    root_plan = sue_believer.get_plan_obj(root_rope)
    x_gogo_want = 5
    x_stop_want = 11
    root_plan.gogo_want = x_gogo_want
    root_plan.stop_want = x_stop_want

    # WHEN
    believer_dict = sue_believer.get_dict()
    planroot_dict = believer_dict.get("planroot")

    # THEN
    assert planroot_dict["laborunit"] == x_laborunit.get_dict()
    assert planroot_dict["laborunit"] == {"_laborlinks": [run_str]}
    assert planroot_dict.get("gogo_want") == x_gogo_want
    assert planroot_dict.get("stop_want") == x_stop_want


def test_BelieverUnit_get_dict_ReturnsObj_Scenario3_With_planroot_healerlink():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    yao_str = "Yao"
    sue_believer.add_partnerunit(yao_str)
    run_str = ";runners"
    yao_partnerunit = sue_believer.get_partner(yao_str)
    yao_partnerunit.add_membership(run_str)
    run_healerlink = healerlink_shop()
    run_healerlink.set_healer_name(x_healer_name=run_str)
    root_rope = to_rope(sue_believer.belief_label)
    sue_believer.edit_plan_attr(root_rope, healerlink=run_healerlink)

    # WHEN
    believer_dict = sue_believer.get_dict()
    planroot_dict = believer_dict.get("planroot")

    # THEN
    assert planroot_dict["healerlink"] == run_healerlink.get_dict()


def test_BelieverUnit_get_dict_ReturnsObj_Scenario4_plankid_LaborUnit():
    # ESTABLISH
    sue_believer = believerunit_shop("Sue")
    yao_str = "Yao"
    sue_believer.add_partnerunit(yao_str)
    run_str = ";runners"
    yao_partnerunit = sue_believer.get_partner(yao_str)
    yao_partnerunit.add_membership(run_str)

    morn_str = "morning"
    morn_rope = sue_believer.make_l1_rope(morn_str)
    sue_believer.set_l1_plan(planunit_shop(morn_str))
    x_laborunit = laborunit_shop()
    x_laborunit.set_laborlink(labor_title=run_str)
    sue_believer.edit_plan_attr(morn_rope, laborunit=x_laborunit)

    # WHEN
    believer_dict = sue_believer.get_dict()
    planroot_dict = believer_dict.get("planroot")

    # THEN
    _kids = "_kids"
    _laborunit = "laborunit"

    labor_dict_x = planroot_dict[_kids][morn_str][_laborunit]
    assert labor_dict_x == x_laborunit.get_dict()
    assert labor_dict_x == {"_laborlinks": [run_str]}


def test_BelieverUnit_get_json_ReturnsCorrectJSON_SimpleExample():
    # ESTABLISH
    zia_believer = get_believerunit_x1_3levels_1reason_1facts()
    x_fund_pool = 66000
    zia_believer.fund_pool = x_fund_pool
    x_fund_iota = 66
    zia_believer.fund_iota = x_fund_iota
    x_respect_bit = 7
    zia_believer.respect_bit = x_respect_bit
    x_penny = 0.3
    zia_believer.penny = x_penny
    override_str = "override"
    yao_str = "Yao"
    run_str = ";runners"
    zia_believer.add_partnerunit(yao_str)
    yao_partnerunit = zia_believer.get_partner(yao_str)
    yao_partnerunit.add_membership(run_str)
    run_healerlink = healerlink_shop({run_str})
    root_rope = to_rope(zia_believer.belief_label)
    zia_believer.edit_plan_attr(root_rope, healerlink=run_healerlink)
    zia_believer.edit_plan_attr(root_rope, problem_bool=True)

    # WHEN
    x_json = zia_believer.get_json()

    # THEN
    _kids = "_kids"

    assert x_json is not None
    assert True == x_is_json(x_json)
    believer_dict = get_dict_from_json(x_json)

    assert believer_dict["believer_name"] == zia_believer.believer_name
    assert believer_dict["belief_label"] == zia_believer.belief_label
    assert believer_dict["tally"] == zia_believer.tally
    assert believer_dict["fund_pool"] == zia_believer.fund_pool
    assert believer_dict["fund_iota"] == zia_believer.fund_iota
    assert believer_dict["respect_bit"] == zia_believer.respect_bit
    assert believer_dict["penny"] == zia_believer.penny
    assert believer_dict["credor_respect"] == zia_believer.credor_respect
    assert believer_dict["debtor_respect"] == zia_believer.debtor_respect
    # with pytest_raises(Exception) as excinfo:
    #     believer_dict["_credor_respect"]
    # assert str(excinfo.value) == "'_credor_respect'"
    # with pytest_raises(Exception) as excinfo:
    #     believer_dict["_debtor_respect"]
    # assert str(excinfo.value) == "'_debtor_respect'"
    with pytest_raises(Exception) as excinfo:
        believer_dict["last_pack_id"]

    x_planroot = zia_believer.planroot
    planroot_dict = believer_dict.get("planroot")

    assert len(planroot_dict[_kids]) == len(x_planroot._kids)

    shave_str = "shave"
    shave_dict = planroot_dict[_kids][shave_str]
    shave_factunits = shave_dict["factunits"]
    print(f"{shave_factunits=}")
    assert len(shave_factunits) == 1
    assert len(shave_factunits) == len(x_planroot._kids[shave_str].factunits)
    planroot_healerlink = planroot_dict["healerlink"]
    print(f"{planroot_healerlink=}")
    assert len(planroot_healerlink) == 1
    assert x_planroot.healerlink.any_healer_name_exists()
    assert x_planroot.problem_bool


def test_BelieverUnit_get_json_ReturnsCorrectJSON_BigExample():
    # ESTABLISH
    yao_believer = believerunit_v001()
    hr_number_str = "hr_number"
    hr_number_rope = yao_believer.make_l1_rope(hr_number_str)
    yao_believer.add_fact(
        f_context=hr_number_rope, f_state=hr_number_rope, f_lower=0, f_upper=23
    )
    day_min_str = "jour_minute"
    day_min_rope = yao_believer.make_l1_rope(day_min_str)
    yao_believer.add_fact(
        f_context=day_min_rope, f_state=day_min_rope, f_lower=0, f_upper=59
    )
    x_factunit = factunit_shop(day_min_rope, day_min_rope, 5, 59)
    yao_believer.edit_plan_attr(x_factunit.f_context, factunit=x_factunit)
    yao_believer.set_max_tree_traverse(2)
    yao_str = "Yao"

    # WHEN
    believer_dict = get_dict_from_json(yao_believer.get_json())

    # THEN
    _kids = "_kids"
    assert believer_dict["believer_name"] == yao_believer.believer_name
    assert believer_dict["belief_label"] == yao_believer.belief_label
    assert believer_dict["tally"] == yao_believer.tally
    assert believer_dict["max_tree_traverse"] == 2
    assert believer_dict["max_tree_traverse"] == yao_believer.max_tree_traverse
    assert believer_dict["knot"] == yao_believer.knot

    x_planroot = yao_believer.planroot
    planroot_dict = believer_dict.get("planroot")
    assert len(planroot_dict[_kids]) == len(x_planroot._kids)

    kids = planroot_dict[_kids]
    day_min_dict = kids[day_min_str]
    day_min_factunits_dict = day_min_dict["factunits"]
    day_min_plan_x = yao_believer.get_plan_obj(day_min_rope)
    print(f"{day_min_factunits_dict=}")
    assert len(day_min_factunits_dict) == 1
    assert len(day_min_factunits_dict) == len(day_min_plan_x.factunits)

    _reasonunits = "reasonunits"
    cont_str = "Freelancing"
    ulti_str = "Ultimate Frisbee"
    cont_rope = yao_believer.make_l1_rope(cont_str)
    ulti_rope = yao_believer.make_l1_rope(ulti_str)
    cont_plan = yao_believer.get_plan_obj(cont_rope)
    ulti_plan = yao_believer.get_plan_obj(ulti_rope)
    cont_reasonunits_dict = planroot_dict[_kids][cont_str][_reasonunits]
    ulti_reasonunits_dict = planroot_dict[_kids][ulti_str][_reasonunits]
    assert len(cont_reasonunits_dict) == len(cont_plan.reasonunits)
    assert len(ulti_reasonunits_dict) == len(ulti_plan.reasonunits)

    anna_str = "Anna"
    anna_partnerunit = yao_believer.get_partner(anna_str)
    assert anna_partnerunit.get_membership(";Family").group_cred_points == 6.2
    assert yao_believer.partners is not None
    assert len(yao_believer.partners) == 22


def test_believerunit_get_from_json_ReturnsObjSimpleExample():
    # ESTABLISH
    zia_believer = get_believerunit_x1_3levels_1reason_1facts()
    zia_believer.set_max_tree_traverse(23)
    tiger_belief_label = "tiger"
    zia_believer.set_belief_label(tiger_belief_label)
    zia_fund_pool = 80000
    zia_believer.fund_pool = zia_fund_pool
    zia_fund_iota = 8
    zia_believer.fund_iota = zia_fund_iota
    zia_resepect_bit = 5
    zia_believer.respect_bit = zia_resepect_bit
    zia_penny = 2
    zia_believer.penny = zia_penny
    zia_credor_respect = 200
    zia_debtor_respect = 200
    zia_believer.set_credor_respect(zia_credor_respect)
    zia_believer.set_debtor_respect(zia_debtor_respect)
    zia_last_pack_id = 73
    zia_believer.set_last_pack_id(zia_last_pack_id)

    shave_str = "shave"
    shave_rope = zia_believer.make_l1_rope(shave_str)
    shave_plan_y1 = zia_believer.get_plan_obj(shave_rope)
    shave_plan_y1.problem_bool = True
    # print(f"{shave_rope=}")
    # print(f"{json_shave_plan.plan_label=} {json_shave_plan.parent_rope=}")

    sue_str = "Sue"
    zia_believer.add_partnerunit(
        partner_name=sue_str, partner_cred_points=199, partner_debt_points=199
    )
    xio_str = "Xio"
    zia_believer.add_partnerunit(partner_name=xio_str)
    run_str = ";runners"
    sue_partnerunit = zia_believer.get_partner(sue_str)
    xio_partnerunit = zia_believer.get_partner(xio_str)
    sue_partnerunit.add_membership(run_str)
    xio_partnerunit.add_membership(run_str)
    run_laborunit = laborunit_shop()
    run_laborunit.set_laborlink(labor_title=run_str)
    root_rope = to_rope(zia_believer.belief_label)
    zia_believer.edit_plan_attr(root_rope, laborunit=run_laborunit)
    xio_laborunit = laborunit_shop()
    xio_laborunit.set_laborlink(labor_title=xio_str)
    zia_believer.edit_plan_attr(shave_rope, laborunit=xio_laborunit)
    zia_believer.edit_plan_attr(shave_rope, awardlink=awardlink_shop(xio_str))
    zia_believer.edit_plan_attr(shave_rope, awardlink=awardlink_shop(sue_str))
    zia_believer.edit_plan_attr(root_rope, awardlink=awardlink_shop(sue_str))
    # add healerlink to shave planunit
    run_healerlink = healerlink_shop({run_str})
    zia_believer.edit_plan_attr(shave_rope, healerlink=run_healerlink)
    shave_plan = zia_believer.get_plan_obj(shave_rope)
    zia_gogo_want = 75
    zia_stop_want = 77
    shave_plan.gogo_want = zia_gogo_want
    shave_plan.stop_want = zia_stop_want

    override_str = "override"

    # WHEN
    x_json = zia_believer.get_json()
    assert x_is_json(x_json) is True
    json_believer = believerunit_get_from_json(x_believer_json=x_json)

    # THEN
    assert str(type(json_believer)).find(".believer.BelieverUnit'>") > 0
    assert json_believer.believer_name is not None
    assert json_believer.believer_name == zia_believer.believer_name
    assert json_believer.belief_label == zia_believer.belief_label
    assert json_believer.fund_pool == zia_fund_pool
    assert json_believer.fund_pool == zia_believer.fund_pool
    assert json_believer.fund_iota == zia_fund_iota
    assert json_believer.fund_iota == zia_believer.fund_iota
    assert json_believer.respect_bit == zia_resepect_bit
    assert json_believer.respect_bit == zia_believer.respect_bit
    assert json_believer.penny == zia_penny
    assert json_believer.penny == zia_believer.penny
    assert json_believer.max_tree_traverse == 23
    assert json_believer.max_tree_traverse == zia_believer.max_tree_traverse
    assert json_believer.knot == zia_believer.knot
    assert json_believer.credor_respect == zia_believer.credor_respect
    assert json_believer.debtor_respect == zia_believer.debtor_respect
    assert json_believer.credor_respect == zia_credor_respect
    assert json_believer.debtor_respect == zia_debtor_respect
    assert json_believer.last_pack_id == zia_believer.last_pack_id
    assert json_believer.last_pack_id == zia_last_pack_id
    # assert json_believer._groups == zia_believer._groups

    json_planroot = json_believer.planroot
    assert json_planroot.parent_rope == ""
    assert json_planroot.parent_rope == zia_believer.planroot.parent_rope
    assert json_planroot.reasonunits == {}
    assert json_planroot.laborunit == zia_believer.planroot.laborunit
    assert json_planroot.laborunit == run_laborunit
    assert json_planroot.fund_iota == 8
    assert json_planroot.fund_iota == zia_fund_iota
    assert len(json_planroot.factunits) == 1
    assert len(json_planroot.awardlinks) == 1

    assert len(json_believer.planroot._kids) == 2

    sem_jour_str = "sem_jours"
    sem_jour_rope = json_believer.make_l1_rope(sem_jour_str)
    sem_jour_plan_x = json_believer.get_plan_obj(sem_jour_rope)
    assert len(sem_jour_plan_x._kids) == 2

    sun_str = "Sun"
    sun_rope = json_believer.make_rope(sem_jour_rope, sun_str)
    sun_plan = json_believer.get_plan_obj(sun_rope)
    assert sun_plan.mass == 20

    json_shave_plan = json_believer.get_plan_obj(shave_rope)
    zia_shave_plan = zia_believer.get_plan_obj(shave_rope)
    assert len(json_shave_plan.reasonunits) == 1
    assert json_shave_plan.laborunit == zia_shave_plan.laborunit
    assert json_shave_plan.laborunit == xio_laborunit
    print(f"{json_shave_plan.healerlink=}")
    assert json_shave_plan.healerlink == zia_shave_plan.healerlink
    assert len(json_shave_plan.awardlinks) == 2
    assert len(json_shave_plan.factunits) == 1
    assert zia_shave_plan.problem_bool
    assert json_shave_plan.problem_bool == zia_shave_plan.problem_bool
    assert json_shave_plan.gogo_want == zia_shave_plan.gogo_want
    assert json_shave_plan.stop_want == zia_shave_plan.stop_want


def test_believerunit_get_from_json_ReturnsCorrectPlanRoot():
    # ESTABLISH
    zia_believer = get_believerunit_x1_3levels_1reason_1facts()
    zia_believer.set_max_tree_traverse(23)
    # root_plan = zia_believer.get_plan_obj(zia_believer.get_plan_obj(zia_believer.belief_label))
    root_plan = zia_believer.planroot
    zia_gogo_want = 75
    zia_stop_want = 77
    root_plan.gogo_want = zia_gogo_want
    root_plan.stop_want = zia_stop_want

    # WHEN
    x_json = zia_believer.get_json()
    assert x_is_json(x_json) is True
    json_believer = believerunit_get_from_json(x_believer_json=x_json)

    # THEN
    json_planroot = json_believer.get_plan_obj(to_rope(zia_believer.belief_label))
    assert json_planroot.gogo_want == zia_gogo_want
    assert json_planroot.stop_want == zia_stop_want


def test_believerunit_get_from_json_ReturnsObj_knot_Example():
    # ESTABLISH
    slash_knot = "/"
    before_bob_believer = believerunit_shop("Bob", knot=slash_knot)
    assert before_bob_believer.knot != default_knot_if_None()

    # WHEN
    bob_json = before_bob_believer.get_json()
    after_bob_believer = believerunit_get_from_json(bob_json)

    # THEN
    assert after_bob_believer.knot != default_knot_if_None()
    assert after_bob_believer.knot == slash_knot
    assert after_bob_believer.knot == before_bob_believer.knot


def test_believerunit_get_from_json_ReturnsObj_knot_PartnerExample():
    # ESTABLISH
    slash_knot = "/"
    before_bob_believer = believerunit_shop("Bob", knot=slash_knot)
    bob_str = ",Bob"
    before_bob_believer.add_partnerunit(bob_str)
    assert before_bob_believer.partner_exists(bob_str)

    # WHEN
    bob_json = before_bob_believer.get_json()
    after_bob_believer = believerunit_get_from_json(bob_json)

    # THEN
    after_bob_partnerunit = after_bob_believer.get_partner(bob_str)
    assert after_bob_partnerunit.knot == slash_knot


def test_believerunit_get_from_json_ReturnsObj_knot_GroupExample():
    # ESTABLISH
    slash_knot = "/"
    before_bob_believer = believerunit_shop("Bob", knot=slash_knot)
    yao_str = "Yao"
    swim_str = f"{slash_knot}Swimmers"
    before_bob_believer.add_partnerunit(yao_str)
    yao_partnerunit = before_bob_believer.get_partner(yao_str)
    yao_partnerunit.add_membership(swim_str)

    # WHEN
    bob_json = before_bob_believer.get_json()
    after_bob_believer = believerunit_get_from_json(bob_json)

    # THEN
    after_yao_partnerunit = after_bob_believer.get_partner(yao_str)
    assert after_yao_partnerunit.knot == slash_knot


def test_believerunit_get_from_json_ReturnsObj_Scenario7_planroot_knot_IsCorrectlySet():
    # ESTABLISH
    slash_str = "/"
    run_str = "runners"
    sue_believer = believerunit_shop("Sue", knot=slash_str)
    root_rope = to_rope(sue_believer.belief_label, slash_str)
    hr_number_str = "hr_number"
    hr_number_rope = sue_believer.make_l1_rope(hr_number_str)
    sue_believer.add_plan(hr_number_rope)
    assert sue_believer.knot == slash_str
    assert sue_believer.get_plan_obj(root_rope).knot == slash_str
    assert sue_believer.get_plan_obj(hr_number_rope).knot == slash_str

    # WHEN
    after_bob_believer = believerunit_get_from_json(sue_believer.get_json())

    # THEN
    assert after_bob_believer.knot == slash_str
    assert after_bob_believer.get_plan_obj(root_rope).knot == slash_str
    assert after_bob_believer.get_plan_obj(hr_number_rope).knot == slash_str


def test_believerunit_get_from_json_ExportsBelieverUnit_mass():
    # ESTABLISH
    x1_believer = believerunit_v001()
    x1_believer.tally = 15
    assert x1_believer.tally == 15
    assert x1_believer.planroot.mass != x1_believer.tally
    assert x1_believer.planroot.mass == 1

    # WHEN
    x2_believer = believerunit_get_from_json(x1_believer.get_json())

    # THEN
    assert x1_believer.tally == 15
    assert x1_believer.tally == x2_believer.tally
    assert x1_believer.planroot.mass == 1
    assert x1_believer.planroot.mass == x2_believer.planroot.mass
    assert x1_believer.planroot._kids == x2_believer.planroot._kids


def test_get_dict_of_believer_from_dict_ReturnsDictOfBelieverUnits():
    # ESTABLISH
    x1_believer = believerunit_v001()
    x2_believer = get_believerunit_x1_3levels_1reason_1facts()
    x3_believer = get_believerunit_r_context_time_example()
    print(f"{x1_believer.believer_name}")
    print(f"{x2_believer.believer_name}")
    print(f"{x3_believer.believer_name}")

    cn_dict_of_dicts = {
        x1_believer.believer_name: x1_believer.get_dict(),
        x2_believer.believer_name: x2_believer.get_dict(),
        x3_believer.believer_name: x3_believer.get_dict(),
    }

    # WHEN
    ccn_dict_of_obj = get_dict_of_believer_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(x1_believer.believer_name) is not None
    assert ccn_dict_of_obj.get(x2_believer.believer_name) is not None
    assert ccn_dict_of_obj.get(x3_believer.believer_name) is not None

    ccn2_believer = ccn_dict_of_obj.get(x2_believer.believer_name)
    assert ccn2_believer.planroot.plan_label == x2_believer.planroot.plan_label
    assert ccn2_believer.planroot.parent_rope == x2_believer.planroot.parent_rope
    assert ccn2_believer.planroot.fund_iota == x2_believer.planroot.fund_iota
    shave_rope = ccn2_believer.make_l1_rope("shave")
    wk_rope = ccn2_believer.make_l1_rope("sem_jours")
    # assert ccn2_believer.get_plan_obj(shave_rope) == x2_believer.get_plan_obj(shave_rope)
    # assert ccn2_believer.get_plan_obj(wk_rope) == x2_believer.get_plan_obj(wk_rope)
    # assert ccn2_believer.planroot == x2_believer.planroot
    assert ccn2_believer.get_dict() == x2_believer.get_dict()

    ccn_believer3 = ccn_dict_of_obj.get(x3_believer.believer_name)
    assert ccn_believer3.get_dict() == x3_believer.get_dict()

    cc1_plan_root = ccn_dict_of_obj.get(x1_believer.believer_name).planroot
    ccn_believer1 = ccn_dict_of_obj.get(x1_believer.believer_name)
    assert ccn_believer1._plan_dict == x1_believer._plan_dict
    philipa_str = "Philipa"
    ccn_philipa_partnerunit = ccn_believer1.get_partner(philipa_str)
    x1_philipa_partnerunit = x1_believer.get_partner(philipa_str)
    assert ccn_philipa_partnerunit._memberships == x1_philipa_partnerunit._memberships
    assert ccn_believer1 == x1_believer
    assert ccn_dict_of_obj.get(x1_believer.believer_name) == x1_believer
