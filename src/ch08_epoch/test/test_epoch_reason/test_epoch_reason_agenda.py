from src.ch07_belief_logic.belief_main import beliefunit_shop, get_sorted_plan_list
from src.ch07_belief_logic.belief_tool import (
    belief_plan_reason_caseunit_exists,
    belief_plan_reason_caseunit_get_obj,
    belief_plan_reason_caseunit_set_obj,
    belief_plan_reasonunit_exists,
    belief_plan_reasonunit_get_obj,
    get_belief_root_facts_dict,
    set_factunits_to_belief,
)
from src.ch08_epoch.epoch_main import add_epoch_planunit
from src.ch08_epoch.epoch_reason_builder import (
    set_epoch_base_case_dayly,
    set_epoch_cases_for_yearly_monthday,
)
from src.ch08_epoch.test._util.ch08_examples import (
    Ch08ExampleStrs as exx,
    get_five_config,
)
from src.ref.keywords import Ch08Keywords as wx


def test_set_epoch_base_case_dayly_ChangesBeliefUnit_agenda():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope, pledge=True)
    assert len(bob_belief.get_agenda_dict()) == 1
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    add_epoch_planunit(bob_belief, five_config)
    mop_day_lower_min = 600
    mop_day_duration = 90
    bob_belief.add_fact(exx.five_rope, exx.five_rope, 500, 500)
    assert len(bob_belief.get_agenda_dict()) == 1

    # WHEN
    set_epoch_base_case_dayly(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        lower_min=mop_day_lower_min,
        duration=mop_day_duration,
    )

    # THEN
    assert len(bob_belief.get_agenda_dict()) == 0
    # WHEN
    bob_belief.add_fact(exx.five_rope, exx.five_rope, 500, 1000)

    # THEN
    bob_belief.cashout()
    print(f"{bob_belief.planroot.factheirs.keys()=}")
    mop_plan = bob_belief.get_plan_obj(exx.mop_rope)
    day_factheir = mop_plan.factheirs.get(exx.day_rope)
    day_reasonheir = mop_plan.reasonheirs.get(exx.day_rope)
    day_heir_case = day_reasonheir.cases.get(exx.day_rope)
    print(f" {day_factheir=}")
    print(f"{day_heir_case=}")
    assert len(bob_belief.get_agenda_dict()) == 1


def test_set_epoch_cases_for_yearly_monthday_ChangesBeliefUnit_agenda():
    # ESTABLISH
    bob_belief = beliefunit_shop(exx.Bob)
    bob_belief.add_plan(exx.mop_rope, pledge=True)
    five_config = get_five_config()
    five_label = five_config.get(wx.epoch_label)
    add_epoch_planunit(bob_belief, five_config)
    month_geo_rope = bob_belief.make_rope(exx.five_year_rope, exx.Geo)
    mop_monthday = 3
    mop_length_days = 4
    mop_day_lower_min = 600
    mop_day_duration = 90
    bob_belief.add_fact(exx.five_rope, exx.five_rope, 400, 440)
    assert len(bob_belief.get_agenda_dict()) == 1

    # WHEN 1
    set_epoch_cases_for_yearly_monthday(
        x_belief=bob_belief,
        plan_rope=exx.mop_rope,
        epoch_label=five_label,
        lower_min=mop_day_lower_min,
        duration=mop_day_duration,
        month_label=exx.Geo,
        monthday=mop_monthday,
        length_days=mop_length_days,
    )

    # THEN 1
    assert len(bob_belief.get_agenda_dict()) == 0

    # WHEN 2
    bob_belief.add_fact(exx.five_rope, exx.five_rope, 400, 100000)

    # THEN 2
    print("epoch fact changed")
    bob_belief.cashout()
    mop_plan = bob_belief.get_plan_obj(exx.mop_rope)
    day_reasonheir = mop_plan.reasonheirs.get(exx.day_rope)
    day_caseunit = day_reasonheir.cases.get(exx.day_rope)
    day_factheir = mop_plan.factheirs.get(exx.day_rope)
    print(f"{day_factheir=}")
    print(f"{day_caseunit=}")
    assert len(bob_belief.get_agenda_dict()) == 1
    # geo_reasonheir = mop_plan.reasonheirs.get(month_geo_rope)
    # geo_factheir = mop_plan.factheirs.get(month_geo_rope)
    # print(f"{geo_factheir=}")
    # print(f"{day_reasonheir=}")
    # print(f"{geo_reasonheir.status=}")
    # print(f"{mop_plan.factheirs.keys()=}")
