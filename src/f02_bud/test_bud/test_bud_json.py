from src.f00_instrument.dict_toolbox import x_is_json, get_dict_from_json
from src.f01_road.road import default_wall_if_None
from src.f02_bud.group import awardlink_shop
from src.f02_bud.healer import healerlink_shop
from src.f02_bud.reason_team import teamunit_shop
from src.f02_bud.reason_item import factunit_shop
from src.f02_bud.item import itemunit_shop
from src.f02_bud.bud import (
    budunit_shop,
    get_from_json as budunit_get_from_json,
    get_dict_of_bud_from_dict,
)
from src.f02_bud.examples.example_buds import (
    budunit_v001,
    get_budunit_x1_3levels_1reason_1facts,
    get_budunit_base_time_example,
)
from pytest import raises as pytest_raises


def test_BudUnit_get_dict_ReturnsDictObject():
    # ESTABLISH
    yao_bud = budunit_v001()
    day_hour_str = "day_hour"
    day_hour_road = yao_bud.make_l1_road(day_hour_str)
    day_hour_item = yao_bud.get_item_obj(day_hour_road)
    day_hour_item._originunit.set_originhold(acct_id="Bob", importance=2)
    yao_bud.set_fact(base=day_hour_road, pick=day_hour_road, fopen=0, fnigh=23)
    time_minute = yao_bud.make_l1_road("day_minute")
    yao_bud.set_fact(base=time_minute, pick=time_minute, fopen=0, fnigh=1440)
    yao_str = "Yao"
    yao_bud._originunit.set_originhold(yao_str, 1)
    yao_fund_pool = 23000
    yao_bud.fund_pool = yao_fund_pool
    yao_fund_coin = 23
    yao_bud.fund_coin = yao_fund_coin
    bud_tally = 23
    yao_bud.tally = bud_tally
    x_credor_respect = 22
    x_debtor_respect = 44
    yao_bud.set_credor_respect(x_credor_respect)
    yao_bud.set_debtor_respect(x_debtor_respect)
    override_str = "override"
    x_last_gift_id = 77
    yao_bud.set_last_gift_id(x_last_gift_id)

    # WHEN
    bud_dict = yao_bud.get_dict()

    # THEN
    assert bud_dict is not None
    assert str(type(bud_dict)) == "<class 'dict'>"
    assert bud_dict["_owner_id"] == yao_bud._owner_id
    assert bud_dict["_fiscal_id"] == yao_bud._fiscal_id
    assert bud_dict["tally"] == yao_bud.tally
    assert bud_dict["tally"] == bud_tally
    assert bud_dict["fund_pool"] == yao_fund_pool
    assert bud_dict["fund_coin"] == yao_fund_coin
    assert bud_dict["max_tree_traverse"] == yao_bud.max_tree_traverse
    assert bud_dict["_wall"] == yao_bud._wall
    assert bud_dict["credor_respect"] == yao_bud.credor_respect
    assert bud_dict["debtor_respect"] == yao_bud.debtor_respect
    assert bud_dict["_last_gift_id"] == yao_bud._last_gift_id
    assert len(bud_dict["_accts"]) == len(yao_bud._accts)
    assert len(bud_dict["_accts"]) != 12
    assert bud_dict.get("_groups") is None

    x_itemroot = yao_bud._itemroot
    itemroot_dict = bud_dict["_itemroot"]
    _kids = "_kids"
    assert x_itemroot._label == yao_bud._fiscal_id
    assert itemroot_dict["_label"] == x_itemroot._label
    assert itemroot_dict["mass"] == x_itemroot.mass
    assert len(itemroot_dict[_kids]) == len(x_itemroot._kids)

    originunit_str = "_originunit"
    day_hour_originunit_dict = itemroot_dict[_kids][day_hour_str][originunit_str]
    assert day_hour_originunit_dict == day_hour_item._originunit.get_dict()
    originholds_str = "_originholds"
    yao_bud_originhold = bud_dict[originunit_str][originholds_str][yao_str]
    print(f"{yao_bud_originhold=}")
    assert yao_bud_originhold
    assert yao_bud_originhold["acct_id"] == yao_str
    assert yao_bud_originhold["importance"] == 1


def test_BudUnit_get_dict_ReturnsDictWith_itemroot_teamunit():
    # ESTABLISH
    run_str = "runners"
    sue_bud = budunit_shop("Sue")
    x_teamunit = teamunit_shop()
    x_teamunit.set_teamlink(team_id=run_str)
    sue_bud.edit_item_attr(sue_bud._fiscal_id, teamunit=x_teamunit)
    root_item = sue_bud.get_item_obj(sue_bud._fiscal_id)
    x_gogo_want = 5
    x_stop_want = 11
    root_item.gogo_want = x_gogo_want
    root_item.stop_want = x_stop_want

    # WHEN
    bud_dict = sue_bud.get_dict()
    itemroot_dict = bud_dict.get("_itemroot")

    # THEN
    assert itemroot_dict["teamunit"] == x_teamunit.get_dict()
    assert itemroot_dict["teamunit"] == {"_teamlinks": [run_str]}
    assert itemroot_dict.get("gogo_want") == x_gogo_want
    assert itemroot_dict.get("stop_want") == x_stop_want


def test_BudUnit_get_dict_ReturnsDictWith_itemroot_healerlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_str = "Yao"
    sue_bud.add_acctunit(yao_str)
    run_str = ";runners"
    yao_acctunit = sue_bud.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)
    run_healerlink = healerlink_shop()
    run_healerlink.set_healer_id(x_healer_id=run_str)
    sue_bud.edit_item_attr(road=sue_bud._fiscal_id, healerlink=run_healerlink)

    # WHEN
    bud_dict = sue_bud.get_dict()
    itemroot_dict = bud_dict.get("_itemroot")

    # THEN
    assert itemroot_dict["healerlink"] == run_healerlink.get_dict()


def test_BudUnit_get_dict_ReturnsDictWith_itemkid_TeamUnit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_str = "Yao"
    sue_bud.add_acctunit(yao_str)
    run_str = ";runners"
    yao_acctunit = sue_bud.get_acct(yao_str)
    yao_acctunit.add_membership(run_str)

    morn_str = "morning"
    morn_road = sue_bud.make_l1_road(morn_str)
    sue_bud.set_l1_item(itemunit_shop(morn_str))
    x_teamunit = teamunit_shop()
    x_teamunit.set_teamlink(team_id=run_str)
    sue_bud.edit_item_attr(teamunit=x_teamunit, road=morn_road)

    # WHEN
    bud_dict = sue_bud.get_dict()
    itemroot_dict = bud_dict.get("_itemroot")

    # THEN
    _kids = "_kids"
    _teamunit = "teamunit"

    team_dict_x = itemroot_dict[_kids][morn_str][_teamunit]
    assert team_dict_x == x_teamunit.get_dict()
    assert team_dict_x == {"_teamlinks": [run_str]}


def test_BudUnit_get_json_ReturnsCorrectJSON_SimpleExample():
    # ESTABLISH
    zia_bud = get_budunit_x1_3levels_1reason_1facts()
    x_fund_pool = 66000
    zia_bud.fund_pool = x_fund_pool
    x_fund_coin = 66
    zia_bud.fund_coin = x_fund_coin
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
    zia_bud.edit_item_attr(road=zia_bud._fiscal_id, healerlink=run_healerlink)
    zia_bud.edit_item_attr(road=zia_bud._fiscal_id, problem_bool=True)

    # WHEN
    x_json = zia_bud.get_json()

    # THEN
    _kids = "_kids"

    assert x_json is not None
    assert True == x_is_json(x_json)
    bud_dict = get_dict_from_json(x_json)

    assert bud_dict["_owner_id"] == zia_bud._owner_id
    assert bud_dict["_fiscal_id"] == zia_bud._fiscal_id
    assert bud_dict["tally"] == zia_bud.tally
    assert bud_dict["fund_pool"] == zia_bud.fund_pool
    assert bud_dict["fund_coin"] == zia_bud.fund_coin
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
        bud_dict["_last_gift_id"]

    x_itemroot = zia_bud._itemroot
    itemroot_dict = bud_dict.get("_itemroot")

    assert len(itemroot_dict[_kids]) == len(x_itemroot._kids)

    shave_str = "shave"
    shave_dict = itemroot_dict[_kids][shave_str]
    shave_factunits = shave_dict["factunits"]
    print(f"{shave_factunits=}")
    assert len(shave_factunits) == 1
    assert len(shave_factunits) == len(x_itemroot._kids[shave_str].factunits)
    itemroot_healerlink = itemroot_dict["healerlink"]
    print(f"{itemroot_healerlink=}")
    assert len(itemroot_healerlink) == 1
    assert x_itemroot.healerlink.any_healer_id_exists()
    assert x_itemroot.problem_bool


def test_BudUnit_get_json_ReturnsCorrectJSON_BigExample():
    # ESTABLISH
    yao_bud = budunit_v001()
    day_hour_str = "day_hour"
    day_hour_road = yao_bud.make_l1_road(day_hour_str)
    yao_bud.set_fact(base=day_hour_road, pick=day_hour_road, fopen=0, fnigh=23)
    day_min_str = "day_minute"
    day_min_road = yao_bud.make_l1_road(day_min_str)
    yao_bud.set_fact(base=day_min_road, pick=day_min_road, fopen=0, fnigh=59)
    factunit_x = factunit_shop(day_min_road, day_min_road, 5, 59)
    yao_bud.edit_item_attr(road=factunit_x.base, factunit=factunit_x)
    yao_bud.set_max_tree_traverse(2)
    yao_str = "Yao"
    yao_bud._originunit.set_originhold(yao_str, 1)

    # WHEN
    bud_dict = get_dict_from_json(yao_bud.get_json())

    # THEN
    _kids = "_kids"
    assert bud_dict["_owner_id"] == yao_bud._owner_id
    assert bud_dict["_fiscal_id"] == yao_bud._fiscal_id
    assert bud_dict["tally"] == yao_bud.tally
    assert bud_dict["max_tree_traverse"] == 2
    assert bud_dict["max_tree_traverse"] == yao_bud.max_tree_traverse
    assert bud_dict["_wall"] == yao_bud._wall

    x_itemroot = yao_bud._itemroot
    itemroot_dict = bud_dict.get("_itemroot")
    assert len(itemroot_dict[_kids]) == len(x_itemroot._kids)

    kids = itemroot_dict[_kids]
    day_min_dict = kids[day_min_str]
    day_min_factunits_dict = day_min_dict["factunits"]
    day_min_item_x = yao_bud.get_item_obj(day_min_road)
    print(f"{day_min_factunits_dict=}")
    assert len(day_min_factunits_dict) == 1
    assert len(day_min_factunits_dict) == len(day_min_item_x.factunits)

    _reasonunits = "reasonunits"
    cont_str = "Freelancing"
    ulti_str = "Ultimate Frisbee"
    cont_road = yao_bud.make_l1_road(cont_str)
    ulti_road = yao_bud.make_l1_road(ulti_str)
    cont_item = yao_bud.get_item_obj(cont_road)
    ulti_item = yao_bud.get_item_obj(ulti_road)
    cont_reasonunits_dict = itemroot_dict[_kids][cont_str][_reasonunits]
    ulti_reasonunits_dict = itemroot_dict[_kids][ulti_str][_reasonunits]
    assert len(cont_reasonunits_dict) == len(cont_item.reasonunits)
    assert len(ulti_reasonunits_dict) == len(ulti_item.reasonunits)
    originunit_str = "_originunit"
    originholds_str = "_originholds"
    assert len(bud_dict[originunit_str][originholds_str])

    anna_str = "Anna"
    anna_acctunit = yao_bud.get_acct(anna_str)
    assert anna_acctunit.get_membership(";Family").credit_vote == 6.2
    assert yao_bud._accts is not None
    assert len(yao_bud._accts) == 22


def test_budunit_get_from_json_ReturnsCorrectObjSimpleExample():
    # ESTABLISH
    zia_bud = get_budunit_x1_3levels_1reason_1facts()
    zia_bud.set_max_tree_traverse(23)
    tiger_fiscal_id = "tiger"
    zia_bud.set_fiscal_id(tiger_fiscal_id)
    zia_fund_pool = 80000
    zia_bud.fund_pool = zia_fund_pool
    zia_fund_coin = 8
    zia_bud.fund_coin = zia_fund_coin
    zia_resepect_bit = 5
    zia_bud.respect_bit = zia_resepect_bit
    zia_penny = 2
    zia_bud.penny = zia_penny
    zia_credor_respect = 200
    zia_debtor_respect = 200
    zia_bud.set_credor_respect(zia_credor_respect)
    zia_bud.set_debtor_respect(zia_debtor_respect)
    zia_last_gift_id = 73
    zia_bud.set_last_gift_id(zia_last_gift_id)

    shave_str = "shave"
    shave_road = zia_bud.make_l1_road(shave_str)
    shave_item_y1 = zia_bud.get_item_obj(shave_road)
    shave_item_y1._originunit.set_originhold(acct_id="Sue", importance=4.3)
    shave_item_y1.problem_bool = True
    # print(f"{shave_road=}")
    # print(f"{json_shave_item._label=} {json_shave_item._parent_road=}")

    sue_str = "Sue"
    zia_bud.add_acctunit(acct_id=sue_str, credit_belief=199, debtit_belief=199)
    xio_str = "Xio"
    zia_bud.add_acctunit(acct_id=xio_str)
    run_str = ";runners"
    sue_acctunit = zia_bud.get_acct(sue_str)
    xio_acctunit = zia_bud.get_acct(xio_str)
    sue_acctunit.add_membership(run_str)
    xio_acctunit.add_membership(run_str)
    run_teamunit = teamunit_shop()
    run_teamunit.set_teamlink(team_id=run_str)
    zia_bud.edit_item_attr(zia_bud._fiscal_id, teamunit=run_teamunit)
    xio_teamunit = teamunit_shop()
    xio_teamunit.set_teamlink(team_id=xio_str)
    zia_bud.edit_item_attr(shave_road, teamunit=xio_teamunit)
    zia_bud.edit_item_attr(shave_road, awardlink=awardlink_shop(xio_str))
    zia_bud.edit_item_attr(shave_road, awardlink=awardlink_shop(sue_str))
    zia_bud.edit_item_attr(zia_bud._fiscal_id, awardlink=awardlink_shop(sue_str))
    # add healerlink to shave itemunit
    run_healerlink = healerlink_shop({run_str})
    zia_bud.edit_item_attr(shave_road, healerlink=run_healerlink)
    shave_item = zia_bud.get_item_obj(shave_road)
    zia_gogo_want = 75
    zia_stop_want = 77
    shave_item.gogo_want = zia_gogo_want
    shave_item.stop_want = zia_stop_want

    yao_str = "Yao"
    zia_bud._originunit.set_originhold(yao_str, 1)
    override_str = "override"

    # WHEN
    x_json = zia_bud.get_json()
    assert x_is_json(x_json) is True
    json_bud = budunit_get_from_json(x_bud_json=x_json)

    # THEN
    assert str(type(json_bud)).find(".bud.BudUnit'>") > 0
    assert json_bud._owner_id is not None
    assert json_bud._owner_id == zia_bud._owner_id
    assert json_bud._fiscal_id == zia_bud._fiscal_id
    assert json_bud.fund_pool == zia_fund_pool
    assert json_bud.fund_pool == zia_bud.fund_pool
    assert json_bud.fund_coin == zia_fund_coin
    assert json_bud.fund_coin == zia_bud.fund_coin
    assert json_bud.respect_bit == zia_resepect_bit
    assert json_bud.respect_bit == zia_bud.respect_bit
    assert json_bud.penny == zia_penny
    assert json_bud.penny == zia_bud.penny
    assert json_bud.max_tree_traverse == 23
    assert json_bud.max_tree_traverse == zia_bud.max_tree_traverse
    assert json_bud._wall == zia_bud._wall
    assert json_bud.credor_respect == zia_bud.credor_respect
    assert json_bud.debtor_respect == zia_bud.debtor_respect
    assert json_bud.credor_respect == zia_credor_respect
    assert json_bud.debtor_respect == zia_debtor_respect
    assert json_bud._last_gift_id == zia_bud._last_gift_id
    assert json_bud._last_gift_id == zia_last_gift_id
    # assert json_bud._groups == zia_bud._groups

    json_itemroot = json_bud._itemroot
    assert json_itemroot._parent_road == ""
    assert json_itemroot._parent_road == zia_bud._itemroot._parent_road
    assert json_itemroot.reasonunits == {}
    assert json_itemroot.teamunit == zia_bud._itemroot.teamunit
    assert json_itemroot.teamunit == run_teamunit
    assert json_itemroot._fund_coin == 8
    assert json_itemroot._fund_coin == zia_fund_coin
    assert len(json_itemroot.factunits) == 1
    assert len(json_itemroot.awardlinks) == 1

    assert len(json_bud._itemroot._kids) == 2

    weekday_str = "weekdays"
    weekday_road = json_bud.make_l1_road(weekday_str)
    weekday_item_x = json_bud.get_item_obj(weekday_road)
    assert len(weekday_item_x._kids) == 2

    sunday_str = "Sunday"
    sunday_road = json_bud.make_road(weekday_road, sunday_str)
    sunday_item = json_bud.get_item_obj(sunday_road)
    assert sunday_item.mass == 20

    json_shave_item = json_bud.get_item_obj(shave_road)
    zia_shave_item = zia_bud.get_item_obj(shave_road)
    assert len(json_shave_item.reasonunits) == 1
    assert json_shave_item.teamunit == zia_shave_item.teamunit
    assert json_shave_item.teamunit == xio_teamunit
    assert json_shave_item._originunit == zia_shave_item._originunit
    print(f"{json_shave_item.healerlink=}")
    assert json_shave_item.healerlink == zia_shave_item.healerlink
    assert len(json_shave_item.awardlinks) == 2
    assert len(json_shave_item.factunits) == 1
    assert zia_shave_item.problem_bool
    assert json_shave_item.problem_bool == zia_shave_item.problem_bool
    assert json_shave_item.gogo_want == zia_shave_item.gogo_want
    assert json_shave_item.stop_want == zia_shave_item.stop_want

    assert len(json_bud._originunit._originholds) == 1
    assert json_bud._originunit == zia_bud._originunit


def test_budunit_get_from_json_ReturnsCorrectItemRoot():
    # ESTABLISH
    zia_bud = get_budunit_x1_3levels_1reason_1facts()
    zia_bud.set_max_tree_traverse(23)
    # root_item = zia_bud.get_item_obj(zia_bud.get_item_obj(zia_bud._fiscal_id))
    root_item = zia_bud._itemroot
    zia_gogo_want = 75
    zia_stop_want = 77
    root_item.gogo_want = zia_gogo_want
    root_item.stop_want = zia_stop_want

    # WHEN
    x_json = zia_bud.get_json()
    assert x_is_json(x_json) is True
    json_bud = budunit_get_from_json(x_bud_json=x_json)

    # THEN
    json_itemroot = json_bud.get_item_obj(zia_bud._fiscal_id)
    assert json_itemroot.gogo_want == zia_gogo_want
    assert json_itemroot.stop_want == zia_stop_want


def test_budunit_get_from_json_ReturnsCorrectObj_wall_Example():
    # ESTABLISH
    slash_wall = "/"
    before_bob_bud = budunit_shop("Bob", _wall=slash_wall)
    assert before_bob_bud._wall != default_wall_if_None()

    # WHEN
    bob_json = before_bob_bud.get_json()
    after_bob_bud = budunit_get_from_json(bob_json)

    # THEN
    assert after_bob_bud._wall != default_wall_if_None()
    assert after_bob_bud._wall == slash_wall
    assert after_bob_bud._wall == before_bob_bud._wall


def test_budunit_get_from_json_ReturnsCorrectObj_wall_AcctExample():
    # ESTABLISH
    slash_wall = "/"
    before_bob_bud = budunit_shop("Bob", _wall=slash_wall)
    bob_str = ",Bob"
    before_bob_bud.add_acctunit(bob_str)
    assert before_bob_bud.acct_exists(bob_str)

    # WHEN
    bob_json = before_bob_bud.get_json()
    after_bob_bud = budunit_get_from_json(bob_json)

    # THEN
    after_bob_acctunit = after_bob_bud.get_acct(bob_str)
    assert after_bob_acctunit._wall == slash_wall


def test_budunit_get_from_json_ReturnsCorrectObj_wall_GroupExample():
    # ESTABLISH
    slash_wall = "/"
    before_bob_bud = budunit_shop("Bob", _wall=slash_wall)
    yao_str = "Yao"
    swim_str = f"{slash_wall}Swimmers"
    before_bob_bud.add_acctunit(yao_str)
    yao_acctunit = before_bob_bud.get_acct(yao_str)
    yao_acctunit.add_membership(swim_str)

    # WHEN
    bob_json = before_bob_bud.get_json()
    after_bob_bud = budunit_get_from_json(bob_json)

    # THEN
    after_yao_acctunit = after_bob_bud.get_acct(yao_str)
    assert after_yao_acctunit._wall == slash_wall


def test_budunit_get_from_json_ExportsBudUnit_mass():
    # ESTABLISH
    x1_bud = budunit_v001()
    x1_bud.tally = 15
    assert x1_bud.tally == 15
    assert x1_bud._itemroot.mass != x1_bud.tally
    assert x1_bud._itemroot.mass == 1

    # WHEN
    x2_bud = budunit_get_from_json(x1_bud.get_json())

    # THEN
    assert x1_bud.tally == 15
    assert x1_bud.tally == x2_bud.tally
    assert x1_bud._itemroot.mass == 1
    assert x1_bud._itemroot.mass == x2_bud._itemroot.mass
    assert x1_bud._itemroot._kids == x2_bud._itemroot._kids


def test_get_dict_of_bud_from_dict_ReturnsDictOfBudUnits():
    # ESTABLISH
    x1_bud = budunit_v001()
    x2_bud = get_budunit_x1_3levels_1reason_1facts()
    x3_bud = get_budunit_base_time_example()
    print(f"{x1_bud._owner_id}")
    print(f"{x2_bud._owner_id}")
    print(f"{x3_bud._owner_id}")

    cn_dict_of_dicts = {
        x1_bud._owner_id: x1_bud.get_dict(),
        x2_bud._owner_id: x2_bud.get_dict(),
        x3_bud._owner_id: x3_bud.get_dict(),
    }

    # WHEN
    ccn_dict_of_obj = get_dict_of_bud_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(x1_bud._owner_id) is not None
    assert ccn_dict_of_obj.get(x2_bud._owner_id) is not None
    assert ccn_dict_of_obj.get(x3_bud._owner_id) is not None

    ccn2_bud = ccn_dict_of_obj.get(x2_bud._owner_id)
    assert ccn2_bud._itemroot._label == x2_bud._itemroot._label
    assert ccn2_bud._itemroot._parent_road == x2_bud._itemroot._parent_road
    assert ccn2_bud._itemroot._fund_coin == x2_bud._itemroot._fund_coin
    shave_road = ccn2_bud.make_l1_road("shave")
    week_road = ccn2_bud.make_l1_road("weekdays")
    # assert ccn2_bud.get_item_obj(shave_road) == x2_bud.get_item_obj(shave_road)
    # assert ccn2_bud.get_item_obj(week_road) == x2_bud.get_item_obj(week_road)
    # assert ccn2_bud._itemroot == x2_bud._itemroot
    assert ccn2_bud.get_dict() == x2_bud.get_dict()

    ccn_bud3 = ccn_dict_of_obj.get(x3_bud._owner_id)
    assert ccn_bud3.get_dict() == x3_bud.get_dict()

    cc1_item_root = ccn_dict_of_obj.get(x1_bud._owner_id)._itemroot
    assert cc1_item_root._originunit == x1_bud._itemroot._originunit
    ccn_bud1 = ccn_dict_of_obj.get(x1_bud._owner_id)
    assert ccn_bud1._item_dict == x1_bud._item_dict
    philipa_str = "Philipa"
    ccn_philipa_acctunit = ccn_bud1.get_acct(philipa_str)
    x1_philipa_acctunit = x1_bud.get_acct(philipa_str)
    assert ccn_philipa_acctunit._memberships == x1_philipa_acctunit._memberships
    assert ccn_bud1 == x1_bud
    assert ccn_dict_of_obj.get(x1_bud._owner_id) == x1_bud
