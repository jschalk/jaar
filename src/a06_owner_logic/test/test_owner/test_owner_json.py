from pytest import raises as pytest_raises
from src.a00_data_toolbox.dict_toolbox import get_dict_from_json, x_is_json
from src.a01_term_logic.rope import default_knot_if_None, to_rope
from src.a03_group_logic.group import awardlink_shop
from src.a04_reason_logic.reason_concept import factunit_shop
from src.a04_reason_logic.reason_labor import laborunit_shop
from src.a05_concept_logic.concept import conceptunit_shop
from src.a05_concept_logic.healer import healerlink_shop
from src.a06_owner_logic.owner import (
    get_dict_of_owner_from_dict,
    get_from_json as ownerunit_get_from_json,
    ownerunit_shop,
)
from src.a06_owner_logic.test._util.example_owners import (
    get_ownerunit_rcontext_time_example,
    get_ownerunit_x1_3levels_1reason_1facts,
    ownerunit_v001,
)


def test_OwnerUnit_get_dict_ReturnsObj_Scenario1_large_json():
    # ESTABLISH
    yao_owner = ownerunit_v001()
    day_hr_str = "day_hr"
    day_hr_rope = yao_owner.make_l1_rope(day_hr_str)
    day_hr_concept = yao_owner.get_concept_obj(day_hr_rope)
    yao_owner.add_fact(fcontext=day_hr_rope, fstate=day_hr_rope, fopen=0, fnigh=23)
    time_minute = yao_owner.make_l1_rope("day_minute")
    yao_owner.add_fact(fcontext=time_minute, fstate=time_minute, fopen=0, fnigh=1440)
    yao_str = "Yao"
    yao_fund_pool = 23000
    yao_owner.fund_pool = yao_fund_pool
    yao_fund_iota = 23
    yao_owner.fund_iota = yao_fund_iota
    owner_tally = 23
    yao_owner.tally = owner_tally
    x_credor_respect = 22
    x_debtor_respect = 44
    yao_owner.set_credor_respect(x_credor_respect)
    yao_owner.set_debtor_respect(x_debtor_respect)
    override_str = "override"
    x_last_pack_id = 77
    yao_owner.set_last_pack_id(x_last_pack_id)

    # WHEN
    owner_dict = yao_owner.get_dict()

    # THEN
    assert owner_dict is not None
    assert str(type(owner_dict)) == "<class 'dict'>"
    assert owner_dict["owner_name"] == yao_owner.owner_name
    assert owner_dict["belief_label"] == yao_owner.belief_label
    assert owner_dict["tally"] == yao_owner.tally
    assert owner_dict["tally"] == owner_tally
    assert owner_dict["fund_pool"] == yao_fund_pool
    assert owner_dict["fund_iota"] == yao_fund_iota
    assert owner_dict["max_tree_traverse"] == yao_owner.max_tree_traverse
    assert owner_dict["knot"] == yao_owner.knot
    assert owner_dict["credor_respect"] == yao_owner.credor_respect
    assert owner_dict["debtor_respect"] == yao_owner.debtor_respect
    assert owner_dict["last_pack_id"] == yao_owner.last_pack_id
    assert len(owner_dict["accts"]) == len(yao_owner.accts)
    assert len(owner_dict["accts"]) != 12
    assert owner_dict.get("_groups") is None

    x_conceptroot = yao_owner.conceptroot
    conceptroot_dict = owner_dict["conceptroot"]
    _kids = "_kids"
    assert x_conceptroot.concept_label == yao_owner.belief_label
    assert conceptroot_dict["concept_label"] == x_conceptroot.concept_label
    assert conceptroot_dict["mass"] == x_conceptroot.mass
    assert len(conceptroot_dict[_kids]) == len(x_conceptroot._kids)


def test_OwnerUnit_get_dict_ReturnsObj_Scenario2_conceptroot_laborunit():
    # ESTABLISH
    run_str = "runners"
    sue_owner = ownerunit_shop("Sue")
    x_laborunit = laborunit_shop()
    x_laborunit.set_laborlink(labor_title=run_str)
    root_rope = to_rope(sue_owner.belief_label)
    sue_owner.edit_concept_attr(root_rope, laborunit=x_laborunit)
    root_concept = sue_owner.get_concept_obj(root_rope)
    x_gogo_want = 5
    x_stop_want = 11
    root_concept.gogo_want = x_gogo_want
    root_concept.stop_want = x_stop_want

    # WHEN
    owner_dict = sue_owner.get_dict()
    conceptroot_dict = owner_dict.get("conceptroot")

    # THEN
    assert conceptroot_dict["laborunit"] == x_laborunit.get_dict()
    assert conceptroot_dict["laborunit"] == {"_laborlinks": [run_str]}
    assert conceptroot_dict.get("gogo_want") == x_gogo_want
    assert conceptroot_dict.get("stop_want") == x_stop_want


def test_OwnerUnit_get_dict_ReturnsObj_Scenario3_With_conceptroot_healerlink():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    yao_str = "Yao"
    sue_owner.add_acctunit(yao_str)
    run_str = ";runners"
    yao_acctunit = sue_owner.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)
    run_healerlink = healerlink_shop()
    run_healerlink.set_healer_name(x_healer_name=run_str)
    root_rope = to_rope(sue_owner.belief_label)
    sue_owner.edit_concept_attr(root_rope, healerlink=run_healerlink)

    # WHEN
    owner_dict = sue_owner.get_dict()
    conceptroot_dict = owner_dict.get("conceptroot")

    # THEN
    assert conceptroot_dict["healerlink"] == run_healerlink.get_dict()


def test_OwnerUnit_get_dict_ReturnsObj_Scenario4_conceptkid_LaborUnit():
    # ESTABLISH
    sue_owner = ownerunit_shop("Sue")
    yao_str = "Yao"
    sue_owner.add_acctunit(yao_str)
    run_str = ";runners"
    yao_acctunit = sue_owner.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)

    morn_str = "morning"
    morn_rope = sue_owner.make_l1_rope(morn_str)
    sue_owner.set_l1_concept(conceptunit_shop(morn_str))
    x_laborunit = laborunit_shop()
    x_laborunit.set_laborlink(labor_title=run_str)
    sue_owner.edit_concept_attr(morn_rope, laborunit=x_laborunit)

    # WHEN
    owner_dict = sue_owner.get_dict()
    conceptroot_dict = owner_dict.get("conceptroot")

    # THEN
    _kids = "_kids"
    _laborunit = "laborunit"

    labor_dict_x = conceptroot_dict[_kids][morn_str][_laborunit]
    assert labor_dict_x == x_laborunit.get_dict()
    assert labor_dict_x == {"_laborlinks": [run_str]}


def test_OwnerUnit_get_json_ReturnsCorrectJSON_SimpleExample():
    # ESTABLISH
    zia_owner = get_ownerunit_x1_3levels_1reason_1facts()
    x_fund_pool = 66000
    zia_owner.fund_pool = x_fund_pool
    x_fund_iota = 66
    zia_owner.fund_iota = x_fund_iota
    x_respect_bit = 7
    zia_owner.respect_bit = x_respect_bit
    x_penny = 0.3
    zia_owner.penny = x_penny
    override_str = "override"
    yao_str = "Yao"
    run_str = ";runners"
    zia_owner.add_acctunit(yao_str)
    yao_acctunit = zia_owner.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)
    run_healerlink = healerlink_shop({run_str})
    root_rope = to_rope(zia_owner.belief_label)
    zia_owner.edit_concept_attr(root_rope, healerlink=run_healerlink)
    zia_owner.edit_concept_attr(root_rope, problem_bool=True)

    # WHEN
    x_json = zia_owner.get_json()

    # THEN
    _kids = "_kids"

    assert x_json is not None
    assert True == x_is_json(x_json)
    owner_dict = get_dict_from_json(x_json)

    assert owner_dict["owner_name"] == zia_owner.owner_name
    assert owner_dict["belief_label"] == zia_owner.belief_label
    assert owner_dict["tally"] == zia_owner.tally
    assert owner_dict["fund_pool"] == zia_owner.fund_pool
    assert owner_dict["fund_iota"] == zia_owner.fund_iota
    assert owner_dict["respect_bit"] == zia_owner.respect_bit
    assert owner_dict["penny"] == zia_owner.penny
    assert owner_dict["credor_respect"] == zia_owner.credor_respect
    assert owner_dict["debtor_respect"] == zia_owner.debtor_respect
    # with pytest_raises(Exception) as excinfo:
    #     owner_dict["_credor_respect"]
    # assert str(excinfo.value) == "'_credor_respect'"
    # with pytest_raises(Exception) as excinfo:
    #     owner_dict["_debtor_respect"]
    # assert str(excinfo.value) == "'_debtor_respect'"
    with pytest_raises(Exception) as excinfo:
        owner_dict["last_pack_id"]

    x_conceptroot = zia_owner.conceptroot
    conceptroot_dict = owner_dict.get("conceptroot")

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


def test_OwnerUnit_get_json_ReturnsCorrectJSON_BigExample():
    # ESTABLISH
    yao_owner = ownerunit_v001()
    day_hr_str = "day_hr"
    day_hr_rope = yao_owner.make_l1_rope(day_hr_str)
    yao_owner.add_fact(fcontext=day_hr_rope, fstate=day_hr_rope, fopen=0, fnigh=23)
    day_min_str = "day_minute"
    day_min_rope = yao_owner.make_l1_rope(day_min_str)
    yao_owner.add_fact(fcontext=day_min_rope, fstate=day_min_rope, fopen=0, fnigh=59)
    x_factunit = factunit_shop(day_min_rope, day_min_rope, 5, 59)
    yao_owner.edit_concept_attr(x_factunit.fcontext, factunit=x_factunit)
    yao_owner.set_max_tree_traverse(2)
    yao_str = "Yao"

    # WHEN
    owner_dict = get_dict_from_json(yao_owner.get_json())

    # THEN
    _kids = "_kids"
    assert owner_dict["owner_name"] == yao_owner.owner_name
    assert owner_dict["belief_label"] == yao_owner.belief_label
    assert owner_dict["tally"] == yao_owner.tally
    assert owner_dict["max_tree_traverse"] == 2
    assert owner_dict["max_tree_traverse"] == yao_owner.max_tree_traverse
    assert owner_dict["knot"] == yao_owner.knot

    x_conceptroot = yao_owner.conceptroot
    conceptroot_dict = owner_dict.get("conceptroot")
    assert len(conceptroot_dict[_kids]) == len(x_conceptroot._kids)

    kids = conceptroot_dict[_kids]
    day_min_dict = kids[day_min_str]
    day_min_factunits_dict = day_min_dict["factunits"]
    day_min_concept_x = yao_owner.get_concept_obj(day_min_rope)
    print(f"{day_min_factunits_dict=}")
    assert len(day_min_factunits_dict) == 1
    assert len(day_min_factunits_dict) == len(day_min_concept_x.factunits)

    _reasonunits = "reasonunits"
    cont_str = "Freelancing"
    ulti_str = "Ultimate Frisbee"
    cont_rope = yao_owner.make_l1_rope(cont_str)
    ulti_rope = yao_owner.make_l1_rope(ulti_str)
    cont_concept = yao_owner.get_concept_obj(cont_rope)
    ulti_concept = yao_owner.get_concept_obj(ulti_rope)
    cont_reasonunits_dict = conceptroot_dict[_kids][cont_str][_reasonunits]
    ulti_reasonunits_dict = conceptroot_dict[_kids][ulti_str][_reasonunits]
    assert len(cont_reasonunits_dict) == len(cont_concept.reasonunits)
    assert len(ulti_reasonunits_dict) == len(ulti_concept.reasonunits)

    anna_str = "Anna"
    anna_acctunit = yao_owner.get_acct(anna_str)
    assert anna_acctunit.get_membership(";Family").group_cred_points == 6.2
    assert yao_owner.accts is not None
    assert len(yao_owner.accts) == 22


def test_ownerunit_get_from_json_ReturnsObjSimpleExample():
    # ESTABLISH
    zia_owner = get_ownerunit_x1_3levels_1reason_1facts()
    zia_owner.set_max_tree_traverse(23)
    tiger_belief_label = "tiger"
    zia_owner.set_belief_label(tiger_belief_label)
    zia_fund_pool = 80000
    zia_owner.fund_pool = zia_fund_pool
    zia_fund_iota = 8
    zia_owner.fund_iota = zia_fund_iota
    zia_resepect_bit = 5
    zia_owner.respect_bit = zia_resepect_bit
    zia_penny = 2
    zia_owner.penny = zia_penny
    zia_credor_respect = 200
    zia_debtor_respect = 200
    zia_owner.set_credor_respect(zia_credor_respect)
    zia_owner.set_debtor_respect(zia_debtor_respect)
    zia_last_pack_id = 73
    zia_owner.set_last_pack_id(zia_last_pack_id)

    shave_str = "shave"
    shave_rope = zia_owner.make_l1_rope(shave_str)
    shave_concept_y1 = zia_owner.get_concept_obj(shave_rope)
    shave_concept_y1.problem_bool = True
    # print(f"{shave_rope=}")
    # print(f"{json_shave_concept.concept_label=} {json_shave_concept.parent_rope=}")

    sue_str = "Sue"
    zia_owner.add_acctunit(
        acct_name=sue_str, acct_cred_points=199, acct_debt_points=199
    )
    xio_str = "Xio"
    zia_owner.add_acctunit(acct_name=xio_str)
    run_str = ";runners"
    sue_acctunit = zia_owner.get_acct(sue_str)
    xio_acctunit = zia_owner.get_acct(xio_str)
    sue_acctunit.add_membership(run_str)
    xio_acctunit.add_membership(run_str)
    run_laborunit = laborunit_shop()
    run_laborunit.set_laborlink(labor_title=run_str)
    root_rope = to_rope(zia_owner.belief_label)
    zia_owner.edit_concept_attr(root_rope, laborunit=run_laborunit)
    xio_laborunit = laborunit_shop()
    xio_laborunit.set_laborlink(labor_title=xio_str)
    zia_owner.edit_concept_attr(shave_rope, laborunit=xio_laborunit)
    zia_owner.edit_concept_attr(shave_rope, awardlink=awardlink_shop(xio_str))
    zia_owner.edit_concept_attr(shave_rope, awardlink=awardlink_shop(sue_str))
    zia_owner.edit_concept_attr(root_rope, awardlink=awardlink_shop(sue_str))
    # add healerlink to shave conceptunit
    run_healerlink = healerlink_shop({run_str})
    zia_owner.edit_concept_attr(shave_rope, healerlink=run_healerlink)
    shave_concept = zia_owner.get_concept_obj(shave_rope)
    zia_gogo_want = 75
    zia_stop_want = 77
    shave_concept.gogo_want = zia_gogo_want
    shave_concept.stop_want = zia_stop_want

    override_str = "override"

    # WHEN
    x_json = zia_owner.get_json()
    assert x_is_json(x_json) is True
    json_owner = ownerunit_get_from_json(x_owner_json=x_json)

    # THEN
    assert str(type(json_owner)).find(".owner.OwnerUnit'>") > 0
    assert json_owner.owner_name is not None
    assert json_owner.owner_name == zia_owner.owner_name
    assert json_owner.belief_label == zia_owner.belief_label
    assert json_owner.fund_pool == zia_fund_pool
    assert json_owner.fund_pool == zia_owner.fund_pool
    assert json_owner.fund_iota == zia_fund_iota
    assert json_owner.fund_iota == zia_owner.fund_iota
    assert json_owner.respect_bit == zia_resepect_bit
    assert json_owner.respect_bit == zia_owner.respect_bit
    assert json_owner.penny == zia_penny
    assert json_owner.penny == zia_owner.penny
    assert json_owner.max_tree_traverse == 23
    assert json_owner.max_tree_traverse == zia_owner.max_tree_traverse
    assert json_owner.knot == zia_owner.knot
    assert json_owner.credor_respect == zia_owner.credor_respect
    assert json_owner.debtor_respect == zia_owner.debtor_respect
    assert json_owner.credor_respect == zia_credor_respect
    assert json_owner.debtor_respect == zia_debtor_respect
    assert json_owner.last_pack_id == zia_owner.last_pack_id
    assert json_owner.last_pack_id == zia_last_pack_id
    # assert json_owner._groups == zia_owner._groups

    json_conceptroot = json_owner.conceptroot
    assert json_conceptroot.parent_rope == ""
    assert json_conceptroot.parent_rope == zia_owner.conceptroot.parent_rope
    assert json_conceptroot.reasonunits == {}
    assert json_conceptroot.laborunit == zia_owner.conceptroot.laborunit
    assert json_conceptroot.laborunit == run_laborunit
    assert json_conceptroot.fund_iota == 8
    assert json_conceptroot.fund_iota == zia_fund_iota
    assert len(json_conceptroot.factunits) == 1
    assert len(json_conceptroot.awardlinks) == 1

    assert len(json_owner.conceptroot._kids) == 2

    wkday_str = "wkdays"
    wkday_rope = json_owner.make_l1_rope(wkday_str)
    wkday_concept_x = json_owner.get_concept_obj(wkday_rope)
    assert len(wkday_concept_x._kids) == 2

    sunday_str = "Sunday"
    sunday_rope = json_owner.make_rope(wkday_rope, sunday_str)
    sunday_concept = json_owner.get_concept_obj(sunday_rope)
    assert sunday_concept.mass == 20

    json_shave_concept = json_owner.get_concept_obj(shave_rope)
    zia_shave_concept = zia_owner.get_concept_obj(shave_rope)
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


def test_ownerunit_get_from_json_ReturnsCorrectConceptRoot():
    # ESTABLISH
    zia_owner = get_ownerunit_x1_3levels_1reason_1facts()
    zia_owner.set_max_tree_traverse(23)
    # root_concept = zia_owner.get_concept_obj(zia_owner.get_concept_obj(zia_owner.belief_label))
    root_concept = zia_owner.conceptroot
    zia_gogo_want = 75
    zia_stop_want = 77
    root_concept.gogo_want = zia_gogo_want
    root_concept.stop_want = zia_stop_want

    # WHEN
    x_json = zia_owner.get_json()
    assert x_is_json(x_json) is True
    json_owner = ownerunit_get_from_json(x_owner_json=x_json)

    # THEN
    json_conceptroot = json_owner.get_concept_obj(to_rope(zia_owner.belief_label))
    assert json_conceptroot.gogo_want == zia_gogo_want
    assert json_conceptroot.stop_want == zia_stop_want


def test_ownerunit_get_from_json_ReturnsObj_knot_Example():
    # ESTABLISH
    slash_knot = "/"
    before_bob_owner = ownerunit_shop("Bob", knot=slash_knot)
    assert before_bob_owner.knot != default_knot_if_None()

    # WHEN
    bob_json = before_bob_owner.get_json()
    after_bob_owner = ownerunit_get_from_json(bob_json)

    # THEN
    assert after_bob_owner.knot != default_knot_if_None()
    assert after_bob_owner.knot == slash_knot
    assert after_bob_owner.knot == before_bob_owner.knot


def test_ownerunit_get_from_json_ReturnsObj_knot_AcctExample():
    # ESTABLISH
    slash_knot = "/"
    before_bob_owner = ownerunit_shop("Bob", knot=slash_knot)
    bob_str = ",Bob"
    before_bob_owner.add_acctunit(bob_str)
    assert before_bob_owner.acct_exists(bob_str)

    # WHEN
    bob_json = before_bob_owner.get_json()
    after_bob_owner = ownerunit_get_from_json(bob_json)

    # THEN
    after_bob_acctunit = after_bob_owner.get_acct(bob_str)
    assert after_bob_acctunit.knot == slash_knot


def test_ownerunit_get_from_json_ReturnsObj_knot_GroupExample():
    # ESTABLISH
    slash_knot = "/"
    before_bob_owner = ownerunit_shop("Bob", knot=slash_knot)
    yao_str = "Yao"
    swim_str = f"{slash_knot}Swimmers"
    before_bob_owner.add_acctunit(yao_str)
    yao_acctunit = before_bob_owner.get_acct(yao_str)
    yao_acctunit.add_membership(swim_str)

    # WHEN
    bob_json = before_bob_owner.get_json()
    after_bob_owner = ownerunit_get_from_json(bob_json)

    # THEN
    after_yao_acctunit = after_bob_owner.get_acct(yao_str)
    assert after_yao_acctunit.knot == slash_knot


def test_ownerunit_get_from_json_ReturnsObj_Scenario7_conceptroot_knot_IsCorrectlySet():
    # ESTABLISH
    slash_str = "/"
    run_str = "runners"
    sue_owner = ownerunit_shop("Sue", knot=slash_str)
    root_rope = to_rope(sue_owner.belief_label, slash_str)
    day_hr_str = "day_hr"
    day_hr_rope = sue_owner.make_l1_rope(day_hr_str)
    sue_owner.add_concept(day_hr_rope)
    assert sue_owner.knot == slash_str
    assert sue_owner.get_concept_obj(root_rope).knot == slash_str
    assert sue_owner.get_concept_obj(day_hr_rope).knot == slash_str

    # WHEN
    after_bob_owner = ownerunit_get_from_json(sue_owner.get_json())

    # THEN
    assert after_bob_owner.knot == slash_str
    assert after_bob_owner.get_concept_obj(root_rope).knot == slash_str
    assert after_bob_owner.get_concept_obj(day_hr_rope).knot == slash_str


def test_ownerunit_get_from_json_ExportsOwnerUnit_mass():
    # ESTABLISH
    x1_owner = ownerunit_v001()
    x1_owner.tally = 15
    assert x1_owner.tally == 15
    assert x1_owner.conceptroot.mass != x1_owner.tally
    assert x1_owner.conceptroot.mass == 1

    # WHEN
    x2_owner = ownerunit_get_from_json(x1_owner.get_json())

    # THEN
    assert x1_owner.tally == 15
    assert x1_owner.tally == x2_owner.tally
    assert x1_owner.conceptroot.mass == 1
    assert x1_owner.conceptroot.mass == x2_owner.conceptroot.mass
    assert x1_owner.conceptroot._kids == x2_owner.conceptroot._kids


def test_get_dict_of_owner_from_dict_ReturnsDictOfOwnerUnits():
    # ESTABLISH
    x1_owner = ownerunit_v001()
    x2_owner = get_ownerunit_x1_3levels_1reason_1facts()
    x3_owner = get_ownerunit_rcontext_time_example()
    print(f"{x1_owner.owner_name}")
    print(f"{x2_owner.owner_name}")
    print(f"{x3_owner.owner_name}")

    cn_dict_of_dicts = {
        x1_owner.owner_name: x1_owner.get_dict(),
        x2_owner.owner_name: x2_owner.get_dict(),
        x3_owner.owner_name: x3_owner.get_dict(),
    }

    # WHEN
    ccn_dict_of_obj = get_dict_of_owner_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(x1_owner.owner_name) is not None
    assert ccn_dict_of_obj.get(x2_owner.owner_name) is not None
    assert ccn_dict_of_obj.get(x3_owner.owner_name) is not None

    ccn2_owner = ccn_dict_of_obj.get(x2_owner.owner_name)
    assert ccn2_owner.conceptroot.concept_label == x2_owner.conceptroot.concept_label
    assert ccn2_owner.conceptroot.parent_rope == x2_owner.conceptroot.parent_rope
    assert ccn2_owner.conceptroot.fund_iota == x2_owner.conceptroot.fund_iota
    shave_rope = ccn2_owner.make_l1_rope("shave")
    wk_rope = ccn2_owner.make_l1_rope("wkdays")
    # assert ccn2_owner.get_concept_obj(shave_rope) == x2_owner.get_concept_obj(shave_rope)
    # assert ccn2_owner.get_concept_obj(wk_rope) == x2_owner.get_concept_obj(wk_rope)
    # assert ccn2_owner.conceptroot == x2_owner.conceptroot
    assert ccn2_owner.get_dict() == x2_owner.get_dict()

    ccn_owner3 = ccn_dict_of_obj.get(x3_owner.owner_name)
    assert ccn_owner3.get_dict() == x3_owner.get_dict()

    cc1_concept_root = ccn_dict_of_obj.get(x1_owner.owner_name).conceptroot
    ccn_owner1 = ccn_dict_of_obj.get(x1_owner.owner_name)
    assert ccn_owner1._concept_dict == x1_owner._concept_dict
    philipa_str = "Philipa"
    ccn_philipa_acctunit = ccn_owner1.get_acct(philipa_str)
    x1_philipa_acctunit = x1_owner.get_acct(philipa_str)
    assert ccn_philipa_acctunit._memberships == x1_philipa_acctunit._memberships
    assert ccn_owner1 == x1_owner
    assert ccn_dict_of_obj.get(x1_owner.owner_name) == x1_owner
