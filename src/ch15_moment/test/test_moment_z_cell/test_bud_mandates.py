from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import open_json, save_json
from src.ch09_belief_lesson._ref.ch09_path import create_moment_json_path
from src.ch12_bud._ref.ch12_path import (
    create_cell_voice_mandate_ledger_path as cell_mandate_path,
)
from src.ch12_bud.bud_main import tranbook_shop
from src.ch15_moment._ref.ch15_path import (
    create_bud_voice_mandate_ledger_path as bud_mandate_path,
)
from src.ch15_moment.moment_cell import create_bud_mandate_ledgers
from src.ch15_moment.moment_main import get_momentunit_from_dict, momentunit_shop
from src.ch15_moment.test._util.ch15_env import get_temp_dir, temp_dir_setup


def test_create_bud_mandate_ledgers_Scenaro0_BudEmpty(temp_dir_setup):
    # ESTABLISH
    a23_str = "amy23"
    mstr_dir = get_temp_dir()
    amy23_moment = momentunit_shop(a23_str, mstr_dir)
    a23_json_path = create_moment_json_path(mstr_dir, a23_str)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    bob_str = "Bob"
    epochtime9 = 9
    bob9_bud_mandate_path = bud_mandate_path(mstr_dir, a23_str, bob_str, epochtime9)
    assert os_path_exists(bob9_bud_mandate_path) is False

    # WHEN
    create_bud_mandate_ledgers(mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob9_bud_mandate_path) is False


def test_create_bud_mandate_ledgers_Scenaro1_BudExists(temp_dir_setup):
    # ESTABLISH
    a23_str = "amy23"
    mstr_dir = get_temp_dir()
    amy23_moment = momentunit_shop(a23_str, mstr_dir)
    bob_str = "Bob"
    tp37 = 37
    bud1_quota = 450
    amy23_moment.add_budunit(bob_str, tp37, bud1_quota)
    a23_json_path = create_moment_json_path(mstr_dir, a23_str)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    bob37_cell_mandate_path = cell_mandate_path(mstr_dir, a23_str, bob_str, tp37)
    bob_mandate = 777
    assert bud1_quota != bob_mandate
    save_json(bob37_cell_mandate_path, None, {bob_str: bob_mandate})
    bob37_bud_mandate_path = bud_mandate_path(mstr_dir, a23_str, bob_str, tp37)
    assert os_path_exists(bob37_bud_mandate_path) is False
    bob37_budunit = amy23_moment.get_budunit(bob_str, tp37)
    assert bob37_budunit._bud_voice_nets == {}

    # WHEN
    create_bud_mandate_ledgers(mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob37_bud_mandate_path)
    expected_bud_voice_nets = {bob_str: bud1_quota}
    assert open_json(bob37_bud_mandate_path) == expected_bud_voice_nets
    gen_a23_momentunit = get_momentunit_from_dict(open_json(a23_json_path))
    gen_a23_momentunit.set_all_tranbook()
    gen_bob37_budunit = gen_a23_momentunit.get_budunit(bob_str, tp37)
    assert gen_bob37_budunit._bud_voice_nets == expected_bud_voice_nets
    expected_a23_all_tranbook = tranbook_shop(a23_str)
    expected_a23_all_tranbook.add_tranunit(bob_str, bob_str, tp37, 450)
    assert gen_a23_momentunit.all_tranbook == expected_a23_all_tranbook


def test_create_bud_mandate_ledgers_Scenaro2_Mutliple_cell_voice_mandate_ledgers(
    temp_dir_setup,
):
    # ESTABLISH
    a23_str = "amy23"
    mstr_dir = get_temp_dir()
    amy23_moment = momentunit_shop(a23_str, mstr_dir)
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    sue_str = "Sue"
    xio_str = "Xio"
    tp37 = 37
    bud1_quota = 450
    amy23_moment.add_budunit(bob_str, tp37, bud1_quota)
    a23_json_path = create_moment_json_path(mstr_dir, a23_str)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    b37_cell_mandate = cell_mandate_path(mstr_dir, a23_str, bob_str, tp37)
    b37_sue_cell_path = cell_mandate_path(mstr_dir, a23_str, bob_str, tp37, [sue_str])
    b37_yao_cell_path = cell_mandate_path(mstr_dir, a23_str, bob_str, tp37, [yao_str])
    yz_anc = [yao_str, zia_str]
    b37_yao_zia_cell_path = cell_mandate_path(mstr_dir, a23_str, bob_str, tp37, yz_anc)
    save_json(b37_cell_mandate, None, {sue_str: 1, yao_str: 3})
    save_json(b37_sue_cell_path, None, {zia_str: 1, sue_str: 3})
    save_json(b37_yao_cell_path, None, {zia_str: 1, yao_str: 3})
    save_json(b37_yao_zia_cell_path, None, {xio_str: 1})
    bob37_bud_mandate_path = bud_mandate_path(mstr_dir, a23_str, bob_str, tp37)
    assert os_path_exists(bob37_bud_mandate_path) is False
    bob37_budunit = amy23_moment.get_budunit(bob_str, tp37)
    assert bob37_budunit._bud_voice_nets == {}

    # WHEN
    create_bud_mandate_ledgers(mstr_dir, a23_str)

    # THEN
    assert os_path_exists(bob37_bud_mandate_path)
    expected_bud_voice_nets = {
        yao_str: 254,
        xio_str: 84,
        sue_str: 84,
        zia_str: 28,
    }
    print(f"{open_json(bob37_bud_mandate_path)=}")
    assert open_json(bob37_bud_mandate_path) == expected_bud_voice_nets
    gen_a23_momentunit = get_momentunit_from_dict(open_json(a23_json_path))
    gen_bob37_budunit = gen_a23_momentunit.get_budunit(bob_str, tp37)
    assert gen_bob37_budunit._bud_voice_nets == expected_bud_voice_nets
    expected_a23_all_tranbook = tranbook_shop(a23_str)
    expected_a23_all_tranbook.add_tranunit(bob_str, sue_str, tp37, 84)
    expected_a23_all_tranbook.add_tranunit(bob_str, xio_str, tp37, 84)
    expected_a23_all_tranbook.add_tranunit(bob_str, zia_str, tp37, 28)
    expected_a23_all_tranbook.add_tranunit(bob_str, yao_str, tp37, 254)
    gen_a23_momentunit.set_all_tranbook()
    gen_all_tranbook = gen_a23_momentunit.all_tranbook
    assert gen_all_tranbook.tranunits == expected_a23_all_tranbook.tranunits
