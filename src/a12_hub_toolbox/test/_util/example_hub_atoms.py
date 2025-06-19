from src.a01_term_logic.rope import RopeTerm, create_rope, create_rope_from_labels
from src.a01_term_logic.term import VowLabel
from src.a02_finance_logic.bud import BudUnit, budunit_shop
from src.a05_concept_logic.concept import get_default_vow_label
from src.a06_plan_logic.test._util.a06_str import (
    acct_name_str,
    concept_rope_str,
    fcontext_str,
    fnigh_str,
    fopen_str,
    plan_acctunit_str,
    plan_concept_factunit_str,
    plan_conceptunit_str,
    planunit_str,
)
from src.a08_plan_atom_logic.atom import PlanAtom, planatom_shop
from src.a08_plan_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import PlanDelta, plandelta_shop
from src.a09_pack_logic.pack import PackUnit, packunit_shop
from src.a12_hub_toolbox.hubunit import HubUnit, hubunit_shop
from src.a12_hub_toolbox.test._util.a12_env import get_module_temp_dir


def get_atom_example_conceptunit_sports(vow_label: VowLabel = None) -> PlanAtom:
    if not vow_label:
        vow_label = "accord23"
    sports_str = "sports"
    x_dimen = plan_conceptunit_str()
    sports_rope = create_rope(vow_label, sports_str)
    insert_conceptunit_planatom = planatom_shop(x_dimen, INSERT_str())
    insert_conceptunit_planatom.set_jkey(concept_rope_str(), sports_rope)
    return insert_conceptunit_planatom


def get_atom_example_conceptunit_ball(vow_label: VowLabel = None) -> PlanAtom:
    if not vow_label:
        vow_label = "accord23"
    sports_str = "sports"
    sports_rope = create_rope(vow_label, sports_str)
    ball_str = "basketball"
    x_dimen = plan_conceptunit_str()
    bball_rope = create_rope(sports_rope, ball_str)
    insert_conceptunit_planatom = planatom_shop(x_dimen, INSERT_str())
    insert_conceptunit_planatom.set_jkey(concept_rope_str(), bball_rope)
    return insert_conceptunit_planatom


def get_atom_example_conceptunit_knee(vow_label: VowLabel = None) -> PlanAtom:
    if not vow_label:
        vow_label = "accord23"
    sports_str = "sports"
    sports_rope = create_rope(vow_label, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_dimen = plan_conceptunit_str()
    begin_str = "begin"
    close_str = "close"
    knee_rope = create_rope(sports_rope, knee_str)
    insert_conceptunit_planatom = planatom_shop(x_dimen, INSERT_str())
    insert_conceptunit_planatom.set_jkey(concept_rope_str(), knee_rope)
    insert_conceptunit_planatom.set_jvalue(begin_str, knee_begin)
    insert_conceptunit_planatom.set_jvalue(close_str, knee_close)
    return insert_conceptunit_planatom


def get_atom_example_factunit_knee(vow_label: VowLabel = None) -> PlanAtom:
    if not vow_label:
        vow_label = "accord23"
    sports_str = "sports"
    sports_rope = create_rope(vow_label, sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope(vow_label, knee_str)
    knee_fopen = 7
    knee_fnigh = 23
    x_dimen = plan_concept_factunit_str()
    insert_factunit_planatom = planatom_shop(x_dimen, INSERT_str())
    insert_factunit_planatom.set_jkey(concept_rope_str(), ball_rope)
    insert_factunit_planatom.set_jkey(fcontext_str(), knee_rope)
    insert_factunit_planatom.set_jvalue(fopen_str(), knee_fopen)
    insert_factunit_planatom.set_jvalue(fnigh_str(), knee_fnigh)
    return insert_factunit_planatom


def get_plandelta_sue_example() -> PlanDelta:
    sue_plandelta = plandelta_shop()

    pool_planatom = planatom_shop(planunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_planatom.set_jvalue(pool_attribute, 77)
    sue_plandelta.set_planatom(pool_planatom)

    dimen = plan_acctunit_str()
    sue_str = "Sue"
    sue_planatom = planatom_shop(dimen, DELETE_str())
    sue_planatom.set_jkey(acct_name_str(), sue_str)
    sue_plandelta.set_planatom(sue_planatom)
    return sue_plandelta


def get_texas_rope() -> RopeTerm:
    vow_label = get_default_vow_label()
    nation_str = "nation"
    usa_str = "USA"
    texas_str = "Texas"
    return create_rope_from_labels([vow_label, nation_str, usa_str, texas_str])


def get_texas_hubunit() -> HubUnit:
    vow_label = get_default_vow_label()
    return hubunit_shop(
        get_module_temp_dir(),
        vow_label,
        owner_name="Sue",
        keep_rope=get_texas_rope(),
        # pipeline_duty_vision_str(),
    )


def get_sue_packunit() -> PackUnit:
    return packunit_shop(owner_name="Sue", _pack_id=37, face_name="Yao")


def sue_1planatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=53, face_name="Yao")
    x_packunit._plandelta.set_planatom(get_atom_example_conceptunit_sports())
    return x_packunit


def sue_2planatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=53, face_name="Yao")
    x_packunit._plandelta.set_planatom(get_atom_example_conceptunit_knee())
    x_packunit._plandelta.set_planatom(get_atom_example_conceptunit_sports())
    return x_packunit


def sue_3planatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=37, face_name="Yao")
    x_packunit._plandelta.set_planatom(get_atom_example_factunit_knee())
    x_packunit._plandelta.set_planatom(get_atom_example_conceptunit_ball())
    x_packunit._plandelta.set_planatom(get_atom_example_conceptunit_knee())
    return x_packunit


def sue_4planatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=47, face_name="Yao")
    x_packunit._plandelta.set_planatom(get_atom_example_factunit_knee())
    x_packunit._plandelta.set_planatom(get_atom_example_conceptunit_ball())
    x_packunit._plandelta.set_planatom(get_atom_example_conceptunit_knee())
    x_packunit._plandelta.set_planatom(get_atom_example_conceptunit_sports())
    return x_packunit


def get_budunit_55_example() -> BudUnit:
    x_bud_time = 55
    return budunit_shop(x_bud_time)


def get_budunit_66_example() -> BudUnit:
    t66_bud_time = 66
    t66_budunit = budunit_shop(t66_bud_time)
    t66_budunit.set_bud_acct_net("Sue", -5)
    t66_budunit.set_bud_acct_net("Bob", 5)
    return t66_budunit


def get_budunit_88_example() -> BudUnit:
    t88_bud_time = 88
    t88_budunit = budunit_shop(t88_bud_time)
    t88_budunit.quota = 800
    return t88_budunit


def get_budunit_invalid_example() -> BudUnit:
    t55_bud_time = 55
    t55_budunit = budunit_shop(t55_bud_time)
    t55_budunit.set_bud_acct_net("Sue", -5)
    t55_budunit.set_bud_acct_net("Bob", 3)
    return t55_budunit
