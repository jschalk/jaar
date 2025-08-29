from src.a01_term_logic.rope import RopeTerm, create_rope, create_rope_from_labels
from src.a01_term_logic.term import MomentLabel
from src.a05_plan_logic.plan import get_default_moment_label
from src.a06_belief_logic.test._util.a06_str import (
    belief_plan_factunit_str,
    belief_planunit_str,
    belief_voiceunit_str,
    beliefunit_str,
    fact_context_str,
    fact_lower_str,
    fact_upper_str,
    plan_rope_str,
    voice_name_str,
)
from src.a08_belief_atom_logic.atom_main import BeliefAtom, beliefatom_shop
from src.a08_belief_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import BeliefDelta, beliefdelta_shop
from src.a09_pack_logic.pack import PackUnit, packunit_shop
from src.a11_bud_logic.bud import BudUnit, budunit_shop
from src.a12_hub_toolbox.hubunit import HubUnit, hubunit_shop
from src.a12_hub_toolbox.test._util.a12_env import get_module_temp_dir


def get_atom_example_planunit_sports(moment_label: MomentLabel = None) -> BeliefAtom:
    if not moment_label:
        moment_label = "amy23"
    sports_str = "sports"
    x_dimen = belief_planunit_str()
    sports_rope = create_rope(moment_label, sports_str)
    insert_planunit_beliefatom = beliefatom_shop(x_dimen, INSERT_str())
    insert_planunit_beliefatom.set_jkey(plan_rope_str(), sports_rope)
    return insert_planunit_beliefatom


def get_atom_example_planunit_ball(moment_label: MomentLabel = None) -> BeliefAtom:
    if not moment_label:
        moment_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(moment_label, sports_str)
    ball_str = "basketball"
    x_dimen = belief_planunit_str()
    bball_rope = create_rope(sports_rope, ball_str)
    insert_planunit_beliefatom = beliefatom_shop(x_dimen, INSERT_str())
    insert_planunit_beliefatom.set_jkey(plan_rope_str(), bball_rope)
    return insert_planunit_beliefatom


def get_atom_example_planunit_knee(moment_label: MomentLabel = None) -> BeliefAtom:
    if not moment_label:
        moment_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(moment_label, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_dimen = belief_planunit_str()
    begin_str = "begin"
    close_str = "close"
    knee_rope = create_rope(sports_rope, knee_str)
    insert_planunit_beliefatom = beliefatom_shop(x_dimen, INSERT_str())
    insert_planunit_beliefatom.set_jkey(plan_rope_str(), knee_rope)
    insert_planunit_beliefatom.set_jvalue(begin_str, knee_begin)
    insert_planunit_beliefatom.set_jvalue(close_str, knee_close)
    return insert_planunit_beliefatom


def get_atom_example_factunit_knee(moment_label: MomentLabel = None) -> BeliefAtom:
    if not moment_label:
        moment_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(moment_label, sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope(moment_label, knee_str)
    knee_fact_lower = 7
    knee_fact_upper = 23
    x_dimen = belief_plan_factunit_str()
    insert_factunit_beliefatom = beliefatom_shop(x_dimen, INSERT_str())
    insert_factunit_beliefatom.set_jkey(plan_rope_str(), ball_rope)
    insert_factunit_beliefatom.set_jkey(fact_context_str(), knee_rope)
    insert_factunit_beliefatom.set_jvalue(fact_lower_str(), knee_fact_lower)
    insert_factunit_beliefatom.set_jvalue(fact_upper_str(), knee_fact_upper)
    return insert_factunit_beliefatom


def get_beliefdelta_sue_example() -> BeliefDelta:
    sue_beliefdelta = beliefdelta_shop()

    pool_beliefatom = beliefatom_shop(beliefunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_beliefatom.set_jvalue(pool_attribute, 77)
    sue_beliefdelta.set_beliefatom(pool_beliefatom)

    dimen = belief_voiceunit_str()
    sue_str = "Sue"
    sue_beliefatom = beliefatom_shop(dimen, DELETE_str())
    sue_beliefatom.set_jkey(voice_name_str(), sue_str)
    sue_beliefdelta.set_beliefatom(sue_beliefatom)
    return sue_beliefdelta


def get_texas_rope() -> RopeTerm:
    moment_label = get_default_moment_label()
    nation_str = "nation"
    usa_str = "USA"
    texas_str = "Texas"
    return create_rope_from_labels([moment_label, nation_str, usa_str, texas_str])


def get_texas_hubunit() -> HubUnit:
    moment_label = get_default_moment_label()
    return hubunit_shop(
        get_module_temp_dir(),
        moment_label,
        belief_name="Sue",
        keep_rope=get_texas_rope(),
        # pipeline_duty_vision_str(),
    )


def get_sue_packunit() -> PackUnit:
    return packunit_shop(belief_name="Sue", _pack_id=37, face_name="Yao")


def sue_1beliefatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(belief_name="Sue", _pack_id=53, face_name="Yao")
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_planunit_sports())
    return x_packunit


def sue_2beliefatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(belief_name="Sue", _pack_id=53, face_name="Yao")
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_planunit_knee())
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_planunit_sports())
    return x_packunit


def sue_3beliefatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(belief_name="Sue", _pack_id=37, face_name="Yao")
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_factunit_knee())
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_planunit_ball())
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_planunit_knee())
    return x_packunit


def sue_4beliefatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(belief_name="Sue", _pack_id=47, face_name="Yao")
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_factunit_knee())
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_planunit_ball())
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_planunit_knee())
    x_packunit._beliefdelta.set_beliefatom(get_atom_example_planunit_sports())
    return x_packunit


def get_budunit_55_example() -> BudUnit:
    x_bud_time = 55
    return budunit_shop(x_bud_time)


def get_budunit_66_example() -> BudUnit:
    t66_bud_time = 66
    t66_budunit = budunit_shop(t66_bud_time)
    t66_budunit.set_bud_voice_net("Sue", -5)
    t66_budunit.set_bud_voice_net("Bob", 5)
    return t66_budunit


def get_budunit_88_example() -> BudUnit:
    t88_bud_time = 88
    t88_budunit = budunit_shop(t88_bud_time)
    t88_budunit.quota = 800
    return t88_budunit


def get_budunit_invalid_example() -> BudUnit:
    t55_bud_time = 55
    t55_budunit = budunit_shop(t55_bud_time)
    t55_budunit.set_bud_voice_net("Sue", -5)
    t55_budunit.set_bud_voice_net("Bob", 3)
    return t55_budunit
