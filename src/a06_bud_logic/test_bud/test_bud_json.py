from pytest import raises as pytest_raises
from src.a00_data_toolbox.dict_toolbox import get_dict_from_json, x_is_json
from src.a01_term_logic.way import default_bridge_if_None, to_way
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factunit_shop
from src.a04_reason_logic.reason_labor import laborunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a05_concept_logic.healer import healerlink_shop
from src.a06_bud_logic._test_util.example_buds import (
    budunit_v001,
    get_budunit_rcontext_time_example,
    get_budunit_x1_3levels_1reason_1facts,
)
from src.a06_bud_logic.bud import (
    budunit_shop,
    get_dict_of_bud_from_dict,
    get_from_json as budunit_get_from_json,
)


def test_BudUnit_get_dict_ReturnsObj_Scenario1_large_json():
    # ESTABLISH
    yao_bud = budunit_v001()
    day_hr_str = "day_hr"
    day_hr_way = yao_bud.make_l1_way(day_hr_str)
    day_hr_concept = yao_bud.get_concept_obj(day_hr_way)
    day_hr_concept._originunit.set_originhold(acct_name="Bob", importance=2)
    yao_bud.add_fact(fcontext=day_hr_way, fstate=day_hr_way, fopen=0, fnigh=23)
    time_minute = yao_bud.make_l1_way("day_minute")
    yao_bud.add_fact(fcontext=time_minute, fstate=time_minute, fopen=0, fnigh=1440)
    yao_str = "Yao"
    yao_bud.originunit.set_originhold(yao_str, 1)
    yao_fund_pool = 23000
    yao_bud.fund_pool = yao_fund_pool
    yao_fund_iota = 23
    yao_bud.fund_iota = yao_fund_iota
    bud_tally = 23
    yao_bud.tally = bud_tally
    x_credor_respect = 22
    x_debtor_respect = 44
    yao_bud.set_credor_respect(x_credor_respect)
    yao_bud.set_debtor_respect(x_debtor_respect)
    override_str = "override"
    x_last_pack_id = 77
    yao_bud.set_last_pack_id(x_last_pack_id)

    # WHEN
    bud_dict = yao_bud.get_dict()

    # THEN
    assert bud_dict is not None
    assert str(type(bud_dict)) == "<class 'dict'>"
    assert bud_dict["owner_name"] == yao_bud.owner_name
    assert bud_dict["fisc_label"] == yao_bud.fisc_label
    assert bud_dict["tally"] == yao_bud.tally
    assert bud_dict["tally"] == bud_tally
    assert bud_dict["fund_pool"] == yao_fund_pool
    assert bud_dict["fund_iota"] == yao_fund_iota
    assert bud_dict["max_tree_traverse"] == yao_bud.max_tree_traverse
    assert bud_dict["bridge"] == yao_bud.bridge
    assert bud_dict["credor_respect"] == yao_bud.credor_respect
    assert bud_dict["debtor_respect"] == yao_bud.debtor_respect
    assert bud_dict["last_pack_id"] == yao_bud.last_pack_id
    assert len(bud_dict["accts"]) == len(yao_bud.accts)
    assert len(bud_dict["accts"]) != 12
    assert bud_dict.get("_groups") is None

    x_conceptroot = yao_bud.conceptroot
    conceptroot_dict = bud_dict["conceptroot"]
    _kids = "_kids"
    assert x_conceptroot.concept_label == yao_bud.fisc_label
    assert conceptroot_dict["concept_label"] == x_conceptroot.concept_label
    assert conceptroot_dict["mass"] == x_conceptroot.mass
    assert len(conceptroot_dict[_kids]) == len(x_conceptroot._kids)

    originunit_str = "originunit"
    day_hr_originunit_dict = conceptroot_dict[_kids][day_hr_str][originunit_str]
    assert day_hr_originunit_dict == day_hr_concept._originunit.get_dict()
    originholds_str = "_originholds"
    yao_bud_originhold = bud_dict[originunit_str][originholds_str][yao_str]
    print(f"{yao_bud_originhold=}")
    assert yao_bud_originhold
    assert yao_bud_originhold["acct_name"] == yao_str
    assert yao_bud_originhold["importance"] == 1


def test_BudUnit_get_dict_ReturnsObj_Scenario2_conceptroot_laborunit():
    # ESTABLISH
    run_str = "runners"
    sue_bud = budunit_shop("Sue")
    x_laborunit = laborunit_shop()
    x_laborunit.set_laborlink(labor_title=run_str)
    root_way = to_way(sue_bud.fisc_label)
    sue_bud.edit_concept_attr(root_way, laborunit=x_laborunit)
    root_concept = sue_bud.get_concept_obj(root_way)
    x_gogo_want = 5
    x_stop_want = 11
    root_concept.gogo_want = x_gogo_want
    root_concept.stop_want = x_stop_want

    # WHEN
    bud_dict = sue_bud.get_dict()
    conceptroot_dict = bud_dict.get("conceptroot")

    # THEN
    assert conceptroot_dict["laborunit"] == x_laborunit.get_dict()
    assert conceptroot_dict["laborunit"] == {"_laborlinks": [run_str]}
    assert conceptroot_dict.get("gogo_want") == x_gogo_want
    assert conceptroot_dict.get("stop_want") == x_stop_want


def test_BudUnit_get_dict_ReturnsObj_Scenario3_With_conceptroot_healerlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_str = "Yao"
    sue_bud.add_acctunit(yao_str)
    run_str = ";runners"
    yao_acctunit = sue_bud.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)
    run_healerlink = healerlink_shop()
    run_healerlink.set_healer_name(x_healer_name=run_str)
    root_way = to_way(sue_bud.fisc_label)
    sue_bud.edit_concept_attr(root_way, healerlink=run_healerlink)

    # WHEN
    bud_dict = sue_bud.get_dict()
    conceptroot_dict = bud_dict.get("conceptroot")

    # THEN
    assert conceptroot_dict["healerlink"] == run_healerlink.get_dict()


def test_BudUnit_get_dict_ReturnsObj_Scenario4_conceptkid_LaborUnit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_str = "Yao"
    sue_bud.add_acctunit(yao_str)
    run_str = ";runners"
    yao_acctunit = sue_bud.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)

    morn_str = "morning"
    morn_way = sue_bud.make_l1_way(morn_str)
    sue_bud.set_l1_concept(conceptunit_shop(morn_str))
    x_laborunit = laborunit_shop()
    x_laborunit.set_laborlink(labor_title=run_str)
    sue_bud.edit_concept_attr(morn_way, laborunit=x_laborunit)

    # WHEN
    bud_dict = sue_bud.get_dict()
    conceptroot_dict = bud_dict.get("conceptroot")

    # THEN
    _kids = "_kids"
    _laborunit = "laborunit"

    labor_dict_x = conceptroot_dict[_kids][morn_str][_laborunit]
    assert labor_dict_x == x_laborunit.get_dict()
    assert labor_dict_x == {"_laborlinks": [run_str]}


def test_BudUnit_get_json_ReturnsCorrectJSON_SimpleExample():
    # ESTABLISH
    zia_bud = get_budunit_x1_3levels_1reason_1facts()
    x_fund_pool = 66000
    zia_bud.fund_pool = x_fund_pool
    x_fund_iota = 66
    zia_bud.fund_iota = x_fund_iota
    x_respect_bit = 7
    zia_bud.respect_bit = x_respect_bit
    x_penny = 0.3
    zia_bud.penny = x_penny
    override_str = "override"
    yao_str = "Yao"
    run_str = ";runners"
    zia_bud.add_acctunit(yao_str)
    yao_acctunit = zia_bud.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)
    run_healerlink = healerlink_shop({run_str})
    root_way = to_way(zia_bud.fisc_label)
    zia_bud.edit_concept_attr(root_way, healerlink=run_healerlink)
    zia_bud.edit_concept_attr(root_way, problem_bool=True)

    # WHEN
    x_json = zia_bud.get_json()

    # THEN
    _kids = "_kids"

    assert x_json is not None
    assert True == x_is_json(x_json)
    bud_dict = get_dict_from_json(x_json)

    assert bud_dict["owner_name"] == zia_bud.owner_name
    assert bud_dict["fisc_label"] == zia_bud.fisc_label
    assert bud_dict["tally"] == zia_bud.tally
    assert bud_dict["fund_pool"] == zia_bud.fund_pool
    assert bud_dict["fund_iota"] == zia_bud.fund_iota
    assert bud_dict["respect_bit"] == zia_bud.respect_bit
    assert bud_dict["penny"] == zia_bud.penny
    assert bud_dict["credor_respect"] == zia_bud.credor_respect
    assert bud_dict["debtor_respect"] == zia_bud.debtor_respect
    # with pytest_raises(Exception) as excinfo:
    #     bud_dict["_credor_respect"]
    # assert str(excinfo.value) == "'_credor_respect'"
    # with pytest_raises(Exception) as excinfo:
    #     bud_dict["_debtor_respect"]
    # assert str(excinfo.value) == "'_debtor_respect'"
    with pytest_raises(Exception) as excinfo:
        bud_dict["last_pack_id"]

    x_conceptroot = zia_bud.conceptroot
    conceptroot_dict = bud_dict.get("conceptroot")

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


def test_BudUnit_get_json_ReturnsCorrectJSON_BigExample():
    # ESTABLISH
    yao_bud = budunit_v001()
    day_hr_str = "day_hr"
    day_hr_way = yao_bud.make_l1_way(day_hr_str)
    yao_bud.add_fact(fcontext=day_hr_way, fstate=day_hr_way, fopen=0, fnigh=23)
    day_min_str = "day_minute"
    day_min_way = yao_bud.make_l1_way(day_min_str)
    yao_bud.add_fact(fcontext=day_min_way, fstate=day_min_way, fopen=0, fnigh=59)
    x_factunit = factunit_shop(day_min_way, day_min_way, 5, 59)
    yao_bud.edit_concept_attr(x_factunit.fcontext, factunit=x_factunit)
    yao_bud.set_max_tree_traverse(2)
    yao_str = "Yao"
    yao_bud.originunit.set_originhold(yao_str, 1)

    # WHEN
    bud_dict = get_dict_from_json(yao_bud.get_json())

    # THEN
    _kids = "_kids"
    assert bud_dict["owner_name"] == yao_bud.owner_name
    assert bud_dict["fisc_label"] == yao_bud.fisc_label
    assert bud_dict["tally"] == yao_bud.tally
    assert bud_dict["max_tree_traverse"] == 2
    assert bud_dict["max_tree_traverse"] == yao_bud.max_tree_traverse
    assert bud_dict["bridge"] == yao_bud.bridge

    x_conceptroot = yao_bud.conceptroot
    conceptroot_dict = bud_dict.get("conceptroot")
    assert len(conceptroot_dict[_kids]) == len(x_conceptroot._kids)

    kids = conceptroot_dict[_kids]
    day_min_dict = kids[day_min_str]
    day_min_factunits_dict = day_min_dict["factunits"]
    day_min_concept_x = yao_bud.get_concept_obj(day_min_way)
    print(f"{day_min_factunits_dict=}")
    assert len(day_min_factunits_dict) == 1
    assert len(day_min_factunits_dict) == len(day_min_concept_x.factunits)

    _reasonunits = "reasonunits"
    cont_str = "Freelancing"
    ulti_str = "Ultimate Frisbee"
    cont_way = yao_bud.make_l1_way(cont_str)
    ulti_way = yao_bud.make_l1_way(ulti_str)
    cont_concept = yao_bud.get_concept_obj(cont_way)
    ulti_concept = yao_bud.get_concept_obj(ulti_way)
    cont_reasonunits_dict = conceptroot_dict[_kids][cont_str][_reasonunits]
    ulti_reasonunits_dict = conceptroot_dict[_kids][ulti_str][_reasonunits]
    assert len(cont_reasonunits_dict) == len(cont_concept.reasonunits)
    assert len(ulti_reasonunits_dict) == len(ulti_concept.reasonunits)
    originunit_str = "originunit"
    originholds_str = "_originholds"
    assert len(bud_dict[originunit_str][originholds_str])

    anna_str = "Anna"
    anna_acctunit = yao_bud.get_acct(anna_str)
    assert anna_acctunit.get_membership(";Family").credit_vote == 6.2
    assert yao_bud.accts is not None
    assert len(yao_bud.accts) == 22


def test_budunit_get_from_json_ReturnsObjSimpleExample():
    # ESTABLISH
    zia_bud = get_budunit_x1_3levels_1reason_1facts()
    zia_bud.set_max_tree_traverse(23)
    tiger_fisc_label = "tiger"
    zia_bud.set_fisc_label(tiger_fisc_label)
    zia_fund_pool = 80000
    zia_bud.fund_pool = zia_fund_pool
    zia_fund_iota = 8
    zia_bud.fund_iota = zia_fund_iota
    zia_resepect_bit = 5
    zia_bud.respect_bit = zia_resepect_bit
    zia_penny = 2
    zia_bud.penny = zia_penny
    zia_credor_respect = 200
    zia_debtor_respect = 200
    zia_bud.set_credor_respect(zia_credor_respect)
    zia_bud.set_debtor_respect(zia_debtor_respect)
    zia_last_pack_id = 73
    zia_bud.set_last_pack_id(zia_last_pack_id)

    shave_str = "shave"
    shave_way = zia_bud.make_l1_way(shave_str)
    shave_concept_y1 = zia_bud.get_concept_obj(shave_way)
    shave_concept_y1._originunit.set_originhold(acct_name="Sue", importance=4.3)
    shave_concept_y1.problem_bool = True
    # print(f"{shave_way=}")
    # print(f"{json_shave_concept.concept_label=} {json_shave_concept.parent_way=}")

    sue_str = "Sue"
    zia_bud.add_acctunit(acct_name=sue_str, credit_belief=199, debtit_belief=199)
    xio_str = "Xio"
    zia_bud.add_acctunit(acct_name=xio_str)
    run_str = ";runners"
    sue_acctunit = zia_bud.get_acct(sue_str)
    xio_acctunit = zia_bud.get_acct(xio_str)
    sue_acctunit.add_membership(run_str)
    xio_acctunit.add_membership(run_str)
    run_laborunit = laborunit_shop()
    run_laborunit.set_laborlink(labor_title=run_str)
    root_way = to_way(zia_bud.fisc_label)
    zia_bud.edit_concept_attr(root_way, laborunit=run_laborunit)
    xio_laborunit = laborunit_shop()
    xio_laborunit.set_laborlink(labor_title=xio_str)
    zia_bud.edit_concept_attr(shave_way, laborunit=xio_laborunit)
    zia_bud.edit_concept_attr(shave_way, awardlink=awardlink_shop(xio_str))
    zia_bud.edit_concept_attr(shave_way, awardlink=awardlink_shop(sue_str))
    zia_bud.edit_concept_attr(root_way, awardlink=awardlink_shop(sue_str))
    # add healerlink to shave conceptunit
    run_healerlink = healerlink_shop({run_str})
    zia_bud.edit_concept_attr(shave_way, healerlink=run_healerlink)
    shave_concept = zia_bud.get_concept_obj(shave_way)
    zia_gogo_want = 75
    zia_stop_want = 77
    shave_concept.gogo_want = zia_gogo_want
    shave_concept.stop_want = zia_stop_want

    yao_str = "Yao"
    zia_bud.originunit.set_originhold(yao_str, 1)
    override_str = "override"

    # WHEN
    x_json = zia_bud.get_json()
    assert x_is_json(x_json) is True
    json_bud = budunit_get_from_json(x_bud_json=x_json)

    # THEN
    assert str(type(json_bud)).find(".bud.BudUnit'>") > 0
    assert json_bud.owner_name is not None
    assert json_bud.owner_name == zia_bud.owner_name
    assert json_bud.fisc_label == zia_bud.fisc_label
    assert json_bud.fund_pool == zia_fund_pool
    assert json_bud.fund_pool == zia_bud.fund_pool
    assert json_bud.fund_iota == zia_fund_iota
    assert json_bud.fund_iota == zia_bud.fund_iota
    assert json_bud.respect_bit == zia_resepect_bit
    assert json_bud.respect_bit == zia_bud.respect_bit
    assert json_bud.penny == zia_penny
    assert json_bud.penny == zia_bud.penny
    assert json_bud.max_tree_traverse == 23
    assert json_bud.max_tree_traverse == zia_bud.max_tree_traverse
    assert json_bud.bridge == zia_bud.bridge
    assert json_bud.credor_respect == zia_bud.credor_respect
    assert json_bud.debtor_respect == zia_bud.debtor_respect
    assert json_bud.credor_respect == zia_credor_respect
    assert json_bud.debtor_respect == zia_debtor_respect
    assert json_bud.last_pack_id == zia_bud.last_pack_id
    assert json_bud.last_pack_id == zia_last_pack_id
    # assert json_bud._groups == zia_bud._groups

    json_conceptroot = json_bud.conceptroot
    assert json_conceptroot.parent_way == ""
    assert json_conceptroot.parent_way == zia_bud.conceptroot.parent_way
    assert json_conceptroot.reasonunits == {}
    assert json_conceptroot.laborunit == zia_bud.conceptroot.laborunit
    assert json_conceptroot.laborunit == run_laborunit
    assert json_conceptroot.fund_iota == 8
    assert json_conceptroot.fund_iota == zia_fund_iota
    assert len(json_conceptroot.factunits) == 1
    assert len(json_conceptroot.awardlinks) == 1

    assert len(json_bud.conceptroot._kids) == 2

    wkday_str = "wkdays"
    wkday_way = json_bud.make_l1_way(wkday_str)
    wkday_concept_x = json_bud.get_concept_obj(wkday_way)
    assert len(wkday_concept_x._kids) == 2

    sunday_str = "Sunday"
    sunday_way = json_bud.make_way(wkday_way, sunday_str)
    sunday_concept = json_bud.get_concept_obj(sunday_way)
    assert sunday_concept.mass == 20

    json_shave_concept = json_bud.get_concept_obj(shave_way)
    zia_shave_concept = zia_bud.get_concept_obj(shave_way)
    assert len(json_shave_concept.reasonunits) == 1
    assert json_shave_concept.laborunit == zia_shave_concept.laborunit
    assert json_shave_concept.laborunit == xio_laborunit
    assert json_shave_concept._originunit == zia_shave_concept._originunit
    print(f"{json_shave_concept.healerlink=}")
    assert json_shave_concept.healerlink == zia_shave_concept.healerlink
    assert len(json_shave_concept.awardlinks) == 2
    assert len(json_shave_concept.factunits) == 1
    assert zia_shave_concept.problem_bool
    assert json_shave_concept.problem_bool == zia_shave_concept.problem_bool
    assert json_shave_concept.gogo_want == zia_shave_concept.gogo_want
    assert json_shave_concept.stop_want == zia_shave_concept.stop_want

    assert len(json_bud.originunit._originholds) == 1
    assert json_bud.originunit == zia_bud.originunit


def test_budunit_get_from_json_ReturnsCorrectConceptRoot():
    # ESTABLISH
    zia_bud = get_budunit_x1_3levels_1reason_1facts()
    zia_bud.set_max_tree_traverse(23)
    # root_concept = zia_bud.get_concept_obj(zia_bud.get_concept_obj(zia_bud.fisc_label))
    root_concept = zia_bud.conceptroot
    zia_gogo_want = 75
    zia_stop_want = 77
    root_concept.gogo_want = zia_gogo_want
    root_concept.stop_want = zia_stop_want

    # WHEN
    x_json = zia_bud.get_json()
    assert x_is_json(x_json) is True
    json_bud = budunit_get_from_json(x_bud_json=x_json)

    # THEN
    json_conceptroot = json_bud.get_concept_obj(to_way(zia_bud.fisc_label))
    assert json_conceptroot.gogo_want == zia_gogo_want
    assert json_conceptroot.stop_want == zia_stop_want


def test_budunit_get_from_json_ReturnsObj_bridge_Example():
    # ESTABLISH
    slash_bridge = "/"
    before_bob_bud = budunit_shop("Bob", bridge=slash_bridge)
    assert before_bob_bud.bridge != default_bridge_if_None()

    # WHEN
    bob_json = before_bob_bud.get_json()
    after_bob_bud = budunit_get_from_json(bob_json)

    # THEN
    assert after_bob_bud.bridge != default_bridge_if_None()
    assert after_bob_bud.bridge == slash_bridge
    assert after_bob_bud.bridge == before_bob_bud.bridge


def test_budunit_get_from_json_ReturnsObj_bridge_AcctExample():
    # ESTABLISH
    slash_bridge = "/"
    before_bob_bud = budunit_shop("Bob", bridge=slash_bridge)
    bob_str = ",Bob"
    before_bob_bud.add_acctunit(bob_str)
    assert before_bob_bud.acct_exists(bob_str)

    # WHEN
    bob_json = before_bob_bud.get_json()
    after_bob_bud = budunit_get_from_json(bob_json)

    # THEN
    after_bob_acctunit = after_bob_bud.get_acct(bob_str)
    assert after_bob_acctunit.bridge == slash_bridge


def test_budunit_get_from_json_ReturnsObj_bridge_GroupExample():
    # ESTABLISH
    slash_bridge = "/"
    before_bob_bud = budunit_shop("Bob", bridge=slash_bridge)
    yao_str = "Yao"
    swim_str = f"{slash_bridge}Swimmers"
    before_bob_bud.add_acctunit(yao_str)
    yao_acctunit = before_bob_bud.get_acct(yao_str)
    yao_acctunit.add_membership(swim_str)

    # WHEN
    bob_json = before_bob_bud.get_json()
    after_bob_bud = budunit_get_from_json(bob_json)

    # THEN
    after_yao_acctunit = after_bob_bud.get_acct(yao_str)
    assert after_yao_acctunit.bridge == slash_bridge


def test_budunit_get_from_json_ReturnsObj_Scenario7_conceptroot_bridge_IsCorrectlySet():
    # ESTABLISH
    slash_str = "/"
    run_str = "runners"
    sue_bud = budunit_shop("Sue", bridge=slash_str)
    root_way = to_way(sue_bud.fisc_label, slash_str)
    day_hr_str = "day_hr"
    day_hr_way = sue_bud.make_l1_way(day_hr_str)
    sue_bud.add_concept(day_hr_way)
    assert sue_bud.bridge == slash_str
    assert sue_bud.get_concept_obj(root_way).bridge == slash_str
    assert sue_bud.get_concept_obj(day_hr_way).bridge == slash_str

    # WHEN
    after_bob_bud = budunit_get_from_json(sue_bud.get_json())

    # THEN
    assert after_bob_bud.bridge == slash_str
    assert after_bob_bud.get_concept_obj(root_way).bridge == slash_str
    assert after_bob_bud.get_concept_obj(day_hr_way).bridge == slash_str


def test_budunit_get_from_json_ExportsBudUnit_mass():
    # ESTABLISH
    x1_bud = budunit_v001()
    x1_bud.tally = 15
    assert x1_bud.tally == 15
    assert x1_bud.conceptroot.mass != x1_bud.tally
    assert x1_bud.conceptroot.mass == 1

    # WHEN
    x2_bud = budunit_get_from_json(x1_bud.get_json())

    # THEN
    assert x1_bud.tally == 15
    assert x1_bud.tally == x2_bud.tally
    assert x1_bud.conceptroot.mass == 1
    assert x1_bud.conceptroot.mass == x2_bud.conceptroot.mass
    assert x1_bud.conceptroot._kids == x2_bud.conceptroot._kids


def test_get_dict_of_bud_from_dict_ReturnsDictOfBudUnits():
    # ESTABLISH
    x1_bud = budunit_v001()
    x2_bud = get_budunit_x1_3levels_1reason_1facts()
    x3_bud = get_budunit_rcontext_time_example()
    print(f"{x1_bud.owner_name}")
    print(f"{x2_bud.owner_name}")
    print(f"{x3_bud.owner_name}")

    cn_dict_of_dicts = {
        x1_bud.owner_name: x1_bud.get_dict(),
        x2_bud.owner_name: x2_bud.get_dict(),
        x3_bud.owner_name: x3_bud.get_dict(),
    }

    # WHEN
    ccn_dict_of_obj = get_dict_of_bud_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(x1_bud.owner_name) is not None
    assert ccn_dict_of_obj.get(x2_bud.owner_name) is not None
    assert ccn_dict_of_obj.get(x3_bud.owner_name) is not None

    ccn2_bud = ccn_dict_of_obj.get(x2_bud.owner_name)
    assert ccn2_bud.conceptroot.concept_label == x2_bud.conceptroot.concept_label
    assert ccn2_bud.conceptroot.parent_way == x2_bud.conceptroot.parent_way
    assert ccn2_bud.conceptroot.fund_iota == x2_bud.conceptroot.fund_iota
    shave_way = ccn2_bud.make_l1_way("shave")
    wk_way = ccn2_bud.make_l1_way("wkdays")
    # assert ccn2_bud.get_concept_obj(shave_way) == x2_bud.get_concept_obj(shave_way)
    # assert ccn2_bud.get_concept_obj(wk_way) == x2_bud.get_concept_obj(wk_way)
    # assert ccn2_bud.conceptroot == x2_bud.conceptroot
    assert ccn2_bud.get_dict() == x2_bud.get_dict()

    ccn_bud3 = ccn_dict_of_obj.get(x3_bud.owner_name)
    assert ccn_bud3.get_dict() == x3_bud.get_dict()

    cc1_concept_root = ccn_dict_of_obj.get(x1_bud.owner_name).conceptroot
    assert cc1_concept_root._originunit == x1_bud.conceptroot._originunit
    ccn_bud1 = ccn_dict_of_obj.get(x1_bud.owner_name)
    assert ccn_bud1._concept_dict == x1_bud._concept_dict
    philipa_str = "Philipa"
    ccn_philipa_acctunit = ccn_bud1.get_acct(philipa_str)
    x1_philipa_acctunit = x1_bud.get_acct(philipa_str)
    assert ccn_philipa_acctunit._memberships == x1_philipa_acctunit._memberships
    assert ccn_bud1 == x1_bud
    assert ccn_dict_of_obj.get(x1_bud.owner_name) == x1_bud
