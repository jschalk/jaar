from pytest import raises as pytest_raises
from src.a00_data_toolbox.dict_toolbox import get_dict_from_json, x_is_json
from src.a01_term_logic.rope import default_knot_if_None, to_rope
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factunit_shop
from src.a04_reason_logic.reason_labor import laborunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a05_concept_logic.healer import healerlink_shop
from src.a06_plan_logic.plan import (
    get_dict_of_plan_from_dict,
    get_from_json as planunit_get_from_json,
    planunit_shop,
)
from src.a06_plan_logic.test._util.example_plans import (
    get_planunit_rcontext_time_example,
    get_planunit_x1_3levels_1reason_1facts,
    planunit_v001,
)


def test_PlanUnit_get_dict_ReturnsObj_Scenario1_large_json():
    # ESTABLISH
    yao_plan = planunit_v001()
    day_hr_str = "day_hr"
    day_hr_rope = yao_plan.make_l1_rope(day_hr_str)
    day_hr_concept = yao_plan.get_concept_obj(day_hr_rope)
    yao_plan.add_fact(fcontext=day_hr_rope, fstate=day_hr_rope, fopen=0, fnigh=23)
    time_minute = yao_plan.make_l1_rope("day_minute")
    yao_plan.add_fact(fcontext=time_minute, fstate=time_minute, fopen=0, fnigh=1440)
    yao_str = "Yao"
    yao_fund_pool = 23000
    yao_plan.fund_pool = yao_fund_pool
    yao_fund_iota = 23
    yao_plan.fund_iota = yao_fund_iota
    plan_tally = 23
    yao_plan.tally = plan_tally
    x_credor_respect = 22
    x_debtor_respect = 44
    yao_plan.set_credor_respect(x_credor_respect)
    yao_plan.set_debtor_respect(x_debtor_respect)
    override_str = "override"
    x_last_pack_id = 77
    yao_plan.set_last_pack_id(x_last_pack_id)

    # WHEN
    plan_dict = yao_plan.get_dict()

    # THEN
    assert plan_dict is not None
    assert str(type(plan_dict)) == "<class 'dict'>"
    assert plan_dict["owner_name"] == yao_plan.owner_name
    assert plan_dict["bank_label"] == yao_plan.bank_label
    assert plan_dict["tally"] == yao_plan.tally
    assert plan_dict["tally"] == plan_tally
    assert plan_dict["fund_pool"] == yao_fund_pool
    assert plan_dict["fund_iota"] == yao_fund_iota
    assert plan_dict["max_tree_traverse"] == yao_plan.max_tree_traverse
    assert plan_dict["knot"] == yao_plan.knot
    assert plan_dict["credor_respect"] == yao_plan.credor_respect
    assert plan_dict["debtor_respect"] == yao_plan.debtor_respect
    assert plan_dict["last_pack_id"] == yao_plan.last_pack_id
    assert len(plan_dict["accts"]) == len(yao_plan.accts)
    assert len(plan_dict["accts"]) != 12
    assert plan_dict.get("_groups") is None

    x_conceptroot = yao_plan.conceptroot
    conceptroot_dict = plan_dict["conceptroot"]
    _kids = "_kids"
    assert x_conceptroot.concept_label == yao_plan.bank_label
    assert conceptroot_dict["concept_label"] == x_conceptroot.concept_label
    assert conceptroot_dict["mass"] == x_conceptroot.mass
    assert len(conceptroot_dict[_kids]) == len(x_conceptroot._kids)


def test_PlanUnit_get_dict_ReturnsObj_Scenario2_conceptroot_laborunit():
    # ESTABLISH
    run_str = "runners"
    sue_plan = planunit_shop("Sue")
    x_laborunit = laborunit_shop()
    x_laborunit.set_laborlink(labor_title=run_str)
    root_rope = to_rope(sue_plan.bank_label)
    sue_plan.edit_concept_attr(root_rope, laborunit=x_laborunit)
    root_concept = sue_plan.get_concept_obj(root_rope)
    x_gogo_want = 5
    x_stop_want = 11
    root_concept.gogo_want = x_gogo_want
    root_concept.stop_want = x_stop_want

    # WHEN
    plan_dict = sue_plan.get_dict()
    conceptroot_dict = plan_dict.get("conceptroot")

    # THEN
    assert conceptroot_dict["laborunit"] == x_laborunit.get_dict()
    assert conceptroot_dict["laborunit"] == {"_laborlinks": [run_str]}
    assert conceptroot_dict.get("gogo_want") == x_gogo_want
    assert conceptroot_dict.get("stop_want") == x_stop_want


def test_PlanUnit_get_dict_ReturnsObj_Scenario3_With_conceptroot_healerlink():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    yao_str = "Yao"
    sue_plan.add_acctunit(yao_str)
    run_str = ";runners"
    yao_acctunit = sue_plan.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)
    run_healerlink = healerlink_shop()
    run_healerlink.set_healer_name(x_healer_name=run_str)
    root_rope = to_rope(sue_plan.bank_label)
    sue_plan.edit_concept_attr(root_rope, healerlink=run_healerlink)

    # WHEN
    plan_dict = sue_plan.get_dict()
    conceptroot_dict = plan_dict.get("conceptroot")

    # THEN
    assert conceptroot_dict["healerlink"] == run_healerlink.get_dict()


def test_PlanUnit_get_dict_ReturnsObj_Scenario4_conceptkid_LaborUnit():
    # ESTABLISH
    sue_plan = planunit_shop("Sue")
    yao_str = "Yao"
    sue_plan.add_acctunit(yao_str)
    run_str = ";runners"
    yao_acctunit = sue_plan.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)

    morn_str = "morning"
    morn_rope = sue_plan.make_l1_rope(morn_str)
    sue_plan.set_l1_concept(conceptunit_shop(morn_str))
    x_laborunit = laborunit_shop()
    x_laborunit.set_laborlink(labor_title=run_str)
    sue_plan.edit_concept_attr(morn_rope, laborunit=x_laborunit)

    # WHEN
    plan_dict = sue_plan.get_dict()
    conceptroot_dict = plan_dict.get("conceptroot")

    # THEN
    _kids = "_kids"
    _laborunit = "laborunit"

    labor_dict_x = conceptroot_dict[_kids][morn_str][_laborunit]
    assert labor_dict_x == x_laborunit.get_dict()
    assert labor_dict_x == {"_laborlinks": [run_str]}


def test_PlanUnit_get_json_ReturnsCorrectJSON_SimpleExample():
    # ESTABLISH
    zia_plan = get_planunit_x1_3levels_1reason_1facts()
    x_fund_pool = 66000
    zia_plan.fund_pool = x_fund_pool
    x_fund_iota = 66
    zia_plan.fund_iota = x_fund_iota
    x_respect_bit = 7
    zia_plan.respect_bit = x_respect_bit
    x_penny = 0.3
    zia_plan.penny = x_penny
    override_str = "override"
    yao_str = "Yao"
    run_str = ";runners"
    zia_plan.add_acctunit(yao_str)
    yao_acctunit = zia_plan.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)
    run_healerlink = healerlink_shop({run_str})
    root_rope = to_rope(zia_plan.bank_label)
    zia_plan.edit_concept_attr(root_rope, healerlink=run_healerlink)
    zia_plan.edit_concept_attr(root_rope, problem_bool=True)

    # WHEN
    x_json = zia_plan.get_json()

    # THEN
    _kids = "_kids"

    assert x_json is not None
    assert True == x_is_json(x_json)
    plan_dict = get_dict_from_json(x_json)

    assert plan_dict["owner_name"] == zia_plan.owner_name
    assert plan_dict["bank_label"] == zia_plan.bank_label
    assert plan_dict["tally"] == zia_plan.tally
    assert plan_dict["fund_pool"] == zia_plan.fund_pool
    assert plan_dict["fund_iota"] == zia_plan.fund_iota
    assert plan_dict["respect_bit"] == zia_plan.respect_bit
    assert plan_dict["penny"] == zia_plan.penny
    assert plan_dict["credor_respect"] == zia_plan.credor_respect
    assert plan_dict["debtor_respect"] == zia_plan.debtor_respect
    # with pytest_raises(Exception) as excinfo:
    #     plan_dict["_credor_respect"]
    # assert str(excinfo.value) == "'_credor_respect'"
    # with pytest_raises(Exception) as excinfo:
    #     plan_dict["_debtor_respect"]
    # assert str(excinfo.value) == "'_debtor_respect'"
    with pytest_raises(Exception) as excinfo:
        plan_dict["last_pack_id"]

    x_conceptroot = zia_plan.conceptroot
    conceptroot_dict = plan_dict.get("conceptroot")

    assert len(conceptroot_dict[_kids]) == len(x_conceptroot._kids)

    shave_str = "shave"
    shave_dict = conceptroot_dict[_kids][shave_str]
    shave_factunits = shave_dict["factunits"]
    print(f"{shave_factunits=}")
    assert len(shave_factunits) == 1
    assert len(shave_factunits) == len(x_conceptroot._kids[shave_str].factunits)
    conceptroot_healerlink = conceptroot_dict["healerlink"]
    print(f"{conceptroot_healerlink=}")
    assert len(conceptroot_healerlink) == 1
    assert x_conceptroot.healerlink.any_healer_name_exists()
    assert x_conceptroot.problem_bool


def test_PlanUnit_get_json_ReturnsCorrectJSON_BigExample():
    # ESTABLISH
    yao_plan = planunit_v001()
    day_hr_str = "day_hr"
    day_hr_rope = yao_plan.make_l1_rope(day_hr_str)
    yao_plan.add_fact(fcontext=day_hr_rope, fstate=day_hr_rope, fopen=0, fnigh=23)
    day_min_str = "day_minute"
    day_min_rope = yao_plan.make_l1_rope(day_min_str)
    yao_plan.add_fact(fcontext=day_min_rope, fstate=day_min_rope, fopen=0, fnigh=59)
    x_factunit = factunit_shop(day_min_rope, day_min_rope, 5, 59)
    yao_plan.edit_concept_attr(x_factunit.fcontext, factunit=x_factunit)
    yao_plan.set_max_tree_traverse(2)
    yao_str = "Yao"

    # WHEN
    plan_dict = get_dict_from_json(yao_plan.get_json())

    # THEN
    _kids = "_kids"
    assert plan_dict["owner_name"] == yao_plan.owner_name
    assert plan_dict["bank_label"] == yao_plan.bank_label
    assert plan_dict["tally"] == yao_plan.tally
    assert plan_dict["max_tree_traverse"] == 2
    assert plan_dict["max_tree_traverse"] == yao_plan.max_tree_traverse
    assert plan_dict["knot"] == yao_plan.knot

    x_conceptroot = yao_plan.conceptroot
    conceptroot_dict = plan_dict.get("conceptroot")
    assert len(conceptroot_dict[_kids]) == len(x_conceptroot._kids)

    kids = conceptroot_dict[_kids]
    day_min_dict = kids[day_min_str]
    day_min_factunits_dict = day_min_dict["factunits"]
    day_min_concept_x = yao_plan.get_concept_obj(day_min_rope)
    print(f"{day_min_factunits_dict=}")
    assert len(day_min_factunits_dict) == 1
    assert len(day_min_factunits_dict) == len(day_min_concept_x.factunits)

    _reasonunits = "reasonunits"
    cont_str = "Freelancing"
    ulti_str = "Ultimate Frisbee"
    cont_rope = yao_plan.make_l1_rope(cont_str)
    ulti_rope = yao_plan.make_l1_rope(ulti_str)
    cont_concept = yao_plan.get_concept_obj(cont_rope)
    ulti_concept = yao_plan.get_concept_obj(ulti_rope)
    cont_reasonunits_dict = conceptroot_dict[_kids][cont_str][_reasonunits]
    ulti_reasonunits_dict = conceptroot_dict[_kids][ulti_str][_reasonunits]
    assert len(cont_reasonunits_dict) == len(cont_concept.reasonunits)
    assert len(ulti_reasonunits_dict) == len(ulti_concept.reasonunits)

    anna_str = "Anna"
    anna_acctunit = yao_plan.get_acct(anna_str)
    assert anna_acctunit.get_membership(";Family").group_cred_points == 6.2
    assert yao_plan.accts is not None
    assert len(yao_plan.accts) == 22


def test_planunit_get_from_json_ReturnsObjSimpleExample():
    # ESTABLISH
    zia_plan = get_planunit_x1_3levels_1reason_1facts()
    zia_plan.set_max_tree_traverse(23)
    tiger_bank_label = "tiger"
    zia_plan.set_bank_label(tiger_bank_label)
    zia_fund_pool = 80000
    zia_plan.fund_pool = zia_fund_pool
    zia_fund_iota = 8
    zia_plan.fund_iota = zia_fund_iota
    zia_resepect_bit = 5
    zia_plan.respect_bit = zia_resepect_bit
    zia_penny = 2
    zia_plan.penny = zia_penny
    zia_credor_respect = 200
    zia_debtor_respect = 200
    zia_plan.set_credor_respect(zia_credor_respect)
    zia_plan.set_debtor_respect(zia_debtor_respect)
    zia_last_pack_id = 73
    zia_plan.set_last_pack_id(zia_last_pack_id)

    shave_str = "shave"
    shave_rope = zia_plan.make_l1_rope(shave_str)
    shave_concept_y1 = zia_plan.get_concept_obj(shave_rope)
    shave_concept_y1.problem_bool = True
    # print(f"{shave_rope=}")
    # print(f"{json_shave_concept.concept_label=} {json_shave_concept.parent_rope=}")

    sue_str = "Sue"
    zia_plan.add_acctunit(acct_name=sue_str, acct_cred_points=199, acct_debt_points=199)
    xio_str = "Xio"
    zia_plan.add_acctunit(acct_name=xio_str)
    run_str = ";runners"
    sue_acctunit = zia_plan.get_acct(sue_str)
    xio_acctunit = zia_plan.get_acct(xio_str)
    sue_acctunit.add_membership(run_str)
    xio_acctunit.add_membership(run_str)
    run_laborunit = laborunit_shop()
    run_laborunit.set_laborlink(labor_title=run_str)
    root_rope = to_rope(zia_plan.bank_label)
    zia_plan.edit_concept_attr(root_rope, laborunit=run_laborunit)
    xio_laborunit = laborunit_shop()
    xio_laborunit.set_laborlink(labor_title=xio_str)
    zia_plan.edit_concept_attr(shave_rope, laborunit=xio_laborunit)
    zia_plan.edit_concept_attr(shave_rope, awardlink=awardlink_shop(xio_str))
    zia_plan.edit_concept_attr(shave_rope, awardlink=awardlink_shop(sue_str))
    zia_plan.edit_concept_attr(root_rope, awardlink=awardlink_shop(sue_str))
    # add healerlink to shave conceptunit
    run_healerlink = healerlink_shop({run_str})
    zia_plan.edit_concept_attr(shave_rope, healerlink=run_healerlink)
    shave_concept = zia_plan.get_concept_obj(shave_rope)
    zia_gogo_want = 75
    zia_stop_want = 77
    shave_concept.gogo_want = zia_gogo_want
    shave_concept.stop_want = zia_stop_want

    override_str = "override"

    # WHEN
    x_json = zia_plan.get_json()
    assert x_is_json(x_json) is True
    json_plan = planunit_get_from_json(x_plan_json=x_json)

    # THEN
    assert str(type(json_plan)).find(".plan.PlanUnit'>") > 0
    assert json_plan.owner_name is not None
    assert json_plan.owner_name == zia_plan.owner_name
    assert json_plan.bank_label == zia_plan.bank_label
    assert json_plan.fund_pool == zia_fund_pool
    assert json_plan.fund_pool == zia_plan.fund_pool
    assert json_plan.fund_iota == zia_fund_iota
    assert json_plan.fund_iota == zia_plan.fund_iota
    assert json_plan.respect_bit == zia_resepect_bit
    assert json_plan.respect_bit == zia_plan.respect_bit
    assert json_plan.penny == zia_penny
    assert json_plan.penny == zia_plan.penny
    assert json_plan.max_tree_traverse == 23
    assert json_plan.max_tree_traverse == zia_plan.max_tree_traverse
    assert json_plan.knot == zia_plan.knot
    assert json_plan.credor_respect == zia_plan.credor_respect
    assert json_plan.debtor_respect == zia_plan.debtor_respect
    assert json_plan.credor_respect == zia_credor_respect
    assert json_plan.debtor_respect == zia_debtor_respect
    assert json_plan.last_pack_id == zia_plan.last_pack_id
    assert json_plan.last_pack_id == zia_last_pack_id
    # assert json_plan._groups == zia_plan._groups

    json_conceptroot = json_plan.conceptroot
    assert json_conceptroot.parent_rope == ""
    assert json_conceptroot.parent_rope == zia_plan.conceptroot.parent_rope
    assert json_conceptroot.reasonunits == {}
    assert json_conceptroot.laborunit == zia_plan.conceptroot.laborunit
    assert json_conceptroot.laborunit == run_laborunit
    assert json_conceptroot.fund_iota == 8
    assert json_conceptroot.fund_iota == zia_fund_iota
    assert len(json_conceptroot.factunits) == 1
    assert len(json_conceptroot.awardlinks) == 1

    assert len(json_plan.conceptroot._kids) == 2

    wkday_str = "wkdays"
    wkday_rope = json_plan.make_l1_rope(wkday_str)
    wkday_concept_x = json_plan.get_concept_obj(wkday_rope)
    assert len(wkday_concept_x._kids) == 2

    sunday_str = "Sunday"
    sunday_rope = json_plan.make_rope(wkday_rope, sunday_str)
    sunday_concept = json_plan.get_concept_obj(sunday_rope)
    assert sunday_concept.mass == 20

    json_shave_concept = json_plan.get_concept_obj(shave_rope)
    zia_shave_concept = zia_plan.get_concept_obj(shave_rope)
    assert len(json_shave_concept.reasonunits) == 1
    assert json_shave_concept.laborunit == zia_shave_concept.laborunit
    assert json_shave_concept.laborunit == xio_laborunit
    print(f"{json_shave_concept.healerlink=}")
    assert json_shave_concept.healerlink == zia_shave_concept.healerlink
    assert len(json_shave_concept.awardlinks) == 2
    assert len(json_shave_concept.factunits) == 1
    assert zia_shave_concept.problem_bool
    assert json_shave_concept.problem_bool == zia_shave_concept.problem_bool
    assert json_shave_concept.gogo_want == zia_shave_concept.gogo_want
    assert json_shave_concept.stop_want == zia_shave_concept.stop_want


def test_planunit_get_from_json_ReturnsCorrectConceptRoot():
    # ESTABLISH
    zia_plan = get_planunit_x1_3levels_1reason_1facts()
    zia_plan.set_max_tree_traverse(23)
    # root_concept = zia_plan.get_concept_obj(zia_plan.get_concept_obj(zia_plan.bank_label))
    root_concept = zia_plan.conceptroot
    zia_gogo_want = 75
    zia_stop_want = 77
    root_concept.gogo_want = zia_gogo_want
    root_concept.stop_want = zia_stop_want

    # WHEN
    x_json = zia_plan.get_json()
    assert x_is_json(x_json) is True
    json_plan = planunit_get_from_json(x_plan_json=x_json)

    # THEN
    json_conceptroot = json_plan.get_concept_obj(to_rope(zia_plan.bank_label))
    assert json_conceptroot.gogo_want == zia_gogo_want
    assert json_conceptroot.stop_want == zia_stop_want


def test_planunit_get_from_json_ReturnsObj_knot_Example():
    # ESTABLISH
    slash_knot = "/"
    before_bob_plan = planunit_shop("Bob", knot=slash_knot)
    assert before_bob_plan.knot != default_knot_if_None()

    # WHEN
    bob_json = before_bob_plan.get_json()
    after_bob_plan = planunit_get_from_json(bob_json)

    # THEN
    assert after_bob_plan.knot != default_knot_if_None()
    assert after_bob_plan.knot == slash_knot
    assert after_bob_plan.knot == before_bob_plan.knot


def test_planunit_get_from_json_ReturnsObj_knot_AcctExample():
    # ESTABLISH
    slash_knot = "/"
    before_bob_plan = planunit_shop("Bob", knot=slash_knot)
    bob_str = ",Bob"
    before_bob_plan.add_acctunit(bob_str)
    assert before_bob_plan.acct_exists(bob_str)

    # WHEN
    bob_json = before_bob_plan.get_json()
    after_bob_plan = planunit_get_from_json(bob_json)

    # THEN
    after_bob_acctunit = after_bob_plan.get_acct(bob_str)
    assert after_bob_acctunit.knot == slash_knot


def test_planunit_get_from_json_ReturnsObj_knot_GroupExample():
    # ESTABLISH
    slash_knot = "/"
    before_bob_plan = planunit_shop("Bob", knot=slash_knot)
    yao_str = "Yao"
    swim_str = f"{slash_knot}Swimmers"
    before_bob_plan.add_acctunit(yao_str)
    yao_acctunit = before_bob_plan.get_acct(yao_str)
    yao_acctunit.add_membership(swim_str)

    # WHEN
    bob_json = before_bob_plan.get_json()
    after_bob_plan = planunit_get_from_json(bob_json)

    # THEN
    after_yao_acctunit = after_bob_plan.get_acct(yao_str)
    assert after_yao_acctunit.knot == slash_knot


def test_planunit_get_from_json_ReturnsObj_Scenario7_conceptroot_knot_IsCorrectlySet():
    # ESTABLISH
    slash_str = "/"
    run_str = "runners"
    sue_plan = planunit_shop("Sue", knot=slash_str)
    root_rope = to_rope(sue_plan.bank_label, slash_str)
    day_hr_str = "day_hr"
    day_hr_rope = sue_plan.make_l1_rope(day_hr_str)
    sue_plan.add_concept(day_hr_rope)
    assert sue_plan.knot == slash_str
    assert sue_plan.get_concept_obj(root_rope).knot == slash_str
    assert sue_plan.get_concept_obj(day_hr_rope).knot == slash_str

    # WHEN
    after_bob_plan = planunit_get_from_json(sue_plan.get_json())

    # THEN
    assert after_bob_plan.knot == slash_str
    assert after_bob_plan.get_concept_obj(root_rope).knot == slash_str
    assert after_bob_plan.get_concept_obj(day_hr_rope).knot == slash_str


def test_planunit_get_from_json_ExportsPlanUnit_mass():
    # ESTABLISH
    x1_plan = planunit_v001()
    x1_plan.tally = 15
    assert x1_plan.tally == 15
    assert x1_plan.conceptroot.mass != x1_plan.tally
    assert x1_plan.conceptroot.mass == 1

    # WHEN
    x2_plan = planunit_get_from_json(x1_plan.get_json())

    # THEN
    assert x1_plan.tally == 15
    assert x1_plan.tally == x2_plan.tally
    assert x1_plan.conceptroot.mass == 1
    assert x1_plan.conceptroot.mass == x2_plan.conceptroot.mass
    assert x1_plan.conceptroot._kids == x2_plan.conceptroot._kids


def test_get_dict_of_plan_from_dict_ReturnsDictOfPlanUnits():
    # ESTABLISH
    x1_plan = planunit_v001()
    x2_plan = get_planunit_x1_3levels_1reason_1facts()
    x3_plan = get_planunit_rcontext_time_example()
    print(f"{x1_plan.owner_name}")
    print(f"{x2_plan.owner_name}")
    print(f"{x3_plan.owner_name}")

    cn_dict_of_dicts = {
        x1_plan.owner_name: x1_plan.get_dict(),
        x2_plan.owner_name: x2_plan.get_dict(),
        x3_plan.owner_name: x3_plan.get_dict(),
    }

    # WHEN
    ccn_dict_of_obj = get_dict_of_plan_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(x1_plan.owner_name) is not None
    assert ccn_dict_of_obj.get(x2_plan.owner_name) is not None
    assert ccn_dict_of_obj.get(x3_plan.owner_name) is not None

    ccn2_plan = ccn_dict_of_obj.get(x2_plan.owner_name)
    assert ccn2_plan.conceptroot.concept_label == x2_plan.conceptroot.concept_label
    assert ccn2_plan.conceptroot.parent_rope == x2_plan.conceptroot.parent_rope
    assert ccn2_plan.conceptroot.fund_iota == x2_plan.conceptroot.fund_iota
    shave_rope = ccn2_plan.make_l1_rope("shave")
    wk_rope = ccn2_plan.make_l1_rope("wkdays")
    # assert ccn2_plan.get_concept_obj(shave_rope) == x2_plan.get_concept_obj(shave_rope)
    # assert ccn2_plan.get_concept_obj(wk_rope) == x2_plan.get_concept_obj(wk_rope)
    # assert ccn2_plan.conceptroot == x2_plan.conceptroot
    assert ccn2_plan.get_dict() == x2_plan.get_dict()

    ccn_plan3 = ccn_dict_of_obj.get(x3_plan.owner_name)
    assert ccn_plan3.get_dict() == x3_plan.get_dict()

    cc1_concept_root = ccn_dict_of_obj.get(x1_plan.owner_name).conceptroot
    ccn_plan1 = ccn_dict_of_obj.get(x1_plan.owner_name)
    assert ccn_plan1._concept_dict == x1_plan._concept_dict
    philipa_str = "Philipa"
    ccn_philipa_acctunit = ccn_plan1.get_acct(philipa_str)
    x1_philipa_acctunit = x1_plan.get_acct(philipa_str)
    assert ccn_philipa_acctunit._memberships == x1_philipa_acctunit._memberships
    assert ccn_plan1 == x1_plan
    assert ccn_dict_of_obj.get(x1_plan.owner_name) == x1_plan
