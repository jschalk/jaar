from src.a01_way_logic.way import (
    create_way,
    get_default_fisc_word as root_word,
    to_way,
)
from src.a04_reason_logic.reason_idea import reasonunit_shop, factunit_shop
from src.a05_idea_logic.idea import ideaunit_shop
from src.a06_bud_logic.bud import budunit_shop
from src.a06_bud_logic._utils.example_buds import get_budunit_with_4_levels
from pytest import raises as pytest_raises


def test_BudUnit_set_fisc_word_CorrectlySetsAttr():
    # ESTABLISH
    x_fisc_word = "accord45"
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str)
    assert sue_bud.fisc_word == root_word()

    # WHEN
    sue_bud.set_fisc_word(fisc_word=x_fisc_word)

    # THEN
    assert sue_bud.fisc_word == x_fisc_word


def test_BudUnit_set_idea_CorrectlySetsfisc_word_AND_fund_coin():
    # ESTABLISH'
    x_fund_coin = 500
    sue_bud = get_budunit_with_4_levels()
    sue_bud.fund_coin = x_fund_coin
    bud_fisc_word = "Texas"
    sue_bud.set_fisc_word(bud_fisc_word)
    assert sue_bud.fisc_word == bud_fisc_word

    casa_way = sue_bud.make_l1_way("casa")
    clean_way = sue_bud.make_way(casa_way, "cleaning")
    cookery_str = "cookery to use"
    cookery_way = sue_bud.make_way(clean_way, cookery_str)

    # WHEN
    sue_bud.set_idea(ideaunit_shop(cookery_str), clean_way)

    # THEN
    cookery_idea = sue_bud.get_idea_obj(cookery_way)
    assert cookery_idea.fisc_word == bud_fisc_word
    assert cookery_idea.fund_coin == x_fund_coin


def test_bud_set_fisc_word_CorrectlySetsAttr():
    # ESTABLISH
    yao_str = "Yao"
    yao_bud = budunit_shop(owner_name=yao_str)
    casa_str = "casa"
    old_casa_way = yao_bud.make_l1_way(casa_str)
    swim_str = "swim"
    old_swim_way = yao_bud.make_way(old_casa_way, swim_str)
    yao_bud.set_l1_idea(ideaunit_shop(casa_str))
    yao_bud.set_idea(ideaunit_shop(swim_str), parent_way=old_casa_way)
    assert yao_bud.owner_name == yao_str
    assert yao_bud.idearoot.idea_word == yao_bud.fisc_word
    casa_idea = yao_bud.get_idea_obj(old_casa_way)
    assert casa_idea.parent_way == to_way(yao_bud.fisc_word)
    swim_idea = yao_bud.get_idea_obj(old_swim_way)
    assert swim_idea.parent_way == old_casa_way
    assert yao_bud.fisc_word == yao_bud.fisc_word

    # WHEN
    x_fisc_word = "accord45"
    yao_bud.set_fisc_word(fisc_word=x_fisc_word)

    # THEN
    new_casa_way = yao_bud.make_l1_way(casa_str)
    swim_str = "swim"
    new_swim_way = yao_bud.make_way(new_casa_way, swim_str)
    assert yao_bud.fisc_word == x_fisc_word
    assert yao_bud.idearoot.idea_word == x_fisc_word
    casa_idea = yao_bud.get_idea_obj(new_casa_way)
    assert casa_idea.parent_way == to_way(x_fisc_word)
    swim_idea = yao_bud.get_idea_obj(new_swim_way)
    assert swim_idea.parent_way == new_casa_way


def test_bud_set_bridge_RaisesErrorIfNew_bridge_IsAnIdea_word():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    print(f"{zia_bud.max_tree_traverse=}")
    casa_str = "casa"
    casa_way = zia_bud.make_l1_way(casa_str)
    zia_bud.set_l1_idea(ideaunit_shop(casa_str))
    slash_str = "/"
    casa_str = f"casa cook{slash_str}clean"
    zia_bud.set_idea(ideaunit_shop(casa_str), parent_way=casa_way)

    # WHEN / THEN
    casa_way = zia_bud.make_way(casa_way, casa_str)
    print(f"{casa_way=}")
    with pytest_raises(Exception) as excinfo:
        zia_bud.set_bridge(slash_str)
    assert (
        str(excinfo.value)
        == f"Cannot modify bridge to '{slash_str}' because it exists an idea idea_word '{casa_way}'"
    )


def test_bud_set_bridge_CorrectlyModifies_parent_way():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    casa_str = "casa"
    zia_bud.set_l1_idea(ideaunit_shop(casa_str))
    semicolon_casa_way = zia_bud.make_l1_way(casa_str)
    cook_str = "cook"
    zia_bud.set_idea(ideaunit_shop(cook_str), semicolon_casa_way)
    semicolon_cook_way = zia_bud.make_way(semicolon_casa_way, cook_str)
    cook_idea = zia_bud.get_idea_obj(semicolon_cook_way)
    semicolon_str = ";"
    assert zia_bud.bridge == semicolon_str
    semicolon_cook_way = zia_bud.make_way(semicolon_casa_way, cook_str)
    # print(f"{zia_bud.fisc_word=} {zia_bud.idearoot.idea_word=} {casa_way=}")
    # print(f"{cook_idea.parent_way=} {cook_idea.idea_word=}")
    # semicolon_casa_idea = zia_bud.get_idea_obj(semicolon_casa_way)
    # print(f"{semicolon_casa_idea.parent_way=} {semicolon_casa_idea.idea_word=}")
    assert cook_idea.get_idea_way() == semicolon_cook_way

    # WHEN
    slash_str = "/"
    zia_bud.set_bridge(slash_str)

    # THEN
    assert cook_idea.get_idea_way() != semicolon_cook_way
    zia_fisc_word = zia_bud.fisc_word
    slash_casa_way = create_way(zia_fisc_word, casa_str, bridge=slash_str)
    slash_cook_way = create_way(slash_casa_way, cook_str, bridge=slash_str)
    assert cook_idea.get_idea_way() == slash_cook_way


def test_bud_set_bridge_CorrectlyModifiesReasonUnit():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    casa_str = "casa"
    zia_bud.set_l1_idea(ideaunit_shop(casa_str))
    time_str = "time"
    semicolon_time_way = zia_bud.make_l1_way(time_str)
    _8am_str = "8am"
    semicolon_8am_way = zia_bud.make_way(semicolon_time_way, _8am_str)

    semicolon_time_reasonunit = reasonunit_shop(rcontext=semicolon_time_way)
    semicolon_time_reasonunit.set_premise(semicolon_8am_way)

    semicolon_casa_way = zia_bud.make_l1_way(casa_str)
    zia_bud.edit_idea_attr(semicolon_casa_way, reason=semicolon_time_reasonunit)
    casa_idea = zia_bud.get_idea_obj(semicolon_casa_way)
    assert casa_idea.reasonunits.get(semicolon_time_way) is not None
    gen_time_reasonunit = casa_idea.reasonunits.get(semicolon_time_way)
    assert gen_time_reasonunit.premises.get(semicolon_8am_way) is not None

    # WHEN
    slash_str = "/"
    zia_bud.set_bridge(slash_str)

    # THEN
    slash_time_way = zia_bud.make_l1_way(time_str)
    slash_8am_way = zia_bud.make_way(slash_time_way, _8am_str)
    slash_casa_way = zia_bud.make_l1_way(casa_str)
    casa_idea = zia_bud.get_idea_obj(slash_casa_way)
    slash_time_way = zia_bud.make_l1_way(time_str)
    slash_8am_way = zia_bud.make_way(slash_time_way, _8am_str)
    assert casa_idea.reasonunits.get(slash_time_way) is not None
    gen_time_reasonunit = casa_idea.reasonunits.get(slash_time_way)
    assert gen_time_reasonunit.premises.get(slash_8am_way) is not None

    assert casa_idea.reasonunits.get(semicolon_time_way) is None
    assert gen_time_reasonunit.premises.get(semicolon_8am_way) is None


def test_bud_set_bridge_CorrectlyModifiesFactUnit():
    # ESTABLISH
    zia_bud = budunit_shop("Zia", "Texas")
    casa_str = "casa"
    zia_bud.set_l1_idea(ideaunit_shop(casa_str))
    time_str = "time"
    semicolon_time_way = zia_bud.make_l1_way(time_str)
    _8am_str = "8am"
    semicolon_8am_way = zia_bud.make_way(semicolon_time_way, _8am_str)
    semicolon_time_factunit = factunit_shop(semicolon_time_way, semicolon_8am_way)

    semicolon_casa_way = zia_bud.make_l1_way(casa_str)
    zia_bud.edit_idea_attr(semicolon_casa_way, factunit=semicolon_time_factunit)
    casa_idea = zia_bud.get_idea_obj(semicolon_casa_way)
    print(f"{casa_idea.factunits=} {semicolon_time_way=}")
    assert casa_idea.factunits.get(semicolon_time_way) is not None
    gen_time_factunit = casa_idea.factunits.get(semicolon_time_way)

    # WHEN
    slash_str = "/"
    zia_bud.set_bridge(slash_str)

    # THEN
    slash_time_way = zia_bud.make_l1_way(time_str)
    slash_casa_way = zia_bud.make_l1_way(casa_str)
    casa_idea = zia_bud.get_idea_obj(slash_casa_way)
    slash_time_way = zia_bud.make_l1_way(time_str)
    slash_8am_way = zia_bud.make_way(slash_time_way, _8am_str)
    assert casa_idea.factunits.get(slash_time_way) is not None
    gen_time_factunit = casa_idea.factunits.get(slash_time_way)
    assert gen_time_factunit.fcontext is not None
    assert gen_time_factunit.fcontext == slash_time_way
    assert gen_time_factunit.fbranch is not None
    assert gen_time_factunit.fbranch == slash_8am_way

    assert casa_idea.factunits.get(semicolon_time_way) is None


def test_BudUnit_set_bridge_CorrectlySetsAttr():
    # ESTABLISH
    x_fisc_word = "accord45"
    slash_bridge = "/"
    sue_str = "Sue"
    sue_bud = budunit_shop(sue_str, x_fisc_word, bridge=slash_bridge)
    assert sue_bud.bridge == slash_bridge

    # WHEN
    at_word_bridge = "@"
    sue_bud.set_bridge(new_bridge=at_word_bridge)

    # THEN
    assert sue_bud.bridge == at_word_bridge
