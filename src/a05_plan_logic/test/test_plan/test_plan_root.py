from pytest import raises as pytest_raises
from src.a05_plan_logic.plan import (
    get_default_belief_label as root_label,
    planunit_shop,
)


def test_planunit_shop_With_root_TrueReturnsObj():
    # ESTABLISH / WHEN
    root_plan = planunit_shop(root=True)

    # THEN
    assert root_plan
    assert root_plan.root
    assert root_plan.plan_label == root_label()
    assert root_plan._kids == {}
    assert root_plan.root is True


def test_PlanUnit_set_plan_label_get_default_belief_label_DoesNotRaisesError():
    # ESTABLISH
    root_plan = planunit_shop(root=True)

    # WHEN
    root_plan.set_plan_label(plan_label=root_label())

    # THEN
    assert root_plan.plan_label == root_label()


def test_PlanUnit_set_plan_label_DoesNotRaisesError():
    # ESTABLISH
    el_paso_str = "El Paso"
    root_plan = planunit_shop(root=True, belief_label=el_paso_str)

    # WHEN
    root_plan.set_plan_label(plan_label=el_paso_str)

    # THEN
    assert root_plan.plan_label == el_paso_str


def test_PlanUnit_set_plan_label_DoesRaisesError():
    # ESTABLISH
    el_paso_str = "El Paso"
    root_plan = planunit_shop(root=True, belief_label=el_paso_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_str = "casa"
        root_plan.set_plan_label(plan_label=casa_str)
    exception_str = f"Cannot set a root Plan to string different than '{el_paso_str}'"
    assert str(excinfo.value) == exception_str


def test_PlanUnit_set_plan_label_RaisesErrorWhenbelief_label_IsNone():
    # ESTABLISH
    root_plan = planunit_shop(root=True)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_str = "casa"
        root_plan.set_plan_label(plan_label=casa_str)
    exception_str = f"Cannot set a root Plan to string different than '{root_label()}'"
    assert str(excinfo.value) == exception_str
