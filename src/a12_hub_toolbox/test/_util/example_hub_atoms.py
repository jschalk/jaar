from src.a01_term_logic.rope import RopeTerm, create_rope, create_rope_from_labels
from src.a01_term_logic.term import BeliefLabel
from src.a05_plan_logic.plan import get_default_belief_label
from src.a06_owner_logic.test._util.a06_str import (
    acct_name_str,
    fcontext_str,
    fnigh_str,
    fopen_str,
    owner_acctunit_str,
    owner_plan_factunit_str,
    owner_planunit_str,
    ownerunit_str,
    plan_rope_str,
)
from src.a08_owner_atom_logic.atom import OwnerAtom, owneratom_shop
from src.a08_owner_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import OwnerDelta, ownerdelta_shop
from src.a09_pack_logic.pack import PackUnit, packunit_shop
from src.a11_bud_logic.bud import BudUnit, budunit_shop
from src.a12_hub_toolbox.hubunit import HubUnit, hubunit_shop
from src.a12_hub_toolbox.test._util.a12_env import get_module_temp_dir


def get_atom_example_planunit_sports(belief_label: BeliefLabel = None) -> OwnerAtom:
    if not belief_label:
        belief_label = "amy23"
    sports_str = "sports"
    x_dimen = owner_planunit_str()
    sports_rope = create_rope(belief_label, sports_str)
    insert_planunit_owneratom = owneratom_shop(x_dimen, INSERT_str())
    insert_planunit_owneratom.set_jkey(plan_rope_str(), sports_rope)
    return insert_planunit_owneratom


def get_atom_example_planunit_ball(belief_label: BeliefLabel = None) -> OwnerAtom:
    if not belief_label:
        belief_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(belief_label, sports_str)
    ball_str = "basketball"
    x_dimen = owner_planunit_str()
    bball_rope = create_rope(sports_rope, ball_str)
    insert_planunit_owneratom = owneratom_shop(x_dimen, INSERT_str())
    insert_planunit_owneratom.set_jkey(plan_rope_str(), bball_rope)
    return insert_planunit_owneratom


def get_atom_example_planunit_knee(belief_label: BeliefLabel = None) -> OwnerAtom:
    if not belief_label:
        belief_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(belief_label, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_dimen = owner_planunit_str()
    begin_str = "begin"
    close_str = "close"
    knee_rope = create_rope(sports_rope, knee_str)
    insert_planunit_owneratom = owneratom_shop(x_dimen, INSERT_str())
    insert_planunit_owneratom.set_jkey(plan_rope_str(), knee_rope)
    insert_planunit_owneratom.set_jvalue(begin_str, knee_begin)
    insert_planunit_owneratom.set_jvalue(close_str, knee_close)
    return insert_planunit_owneratom


def get_atom_example_factunit_knee(belief_label: BeliefLabel = None) -> OwnerAtom:
    if not belief_label:
        belief_label = "amy23"
    sports_str = "sports"
    sports_rope = create_rope(belief_label, sports_str)
    ball_str = "basketball"
    ball_rope = create_rope(sports_rope, ball_str)
    knee_str = "knee"
    knee_rope = create_rope(belief_label, knee_str)
    knee_fopen = 7
    knee_fnigh = 23
    x_dimen = owner_plan_factunit_str()
    insert_factunit_owneratom = owneratom_shop(x_dimen, INSERT_str())
    insert_factunit_owneratom.set_jkey(plan_rope_str(), ball_rope)
    insert_factunit_owneratom.set_jkey(fcontext_str(), knee_rope)
    insert_factunit_owneratom.set_jvalue(fopen_str(), knee_fopen)
    insert_factunit_owneratom.set_jvalue(fnigh_str(), knee_fnigh)
    return insert_factunit_owneratom


def get_ownerdelta_sue_example() -> OwnerDelta:
    sue_ownerdelta = ownerdelta_shop()

    pool_owneratom = owneratom_shop(ownerunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_owneratom.set_jvalue(pool_attribute, 77)
    sue_ownerdelta.set_owneratom(pool_owneratom)

    dimen = owner_acctunit_str()
    sue_str = "Sue"
    sue_owneratom = owneratom_shop(dimen, DELETE_str())
    sue_owneratom.set_jkey(acct_name_str(), sue_str)
    sue_ownerdelta.set_owneratom(sue_owneratom)
    return sue_ownerdelta


def get_texas_rope() -> RopeTerm:
    belief_label = get_default_belief_label()
    nation_str = "nation"
    usa_str = "USA"
    texas_str = "Texas"
    return create_rope_from_labels([belief_label, nation_str, usa_str, texas_str])


def get_texas_hubunit() -> HubUnit:
    belief_label = get_default_belief_label()
    return hubunit_shop(
        get_module_temp_dir(),
        belief_label,
        owner_name="Sue",
        keep_rope=get_texas_rope(),
        # pipeline_duty_vision_str(),
    )


def get_sue_packunit() -> PackUnit:
    return packunit_shop(owner_name="Sue", _pack_id=37, face_name="Yao")


def sue_1owneratoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=53, face_name="Yao")
    x_packunit._ownerdelta.set_owneratom(get_atom_example_planunit_sports())
    return x_packunit


def sue_2owneratoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=53, face_name="Yao")
    x_packunit._ownerdelta.set_owneratom(get_atom_example_planunit_knee())
    x_packunit._ownerdelta.set_owneratom(get_atom_example_planunit_sports())
    return x_packunit


def sue_3owneratoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=37, face_name="Yao")
    x_packunit._ownerdelta.set_owneratom(get_atom_example_factunit_knee())
    x_packunit._ownerdelta.set_owneratom(get_atom_example_planunit_ball())
    x_packunit._ownerdelta.set_owneratom(get_atom_example_planunit_knee())
    return x_packunit


def sue_4owneratoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=47, face_name="Yao")
    x_packunit._ownerdelta.set_owneratom(get_atom_example_factunit_knee())
    x_packunit._ownerdelta.set_owneratom(get_atom_example_planunit_ball())
    x_packunit._ownerdelta.set_owneratom(get_atom_example_planunit_knee())
    x_packunit._ownerdelta.set_owneratom(get_atom_example_planunit_sports())
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
