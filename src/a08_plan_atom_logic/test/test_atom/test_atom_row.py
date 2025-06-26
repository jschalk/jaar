from src.a01_term_logic.rope import create_rope, to_rope
from src.a06_plan_logic.test._util.a06_str import (
    acct_name_str,
    plan_acct_membership_str,
    plan_acctunit_str,
    plan_concept_healerlink_str,
    plan_conceptunit_str,
)
from src.a08_plan_atom_logic.atom import AtomRow, atomrow_shop, planatom_shop
from src.a08_plan_atom_logic.atom_config import get_atom_args_class_types
from src.a08_plan_atom_logic.test._util.a08_str import DELETE_str, INSERT_str


def test_AtomRow_exists():
    # ESTABLISH /  WHEN
    x_atomrow = AtomRow()

    # THEN
    assert x_atomrow._atom_dimens is None
    assert x_atomrow._crud_command is None
    assert x_atomrow.acct_name is None
    assert x_atomrow.addin is None
    assert x_atomrow.rcontext is None
    assert x_atomrow.rconcept_active_requisite is None
    assert x_atomrow.begin is None
    assert x_atomrow.respect_bit is None
    assert x_atomrow.close is None
    assert x_atomrow.acct_cred_points is None
    assert x_atomrow.group_cred_points is None
    assert x_atomrow.credor_respect is None
    assert x_atomrow.acct_debt_points is None
    assert x_atomrow.group_debt_points is None
    assert x_atomrow.debtor_respect is None
    assert x_atomrow.denom is None
    assert x_atomrow.pdivisor is None
    assert x_atomrow.fcontext is None
    assert x_atomrow.fnigh is None
    assert x_atomrow.fopen is None
    assert x_atomrow.fund_iota is None
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
    assert x_atomrow.task is None
    assert x_atomrow.problem_bool is None
    assert x_atomrow.concept_rope is None
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


def test_atomrow_shop_ReturnsObj():
    # ESTABLISH
    x_atom_dimens = {plan_acctunit_str()}

    # WHEN
    x_atomrow = atomrow_shop(x_atom_dimens, INSERT_str())

    # THEN
    assert x_atomrow._atom_dimens == x_atom_dimens
    assert x_atomrow._crud_command == INSERT_str()


def test_AtomRow_set_atom_dimen_SetsAttr():
    # ESTABLISH
    x_atomrow = atomrow_shop({plan_acctunit_str()}, INSERT_str())
    assert plan_acct_membership_str() not in x_atomrow._atom_dimens

    # WHEN
    x_atomrow.set_atom_dimen(plan_acct_membership_str())

    # THEN
    assert plan_acct_membership_str() in x_atomrow._atom_dimens


def test_AtomRow_atom_dimen_exists_ReturnsObj():
    # ESTABLISH
    x_atomrow = atomrow_shop(set(), INSERT_str())
    assert not x_atomrow.atom_dimen_exists(plan_acctunit_str())
    assert not x_atomrow.atom_dimen_exists(plan_acct_membership_str())

    # WHEN
    x_atomrow.set_atom_dimen(plan_acct_membership_str())

    # THEN
    assert not x_atomrow.atom_dimen_exists(plan_acctunit_str())
    assert x_atomrow.atom_dimen_exists(plan_acct_membership_str())


def test_AtomRow_delete_atom_dimen_SetsAttr():
    # ESTABLISH
    x_atomrow = atomrow_shop({plan_acctunit_str()}, INSERT_str())
    x_atomrow.set_atom_dimen(plan_acctunit_str())
    x_atomrow.set_atom_dimen(plan_acct_membership_str())
    assert x_atomrow.atom_dimen_exists(plan_acctunit_str())
    assert x_atomrow.atom_dimen_exists(plan_acct_membership_str())

    # WHEN
    x_atomrow.delete_atom_dimen(plan_acct_membership_str())

    # THEN
    assert x_atomrow.atom_dimen_exists(plan_acctunit_str())
    assert not x_atomrow.atom_dimen_exists(plan_acct_membership_str())


def test_AtomRow_set_class_types_SetsAttr():
    # ESTABLISH
    x_atomrow = atomrow_shop({}, INSERT_str())
    x_atomrow.close = "4"
    x_parent_rope = "fizz_buzz"
    x_concept_label = "buzzziy"
    x_morph_str = "True"
    x_morph_bool = True
    x_rope = create_rope(x_parent_rope, x_concept_label)
    x_atomrow.concept_rope = x_rope
    x_atomrow.morph = x_morph_str
    four_int = 4
    assert x_atomrow.close != four_int
    assert x_atomrow.concept_rope == x_rope
    assert x_atomrow.morph == x_morph_str

    # WHEN
    x_atomrow._set_class_types()

    # THEN
    assert x_atomrow.close == four_int
    assert x_atomrow.concept_rope == x_rope
    assert x_atomrow.morph == x_morph_bool


def test_AtomRow_get_planatoms_ReturnsObj_plan_acctunit_str_INSERT_Scenario0():
    # ESTABLISH
    x_dimen = plan_acctunit_str()
    x_atomrow = atomrow_shop({x_dimen}, INSERT_str())
    x_atomrow.acct_name = "Bob"

    # WHEN
    x_planatoms = x_atomrow.get_planatoms()

    # THEN
    assert len(x_planatoms) == 1
    static_atom = planatom_shop(x_dimen, INSERT_str())
    static_atom.set_arg(acct_name_str(), "Bob")
    assert x_planatoms[0] == static_atom


def test_AtomRow_get_planatoms_ReturnsObj_plan_acctunit_str_INSERT_Scenario1():
    # ESTABLISH
    x_dimen = plan_acctunit_str()
    x_atomrow = atomrow_shop({x_dimen}, INSERT_str())
    x_atomrow.acct_name = "Bob"
    x_atomrow.acct_cred_points = 5

    # WHEN
    x_planatoms = x_atomrow.get_planatoms()

    # THEN
    assert len(x_planatoms) == 1
    static_atom = planatom_shop(x_dimen, INSERT_str())
    static_atom.set_arg(acct_name_str(), "Bob")
    static_atom.set_arg("acct_cred_points", 5)
    assert x_planatoms[0] == static_atom


def test_AtomRow_get_planatoms_ReturnsObj_plan_acctunit_NSERT_Fails():
    # ESTABLISH
    x_dimen = plan_acctunit_str()
    x_atomrow = atomrow_shop({x_dimen}, INSERT_str())

    # WHEN
    x_planatoms = x_atomrow.get_planatoms()

    # THEN
    assert len(x_planatoms) == 0


def test_AtomRow_get_planatoms_ReturnsObj_plan_acctunit_INSERT_Scenario2():
    # ESTABLISH
    x_dimen = plan_acctunit_str()
    x_atomrow = atomrow_shop({x_dimen}, INSERT_str())
    x_atomrow.acct_name = "Bob"
    four_str = "4"
    x_atomrow.acct_cred_points = four_str

    # WHEN
    x_planatoms = x_atomrow.get_planatoms()

    # THEN
    assert len(x_planatoms) == 1
    static_atom = planatom_shop(x_dimen, INSERT_str())
    static_atom.set_arg(acct_name_str(), "Bob")
    four_int = 4
    static_atom.set_arg("acct_cred_points", four_int)
    assert x_planatoms[0] == static_atom


def test_AtomRow_get_planatoms_ReturnsObjIfDimenIsCorrect():
    # ESTABLISH
    x_atomrow = atomrow_shop(set(), INSERT_str())
    x_atomrow.acct_name = "Bob"
    four_str = "4"
    x_atomrow.acct_cred_points = four_str
    assert len(x_atomrow.get_planatoms()) == 0

    # WHEN / THEN
    x_atomrow.set_atom_dimen(plan_acct_membership_str())
    assert len(x_atomrow.get_planatoms()) == 0

    # THEN
    x_atomrow.set_atom_dimen(plan_acctunit_str())
    assert len(x_atomrow.get_planatoms()) == 1


def test_AtomRow_get_planatoms_ReturnsObj_plan_conceptunit_INSERT_task_False_Scenario0():
    # ESTABLISH
    x_atomrow = atomrow_shop({plan_conceptunit_str()}, INSERT_str())
    x_atomrow.concept_rope = create_rope("amy78", "casa")
    x_atomrow.task = False
    assert len(x_atomrow.get_planatoms()) == 1

    # WHEN / THEN
    x_planatom = x_atomrow.get_planatoms()[0]

    # THEN
    static_planatom = planatom_shop(plan_conceptunit_str(), INSERT_str())
    static_planatom.set_arg("concept_rope", create_rope("amy78", "casa"))
    static_planatom.set_arg("task", False)
    print(static_planatom)
    print(x_planatom)
    assert x_planatom == static_planatom


def test_AtomRow_get_planatoms_ReturnsObj_plan_conceptunit_INSERT_task_False_Scenario1():
    # ESTABLISH
    x_dimens = {plan_conceptunit_str(), plan_concept_healerlink_str()}
    x_atomrow = atomrow_shop(x_dimens, INSERT_str())
    x_atomrow.concept_rope = create_rope("amy78", "casa")
    x_atomrow.task = False
    x_atomrow.healer_name = "Bob"

    # WHEN / THEN
    x_planatoms = x_atomrow.get_planatoms()

    # THEN
    assert len(x_planatoms) == 2
    y_concept_planatom = planatom_shop(plan_conceptunit_str(), INSERT_str())
    casa_rope = create_rope("amy78", "casa")
    y_concept_planatom.set_arg("concept_rope", casa_rope)
    y_concept_planatom.set_arg("task", False)
    assert y_concept_planatom in x_planatoms
    healerlink_planatom = planatom_shop(plan_concept_healerlink_str(), INSERT_str())
    healerlink_planatom.set_arg("concept_rope", casa_rope)
    healerlink_planatom.set_arg("healer_name", "Bob")
    assert healerlink_planatom in x_planatoms
