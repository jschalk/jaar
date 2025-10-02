from os.path import exists as os_path_exists
from src.ch01_data_toolbox.file_toolbox import create_path, open_file, save_file
from src.ch07_belief_logic.belief_main import beliefunit_shop, get_beliefunit_from_json
from src.ch10_pack_logic.pack import get_packunit_from_json, packunit_shop
from src.ch12_hub_toolbox.ch12_path import (
    create_belief_event_dir_path,
    create_event_all_pack_path,
    create_event_expressed_pack_path,
)
from src.ch18_etl_toolbox._ref.ch18_keywords import Ch18Keywords as wx
from src.ch18_etl_toolbox.test._util.ch18_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)
from src.ch18_etl_toolbox.transformers import (
    etl_event_pack_json_to_event_inherited_beliefunits,
)


def test_etl_event_pack_json_to_event_inherited_beliefunits_SetsFiles_belief_json(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    event3 = 3
    event7 = 7
    credit44 = 44
    credit77 = 77
    credit88 = 88
    a23_str = "amy23"
    moment_mstr_dir = get_chapter_temp_dir()
    a23_bob_e3_dir = create_belief_event_dir_path(
        moment_mstr_dir, a23_str, bob_inx, event3
    )
    a23_bob_e7_dir = create_belief_event_dir_path(
        moment_mstr_dir, a23_str, bob_inx, event7
    )
    a23_bob_e3_pack = packunit_shop(bob_inx, None, a23_str, event_int=event3)
    a23_bob_e7_pack = packunit_shop(bob_inx, None, a23_str, event_int=event7)
    blrpern_dimen = wx.belief_voiceunit
    bob_jkeys = {wx.voice_name: bob_inx}
    bob_jvalues = {wx.voice_cred_points: credit77, wx.voice_debt_points: None}
    yao_jkeys = {wx.voice_name: yao_inx}
    yao_jvalues = {wx.voice_cred_points: credit44, wx.voice_debt_points: None}
    a23_bob_e3_pack.add_p_beliefatom(blrpern_dimen, wx.INSERT, bob_jkeys, bob_jvalues)
    a23_bob_e3_pack.add_p_beliefatom(blrpern_dimen, wx.INSERT, yao_jkeys, yao_jvalues)
    sue_jkeys = {wx.voice_name: sue_inx}
    sue_jvalues = {wx.voice_cred_points: credit88, wx.voice_debt_points: None}
    a23_bob_e7_pack.add_p_beliefatom(blrpern_dimen, wx.INSERT, bob_jkeys, bob_jvalues)
    a23_bob_e7_pack.add_p_beliefatom(blrpern_dimen, wx.INSERT, sue_jkeys, sue_jvalues)
    e3_all_pack_path = create_event_all_pack_path(
        moment_mstr_dir, a23_str, bob_inx, event3
    )
    e7_all_pack_path = create_event_all_pack_path(
        moment_mstr_dir, a23_str, bob_inx, event7
    )
    save_file(e3_all_pack_path, None, a23_bob_e3_pack.get_json())
    save_file(e7_all_pack_path, None, a23_bob_e7_pack.get_json())
    assert os_path_exists(e3_all_pack_path)
    assert os_path_exists(e7_all_pack_path)
    belief_filename = "belief.json"
    e3_belief_path = create_path(a23_bob_e3_dir, belief_filename)
    e7_belief_path = create_path(a23_bob_e7_dir, belief_filename)
    assert os_path_exists(e3_belief_path) is False
    assert os_path_exists(e7_belief_path) is False

    # WHEN
    etl_event_pack_json_to_event_inherited_beliefunits(moment_mstr_dir)

    # THEN
    assert os_path_exists(e3_belief_path)
    assert os_path_exists(e7_belief_path)
    expected_e3_bob_belief = beliefunit_shop(bob_inx, a23_str)
    expected_e7_bob_belief = beliefunit_shop(bob_inx, a23_str)
    expected_e3_bob_belief.add_voiceunit(bob_inx, credit77)
    expected_e3_bob_belief.add_voiceunit(yao_inx, credit44)
    expected_e7_bob_belief.add_voiceunit(bob_inx, credit77)
    expected_e7_bob_belief.add_voiceunit(sue_inx, credit88)
    expected_e7_bob_belief.add_voiceunit(yao_inx, credit44)
    generated_e3_belief = get_beliefunit_from_json(open_file(e3_belief_path))
    generated_e7_belief = get_beliefunit_from_json(open_file(e7_belief_path))
    assert generated_e3_belief.voices == expected_e3_bob_belief.voices
    assert generated_e3_belief == expected_e3_bob_belief
    assert generated_e3_belief.to_dict() == expected_e3_bob_belief.to_dict()
    assert generated_e7_belief.voices == expected_e7_bob_belief.voices
    assert generated_e7_belief.to_dict() == expected_e7_bob_belief.to_dict()


def test_etl_event_pack_json_to_event_inherited_beliefunits_SetsFiles_expressed_pack(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    xia_inx = "Xia"
    event3 = 3
    event7 = 7
    credit44 = 44
    credit77 = 77
    credit88 = 88
    a23_str = "amy23"
    moment_mstr_dir = get_chapter_temp_dir()
    a23_bob_e3_pack = packunit_shop(bob_inx, xia_inx, a23_str, event_int=event3)
    a23_bob_e7_pack = packunit_shop(bob_inx, xia_inx, a23_str, event_int=event7)
    blrpern_dimen = wx.belief_voiceunit
    bob_jkeys = {wx.voice_name: bob_inx}
    bob_jvalues = {wx.voice_cred_points: credit77}
    yao_jkeys = {wx.voice_name: yao_inx}
    yao_jvalues = {wx.voice_cred_points: credit44}
    a23_bob_e3_pack.add_p_beliefatom(blrpern_dimen, wx.INSERT, bob_jkeys, bob_jvalues)
    a23_bob_e3_pack.add_p_beliefatom(blrpern_dimen, wx.INSERT, yao_jkeys, yao_jvalues)
    sue_jkeys = {wx.voice_name: sue_inx}
    sue_jvalues = {wx.voice_cred_points: credit88}
    a23_bob_e7_pack.add_p_beliefatom(blrpern_dimen, wx.INSERT, bob_jkeys, bob_jvalues)
    a23_bob_e7_pack.add_p_beliefatom(blrpern_dimen, wx.INSERT, sue_jkeys, sue_jvalues)
    a23_bob_e3_all_pack_path = create_event_all_pack_path(
        moment_mstr_dir, a23_str, bob_inx, event3
    )
    a23_bob_e7_all_pack_path = create_event_all_pack_path(
        moment_mstr_dir, a23_str, bob_inx, event7
    )
    save_file(a23_bob_e3_all_pack_path, None, a23_bob_e3_pack.get_json())
    save_file(a23_bob_e7_all_pack_path, None, a23_bob_e7_pack.get_json())
    e3_expressed_pack_path = create_event_expressed_pack_path(
        moment_mstr_dir, a23_str, bob_inx, event3
    )
    e7_expressed_pack_path = create_event_expressed_pack_path(
        moment_mstr_dir, a23_str, bob_inx, event7
    )
    assert os_path_exists(a23_bob_e3_all_pack_path)
    assert os_path_exists(a23_bob_e7_all_pack_path)
    assert os_path_exists(e3_expressed_pack_path) is False
    assert os_path_exists(e7_expressed_pack_path) is False

    # WHEN
    etl_event_pack_json_to_event_inherited_beliefunits(moment_mstr_dir)

    # THEN
    assert os_path_exists(e3_expressed_pack_path)
    assert os_path_exists(e7_expressed_pack_path)
    gen_e3_express_pack = get_packunit_from_json(open_file(e3_expressed_pack_path))
    gen_e7_express_pack = get_packunit_from_json(open_file(e7_expressed_pack_path))
    expected_e3_bob_pack = packunit_shop(bob_inx, xia_inx, a23_str, event_int=event3)
    expected_e7_bob_pack = packunit_shop(bob_inx, xia_inx, a23_str, event_int=event7)
    expected_e3_bob_pack.add_p_beliefatom(
        blrpern_dimen, wx.INSERT, bob_jkeys, bob_jvalues
    )
    expected_e3_bob_pack.add_p_beliefatom(
        blrpern_dimen, wx.INSERT, yao_jkeys, yao_jvalues
    )
    expected_e7_bob_pack.add_p_beliefatom(
        blrpern_dimen, wx.INSERT, sue_jkeys, sue_jvalues
    )
    assert expected_e3_bob_pack == a23_bob_e3_pack
    assert expected_e7_bob_pack._beliefdelta != a23_bob_e7_pack._beliefdelta
    assert expected_e7_bob_pack != a23_bob_e7_pack
    # expected_e3_bob_pack.add_p_beliefatom()
    # expected_e3_bob_pack.add_p_beliefatom()
    # expected_e7_bob_pack.add_p_beliefatom()
    # expected_e7_bob_pack.add_p_beliefatom()
    # expected_e7_bob_pack.add_p_beliefatom()
    assert gen_e3_express_pack == expected_e3_bob_pack
    gen_e7_express_delta = gen_e7_express_pack._beliefdelta
    expected_e7_delta = expected_e7_bob_pack._beliefdelta
    assert gen_e7_express_delta.beliefatoms == expected_e7_delta.beliefatoms
    assert gen_e7_express_pack._beliefdelta == expected_e7_bob_pack._beliefdelta
    assert gen_e7_express_pack == expected_e7_bob_pack
