from src.f1_road.road import create_road
from src.f2_bud.bud_tool import (
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_ideaunit_str,
    bud_idea_healerlink_str,
)
from src.f4_gift.atom_config import atom_insert, atom_delete, acct_id_str
from src.f4_gift.atom import AtomRow, atomrow_shop, atomunit_shop


def test_AtomRow_exists():
    # ESTABLISH /  WHEN
    x_atomrow = AtomRow()

    # THEN
    assert x_atomrow._atom_categorys is None
    assert x_atomrow._crud_command is None
    assert x_atomrow.acct_id is None
    assert x_atomrow.addin is None
    assert x_atomrow.base is None
    assert x_atomrow.base_idea_active_requisite is None
    assert x_atomrow.begin is None
    assert x_atomrow.respect_bit is None
    assert x_atomrow.close is None
    assert x_atomrow.credit_belief is None
    assert x_atomrow.credit_vote is None
    assert x_atomrow.credor_respect is None
    assert x_atomrow.debtit_belief is None
    assert x_atomrow.debtit_vote is None
    assert x_atomrow.debtor_respect is None
    assert x_atomrow.denom is None
    assert x_atomrow.divisor is None
    assert x_atomrow.fnigh is None
    assert x_atomrow.fopen is None
    assert x_atomrow.fund_coin is None
    assert x_atomrow.fund_pool is None
    assert x_atomrow.give_force is None
    assert x_atomrow.gogo_want is None
    assert x_atomrow.group_id is None
    assert x_atomrow.healer_id is None
    assert x_atomrow.label is None
    assert x_atomrow.mass is None
    assert x_atomrow.max_tree_traverse is None
    assert x_atomrow.tender_desc is None
    assert x_atomrow.morph is None
    assert x_atomrow.need is None
    assert x_atomrow.nigh is None
    assert x_atomrow.numor is None
    assert x_atomrow.open is None
    assert x_atomrow.parent_road is None
    assert x_atomrow.penny is None
    assert x_atomrow.pick is None
    assert x_atomrow.pledge is None
    assert x_atomrow.problem_bool is None
    assert x_atomrow.road is None
    assert x_atomrow.stop_want is None
    assert x_atomrow.take_force is None
    assert x_atomrow.tally is None


def test_atomrow_shop_ReturnObj():
    # ESTABLISH
    x_atom_categorys = {bud_acctunit_str()}

    # WHEN
    x_atomrow = atomrow_shop(x_atom_categorys, atom_insert())

    # THEN
    assert x_atomrow._atom_categorys == x_atom_categorys
    assert x_atomrow._crud_command == atom_insert()


def test_AtomRow_set_atom_category_SetsAttr():
    # ESTABLISH
    x_atomrow = atomrow_shop({bud_acctunit_str()}, atom_insert())
    assert bud_acct_membership_str() not in x_atomrow._atom_categorys

    # WHEN
    x_atomrow.set_atom_category(bud_acct_membership_str())

    # THEN
    assert bud_acct_membership_str() in x_atomrow._atom_categorys


def test_AtomRow_atom_category_exists_ReturnsObj():
    # ESTABLISH
    x_atomrow = atomrow_shop(set(), atom_insert())
    assert not x_atomrow.atom_category_exists(bud_acctunit_str())
    assert not x_atomrow.atom_category_exists(bud_acct_membership_str())

    # WHEN
    x_atomrow.set_atom_category(bud_acct_membership_str())

    # THEN
    assert not x_atomrow.atom_category_exists(bud_acctunit_str())
    assert x_atomrow.atom_category_exists(bud_acct_membership_str())


def test_AtomRow_delete_atom_category_SetsAttr():
    # ESTABLISH
    x_atomrow = atomrow_shop({bud_acctunit_str()}, atom_insert())
    x_atomrow.set_atom_category(bud_acctunit_str())
    x_atomrow.set_atom_category(bud_acct_membership_str())
    assert x_atomrow.atom_category_exists(bud_acctunit_str())
    assert x_atomrow.atom_category_exists(bud_acct_membership_str())

    # WHEN
    x_atomrow.delete_atom_category(bud_acct_membership_str())

    # THEN
    assert x_atomrow.atom_category_exists(bud_acctunit_str())
    assert not x_atomrow.atom_category_exists(bud_acct_membership_str())


def test_AtomRow_set_python_types_SetsAttr():
    # ESTABLISH
    x_atomrow = atomrow_shop({}, atom_insert())
    x_atomrow.close = "4"
    x_parent_road = "fizz_buzz"
    x_label = "buzzziy"
    x_tender_desc = "boullons"
    x_morph_str = "True"
    x_morph_bool = True
    x_atomrow.parent_road = x_parent_road
    x_atomrow.label = x_label
    x_atomrow.tender_desc = x_tender_desc
    x_atomrow.morph = x_morph_str
    four_int = 4
    assert x_atomrow.close != four_int
    assert x_atomrow.parent_road == x_parent_road
    assert x_atomrow.label == x_label
    assert x_atomrow.tender_desc == x_tender_desc
    assert x_atomrow.morph == x_morph_str
    assert not x_atomrow.road

    # WHEN
    x_atomrow._set_python_types()

    # THEN
    assert x_atomrow.close == four_int
    assert x_atomrow.parent_road == x_parent_road
    assert x_atomrow.label == x_label
    assert x_atomrow.tender_desc == x_tender_desc
    assert x_atomrow.morph == x_morph_bool
    assert x_atomrow.road == create_road(x_parent_road, x_label)


def test_AtomRow_get_atomunits_ReturnsObj_bud_acctunit_str_INSERT_Scenario0():
    # ESTABLISH
    x_category = bud_acctunit_str()
    x_atomrow = atomrow_shop({x_category}, atom_insert())
    x_atomrow.acct_id = "Bob"

    # WHEN
    x_atomunits = x_atomrow.get_atomunits()

    # THEN
    assert len(x_atomunits) == 1
    static_atom = atomunit_shop(x_category, atom_insert())
    static_atom.set_arg(acct_id_str(), "Bob")
    assert x_atomunits[0] == static_atom


def test_AtomRow_get_atomunits_ReturnsObj_bud_acctunit_str_INSERT_Scenario1():
    # ESTABLISH
    x_category = bud_acctunit_str()
    x_atomrow = atomrow_shop({x_category}, atom_insert())
    x_atomrow.acct_id = "Bob"
    x_atomrow.credit_belief = 5

    # WHEN
    x_atomunits = x_atomrow.get_atomunits()

    # THEN
    assert len(x_atomunits) == 1
    static_atom = atomunit_shop(x_category, atom_insert())
    static_atom.set_arg(acct_id_str(), "Bob")
    static_atom.set_arg("credit_belief", 5)
    assert x_atomunits[0] == static_atom


def test_AtomRow_get_atomunits_ReturnsObj_bud_acctunit_NSERT_Fails():
    # ESTABLISH
    x_category = bud_acctunit_str()
    x_atomrow = atomrow_shop({x_category}, atom_insert())

    # WHEN
    x_atomunits = x_atomrow.get_atomunits()

    # THEN
    assert len(x_atomunits) == 0


def test_AtomRow_get_atomunits_ReturnsObj_bud_acctunit_INSERT_Scenario2():
    # ESTABLISH
    x_category = bud_acctunit_str()
    x_atomrow = atomrow_shop({x_category}, atom_insert())
    x_atomrow.acct_id = "Bob"
    four_str = "4"
    x_atomrow.credit_belief = four_str

    # WHEN
    x_atomunits = x_atomrow.get_atomunits()

    # THEN
    assert len(x_atomunits) == 1
    static_atom = atomunit_shop(x_category, atom_insert())
    static_atom.set_arg(acct_id_str(), "Bob")
    four_int = 4
    static_atom.set_arg("credit_belief", four_int)
    assert x_atomunits[0] == static_atom


def test_AtomRow_get_atomunits_ReturnsObjIfCategoryIsCorrect():
    # ESTABLISH
    x_atomrow = atomrow_shop(set(), atom_insert())
    x_atomrow.acct_id = "Bob"
    four_str = "4"
    x_atomrow.credit_belief = four_str
    assert len(x_atomrow.get_atomunits()) == 0

    # WHEN / THEN
    x_atomrow.set_atom_category(bud_acct_membership_str())
    assert len(x_atomrow.get_atomunits()) == 0

    # THEN
    x_atomrow.set_atom_category(bud_acctunit_str())
    assert len(x_atomrow.get_atomunits()) == 1


def test_AtomRow_get_atomunits_ReturnsObj_bud_ideaunit_INSERT_pledge_False():
    # ESTABLISH
    x_atomrow = atomrow_shop({bud_ideaunit_str()}, atom_insert())
    x_atomrow.parent_road = "music78"
    x_atomrow.label = "casa"
    x_atomrow.pledge = False
    assert len(x_atomrow.get_atomunits()) == 1

    # WHEN / THEN
    x_atomunit = x_atomrow.get_atomunits()[0]

    # THEN
    static_atomunit = atomunit_shop(bud_ideaunit_str(), atom_insert())
    static_atomunit.set_arg("parent_road", "music78")
    static_atomunit.set_arg("label", "casa")
    static_atomunit.set_arg("pledge", False)
    assert x_atomunit == static_atomunit


def test_AtomRow_get_atomunits_ReturnsObj_bud_ideaunit_INSERT_pledge_False():
    # ESTABLISH
    x_categorys = {bud_ideaunit_str(), bud_idea_healerlink_str()}
    x_atomrow = atomrow_shop(x_categorys, atom_insert())
    x_atomrow.parent_road = "music78"
    x_atomrow.label = "casa"
    x_atomrow.pledge = False
    x_atomrow.healer_id = "Bob"

    # WHEN / THEN
    x_atomunits = x_atomrow.get_atomunits()

    # THEN
    assert len(x_atomunits) == 2
    y_idea_atomunit = atomunit_shop(bud_ideaunit_str(), atom_insert())
    y_idea_atomunit.set_arg("parent_road", "music78")
    y_idea_atomunit.set_arg("label", "casa")
    y_idea_atomunit.set_arg("pledge", False)
    assert y_idea_atomunit in x_atomunits
    healerlink_atomunit = atomunit_shop(bud_idea_healerlink_str(), atom_insert())
    healerlink_atomunit.set_arg("road", "music78;casa")
    healerlink_atomunit.set_arg("healer_id", "Bob")
    assert healerlink_atomunit in x_atomunits