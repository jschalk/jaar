from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import count_dirs_files, open_json, save_json
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch09_belief_lesson._ref.ch09_path import (
    create_moment_beliefs_dir_path,
    create_moment_json_path,
)
from src.ch10_bud._ref.ch10_path import create_beliefspark_path
from src.ch15_moment._ref.ch15_path import (
    create_bud_voice_mandate_ledger_path as bud_mandate_path,
)
from src.ch15_moment.moment_main import get_momentunit_from_dict, momentunit_shop
from src.ch15_moment.test._util.ch15_examples import example_casa_floor_clean_factunit
from src.ch18_world_etl._ref.ch18_path import create_moment_ote1_json_path
from src.ch20_world_logic.test._util.ch20_env import (
    get_temp_dir as worlds_dir,
    temp_dir_setup,
)
from src.ch20_world_logic.test._util.ch20_examples import (
    get_bob_mop_reason_beliefunit_example,
)
from src.ch20_world_logic.world import worldunit_shop


def test_WorldUnit_calc_moment_bud_voice_mandate_net_ledgers_Scenaro0_BudEmpty(
    temp_dir_setup,
):
    # ESTABLISH
    fay_world = worldunit_shop("Fay", worlds_dir())
    a23_str = "amy23"
    moment_mstr_dir = fay_world._moment_mstr_dir
    amy23_moment = momentunit_shop(a23_str, moment_mstr_dir)
    a23_json_path = create_moment_json_path(fay_world._moment_mstr_dir, a23_str)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    print(f"{a23_json_path=}")
    a23_beliefs_path = create_moment_beliefs_dir_path(
        fay_world._moment_mstr_dir, a23_str
    )
    assert count_dirs_files(a23_beliefs_path) == 0

    # WHEN
    fay_world.calc_moment_bud_voice_mandate_net_ledgers()

    # THEN
    assert count_dirs_files(a23_beliefs_path) == 0


def test_WorldUnit_calc_moment_bud_voice_mandate_net_ledgers_Scenaro1_SimpleBud(
    temp_dir_setup,
):
    # ESTABLISH
    fay_world = worldunit_shop("Fay", worlds_dir())
    mstr_dir = fay_world._moment_mstr_dir
    a23_str = "amy23"
    amy23_moment = momentunit_shop(a23_str, mstr_dir)
    bob_str = "Bob"
    tp37 = 37
    bud1_quota = 450
    x_celldepth = 2
    amy23_moment.add_budunit(bob_str, tp37, bud1_quota, celldepth=x_celldepth)
    a23_json_path = create_moment_json_path(mstr_dir, a23_str)
    save_json(a23_json_path, None, amy23_moment.to_dict())
    # Create empty ote1 file
    a23_ote1_json_path = create_moment_ote1_json_path(mstr_dir, a23_str)
    save_json(a23_ote1_json_path, None, {})
    bob37_bud_mandate_path = bud_mandate_path(mstr_dir, a23_str, bob_str, tp37)
    assert os_path_exists(bob37_bud_mandate_path) is False

    # WHEN
    fay_world.calc_moment_bud_voice_mandate_net_ledgers()

    # THEN
    assert os_path_exists(bob37_bud_mandate_path)
    expected_bud_voice_nets = {bob_str: bud1_quota}
    assert open_json(bob37_bud_mandate_path) == expected_bud_voice_nets
    gen_a23_momentunit = get_momentunit_from_dict(open_json(a23_json_path))
    gen_bob37_budunit = gen_a23_momentunit.get_budunit(bob_str, tp37)
    assert gen_bob37_budunit._bud_voice_nets == expected_bud_voice_nets


def test_WorldUnit_calc_moment_bud_voice_mandate_net_ledgers_Scenaro2_BudExists(
    temp_dir_setup,
):
    # ESTABLISH
    fay_world = worldunit_shop("Fay", worlds_dir())
    mstr_dir = fay_world._moment_mstr_dir
    a23_str = "amy23"

    # Create MomentUnit with bob bud at time 37
    amy23_moment = momentunit_shop(a23_str, mstr_dir)
    a23_str = "amy23"
    sue_str = "Sue"
    bob_str = "Bob"
    yao_str = "Yao"
    zia_str = "Zia"
    tp37 = 37
    bud1_quota = 450
    x_celldepth = 2
    amy23_moment.add_budunit(bob_str, tp37, bud1_quota, celldepth=x_celldepth)
    a23_json_path = create_moment_json_path(mstr_dir, a23_str)
    save_json(a23_json_path, None, amy23_moment.to_dict())

    # Create spark time mapping belief_time_agg for time 37
    spark33 = 33
    spark44 = 44
    spark55 = 55
    bob55_beliefspark = get_bob_mop_reason_beliefunit_example()
    bob55_beliefspark.add_voiceunit(sue_str, 1)
    sue44_beliefspark = beliefunit_shop(sue_str, a23_str)
    sue44_beliefspark.set_belief_name(sue_str)
    sue44_beliefspark.add_voiceunit(yao_str, 1)
    yao44_beliefspark = get_bob_mop_reason_beliefunit_example()
    yao44_beliefspark.set_belief_name(yao_str)
    yao44_beliefspark.add_voiceunit(zia_str, 1)
    clean_fact = example_casa_floor_clean_factunit()
    yao44_beliefspark.add_fact(clean_fact.fact_context, clean_fact.fact_state)
    zia33_beliefspark = get_bob_mop_reason_beliefunit_example()
    zia33_beliefspark.set_belief_name(zia_str)
    bob55_path = create_beliefspark_path(mstr_dir, a23_str, bob_str, spark55)
    sue44_path = create_beliefspark_path(mstr_dir, a23_str, sue_str, spark44)
    yao44_path = create_beliefspark_path(mstr_dir, a23_str, yao_str, spark44)
    zia33_path = create_beliefspark_path(mstr_dir, a23_str, zia_str, spark33)
    save_json(bob55_path, None, bob55_beliefspark.to_dict())
    save_json(sue44_path, None, sue44_beliefspark.to_dict())
    save_json(yao44_path, None, yao44_beliefspark.to_dict())
    save_json(zia33_path, None, zia33_beliefspark.to_dict())

    # Create empty ote1 file
    a23_ote1_dict = {
        bob_str: {str(tp37): spark55},
        sue_str: {str(tp37): spark44},
        yao_str: {str(tp37): spark44},
        zia_str: {str(tp37): spark33},
    }
    a23_ote1_json_path = create_moment_ote1_json_path(mstr_dir, a23_str)
    save_json(a23_ote1_json_path, None, a23_ote1_dict)

    # create result bud_voice_mandate_ledger file
    bob37_bud_mandate_path = bud_mandate_path(mstr_dir, a23_str, bob_str, tp37)
    assert os_path_exists(bob37_bud_mandate_path) is False

    # WHEN
    fay_world.calc_moment_bud_voice_mandate_net_ledgers()

    # THEN
    assert os_path_exists(bob37_bud_mandate_path)
    expected_bud_voice_nets = {zia_str: bud1_quota}
    assert open_json(bob37_bud_mandate_path) == expected_bud_voice_nets
    gen_a23_momentunit = get_momentunit_from_dict(open_json(a23_json_path))
    gen_bob37_budunit = gen_a23_momentunit.get_budunit(bob_str, tp37)
    assert gen_bob37_budunit._bud_voice_nets == expected_bud_voice_nets
