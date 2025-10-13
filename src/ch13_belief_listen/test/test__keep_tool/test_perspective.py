from src.ch02_rope.rope import create_rope, default_knot_if_None
from src.ch07_belief_logic.test._util.ch07_examples import get_beliefunit_with_4_levels
from src.ch12_pack_file.packfilehandler import packfilehandler_shop, save_job_file
from src.ch12_pack_file.test._util.ch12_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir as env_dir,
)
from src.ch13_belief_listen.keep_tool import (
    get_dw_perspective_belief,
    get_perspective_belief,
    rj_perspective_belief,
    save_vision_belief,
)


def test_get_perspective_belief_ReturnsBeliefWith_belief_nameSetToPackFileHandler_belief_name():
    # ESTABLISH
    bob_str = "Bob"
    bob_beliefunit = get_beliefunit_with_4_levels()
    bob_beliefunit.set_belief_name(bob_str)

    sue_str = "Sue"

    # WHEN
    perspective_beliefunit = get_perspective_belief(bob_beliefunit, sue_str)

    # THEN
    assert perspective_beliefunit.to_dict() != bob_beliefunit.to_dict()
    assert perspective_beliefunit.belief_name == sue_str
    perspective_beliefunit.set_belief_name(bob_str)
    assert perspective_beliefunit.to_dict() == bob_beliefunit.to_dict()


def test_get_dw_perspective_belief_ReturnsBeliefWith_belief_nameSetToPackFileHandler_belief_name(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_str = "Bob"
    a23_str = "amy23"
    bob_beliefunit = get_beliefunit_with_4_levels()
    bob_beliefunit.set_belief_name(bob_str)
    bob_packfilehandler = packfilehandler_shop(env_dir(), a23_str, bob_str)
    save_job_file(bob_packfilehandler.moment_mstr_dir, bob_beliefunit)
    sue_str = "Sue"

    # WHEN
    perspective_beliefunit = get_dw_perspective_belief(
        env_dir(), a23_str, bob_str, sue_str
    )

    # THEN
    assert perspective_beliefunit.belief_name == sue_str
    assert perspective_beliefunit.to_dict() != bob_beliefunit.to_dict()
    perspective_beliefunit.set_belief_name(bob_str)
    assert perspective_beliefunit.to_dict() == bob_beliefunit.to_dict()


def test_rj_perspective_belief_ReturnsBeliefWith_belief_nameSetToPackFileHandler_belief_name(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    nation_str = "nation"
    nation_rope = create_rope("amy23", nation_str)
    iowa_rope = create_rope(nation_rope, "Iowa")
    a23_str = "amy23"

    bob_str = "Bob"
    yao_str = "Yao"
    yao_beliefunit = get_beliefunit_with_4_levels()
    yao_beliefunit.set_belief_name(yao_str)

    save_vision_belief(
        moment_mstr_dir=env_dir(),
        moment_label=a23_str,
        healer_name=bob_str,
        keep_rope=iowa_rope,
        knot=default_knot_if_None(),
        x_belief=yao_beliefunit,
    )

    sue_str = "Sue"

    # WHEN
    perspective_beliefunit = rj_perspective_belief(
        moment_mstr_dir=env_dir(),
        moment_label=a23_str,
        keep_rope=iowa_rope,
        knot=default_knot_if_None(),
        healer_name=bob_str,
        speaker_id=yao_str,
        perspective_id=sue_str,
    )

    # THEN
    assert perspective_beliefunit.belief_name == sue_str
    assert perspective_beliefunit.to_dict() != yao_beliefunit.to_dict()
    perspective_beliefunit.set_belief_name(yao_str)
    assert perspective_beliefunit.to_dict() == yao_beliefunit.to_dict()
