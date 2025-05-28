from src.a01_way_logic.way import create_way, to_way
from src.a06_bud_logic._utils.str_a06 import (
    bud_acctunit_str,
    bud_acct_membership_str,
    bud_conceptunit_str,
    bud_concept_healerlink_str,
)
from src.a06_bud_logic._utils.str_a06 import acct_name_str
from src.a08_bud_atom_logic._utils.str_a08 import atom_insert, atom_delete
from src.a08_bud_atom_logic.atom import AtomRow, atomrow_shop, budatom_shop
from src.a08_bud_atom_logic.atom_config import get_atom_args_class_types


def test_AtomRow_exists():
    # ESTABLISH /  WHEN
    x_atomrow = AtomRow()

    # THEN
    assert x_atomrow._atom_dimens is None
    assert x_atomrow._crud_command is None
    assert x_atomrow.acct_name is None
    assert x_atomrow.addin is None
    assert x_atomrow.rcontext is None
    assert x_atomrow.rcontext_concept_active_requisite is None
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
    assert x_atomrow.pdivisor is None
    assert x_atomrow.fcontext is None
    assert x_atomrow.fnigh is None
    assert x_atomrow.fopen is None
    assert x_atomrow.fund_coin is None
    assert x_atomrow.fund_pool is None
    assert x_atomrow.give_force is None
    assert x_atomrow.gogo_want is None
    assert x_atomrow.group_title is None
    assert x_atomrow.healer_name is None
    assert x_atomrow.mass is None
    assert x_atomrow.max_tree_traverse is None
    assert x_atomrow.morph is None
    assert x_atomrow.pstate is None
    assert x_atomrow.pnigh is None
    assert x_atomrow.numor is None
    assert x_atomrow.popen is None
    assert x_atomrow.penny is None
    assert x_atomrow.fstate is None
    assert x_atomrow.pledge is None
    assert x_atomrow.problem_bool is None
    assert x_atomrow.concept_way is None
    assert x_atomrow.stop_want is None
    assert x_atomrow.take_force is None
    assert x_atomrow.tally is None

    print(f"{set(x_atomrow.__dict__.keys())=}")
    print(f"{set(get_atom_args_class_types().keys())=}")
    atomrow_args_set = set(x_atomrow.__dict__.keys())
    atomrow_args_set.remove("_atom_dimens")
    atomrow_args_set.remove("_crud_command")
    config_args_set = set(get_atom_args_class_types().keys())
    assert atomrow_args_set == config_args_set


def test_atomrow_shop_ReturnObj():
    # ESTABLISH
    x_atom_dimens = {bud_acctunit_str()}

    # WHEN
    x_atomrow = atomrow_shop(x_atom_dimens, atom_insert())

    # THEN
    assert x_atomrow._atom_dimens == x_atom_dimens
    assert x_atomrow._crud_command == atom_insert()


def test_AtomRow_set_atom_dimen_SetsAttr():
    # ESTABLISH
    x_atomrow = atomrow_shop({bud_acctunit_str()}, atom_insert())
    assert bud_acct_membership_str() not in x_atomrow._atom_dimens

    # WHEN
    x_atomrow.set_atom_dimen(bud_acct_membership_str())

    # THEN
    assert bud_acct_membership_str() in x_atomrow._atom_dimens


def test_AtomRow_atom_dimen_exists_ReturnsObj():
    # ESTABLISH
    x_atomrow = atomrow_shop(set(), atom_insert())
    assert not x_atomrow.atom_dimen_exists(bud_acctunit_str())
    assert not x_atomrow.atom_dimen_exists(bud_acct_membership_str())

    # WHEN
    x_atomrow.set_atom_dimen(bud_acct_membership_str())

    # THEN
    assert not x_atomrow.atom_dimen_exists(bud_acctunit_str())
    assert x_atomrow.atom_dimen_exists(bud_acct_membership_str())


def test_AtomRow_delete_atom_dimen_SetsAttr():
    # ESTABLISH
    x_atomrow = atomrow_shop({bud_acctunit_str()}, atom_insert())
    x_atomrow.set_atom_dimen(bud_acctunit_str())
    x_atomrow.set_atom_dimen(bud_acct_membership_str())
    assert x_atomrow.atom_dimen_exists(bud_acctunit_str())
    assert x_atomrow.atom_dimen_exists(bud_acct_membership_str())

    # WHEN
    x_atomrow.delete_atom_dimen(bud_acct_membership_str())

    # THEN
    assert x_atomrow.atom_dimen_exists(bud_acctunit_str())
    assert not x_atomrow.atom_dimen_exists(bud_acct_membership_str())


def test_AtomRow_set_class_types_SetsAttr():
    # ESTABLISH
    x_atomrow = atomrow_shop({}, atom_insert())
    x_atomrow.close = "4"
    x_parent_way = "fizz_buzz"
    x_concept_label = "buzzziy"
    x_morph_str = "True"
    x_morph_bool = True
    x_way = create_way(x_parent_way, x_concept_label)
    x_atomrow.concept_way = x_way
    x_atomrow.morph = x_morph_str
    four_int = 4
    assert x_atomrow.close != four_int
    assert x_atomrow.concept_way == x_way
    assert x_atomrow.morph == x_morph_str

    # WHEN
    x_atomrow._set_class_types()

    # THEN
    assert x_atomrow.close == four_int
    assert x_atomrow.concept_way == x_way
    assert x_atomrow.morph == x_morph_bool


def test_AtomRow_get_budatoms_ReturnsObj_bud_acctunit_str_INSERT_Scenario0():
    # ESTABLISH
    x_dimen = bud_acctunit_str()
    x_atomrow = atomrow_shop({x_dimen}, atom_insert())
    x_atomrow.acct_name = "Bob"

    # WHEN
    x_budatoms = x_atomrow.get_budatoms()

    # THEN
    assert len(x_budatoms) == 1
    static_atom = budatom_shop(x_dimen, atom_insert())
    static_atom.set_arg(acct_name_str(), "Bob")
    assert x_budatoms[0] == static_atom


def test_AtomRow_get_budatoms_ReturnsObj_bud_acctunit_str_INSERT_Scenario1():
    # ESTABLISH
    x_dimen = bud_acctunit_str()
    x_atomrow = atomrow_shop({x_dimen}, atom_insert())
    x_atomrow.acct_name = "Bob"
    x_atomrow.credit_belief = 5

    # WHEN
    x_budatoms = x_atomrow.get_budatoms()

    # THEN
    assert len(x_budatoms) == 1
    static_atom = budatom_shop(x_dimen, atom_insert())
    static_atom.set_arg(acct_name_str(), "Bob")
    static_atom.set_arg("credit_belief", 5)
    assert x_budatoms[0] == static_atom


def test_AtomRow_get_budatoms_ReturnsObj_bud_acctunit_NSERT_Fails():
    # ESTABLISH
    x_dimen = bud_acctunit_str()
    x_atomrow = atomrow_shop({x_dimen}, atom_insert())

    # WHEN
    x_budatoms = x_atomrow.get_budatoms()

    # THEN
    assert len(x_budatoms) == 0


def test_AtomRow_get_budatoms_ReturnsObj_bud_acctunit_INSERT_Scenario2():
    # ESTABLISH
    x_dimen = bud_acctunit_str()
    x_atomrow = atomrow_shop({x_dimen}, atom_insert())
    x_atomrow.acct_name = "Bob"
    four_str = "4"
    x_atomrow.credit_belief = four_str

    # WHEN
    x_budatoms = x_atomrow.get_budatoms()

    # THEN
    assert len(x_budatoms) == 1
    static_atom = budatom_shop(x_dimen, atom_insert())
    static_atom.set_arg(acct_name_str(), "Bob")
    four_int = 4
    static_atom.set_arg("credit_belief", four_int)
    assert x_budatoms[0] == static_atom


def test_AtomRow_get_budatoms_ReturnsObjIfDimenIsCorrect():
    # ESTABLISH
    x_atomrow = atomrow_shop(set(), atom_insert())
    x_atomrow.acct_name = "Bob"
    four_str = "4"
    x_atomrow.credit_belief = four_str
    assert len(x_atomrow.get_budatoms()) == 0

    # WHEN / THEN
    x_atomrow.set_atom_dimen(bud_acct_membership_str())
    assert len(x_atomrow.get_budatoms()) == 0

    # THEN
    x_atomrow.set_atom_dimen(bud_acctunit_str())
    assert len(x_atomrow.get_budatoms()) == 1


def test_AtomRow_get_budatoms_ReturnsObj_bud_conceptunit_INSERT_pledge_False_Scenario0():
    # ESTABLISH
    x_atomrow = atomrow_shop({bud_conceptunit_str()}, atom_insert())
    x_atomrow.concept_way = create_way("accord78", "casa")
    x_atomrow.pledge = False
    assert len(x_atomrow.get_budatoms()) == 1

    # WHEN / THEN
    x_budatom = x_atomrow.get_budatoms()[0]

    # THEN
    static_budatom = budatom_shop(bud_conceptunit_str(), atom_insert())
    static_budatom.set_arg("concept_way", create_way("accord78", "casa"))
    static_budatom.set_arg("pledge", False)
    print(static_budatom)
    print(x_budatom)
    assert x_budatom == static_budatom


def test_AtomRow_get_budatoms_ReturnsObj_bud_conceptunit_INSERT_pledge_False_Scenario1():
    # ESTABLISH
    x_dimens = {bud_conceptunit_str(), bud_concept_healerlink_str()}
    x_atomrow = atomrow_shop(x_dimens, atom_insert())
    x_atomrow.concept_way = create_way("accord78", "casa")
    x_atomrow.pledge = False
    x_atomrow.healer_name = "Bob"

    # WHEN / THEN
    x_budatoms = x_atomrow.get_budatoms()

    # THEN
    assert len(x_budatoms) == 2
    y_concept_budatom = budatom_shop(bud_conceptunit_str(), atom_insert())
    casa_way = create_way("accord78", "casa")
    y_concept_budatom.set_arg("concept_way", casa_way)
    y_concept_budatom.set_arg("pledge", False)
    assert y_concept_budatom in x_budatoms
    healerlink_budatom = budatom_shop(bud_concept_healerlink_str(), atom_insert())
    healerlink_budatom.set_arg("concept_way", casa_way)
    healerlink_budatom.set_arg("healer_name", "Bob")
    assert healerlink_budatom in x_budatoms
