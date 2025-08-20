from src.a01_term_logic.rope import create_rope, to_rope
from src.a06_belief_logic.test._util.a06_str import (
    belief_partner_membership_str,
    belief_partnerunit_str,
    belief_plan_healerunit_str,
    belief_planunit_str,
    partner_name_str,
)
from src.a08_belief_atom_logic.atom_config import get_atom_args_class_types
from src.a08_belief_atom_logic.atom_main import AtomRow, atomrow_shop, beliefatom_shop
from src.a08_belief_atom_logic.test._util.a08_str import DELETE_str, INSERT_str


def test_AtomRow_Exists():
    # ESTABLISH /  WHEN
    x_atomrow = AtomRow()

    # THEN
    assert x_atomrow._atom_dimens is None
    assert x_atomrow._crud_command is None
    assert x_atomrow.partner_name is None
    assert x_atomrow.addin is None
    assert x_atomrow.reason_context is None
    assert x_atomrow.reason_active_requisite is None
    assert x_atomrow.begin is None
    assert x_atomrow.respect_bit is None
    assert x_atomrow.close is None
    assert x_atomrow.partner_cred_points is None
    assert x_atomrow.group_cred_points is None
    assert x_atomrow.credor_respect is None
    assert x_atomrow.partner_debt_points is None
    assert x_atomrow.group_debt_points is None
    assert x_atomrow.debtor_respect is None
    assert x_atomrow.denom is None
    assert x_atomrow.reason_divisor is None
    assert x_atomrow.fact_context is None
    assert x_atomrow.fact_upper is None
    assert x_atomrow.fact_lower is None
    assert x_atomrow.fund_iota is None
    assert x_atomrow.fund_pool is None
    assert x_atomrow.give_force is None
    assert x_atomrow.gogo_want is None
    assert x_atomrow.group_title is None
    assert x_atomrow.healer_name is None
    assert x_atomrow.solo is None
    assert x_atomrow.star is None
    assert x_atomrow.max_tree_traverse is None
    assert x_atomrow.morph is None
    assert x_atomrow.reason_state is None
    assert x_atomrow.reason_upper is None
    assert x_atomrow.numor is None
    assert x_atomrow.reason_lower is None
    assert x_atomrow.penny is None
    assert x_atomrow.fact_state is None
    assert x_atomrow.task is None
    assert x_atomrow.problem_bool is None
    assert x_atomrow.plan_rope is None
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
    x_atom_dimens = {belief_partnerunit_str()}

    # WHEN
    x_atomrow = atomrow_shop(x_atom_dimens, INSERT_str())

    # THEN
    assert x_atomrow._atom_dimens == x_atom_dimens
    assert x_atomrow._crud_command == INSERT_str()


def test_AtomRow_set_atom_dimen_SetsAttr():
    # ESTABLISH
    x_atomrow = atomrow_shop({belief_partnerunit_str()}, INSERT_str())
    assert belief_partner_membership_str() not in x_atomrow._atom_dimens

    # WHEN
    x_atomrow.set_atom_dimen(belief_partner_membership_str())

    # THEN
    assert belief_partner_membership_str() in x_atomrow._atom_dimens


def test_AtomRow_atom_dimen_exists_ReturnsObj():
    # ESTABLISH
    x_atomrow = atomrow_shop(set(), INSERT_str())
    assert not x_atomrow.atom_dimen_exists(belief_partnerunit_str())
    assert not x_atomrow.atom_dimen_exists(belief_partner_membership_str())

    # WHEN
    x_atomrow.set_atom_dimen(belief_partner_membership_str())

    # THEN
    assert not x_atomrow.atom_dimen_exists(belief_partnerunit_str())
    assert x_atomrow.atom_dimen_exists(belief_partner_membership_str())


def test_AtomRow_delete_atom_dimen_SetsAttr():
    # ESTABLISH
    x_atomrow = atomrow_shop({belief_partnerunit_str()}, INSERT_str())
    x_atomrow.set_atom_dimen(belief_partnerunit_str())
    x_atomrow.set_atom_dimen(belief_partner_membership_str())
    assert x_atomrow.atom_dimen_exists(belief_partnerunit_str())
    assert x_atomrow.atom_dimen_exists(belief_partner_membership_str())

    # WHEN
    x_atomrow.delete_atom_dimen(belief_partner_membership_str())

    # THEN
    assert x_atomrow.atom_dimen_exists(belief_partnerunit_str())
    assert not x_atomrow.atom_dimen_exists(belief_partner_membership_str())


def test_AtomRow_set_class_types_SetsAttr():
    # ESTABLISH
    x_atomrow = atomrow_shop({}, INSERT_str())
    x_atomrow.close = "4"
    x_parent_rope = "Fay_bob"
    x_plan_label = "Bobziy"
    x_morph_str = "True"
    x_morph_bool = True
    x_rope = create_rope(x_parent_rope, x_plan_label)
    x_atomrow.plan_rope = x_rope
    x_atomrow.morph = x_morph_str
    four_int = 4
    assert x_atomrow.close != four_int
    assert x_atomrow.plan_rope == x_rope
    assert x_atomrow.morph == x_morph_str

    # WHEN
    x_atomrow._set_class_types()

    # THEN
    assert x_atomrow.close == four_int
    assert x_atomrow.plan_rope == x_rope
    assert x_atomrow.morph == x_morph_bool


def test_AtomRow_get_beliefatoms_ReturnsObj_belief_partnerunit_str_INSERT_Scenario0():
    # ESTABLISH
    x_dimen = belief_partnerunit_str()
    x_atomrow = atomrow_shop({x_dimen}, INSERT_str())
    x_atomrow.partner_name = "Bob"

    # WHEN
    x_beliefatoms = x_atomrow.get_beliefatoms()

    # THEN
    assert len(x_beliefatoms) == 1
    static_atom = beliefatom_shop(x_dimen, INSERT_str())
    static_atom.set_arg(partner_name_str(), "Bob")
    assert x_beliefatoms[0] == static_atom


def test_AtomRow_get_beliefatoms_ReturnsObj_belief_partnerunit_str_INSERT_Scenario1():
    # ESTABLISH
    x_dimen = belief_partnerunit_str()
    x_atomrow = atomrow_shop({x_dimen}, INSERT_str())
    x_atomrow.partner_name = "Bob"
    x_atomrow.partner_cred_points = 5

    # WHEN
    x_beliefatoms = x_atomrow.get_beliefatoms()

    # THEN
    assert len(x_beliefatoms) == 1
    static_atom = beliefatom_shop(x_dimen, INSERT_str())
    static_atom.set_arg(partner_name_str(), "Bob")
    static_atom.set_arg("partner_cred_points", 5)
    assert x_beliefatoms[0] == static_atom


def test_AtomRow_get_beliefatoms_ReturnsObj_belief_partnerunit_NSERT_Fails():
    # ESTABLISH
    x_dimen = belief_partnerunit_str()
    x_atomrow = atomrow_shop({x_dimen}, INSERT_str())

    # WHEN
    x_beliefatoms = x_atomrow.get_beliefatoms()

    # THEN
    assert len(x_beliefatoms) == 0


def test_AtomRow_get_beliefatoms_ReturnsObj_belief_partnerunit_INSERT_Scenario2():
    # ESTABLISH
    x_dimen = belief_partnerunit_str()
    x_atomrow = atomrow_shop({x_dimen}, INSERT_str())
    x_atomrow.partner_name = "Bob"
    four_str = "4"
    x_atomrow.partner_cred_points = four_str

    # WHEN
    x_beliefatoms = x_atomrow.get_beliefatoms()

    # THEN
    assert len(x_beliefatoms) == 1
    static_atom = beliefatom_shop(x_dimen, INSERT_str())
    static_atom.set_arg(partner_name_str(), "Bob")
    four_int = 4
    static_atom.set_arg("partner_cred_points", four_int)
    assert x_beliefatoms[0] == static_atom


def test_AtomRow_get_beliefatoms_ReturnsObjIfDimenIsCorrect():
    # ESTABLISH
    x_atomrow = atomrow_shop(set(), INSERT_str())
    x_atomrow.partner_name = "Bob"
    four_str = "4"
    x_atomrow.partner_cred_points = four_str
    assert len(x_atomrow.get_beliefatoms()) == 0

    # WHEN / THEN
    x_atomrow.set_atom_dimen(belief_partner_membership_str())
    assert len(x_atomrow.get_beliefatoms()) == 0

    # THEN
    x_atomrow.set_atom_dimen(belief_partnerunit_str())
    assert len(x_atomrow.get_beliefatoms()) == 1


def test_AtomRow_get_beliefatoms_ReturnsObj_belief_planunit_INSERT_task_False_Scenario0():
    # ESTABLISH
    x_atomrow = atomrow_shop({belief_planunit_str()}, INSERT_str())
    x_atomrow.plan_rope = create_rope("amy78", "casa")
    x_atomrow.task = False
    assert len(x_atomrow.get_beliefatoms()) == 1

    # WHEN / THEN
    x_beliefatom = x_atomrow.get_beliefatoms()[0]

    # THEN
    static_beliefatom = beliefatom_shop(belief_planunit_str(), INSERT_str())
    static_beliefatom.set_arg("plan_rope", create_rope("amy78", "casa"))
    static_beliefatom.set_arg("task", False)
    print(static_beliefatom)
    print(x_beliefatom)
    assert x_beliefatom == static_beliefatom


def test_AtomRow_get_beliefatoms_ReturnsObj_belief_planunit_INSERT_task_False_Scenario1():
    # ESTABLISH
    x_dimens = {belief_planunit_str(), belief_plan_healerunit_str()}
    x_atomrow = atomrow_shop(x_dimens, INSERT_str())
    x_atomrow.plan_rope = create_rope("amy78", "casa")
    x_atomrow.task = False
    x_atomrow.healer_name = "Bob"

    # WHEN / THEN
    x_beliefatoms = x_atomrow.get_beliefatoms()

    # THEN
    assert len(x_beliefatoms) == 2
    y_plan_beliefatom = beliefatom_shop(belief_planunit_str(), INSERT_str())
    casa_rope = create_rope("amy78", "casa")
    y_plan_beliefatom.set_arg("plan_rope", casa_rope)
    y_plan_beliefatom.set_arg("task", False)
    assert y_plan_beliefatom in x_beliefatoms
    healerunit_beliefatom = beliefatom_shop(belief_plan_healerunit_str(), INSERT_str())
    healerunit_beliefatom.set_arg("plan_rope", casa_rope)
    healerunit_beliefatom.set_arg("healer_name", "Bob")
    assert healerunit_beliefatom in x_beliefatoms
