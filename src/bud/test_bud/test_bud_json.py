from src._instrument.python_tool import x_is_json, get_dict_from_json
from src._road.road import default_road_delimiter_if_none
from src.bud.group import awardlink_shop
from src.bud.healer import healerlink_shop
from src.bud.reason_team import teamunit_shop
from src.bud.reason_idea import factunit_shop
from src.bud.idea import ideaunit_shop
from src.bud.bud import (
    budunit_shop,
    get_from_json as budunit_get_from_json,
    get_dict_of_bud_from_dict,
)
from src.bud.examples.example_buds import (
    budunit_v001,
    get_budunit_x1_3levels_1reason_1facts,
    get_budunit_base_time_example,
)
from pytest import raises as pytest_raises


def test_BudUnit_get_dict_ReturnsDictObject():
    # ESTABLISH
    yao_bud = budunit_v001()
    day_hour_text = "day_hour"
    day_hour_road = yao_bud.make_l1_road(day_hour_text)
    day_hour_idea = yao_bud.get_idea_obj(day_hour_road)
    day_hour_idea._originunit.set_originhold(acct_id="Bob", importance=2)
    yao_bud.set_fact(base=day_hour_road, pick=day_hour_road, fopen=0, fnigh=23)
    time_minute = yao_bud.make_l1_road("day_minute")
    yao_bud.set_fact(base=time_minute, pick=time_minute, fopen=0, fnigh=1440)
    yao_text = "Yao"
    yao_bud._originunit.set_originhold(yao_text, 1)
    yao_fund_pool = 23000
    yao_bud._fund_pool = yao_fund_pool
    yao_fund_coin = 23
    yao_bud._fund_coin = yao_fund_coin
    bud_tally = 23
    yao_bud._tally = bud_tally
    x_credor_respect = 22
    x_debtor_respect = 44
    yao_bud.set_credor_respect(x_credor_respect)
    yao_bud.set_debtor_respect(x_debtor_respect)
    override_text = "override"
    x_last_gift_id = 77
    yao_bud.set_last_gift_id(x_last_gift_id)

    # WHEN
    bud_dict = yao_bud.get_dict()

    # THEN
    assert bud_dict is not None
    assert str(type(bud_dict)) == "<class 'dict'>"
    assert bud_dict["_owner_id"] == yao_bud._owner_id
    assert bud_dict["_real_id"] == yao_bud._real_id
    assert bud_dict["_tally"] == yao_bud._tally
    assert bud_dict["_tally"] == bud_tally
    assert bud_dict["_fund_pool"] == yao_fund_pool
    assert bud_dict["_fund_coin"] == yao_fund_coin
    assert bud_dict["_max_tree_traverse"] == yao_bud._max_tree_traverse
    assert bud_dict["_road_delimiter"] == yao_bud._road_delimiter
    assert bud_dict["_credor_respect"] == yao_bud._credor_respect
    assert bud_dict["_debtor_respect"] == yao_bud._debtor_respect
    assert bud_dict["_last_gift_id"] == yao_bud._last_gift_id
    assert len(bud_dict["_accts"]) == len(yao_bud._accts)
    assert len(bud_dict["_accts"]) != 12
    assert bud_dict.get("_groups") is None

    x_idearoot = yao_bud._idearoot
    idearoot_dict = bud_dict["_idearoot"]
    _kids = "_kids"
    assert x_idearoot._label == yao_bud._real_id
    assert idearoot_dict["_label"] == x_idearoot._label
    assert idearoot_dict["mass"] == x_idearoot.mass
    assert len(idearoot_dict[_kids]) == len(x_idearoot._kids)

    originunit_text = "_originunit"
    day_hour_originunit_dict = idearoot_dict[_kids][day_hour_text][originunit_text]
    assert day_hour_originunit_dict == day_hour_idea._originunit.get_dict()
    originholds_text = "_originholds"
    yao_bud_originhold = bud_dict[originunit_text][originholds_text][yao_text]
    print(f"{yao_bud_originhold=}")
    assert yao_bud_originhold
    assert yao_bud_originhold["acct_id"] == yao_text
    assert yao_bud_originhold["importance"] == 1


def test_BudUnit_get_dict_ReturnsDictWith_idearoot_teamunit():
    # ESTABLISH
    run_text = "runners"
    sue_bud = budunit_shop("Sue")
    x_teamunit = teamunit_shop()
    x_teamunit.set_teamlink(group_id=run_text)
    sue_bud.edit_idea_attr(sue_bud._real_id, teamunit=x_teamunit)
    root_idea = sue_bud.get_idea_obj(sue_bud._real_id)
    x_gogo_want = 5
    x_stop_want = 11
    root_idea.gogo_want = x_gogo_want
    root_idea.stop_want = x_stop_want

    # WHEN
    bud_dict = sue_bud.get_dict()
    idearoot_dict = bud_dict.get("_idearoot")

    # THEN
    assert idearoot_dict["_teamunit"] == x_teamunit.get_dict()
    assert idearoot_dict["_teamunit"] == {"_teamlinks": [run_text]}
    assert idearoot_dict.get("gogo_want") == x_gogo_want
    assert idearoot_dict.get("stop_want") == x_stop_want


def test_BudUnit_get_dict_ReturnsDictWith_idearoot_healerlink():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_text = "Yao"
    sue_bud.add_acctunit(yao_text)
    run_text = ";runners"
    yao_acctunit = sue_bud.get_acct(yao_text)
    yao_acctunit.add_membership(run_text)
    run_healerlink = healerlink_shop()
    run_healerlink.set_healer_id(x_healer_id=run_text)
    sue_bud.edit_idea_attr(road=sue_bud._real_id, healerlink=run_healerlink)

    # WHEN
    bud_dict = sue_bud.get_dict()
    idearoot_dict = bud_dict.get("_idearoot")

    # THEN
    assert idearoot_dict["healerlink"] == run_healerlink.get_dict()


def test_BudUnit_get_dict_ReturnsDictWith_ideakid_TeamUnit():
    # ESTABLISH
    sue_bud = budunit_shop("Sue")
    yao_text = "Yao"
    sue_bud.add_acctunit(yao_text)
    run_text = ";runners"
    yao_acctunit = sue_bud.get_acct(yao_text)
    yao_acctunit.add_membership(run_text)

    morn_text = "morning"
    morn_road = sue_bud.make_l1_road(morn_text)
    sue_bud.set_l1_idea(ideaunit_shop(morn_text))
    x_teamunit = teamunit_shop()
    x_teamunit.set_teamlink(group_id=run_text)
    sue_bud.edit_idea_attr(teamunit=x_teamunit, road=morn_road)

    # WHEN
    bud_dict = sue_bud.get_dict()
    idearoot_dict = bud_dict.get("_idearoot")

    # THEN
    _kids = "_kids"
    _teamunit = "_teamunit"

    team_dict_x = idearoot_dict[_kids][morn_text][_teamunit]
    assert team_dict_x == x_teamunit.get_dict()
    assert team_dict_x == {"_teamlinks": [run_text]}


def test_BudUnit_get_json_ReturnsCorrectJSON_SimpleExample():
    # ESTABLISH
    zia_bud = get_budunit_x1_3levels_1reason_1facts()
    x_fund_pool = 66000
    zia_bud._fund_pool = x_fund_pool
    x_fund_coin = 66
    zia_bud._fund_coin = x_fund_coin
    x_bit = 7
    zia_bud._bit = x_bit
    x_penny = 0.3
    zia_bud._penny = x_penny
    override_text = "override"
    yao_text = "Yao"
    run_text = ";runners"
    zia_bud.add_acctunit(yao_text)
    yao_acctunit = zia_bud.get_acct(yao_text)
    yao_acctunit.add_membership(run_text)
    run_healerlink = healerlink_shop({run_text})
    zia_bud.edit_idea_attr(road=zia_bud._real_id, healerlink=run_healerlink)
    zia_bud.edit_idea_attr(road=zia_bud._real_id, problem_bool=True)

    # WHEN
    x_json = zia_bud.get_json()

    # THEN
    _kids = "_kids"

    assert x_json is not None
    assert True == x_is_json(x_json)
    bud_dict = get_dict_from_json(x_json)

    assert bud_dict["_owner_id"] == zia_bud._owner_id
    assert bud_dict["_real_id"] == zia_bud._real_id
    assert bud_dict["_tally"] == zia_bud._tally
    assert bud_dict["_fund_pool"] == zia_bud._fund_pool
    assert bud_dict["_fund_coin"] == zia_bud._fund_coin
    assert bud_dict["_bit"] == zia_bud._bit
    assert bud_dict["_penny"] == zia_bud._penny
    assert bud_dict["_credor_respect"] == zia_bud._credor_respect
    assert bud_dict["_debtor_respect"] == zia_bud._debtor_respect
    # with pytest_raises(Exception) as excinfo:
    #     bud_dict["_credor_respect"]
    # assert str(excinfo.value) == "'_credor_respect'"
    # with pytest_raises(Exception) as excinfo:
    #     bud_dict["_debtor_respect"]
    # assert str(excinfo.value) == "'_debtor_respect'"
    with pytest_raises(Exception) as excinfo:
        bud_dict["_last_gift_id"]

    x_idearoot = zia_bud._idearoot
    idearoot_dict = bud_dict.get("_idearoot")

    assert len(idearoot_dict[_kids]) == len(x_idearoot._kids)

    shave_text = "shave"
    shave_dict = idearoot_dict[_kids][shave_text]
    shave_factunits = shave_dict["_factunits"]
    print(f"{shave_factunits=}")
    assert len(shave_factunits) == 1
    assert len(shave_factunits) == len(x_idearoot._kids[shave_text]._factunits)
    idearoot_healerlink = idearoot_dict["healerlink"]
    print(f"{idearoot_healerlink=}")
    assert len(idearoot_healerlink) == 1
    assert x_idearoot.healerlink.any_healer_id_exists()
    assert x_idearoot.problem_bool


def test_BudUnit_get_json_ReturnsCorrectJSON_BigExample():
    # ESTABLISH
    yao_bud = budunit_v001()
    day_hour_text = "day_hour"
    day_hour_road = yao_bud.make_l1_road(day_hour_text)
    yao_bud.set_fact(base=day_hour_road, pick=day_hour_road, fopen=0, fnigh=23)
    day_min_text = "day_minute"
    day_min_road = yao_bud.make_l1_road(day_min_text)
    yao_bud.set_fact(base=day_min_road, pick=day_min_road, fopen=0, fnigh=59)
    factunit_x = factunit_shop(day_min_road, day_min_road, 5, 59)
    yao_bud.edit_idea_attr(road=factunit_x.base, factunit=factunit_x)
    yao_bud.set_max_tree_traverse(2)
    yao_text = "Yao"
    yao_bud._originunit.set_originhold(yao_text, 1)

    # WHEN
    bud_dict = get_dict_from_json(yao_bud.get_json())

    # THEN
    _kids = "_kids"
    assert bud_dict["_owner_id"] == yao_bud._owner_id
    assert bud_dict["_real_id"] == yao_bud._real_id
    assert bud_dict["_tally"] == yao_bud._tally
    assert bud_dict["_max_tree_traverse"] == 2
    assert bud_dict["_max_tree_traverse"] == yao_bud._max_tree_traverse
    assert bud_dict["_road_delimiter"] == yao_bud._road_delimiter

    x_idearoot = yao_bud._idearoot
    idearoot_dict = bud_dict.get("_idearoot")
    assert len(idearoot_dict[_kids]) == len(x_idearoot._kids)

    kids = idearoot_dict[_kids]
    day_min_dict = kids[day_min_text]
    day_min_factunits_dict = day_min_dict["_factunits"]
    day_min_idea_x = yao_bud.get_idea_obj(day_min_road)
    print(f"{day_min_factunits_dict=}")
    assert len(day_min_factunits_dict) == 1
    assert len(day_min_factunits_dict) == len(day_min_idea_x._factunits)

    _reasonunits = "_reasonunits"
    cont_text = "Freelancing"
    ulti_text = "Ultimate Frisbee"
    cont_road = yao_bud.make_l1_road(cont_text)
    ulti_road = yao_bud.make_l1_road(ulti_text)
    cont_idea = yao_bud.get_idea_obj(cont_road)
    ulti_idea = yao_bud.get_idea_obj(ulti_road)
    cont_reasonunits_dict = idearoot_dict[_kids][cont_text][_reasonunits]
    ulti_reasonunits_dict = idearoot_dict[_kids][ulti_text][_reasonunits]
    assert len(cont_reasonunits_dict) == len(cont_idea._reasonunits)
    assert len(ulti_reasonunits_dict) == len(ulti_idea._reasonunits)
    originunit_text = "_originunit"
    originholds_text = "_originholds"
    assert len(bud_dict[originunit_text][originholds_text])

    anna_text = "Anna"
    anna_acctunit = yao_bud.get_acct(anna_text)
    assert anna_acctunit.get_membership(";Family").credit_vote == 6.2
    assert yao_bud._accts is not None
    assert len(yao_bud._accts) == 22


def test_budunit_get_from_json_ReturnsCorrectObjSimpleExample():
    # ESTABLISH
    zia_bud = get_budunit_x1_3levels_1reason_1facts()
    zia_bud.set_max_tree_traverse(23)
    tiger_real_id = "tiger"
    zia_bud.set_real_id(tiger_real_id)
    zia_fund_pool = 80000
    zia_bud._fund_pool = zia_fund_pool
    zia_fund_coin = 8
    zia_bud._fund_coin = zia_fund_coin
    zia_bit = 5
    zia_bud._bit = zia_bit
    zia_penny = 2
    zia_bud._penny = zia_penny
    zia_credor_respect = 200
    zia_debtor_respect = 200
    zia_bud.set_credor_respect(zia_credor_respect)
    zia_bud.set_debtor_respect(zia_debtor_respect)
    zia_last_gift_id = 73
    zia_bud.set_last_gift_id(zia_last_gift_id)

    shave_text = "shave"
    shave_road = zia_bud.make_l1_road(shave_text)
    shave_idea_y1 = zia_bud.get_idea_obj(shave_road)
    shave_idea_y1._originunit.set_originhold(acct_id="Sue", importance=4.3)
    shave_idea_y1.problem_bool = True
    # print(f"{shave_road=}")
    # print(f"{json_shave_idea._label=} {json_shave_idea._parent_road=}")

    sue_text = "Sue"
    zia_bud.add_acctunit(acct_id=sue_text, credit_belief=199, debtit_belief=199)
    xio_text = "Xio"
    zia_bud.add_acctunit(acct_id=xio_text)
    run_text = ";runners"
    sue_acctunit = zia_bud.get_acct(sue_text)
    xio_acctunit = zia_bud.get_acct(xio_text)
    sue_acctunit.add_membership(run_text)
    xio_acctunit.add_membership(run_text)
    run_teamunit = teamunit_shop()
    run_teamunit.set_teamlink(group_id=run_text)
    zia_bud.edit_idea_attr(zia_bud._real_id, teamunit=run_teamunit)
    xio_teamunit = teamunit_shop()
    xio_teamunit.set_teamlink(group_id=xio_text)
    zia_bud.edit_idea_attr(shave_road, teamunit=xio_teamunit)
    zia_bud.edit_idea_attr(shave_road, awardlink=awardlink_shop(xio_text))
    zia_bud.edit_idea_attr(shave_road, awardlink=awardlink_shop(sue_text))
    zia_bud.edit_idea_attr(zia_bud._real_id, awardlink=awardlink_shop(sue_text))
    # add healerlink to shave ideaunit
    run_healerlink = healerlink_shop({run_text})
    zia_bud.edit_idea_attr(shave_road, healerlink=run_healerlink)
    shave_idea = zia_bud.get_idea_obj(shave_road)
    zia_gogo_want = 75
    zia_stop_want = 77
    shave_idea.gogo_want = zia_gogo_want
    shave_idea.stop_want = zia_stop_want

    yao_text = "Yao"
    zia_bud._originunit.set_originhold(yao_text, 1)
    override_text = "override"

    # WHEN
    x_json = zia_bud.get_json()
    assert x_is_json(x_json) is True
    json_bud = budunit_get_from_json(x_bud_json=x_json)

    # THEN
    assert str(type(json_bud)).find(".bud.BudUnit'>") > 0
    assert json_bud._owner_id is not None
    assert json_bud._owner_id == zia_bud._owner_id
    assert json_bud._real_id == zia_bud._real_id
    assert json_bud._fund_pool == zia_fund_pool
    assert json_bud._fund_pool == zia_bud._fund_pool
    assert json_bud._fund_coin == zia_fund_coin
    assert json_bud._fund_coin == zia_bud._fund_coin
    assert json_bud._bit == zia_bit
    assert json_bud._bit == zia_bud._bit
    assert json_bud._penny == zia_penny
    assert json_bud._penny == zia_bud._penny
    assert json_bud._max_tree_traverse == 23
    assert json_bud._max_tree_traverse == zia_bud._max_tree_traverse
    assert json_bud._road_delimiter == zia_bud._road_delimiter
    assert json_bud._credor_respect == zia_bud._credor_respect
    assert json_bud._debtor_respect == zia_bud._debtor_respect
    assert json_bud._credor_respect == zia_credor_respect
    assert json_bud._debtor_respect == zia_debtor_respect
    assert json_bud._last_gift_id == zia_bud._last_gift_id
    assert json_bud._last_gift_id == zia_last_gift_id
    # assert json_bud._groups == zia_bud._groups

    json_idearoot = json_bud._idearoot
    assert json_idearoot._parent_road == ""
    assert json_idearoot._parent_road == zia_bud._idearoot._parent_road
    assert json_idearoot._reasonunits == {}
    assert json_idearoot._teamunit == zia_bud._idearoot._teamunit
    assert json_idearoot._teamunit == run_teamunit
    assert json_idearoot._fund_coin == 8
    assert json_idearoot._fund_coin == zia_fund_coin
    assert len(json_idearoot._factunits) == 1
    assert len(json_idearoot._awardlinks) == 1

    assert len(json_bud._idearoot._kids) == 2

    weekday_text = "weekdays"
    weekday_road = json_bud.make_l1_road(weekday_text)
    weekday_idea_x = json_bud.get_idea_obj(weekday_road)
    assert len(weekday_idea_x._kids) == 2

    sunday_text = "Sunday"
    sunday_road = json_bud.make_road(weekday_road, sunday_text)
    sunday_idea = json_bud.get_idea_obj(sunday_road)
    assert sunday_idea.mass == 20

    json_shave_idea = json_bud.get_idea_obj(shave_road)
    zia_shave_idea = zia_bud.get_idea_obj(shave_road)
    assert len(json_shave_idea._reasonunits) == 1
    assert json_shave_idea._teamunit == zia_shave_idea._teamunit
    assert json_shave_idea._teamunit == xio_teamunit
    assert json_shave_idea._originunit == zia_shave_idea._originunit
    print(f"{json_shave_idea.healerlink=}")
    assert json_shave_idea.healerlink == zia_shave_idea.healerlink
    assert len(json_shave_idea._awardlinks) == 2
    assert len(json_shave_idea._factunits) == 1
    assert zia_shave_idea.problem_bool
    assert json_shave_idea.problem_bool == zia_shave_idea.problem_bool
    assert json_shave_idea.gogo_want == zia_shave_idea.gogo_want
    assert json_shave_idea.stop_want == zia_shave_idea.stop_want

    assert len(json_bud._originunit._originholds) == 1
    assert json_bud._originunit == zia_bud._originunit


def test_budunit_get_from_json_ReturnsCorrectIdeaRoot():
    # ESTABLISH
    zia_bud = get_budunit_x1_3levels_1reason_1facts()
    zia_bud.set_max_tree_traverse(23)
    # root_idea = zia_bud.get_idea_obj(zia_bud.get_idea_obj(zia_bud._real_id))
    root_idea = zia_bud._idearoot
    zia_gogo_want = 75
    zia_stop_want = 77
    root_idea.gogo_want = zia_gogo_want
    root_idea.stop_want = zia_stop_want

    # WHEN
    x_json = zia_bud.get_json()
    assert x_is_json(x_json) is True
    json_bud = budunit_get_from_json(x_bud_json=x_json)

    # THEN
    json_idearoot = json_bud.get_idea_obj(zia_bud._real_id)
    assert json_idearoot.gogo_want == zia_gogo_want
    assert json_idearoot.stop_want == zia_stop_want


def test_budunit_get_from_json_ReturnsCorrectObj_road_delimiter_Example():
    # ESTABLISH
    slash_delimiter = "/"
    before_bob_bud = budunit_shop("Bob", _road_delimiter=slash_delimiter)
    assert before_bob_bud._road_delimiter != default_road_delimiter_if_none()

    # WHEN
    bob_json = before_bob_bud.get_json()
    after_bob_bud = budunit_get_from_json(bob_json)

    # THEN
    assert after_bob_bud._road_delimiter != default_road_delimiter_if_none()
    assert after_bob_bud._road_delimiter == slash_delimiter
    assert after_bob_bud._road_delimiter == before_bob_bud._road_delimiter


def test_budunit_get_from_json_ReturnsCorrectObj_road_delimiter_AcctExample():
    # ESTABLISH
    slash_delimiter = "/"
    before_bob_bud = budunit_shop("Bob", _road_delimiter=slash_delimiter)
    bob_text = ",Bob"
    before_bob_bud.add_acctunit(bob_text)
    assert before_bob_bud.acct_exists(bob_text)

    # WHEN
    bob_json = before_bob_bud.get_json()
    after_bob_bud = budunit_get_from_json(bob_json)

    # THEN
    after_bob_acctunit = after_bob_bud.get_acct(bob_text)
    assert after_bob_acctunit._road_delimiter == slash_delimiter


def test_budunit_get_from_json_ReturnsCorrectObj_road_delimiter_GroupExample():
    # ESTABLISH
    slash_delimiter = "/"
    before_bob_bud = budunit_shop("Bob", _road_delimiter=slash_delimiter)
    yao_text = "Yao"
    swim_text = f"{slash_delimiter}Swimmers"
    before_bob_bud.add_acctunit(yao_text)
    yao_acctunit = before_bob_bud.get_acct(yao_text)
    yao_acctunit.add_membership(swim_text)

    # WHEN
    bob_json = before_bob_bud.get_json()
    after_bob_bud = budunit_get_from_json(bob_json)

    # THEN
    after_yao_acctunit = after_bob_bud.get_acct(yao_text)
    assert after_yao_acctunit._road_delimiter == slash_delimiter


def test_budunit_get_from_json_ExportsBudUnit_mass():
    # ESTABLISH
    x1_bud = budunit_v001()
    x1_bud._tally = 15
    assert x1_bud._tally == 15
    assert x1_bud._idearoot.mass != x1_bud._tally
    assert x1_bud._idearoot.mass == 1

    # WHEN
    x2_bud = budunit_get_from_json(x1_bud.get_json())

    # THEN
    assert x1_bud._tally == 15
    assert x1_bud._tally == x2_bud._tally
    assert x1_bud._idearoot.mass == 1
    assert x1_bud._idearoot.mass == x2_bud._idearoot.mass
    assert x1_bud._idearoot._kids == x2_bud._idearoot._kids


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
    assert ccn2_bud._idearoot._label == x2_bud._idearoot._label
    assert ccn2_bud._idearoot._parent_road == x2_bud._idearoot._parent_road
    assert ccn2_bud._idearoot._fund_coin == x2_bud._idearoot._fund_coin
    shave_road = ccn2_bud.make_l1_road("shave")
    week_road = ccn2_bud.make_l1_road("weekdays")
    # assert ccn2_bud.get_idea_obj(shave_road) == x2_bud.get_idea_obj(shave_road)
    # assert ccn2_bud.get_idea_obj(week_road) == x2_bud.get_idea_obj(week_road)
    # assert ccn2_bud._idearoot == x2_bud._idearoot
    assert ccn2_bud.get_dict() == x2_bud.get_dict()

    ccn_bud3 = ccn_dict_of_obj.get(x3_bud._owner_id)
    assert ccn_bud3.get_dict() == x3_bud.get_dict()

    cc1_idea_root = ccn_dict_of_obj.get(x1_bud._owner_id)._idearoot
    assert cc1_idea_root._originunit == x1_bud._idearoot._originunit
    ccn_bud1 = ccn_dict_of_obj.get(x1_bud._owner_id)
    assert ccn_bud1._idea_dict == x1_bud._idea_dict
    philipa_text = "Philipa"
    ccn_philipa_acctunit = ccn_bud1.get_acct(philipa_text)
    x1_philipa_acctunit = x1_bud.get_acct(philipa_text)
    assert ccn_philipa_acctunit._memberships == x1_philipa_acctunit._memberships
    assert ccn_bud1 == x1_bud
    assert ccn_dict_of_obj.get(x1_bud._owner_id) == x1_bud
