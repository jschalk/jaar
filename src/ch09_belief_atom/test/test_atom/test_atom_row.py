from src.ch02_rope.rope import create_rope, to_rope
from src.ch09_belief_atom.atom_config import get_atom_args_class_types
from src.ch09_belief_atom.atom_main import AtomRow, atomrow_shop, beliefatom_shop
from src.ref.keywords import Ch09Keywords as wx


def test_AtomRow_Exists():
    # ESTABLISH /  WHEN
    x_atomrow = AtomRow()

    # THEN
    assert x_atomrow._atom_dimens is None
    assert x_atomrow._crud_command is None
    assert x_atomrow.voice_name is None
    assert x_atomrow.addin is None
    assert x_atomrow.reason_context is None
    assert x_atomrow.active_requisite is None
    assert x_atomrow.begin is None
    assert x_atomrow.respect_grain is None
    assert x_atomrow.close is None
    assert x_atomrow.voice_cred_lumen is None
    assert x_atomrow.group_cred_lumen is None
    assert x_atomrow.credor_respect is None
    assert x_atomrow.voice_debt_lumen is None
    assert x_atomrow.group_debt_lumen is None
    assert x_atomrow.debtor_respect is None
    assert x_atomrow.denom is None
    assert x_atomrow.reason_divisor is None
    assert x_atomrow.fact_context is None
    assert x_atomrow.fact_upper is None
    assert x_atomrow.fact_lower is None
    assert x_atomrow.fund_grain is None
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
    assert x_atomrow.money_grain is None
    assert x_atomrow.fact_state is None
    assert x_atomrow.pledge is None
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
    x_atom_dimens = {wx.belief_voiceunit}

    # WHEN
    x_atomrow = atomrow_shop(x_atom_dimens, wx.INSERT)

    # THEN
    assert x_atomrow._atom_dimens == x_atom_dimens
    assert x_atomrow._crud_command == wx.INSERT


def test_AtomRow_set_atom_dimen_SetsAttr():
    # ESTABLISH
    x_atomrow = atomrow_shop({wx.belief_voiceunit}, wx.INSERT)
    assert wx.belief_voice_membership not in x_atomrow._atom_dimens

    # WHEN
    x_atomrow.set_atom_dimen(wx.belief_voice_membership)

    # THEN
    assert wx.belief_voice_membership in x_atomrow._atom_dimens


def test_AtomRow_atom_dimen_exists_ReturnsObj():
    # ESTABLISH
    x_atomrow = atomrow_shop(set(), wx.INSERT)
    assert not x_atomrow.atom_dimen_exists(wx.belief_voiceunit)
    assert not x_atomrow.atom_dimen_exists(wx.belief_voice_membership)

    # WHEN
    x_atomrow.set_atom_dimen(wx.belief_voice_membership)

    # THEN
    assert not x_atomrow.atom_dimen_exists(wx.belief_voiceunit)
    assert x_atomrow.atom_dimen_exists(wx.belief_voice_membership)


def test_AtomRow_delete_atom_dimen_SetsAttr():
    # ESTABLISH
    x_atomrow = atomrow_shop({wx.belief_voiceunit}, wx.INSERT)
    x_atomrow.set_atom_dimen(wx.belief_voiceunit)
    x_atomrow.set_atom_dimen(wx.belief_voice_membership)
    assert x_atomrow.atom_dimen_exists(wx.belief_voiceunit)
    assert x_atomrow.atom_dimen_exists(wx.belief_voice_membership)

    # WHEN
    x_atomrow.delete_atom_dimen(wx.belief_voice_membership)

    # THEN
    assert x_atomrow.atom_dimen_exists(wx.belief_voiceunit)
    assert not x_atomrow.atom_dimen_exists(wx.belief_voice_membership)


def test_AtomRow_set_class_types_SetsAttr():
    # ESTABLISH
    x_atomrow = atomrow_shop({}, wx.INSERT)
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


def test_AtomRow_get_beliefatoms_ReturnsObj_belief_voiceunit_str_INSERT_Scenario0():
    # ESTABLISH
    x_dimen = wx.belief_voiceunit
    x_atomrow = atomrow_shop({x_dimen}, wx.INSERT)
    x_atomrow.voice_name = "Bob"

    # WHEN
    x_beliefatoms = x_atomrow.get_beliefatoms()

    # THEN
    assert len(x_beliefatoms) == 1
    static_atom = beliefatom_shop(x_dimen, wx.INSERT)
    static_atom.set_arg(wx.voice_name, "Bob")
    assert x_beliefatoms[0] == static_atom


def test_AtomRow_get_beliefatoms_ReturnsObj_belief_voiceunit_str_INSERT_Scenario1():
    # ESTABLISH
    x_dimen = wx.belief_voiceunit
    x_atomrow = atomrow_shop({x_dimen}, wx.INSERT)
    x_atomrow.voice_name = "Bob"
    x_atomrow.voice_cred_lumen = 5

    # WHEN
    x_beliefatoms = x_atomrow.get_beliefatoms()

    # THEN
    assert len(x_beliefatoms) == 1
    static_atom = beliefatom_shop(x_dimen, wx.INSERT)
    static_atom.set_arg(wx.voice_name, "Bob")
    static_atom.set_arg("voice_cred_lumen", 5)
    assert x_beliefatoms[0] == static_atom


def test_AtomRow_get_beliefatoms_ReturnsObj_belief_voiceunit_NSERT_Fails():
    # ESTABLISH
    x_dimen = wx.belief_voiceunit
    x_atomrow = atomrow_shop({x_dimen}, wx.INSERT)

    # WHEN
    x_beliefatoms = x_atomrow.get_beliefatoms()

    # THEN
    assert len(x_beliefatoms) == 0


def test_AtomRow_get_beliefatoms_ReturnsObj_belief_voiceunit_INSERT_Scenario2():
    # ESTABLISH
    x_dimen = wx.belief_voiceunit
    x_atomrow = atomrow_shop({x_dimen}, wx.INSERT)
    x_atomrow.voice_name = "Bob"
    four_str = "4"
    x_atomrow.voice_cred_lumen = four_str

    # WHEN
    x_beliefatoms = x_atomrow.get_beliefatoms()

    # THEN
    assert len(x_beliefatoms) == 1
    static_atom = beliefatom_shop(x_dimen, wx.INSERT)
    static_atom.set_arg(wx.voice_name, "Bob")
    four_int = 4
    static_atom.set_arg("voice_cred_lumen", four_int)
    assert x_beliefatoms[0] == static_atom


def test_AtomRow_get_beliefatoms_ReturnsObjIfDimenIsCorrect():
    # ESTABLISH
    x_atomrow = atomrow_shop(set(), wx.INSERT)
    x_atomrow.voice_name = "Bob"
    four_str = "4"
    x_atomrow.voice_cred_lumen = four_str
    assert len(x_atomrow.get_beliefatoms()) == 0

    # WHEN / THEN
    x_atomrow.set_atom_dimen(wx.belief_voice_membership)
    assert len(x_atomrow.get_beliefatoms()) == 0

    # THEN
    x_atomrow.set_atom_dimen(wx.belief_voiceunit)
    assert len(x_atomrow.get_beliefatoms()) == 1


def test_AtomRow_get_beliefatoms_ReturnsObj_belief_planunit_INSERT_pledge_False_Scenario0():
    # ESTABLISH
    x_atomrow = atomrow_shop({wx.belief_planunit}, wx.INSERT)
    x_atomrow.plan_rope = create_rope("amy78", "casa")
    x_atomrow.pledge = False
    assert len(x_atomrow.get_beliefatoms()) == 1

    # WHEN / THEN
    x_beliefatom = x_atomrow.get_beliefatoms()[0]

    # THEN
    static_beliefatom = beliefatom_shop(wx.belief_planunit, wx.INSERT)
    static_beliefatom.set_arg("plan_rope", create_rope("amy78", "casa"))
    static_beliefatom.set_arg("pledge", False)
    print(static_beliefatom)
    print(x_beliefatom)
    assert x_beliefatom == static_beliefatom


def test_AtomRow_get_beliefatoms_ReturnsObj_belief_planunit_INSERT_pledge_False_Scenario1():
    # ESTABLISH
    x_dimens = {wx.belief_planunit, wx.belief_plan_healerunit}
    x_atomrow = atomrow_shop(x_dimens, wx.INSERT)
    x_atomrow.plan_rope = create_rope("amy78", "casa")
    x_atomrow.pledge = False
    x_atomrow.healer_name = "Bob"

    # WHEN / THEN
    x_beliefatoms = x_atomrow.get_beliefatoms()

    # THEN
    assert len(x_beliefatoms) == 2
    y_plan_beliefatom = beliefatom_shop(wx.belief_planunit, wx.INSERT)
    casa_rope = create_rope("amy78", "casa")
    y_plan_beliefatom.set_arg("plan_rope", casa_rope)
    y_plan_beliefatom.set_arg("pledge", False)
    assert y_plan_beliefatom in x_beliefatoms
    healerunit_beliefatom = beliefatom_shop(wx.belief_plan_healerunit, wx.INSERT)
    healerunit_beliefatom.set_arg("plan_rope", casa_rope)
    healerunit_beliefatom.set_arg("healer_name", "Bob")
    assert healerunit_beliefatom in x_beliefatoms
