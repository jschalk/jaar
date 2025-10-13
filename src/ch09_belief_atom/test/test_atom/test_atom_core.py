from src.ch04_voice.voice import voiceunit_shop
from src.ch09_belief_atom.atom_main import BeliefAtom, beliefatom_shop
from src.ref.keywords import Ch09Keywords as wx


def test_BeliefAtom_Exists():
    # ESTABLISH / WHEN
    x_beliefatom = BeliefAtom()

    # THEN
    assert not x_beliefatom.dimen
    assert not x_beliefatom.crud_str
    assert not x_beliefatom.jkeys
    assert not x_beliefatom.jvalues
    assert not x_beliefatom.atom_order


def test_beliefatom_shop_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_voice_cred_lumen = 55
    bob_voice_debt_lumen = 66
    bob_voiceunit = voiceunit_shop(bob_str, bob_voice_cred_lumen, bob_voice_debt_lumen)
    cw_str = "_voice_cred_lumen"
    dw_str = "_voice_debt_lumen"
    bob_required_dict = {wx.voice_name: "huh"}
    bob_optional_dict = {cw_str: bob_voiceunit.to_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_voiceunit.to_dict().get(dw_str)
    voiceunit_str = wx.belief_voiceunit

    # WHEN
    x_beliefatom = beliefatom_shop(
        dimen=voiceunit_str,
        crud_str=wx.INSERT,
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    print(f"{x_beliefatom=}")
    assert x_beliefatom.dimen == voiceunit_str
    assert x_beliefatom.crud_str == wx.INSERT
    assert x_beliefatom.jkeys == bob_required_dict
    assert x_beliefatom.jvalues == bob_optional_dict


def test_BeliefAtom_set_jkey_SetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    voiceunit_str = wx.belief_voiceunit
    voiceunit_beliefatom = beliefatom_shop(voiceunit_str, wx.INSERT)
    assert voiceunit_beliefatom.jkeys == {}

    # WHEN
    voiceunit_beliefatom.set_jkey(x_key=wx.voice_name, x_value=bob_str)

    # THEN
    assert voiceunit_beliefatom.jkeys == {wx.voice_name: bob_str}


def test_BeliefAtom_set_jvalue_SetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    voiceunit_str = wx.belief_voiceunit
    voiceunit_beliefatom = beliefatom_shop(voiceunit_str, wx.INSERT)
    assert voiceunit_beliefatom.jvalues == {}

    # WHEN
    voiceunit_beliefatom.set_jvalue(x_key=wx.voice_name, x_value=bob_str)

    # THEN
    assert voiceunit_beliefatom.jvalues == {wx.voice_name: bob_str}


def test_BeliefAtom_get_value_ReturnsObj_Scenario0():
    # ESTABLISH
    bob_str = "Bob"
    voiceunit_str = wx.belief_voiceunit
    voiceunit_beliefatom = beliefatom_shop(voiceunit_str, wx.INSERT)
    voiceunit_beliefatom.set_jkey(x_key=wx.voice_name, x_value=bob_str)

    # WHEN / THEN
    assert voiceunit_beliefatom.get_value(wx.voice_name) == bob_str


def test_BeliefAtom_is_jvalues_valid_ReturnsBoolean():
    # ESTABLISH / WHEN
    voiceunit_str = wx.belief_voiceunit
    bob_insert_beliefatom = beliefatom_shop(voiceunit_str, crud_str=wx.INSERT)
    assert bob_insert_beliefatom.is_jvalues_valid()

    # WHEN
    bob_insert_beliefatom.set_jvalue(wx.voice_cred_lumen, 55)
    # THEN
    assert len(bob_insert_beliefatom.jvalues) == 1
    assert bob_insert_beliefatom.is_jvalues_valid()

    # WHEN
    bob_insert_beliefatom.set_jvalue(wx.voice_debt_lumen, 66)
    # THEN
    assert len(bob_insert_beliefatom.jvalues) == 2
    assert bob_insert_beliefatom.is_jvalues_valid()

    # WHEN
    bob_insert_beliefatom.set_jvalue("x_x_x", 77)
    # THEN
    assert len(bob_insert_beliefatom.jvalues) == 3
    assert bob_insert_beliefatom.is_jvalues_valid() is False


def test_BeliefAtom_is_valid_ReturnsBoolean_VoiceUnit_INSERT():
    # ESTABLISH
    bob_str = "Bob"
    bob_voice_cred_lumen = 55
    bob_voice_debt_lumen = 66
    bob_voiceunit = voiceunit_shop(bob_str, bob_voice_cred_lumen, bob_voice_debt_lumen)
    voiceunit_str = wx.belief_voiceunit

    # WHEN
    bob_insert_beliefatom = beliefatom_shop(voiceunit_str, crud_str=wx.INSERT)

    # THEN
    assert bob_insert_beliefatom.is_jkeys_valid() is False
    assert bob_insert_beliefatom.is_jvalues_valid()
    assert bob_insert_beliefatom.is_valid() is False

    # WHEN
    bob_insert_beliefatom.set_jvalue("x_x_x", 12)

    # THEN
    assert bob_insert_beliefatom.is_jkeys_valid() is False
    assert bob_insert_beliefatom.is_jvalues_valid() is False
    assert bob_insert_beliefatom.is_valid() is False

    # WHEN
    bob_insert_beliefatom.set_jkey(wx.voice_name, bob_str)

    # THEN
    assert bob_insert_beliefatom.is_jkeys_valid()
    assert bob_insert_beliefatom.is_jvalues_valid() is False
    assert bob_insert_beliefatom.is_valid() is False

    # WHEN
    bob_insert_beliefatom.jvalues = {}
    cw_str = wx.voice_cred_lumen
    dw_str = wx.voice_debt_lumen
    bob_insert_beliefatom.set_jvalue(cw_str, bob_voiceunit.to_dict().get(cw_str))
    bob_insert_beliefatom.set_jvalue(dw_str, bob_voiceunit.to_dict().get(dw_str))

    # THEN
    assert bob_insert_beliefatom.is_jkeys_valid()
    assert bob_insert_beliefatom.is_jvalues_valid()
    assert bob_insert_beliefatom.is_valid()

    # WHEN
    bob_insert_beliefatom.crud_str = None

    # THEN
    assert bob_insert_beliefatom.is_jkeys_valid() is False
    assert bob_insert_beliefatom.is_valid() is False

    # WHEN
    bob_insert_beliefatom.crud_str = wx.INSERT

    # THEN
    assert bob_insert_beliefatom.is_jkeys_valid()
    assert bob_insert_beliefatom.is_valid()


def test_BeliefAtom_get_value_ReturnsObj_Scenario1():
    # ESTABLISH
    bob_str = "Bob"
    bob_voice_cred_lumen = 55
    bob_voice_debt_lumen = 66
    bob_voiceunit = voiceunit_shop(bob_str, bob_voice_cred_lumen, bob_voice_debt_lumen)
    voiceunit_str = wx.belief_voiceunit
    bob_insert_beliefatom = beliefatom_shop(voiceunit_str, wx.INSERT)
    cw_str = wx.voice_cred_lumen
    dw_str = wx.voice_debt_lumen
    print(f"{bob_voiceunit.to_dict()=}")
    # bob_voiceunit_dict = {wx.voice_name: bob_voiceunit.to_dict().get(wx.voice_name)}
    # print(f"{bob_voiceunit_dict=}")
    bob_insert_beliefatom.set_jkey(wx.voice_name, bob_str)
    bob_insert_beliefatom.set_jvalue(cw_str, bob_voiceunit.to_dict().get(cw_str))
    bob_insert_beliefatom.set_jvalue(dw_str, bob_voiceunit.to_dict().get(dw_str))
    assert bob_insert_beliefatom.is_valid()

    # WHEN / THEN
    assert bob_insert_beliefatom.get_value(cw_str) == bob_voice_cred_lumen
    assert bob_insert_beliefatom.get_value(dw_str) == bob_voice_debt_lumen


def test_BeliefAtom_is_valid_ReturnsBoolean_VoiceUnit_DELETE():
    # ESTABLISH
    bob_str = "Bob"
    voiceunit_str = wx.belief_voiceunit
    delete_str = wx.DELETE

    # WHEN
    bob_delete_beliefatom = beliefatom_shop(voiceunit_str, crud_str=delete_str)

    # THEN
    assert bob_delete_beliefatom.is_jkeys_valid() is False
    assert bob_delete_beliefatom.is_valid() is False

    # WHEN
    bob_delete_beliefatom.set_jkey(wx.voice_name, bob_str)

    # THEN
    assert bob_delete_beliefatom.is_jkeys_valid()
    assert bob_delete_beliefatom.is_valid()


def test_BeliefAtom_is_valid_ReturnsBoolean_beliefunit():
    # ESTABLISH / WHEN
    bob_update_beliefatom = beliefatom_shop(wx.beliefunit, wx.INSERT)

    # THEN
    assert bob_update_beliefatom.is_jkeys_valid()
    assert bob_update_beliefatom.is_valid() is False

    # WHEN
    bob_update_beliefatom.set_jvalue(wx.max_tree_traverse, 14)

    # THEN
    assert bob_update_beliefatom.is_jkeys_valid()
    assert bob_update_beliefatom.is_valid()


def test_BeliefAtom_set_atom_order_SetsAttr():
    # ESTABLISH
    bob_str = "Bob"
    bob_voice_cred_lumen = 55
    bob_voice_debt_lumen = 66
    voiceunit_str = wx.belief_voiceunit
    bob_insert_beliefatom = beliefatom_shop(voiceunit_str, wx.INSERT)
    cw_str = wx.voice_cred_lumen
    dw_str = wx.voice_debt_lumen
    bob_insert_beliefatom.set_jkey(wx.voice_name, bob_str)
    bob_insert_beliefatom.set_jvalue(cw_str, bob_voice_cred_lumen)
    bob_insert_beliefatom.set_jvalue(dw_str, bob_voice_debt_lumen)
    assert bob_insert_beliefatom.is_valid()

    # WHEN / THEN
    assert bob_insert_beliefatom.get_value(cw_str) == bob_voice_cred_lumen
    assert bob_insert_beliefatom.get_value(dw_str) == bob_voice_debt_lumen


def test_BeliefAtom_set_arg_SetsAny_jkey_jvalue():
    # ESTABLISH
    bob_str = "Bob"
    bob_voice_cred_lumen = 55
    bob_voice_debt_lumen = 66
    voiceunit_str = wx.belief_voiceunit
    bob_insert_beliefatom = beliefatom_shop(voiceunit_str, wx.INSERT)
    cw_str = wx.voice_cred_lumen
    dw_str = wx.voice_debt_lumen

    # WHEN
    bob_insert_beliefatom.set_arg(wx.voice_name, bob_str)
    bob_insert_beliefatom.set_arg(cw_str, bob_voice_cred_lumen)
    bob_insert_beliefatom.set_arg(dw_str, bob_voice_debt_lumen)

    # THEN
    assert bob_insert_beliefatom.get_value(wx.voice_name) == bob_str
    assert bob_insert_beliefatom.get_value(cw_str) == bob_voice_cred_lumen
    assert bob_insert_beliefatom.get_value(dw_str) == bob_voice_debt_lumen
    assert bob_insert_beliefatom.get_value(wx.voice_name) == bob_str
    assert bob_insert_beliefatom.is_valid()


def test_BeliefAtom_get_nesting_order_args_ReturnsObj_belief_voiceunit():
    # ESTABLISH
    sue_str = "Sue"
    sue_insert_beliefatom = beliefatom_shop(wx.belief_voiceunit, wx.INSERT)
    sue_insert_beliefatom.set_arg(wx.voice_name, sue_str)
    print(f"{sue_insert_beliefatom.jkeys=}")

    # WHEN / THEN
    ordered_jkeys = [sue_str]
    assert sue_insert_beliefatom.get_nesting_order_args() == ordered_jkeys


def test_BeliefAtom_get_nesting_order_args_ReturnsObj_belief_voice_membership():
    # ESTABLISH
    sue_str = "Sue"
    iowa_str = ";Iowa"
    sue_insert_beliefatom = beliefatom_shop(wx.belief_voice_membership, wx.INSERT)
    sue_insert_beliefatom.set_arg(wx.group_title, iowa_str)
    sue_insert_beliefatom.set_arg(wx.voice_name, sue_str)
    print(f"{sue_insert_beliefatom.jkeys=}")

    # WHEN / THEN
    ordered_jkeys = [sue_str, iowa_str]
    assert sue_insert_beliefatom.get_nesting_order_args() == ordered_jkeys
