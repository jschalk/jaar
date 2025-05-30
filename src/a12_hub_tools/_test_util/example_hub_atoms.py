from src.a01_way_logic.way import (
    WayTerm,
    create_way,
    FiscLabel,
    get_default_fisc_label,
    create_way_from_labels,
)
from src.a02_finance_logic.deal import dealunit_shop, DealUnit
from src.a06_bud_logic._test_util.a06_str import (
    budunit_str,
    bud_acctunit_str,
    bud_conceptunit_str,
    bud_concept_factunit_str,
    acct_name_str,
    concept_way_str,
    fcontext_str,
    fopen_str,
    fnigh_str,
)
from src.a08_bud_atom_logic._test_util.a08_str import (
    INSERT_str,
    UPDATE_str,
    DELETE_str,
)
from src.a08_bud_atom_logic.atom import budatom_shop, BudAtom
from src.a09_pack_logic.pack import PackUnit, packunit_shop
from src.a09_pack_logic.delta import buddelta_shop, BudDelta
from src.a12_hub_tools.hubunit import HubUnit, hubunit_shop
from src.a12_hub_tools._test_util.a12_env import get_module_temp_dir


def get_atom_example_conceptunit_sports(fisc_label: FiscLabel = None) -> BudAtom:
    if not fisc_label:
        fisc_label = "accord23"
    sports_str = "sports"
    x_dimen = bud_conceptunit_str()
    sports_way = create_way(fisc_label, sports_str)
    insert_conceptunit_budatom = budatom_shop(x_dimen, INSERT_str())
    insert_conceptunit_budatom.set_jkey(concept_way_str(), sports_way)
    return insert_conceptunit_budatom


def get_atom_example_conceptunit_ball(fisc_label: FiscLabel = None) -> BudAtom:
    if not fisc_label:
        fisc_label = "accord23"
    sports_str = "sports"
    sports_way = create_way(fisc_label, sports_str)
    ball_str = "basketball"
    x_dimen = bud_conceptunit_str()
    bball_way = create_way(sports_way, ball_str)
    insert_conceptunit_budatom = budatom_shop(x_dimen, INSERT_str())
    insert_conceptunit_budatom.set_jkey(concept_way_str(), bball_way)
    return insert_conceptunit_budatom


def get_atom_example_conceptunit_knee(fisc_label: FiscLabel = None) -> BudAtom:
    if not fisc_label:
        fisc_label = "accord23"
    sports_str = "sports"
    sports_way = create_way(fisc_label, sports_str)
    knee_str = "knee"
    knee_begin = 1
    knee_close = 71
    x_dimen = bud_conceptunit_str()
    begin_str = "begin"
    close_str = "close"
    knee_way = create_way(sports_way, knee_str)
    insert_conceptunit_budatom = budatom_shop(x_dimen, INSERT_str())
    insert_conceptunit_budatom.set_jkey(concept_way_str(), knee_way)
    insert_conceptunit_budatom.set_jvalue(begin_str, knee_begin)
    insert_conceptunit_budatom.set_jvalue(close_str, knee_close)
    return insert_conceptunit_budatom


def get_atom_example_factunit_knee(fisc_label: FiscLabel = None) -> BudAtom:
    if not fisc_label:
        fisc_label = "accord23"
    sports_str = "sports"
    sports_way = create_way(fisc_label, sports_str)
    ball_str = "basketball"
    ball_way = create_way(sports_way, ball_str)
    knee_str = "knee"
    knee_way = create_way(fisc_label, knee_str)
    knee_fopen = 7
    knee_fnigh = 23
    x_dimen = bud_concept_factunit_str()
    insert_factunit_budatom = budatom_shop(x_dimen, INSERT_str())
    insert_factunit_budatom.set_jkey(concept_way_str(), ball_way)
    insert_factunit_budatom.set_jkey(fcontext_str(), knee_way)
    insert_factunit_budatom.set_jvalue(fopen_str(), knee_fopen)
    insert_factunit_budatom.set_jvalue(fnigh_str(), knee_fnigh)
    return insert_factunit_budatom


def get_buddelta_sue_example() -> BudDelta:
    sue_buddelta = buddelta_shop()

    pool_budatom = budatom_shop(budunit_str(), UPDATE_str())
    pool_attribute = "credor_respect"
    pool_budatom.set_jvalue(pool_attribute, 77)
    sue_buddelta.set_budatom(pool_budatom)

    dimen = bud_acctunit_str()
    sue_str = "Sue"
    sue_budatom = budatom_shop(dimen, DELETE_str())
    sue_budatom.set_jkey(acct_name_str(), sue_str)
    sue_buddelta.set_budatom(sue_budatom)
    return sue_buddelta


def get_texas_way() -> WayTerm:
    fisc_label = get_default_fisc_label()
    nation_str = "nation"
    usa_str = "USA"
    texas_str = "Texas"
    return create_way_from_labels([fisc_label, nation_str, usa_str, texas_str])


def get_texas_hubunit() -> HubUnit:
    fisc_label = get_default_fisc_label()
    return hubunit_shop(
        get_module_temp_dir(),
        fisc_label,
        owner_name="Sue",
        keep_way=get_texas_way(),
        # pipeline_duty_plan_str(),
    )


def get_sue_packunit() -> PackUnit:
    return packunit_shop(owner_name="Sue", _pack_id=37, face_name="Yao")


def sue_1budatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=53, face_name="Yao")
    x_packunit._buddelta.set_budatom(get_atom_example_conceptunit_sports())
    return x_packunit


def sue_2budatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=53, face_name="Yao")
    x_packunit._buddelta.set_budatom(get_atom_example_conceptunit_knee())
    x_packunit._buddelta.set_budatom(get_atom_example_conceptunit_sports())
    return x_packunit


def sue_3budatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=37, face_name="Yao")
    x_packunit._buddelta.set_budatom(get_atom_example_factunit_knee())
    x_packunit._buddelta.set_budatom(get_atom_example_conceptunit_ball())
    x_packunit._buddelta.set_budatom(get_atom_example_conceptunit_knee())
    return x_packunit


def sue_4budatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=47, face_name="Yao")
    x_packunit._buddelta.set_budatom(get_atom_example_factunit_knee())
    x_packunit._buddelta.set_budatom(get_atom_example_conceptunit_ball())
    x_packunit._buddelta.set_budatom(get_atom_example_conceptunit_knee())
    x_packunit._buddelta.set_budatom(get_atom_example_conceptunit_sports())
    return x_packunit


def get_dealunit_55_example() -> DealUnit:
    x_deal_time = 55
    return dealunit_shop(x_deal_time)


def get_dealunit_66_example() -> DealUnit:
    t66_deal_time = 66
    t66_dealunit = dealunit_shop(t66_deal_time)
    t66_dealunit.set_deal_acct_net("Sue", -5)
    t66_dealunit.set_deal_acct_net("Bob", 5)
    return t66_dealunit


def get_dealunit_88_example() -> DealUnit:
    t88_deal_time = 88
    t88_dealunit = dealunit_shop(t88_deal_time)
    t88_dealunit.quota = 800
    return t88_dealunit


def get_dealunit_invalid_example() -> DealUnit:
    t55_deal_time = 55
    t55_dealunit = dealunit_shop(t55_deal_time)
    t55_dealunit.set_deal_acct_net("Sue", -5)
    t55_dealunit.set_deal_acct_net("Bob", 3)
    return t55_dealunit
