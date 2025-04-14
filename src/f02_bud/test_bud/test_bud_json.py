from src.a00_data_toolboxs.dict_toolbox import x_is_json, get_dict_from_json
from src.a01_word_logic.road import default_bridge_if_None
from src.a03_group_logic.group import awardlink_shop
from src.f02_bud.healer import healerlink_shop
from src.a04_reason_logic.reason_team import teamunit_shop
from src.a04_reason_logic.reason_item import factunit_shop
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
    day_hour_item._originunit.set_originhold(acct_name="Bob", importance=2)
    yao_bud.add_fact(base=day_hour_road, pick=day_hour_road, fopen=0, fnigh=23)
    time_minute = yao_bud.make_l1_road("day_minute")
    yao_bud.add_fact(base=time_minute, pick=time_minute, fopen=0, fnigh=1440)
    yao_str = "Yao"
    yao_bud.originunit.set_originhold(yao_str, 1)
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
    x_last_pack_id = 77
    yao_bud.set_last_pack_id(x_last_pack_id)

    # WHEN
    bud_dict = yao_bud.get_dict()

    # THEN
    assert bud_dict is not None
    assert str(type(bud_dict)) == "<class 'dict'>"
    assert bud_dict["owner_name"] == yao_bud.owner_name
    assert bud_dict["fisc_title"] == yao_bud.fisc_title
    assert bud_dict["tally"] == yao_bud.tally
    assert bud_dict["tally"] == bud_tally
    assert bud_dict["fund_pool"] == yao_fund_pool
    assert bud_dict["fund_coin"] == yao_fund_coin
    assert bud_dict["max_tree_traverse"] == yao_bud.max_tree_traverse
    assert bud_dict["bridge"] == yao_bud.bridge
    assert bud_dict["credor_respect"] == yao_bud.credor_respect
    assert bud_dict["debtor_respect"] == yao_bud.debtor_respect
    assert bud_dict["last_pack_id"] == yao_bud.last_pack_id
    assert len(bud_dict["accts"]) == len(yao_bud.accts)
    assert len(bud_dict["accts"]) != 12
    assert bud_dict.get("_groups") is None

    x_itemroot = yao_bud.itemroot
    itemroot_dict = bud_dict["itemroot"]
    _kids = "_kids"
    assert x_itemroot.item_title == yao_bud.fisc_title
    assert itemroot_dict["item_title"] == x_itemroot.item_title
    assert itemroot_dict["mass"] == x_itemroot.mass
    assert len(itemroot_dict[_kids]) == len(x_itemroot._kids)

    originunit_str = "originunit"
    day_hour_originunit_dict = itemroot_dict[_kids][day_hour_str][originunit_str]
    assert day_hour_originunit_dict == day_hour_item._originunit.get_dict()
    originholds_str = "_originholds"
    yao_bud_originhold = bud_dict[originunit_str][originholds_str][yao_str]
    print(f"{yao_bud_originhold=}")
    assert yao_bud_originhold
    assert yao_bud_originhold["acct_name"] == yao_str
    assert yao_bud_originhold["importance"] == 1


def test_BudUnit_get_dict_ReturnsDictWith_itemroot_teamunit():
    # ESTABLISH
    run_str = "runners"
    sue_bud = budunit_shop("Sue")
    x_teamunit = teamunit_shop()
    x_teamunit.set_teamlink(team_tag=run_str)
    sue_bud.edit_item_attr(sue_bud.fisc_title, teamunit=x_teamunit)
    root_item = sue_bud.get_item_obj(sue_bud.fisc_title)
    x_gogo_want = 5
    x_stop_want = 11
    root_item.gogo_want = x_gogo_want
    root_item.stop_want = x_stop_want

    # WHEN
    bud_dict = sue_bud.get_dict()
    itemroot_dict = bud_dict.get("itemroot")

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
    run_healerlink.set_healer_name(x_healer_name=run_str)
    sue_bud.edit_item_attr(road=sue_bud.fisc_title, healerlink=run_healerlink)

    # WHEN
    bud_dict = sue_bud.get_dict()
    itemroot_dict = bud_dict.get("itemroot")

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
    x_teamunit.set_teamlink(team_tag=run_str)
    sue_bud.edit_item_attr(teamunit=x_teamunit, road=morn_road)

    # WHEN
    bud_dict = sue_bud.get_dict()
    itemroot_dict = bud_dict.get("itemroot")

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
    zia_bud.edit_item_attr(road=zia_bud.fisc_title, healerlink=run_healerlink)
    zia_bud.edit_item_attr(road=zia_bud.fisc_title, problem_bool=True)

    # WHEN
    x_json = zia_bud.get_json()

    # THEN
    _kids = "_kids"

    assert x_json is not None
    assert True == x_is_json(x_json)
    bud_dict = get_dict_from_json(x_json)

    assert bud_dict["owner_name"] == zia_bud.owner_name
    assert bud_dict["fisc_title"] == zia_bud.fisc_title
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
        bud_dict["last_pack_id"]

    x_itemroot = zia_bud.itemroot
    itemroot_dict = bud_dict.get("itemroot")

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
    assert x_itemroot.healerlink.any_healer_name_exists()
    assert x_itemroot.problem_bool


def test_BudUnit_get_json_ReturnsCorrectJSON_BigExample():
    # ESTABLISH
    yao_bud = budunit_v001()
    day_hour_str = "day_hour"
    day_hour_road = yao_bud.make_l1_road(day_hour_str)
    yao_bud.add_fact(base=day_hour_road, pick=day_hour_road, fopen=0, fnigh=23)
    day_min_str = "day_minute"
    day_min_road = yao_bud.make_l1_road(day_min_str)
    yao_bud.add_fact(base=day_min_road, pick=day_min_road, fopen=0, fnigh=59)
    factunit_x = factunit_shop(day_min_road, day_min_road, 5, 59)
    yao_bud.edit_item_attr(road=factunit_x.base, factunit=factunit_x)
    yao_bud.set_max_tree_traverse(2)
    yao_str = "Yao"
    yao_bud.originunit.set_originhold(yao_str, 1)

    # WHEN
    bud_dict = get_dict_from_json(yao_bud.get_json())

    # THEN
    _kids = "_kids"
    assert bud_dict["owner_name"] == yao_bud.owner_name
    assert bud_dict["fisc_title"] == yao_bud.fisc_title
    assert bud_dict["tally"] == yao_bud.tally
    assert bud_dict["max_tree_traverse"] == 2
    assert bud_dict["max_tree_traverse"] == yao_bud.max_tree_traverse
    assert bud_dict["bridge"] == yao_bud.bridge

    x_itemroot = yao_bud.itemroot
    itemroot_dict = bud_dict.get("itemroot")
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
    tiger_fisc_title = "tiger"
    zia_bud.set_fisc_title(tiger_fisc_title)
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
    zia_last_pack_id = 73
    zia_bud.set_last_pack_id(zia_last_pack_id)

    shave_str = "shave"
    shave_road = zia_bud.make_l1_road(shave_str)
    shave_item_y1 = zia_bud.get_item_obj(shave_road)
    shave_item_y1._originunit.set_originhold(acct_name="Sue", importance=4.3)
    shave_item_y1.problem_bool = True
    # print(f"{shave_road=}")
    # print(f"{json_shave_item.item_title=} {json_shave_item.parent_road=}")

    sue_str = "Sue"
    zia_bud.add_acctunit(acct_name=sue_str, credit_belief=199, debtit_belief=199)
    xio_str = "Xio"
    zia_bud.add_acctunit(acct_name=xio_str)
    run_str = ";runners"
    sue_acctunit = zia_bud.get_acct(sue_str)
    xio_acctunit = zia_bud.get_acct(xio_str)
    sue_acctunit.add_membership(run_str)
    xio_acctunit.add_membership(run_str)
    run_teamunit = teamunit_shop()
    run_teamunit.set_teamlink(team_tag=run_str)
    zia_bud.edit_item_attr(zia_bud.fisc_title, teamunit=run_teamunit)
    xio_teamunit = teamunit_shop()
    xio_teamunit.set_teamlink(team_tag=xio_str)
    zia_bud.edit_item_attr(shave_road, teamunit=xio_teamunit)
    zia_bud.edit_item_attr(shave_road, awardlink=awardlink_shop(xio_str))
    zia_bud.edit_item_attr(shave_road, awardlink=awardlink_shop(sue_str))
    zia_bud.edit_item_attr(zia_bud.fisc_title, awardlink=awardlink_shop(sue_str))
    # add healerlink to shave itemunit
    run_healerlink = healerlink_shop({run_str})
    zia_bud.edit_item_attr(shave_road, healerlink=run_healerlink)
    shave_item = zia_bud.get_item_obj(shave_road)
    zia_gogo_want = 75
    zia_stop_want = 77
    shave_item.gogo_want = zia_gogo_want
    shave_item.stop_want = zia_stop_want

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
    assert json_bud.fisc_title == zia_bud.fisc_title
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
    assert json_bud.bridge == zia_bud.bridge
    assert json_bud.credor_respect == zia_bud.credor_respect
    assert json_bud.debtor_respect == zia_bud.debtor_respect
    assert json_bud.credor_respect == zia_credor_respect
    assert json_bud.debtor_respect == zia_debtor_respect
    assert json_bud.last_pack_id == zia_bud.last_pack_id
    assert json_bud.last_pack_id == zia_last_pack_id
    # assert json_bud._groups == zia_bud._groups

    json_itemroot = json_bud.itemroot
    assert json_itemroot.parent_road == ""
    assert json_itemroot.parent_road == zia_bud.itemroot.parent_road
    assert json_itemroot.reasonunits == {}
    assert json_itemroot.teamunit == zia_bud.itemroot.teamunit
    assert json_itemroot.teamunit == run_teamunit
    assert json_itemroot.fund_coin == 8
    assert json_itemroot.fund_coin == zia_fund_coin
    assert len(json_itemroot.factunits) == 1
    assert len(json_itemroot.awardlinks) == 1

    assert len(json_bud.itemroot._kids) == 2

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

    assert len(json_bud.originunit._originholds) == 1
    assert json_bud.originunit == zia_bud.originunit


def test_budunit_get_from_json_ReturnsCorrectItemRoot():
    # ESTABLISH
    zia_bud = get_budunit_x1_3levels_1reason_1facts()
    zia_bud.set_max_tree_traverse(23)
    # root_item = zia_bud.get_item_obj(zia_bud.get_item_obj(zia_bud.fisc_title))
    root_item = zia_bud.itemroot
    zia_gogo_want = 75
    zia_stop_want = 77
    root_item.gogo_want = zia_gogo_want
    root_item.stop_want = zia_stop_want

    # WHEN
    x_json = zia_bud.get_json()
    assert x_is_json(x_json) is True
    json_bud = budunit_get_from_json(x_bud_json=x_json)

    # THEN
    json_itemroot = json_bud.get_item_obj(zia_bud.fisc_title)
    assert json_itemroot.gogo_want == zia_gogo_want
    assert json_itemroot.stop_want == zia_stop_want


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


def test_budunit_get_from_json_ExportsBudUnit_mass():
    # ESTABLISH
    x1_bud = budunit_v001()
    x1_bud.tally = 15
    assert x1_bud.tally == 15
    assert x1_bud.itemroot.mass != x1_bud.tally
    assert x1_bud.itemroot.mass == 1

    # WHEN
    x2_bud = budunit_get_from_json(x1_bud.get_json())

    # THEN
    assert x1_bud.tally == 15
    assert x1_bud.tally == x2_bud.tally
    assert x1_bud.itemroot.mass == 1
    assert x1_bud.itemroot.mass == x2_bud.itemroot.mass
    assert x1_bud.itemroot._kids == x2_bud.itemroot._kids


def test_get_dict_of_bud_from_dict_ReturnsDictOfBudUnits():
    # ESTABLISH
    x1_bud = budunit_v001()
    x2_bud = get_budunit_x1_3levels_1reason_1facts()
    x3_bud = get_budunit_base_time_example()
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
    assert ccn2_bud.itemroot.item_title == x2_bud.itemroot.item_title
    assert ccn2_bud.itemroot.parent_road == x2_bud.itemroot.parent_road
    assert ccn2_bud.itemroot.fund_coin == x2_bud.itemroot.fund_coin
    shave_road = ccn2_bud.make_l1_road("shave")
    week_road = ccn2_bud.make_l1_road("weekdays")
    # assert ccn2_bud.get_item_obj(shave_road) == x2_bud.get_item_obj(shave_road)
    # assert ccn2_bud.get_item_obj(week_road) == x2_bud.get_item_obj(week_road)
    # assert ccn2_bud.itemroot == x2_bud.itemroot
    assert ccn2_bud.get_dict() == x2_bud.get_dict()

    ccn_bud3 = ccn_dict_of_obj.get(x3_bud.owner_name)
    assert ccn_bud3.get_dict() == x3_bud.get_dict()

    cc1_item_root = ccn_dict_of_obj.get(x1_bud.owner_name).itemroot
    assert cc1_item_root._originunit == x1_bud.itemroot._originunit
    ccn_bud1 = ccn_dict_of_obj.get(x1_bud.owner_name)
    assert ccn_bud1._item_dict == x1_bud._item_dict
    philipa_str = "Philipa"
    ccn_philipa_acctunit = ccn_bud1.get_acct(philipa_str)
    x1_philipa_acctunit = x1_bud.get_acct(philipa_str)
    assert ccn_philipa_acctunit._memberships == x1_philipa_acctunit._memberships
    assert ccn_bud1 == x1_bud
    assert ccn_dict_of_obj.get(x1_bud.owner_name) == x1_bud
