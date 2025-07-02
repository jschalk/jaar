from pytest import raises as pytest_raises
from src.a05_plan_logic.plan import (
    get_default_belief_label as root_label,
    planunit_shop,
)


def test_planunit_shop_With_root_TrueReturnsObj():
    # ESTABLISH / WHEN
    x_planroot = planunit_shop(root=True)

    # THEN
    assert x_planroot
    assert x_planroot.root
    assert x_planroot.plan_label == root_label()
    assert x_planroot._kids == {}
    assert x_planroot.root is True


def test_PlanUnit_set_plan_label_get_default_belief_label_DoesNotRaisesError():
    # ESTABLISH
    x_planroot = planunit_shop(root=True)

    # WHEN
    x_planroot.set_plan_label(plan_label=root_label())

    # THEN
    assert x_planroot.plan_label == root_label()


def test_PlanUnit_set_plan_label_DoesNotRaisesError():
    # ESTABLISH
    el_paso_str = "El Paso"
    x_planroot = planunit_shop(root=True, belief_label=el_paso_str)

    # WHEN
    x_planroot.set_plan_label(plan_label=el_paso_str)

    # THEN
    assert x_planroot.plan_label == el_paso_str


def test_PlanUnit_set_plan_label_DoesRaisesError():
    # ESTABLISH
    el_paso_str = "El Paso"
    x_planroot = planunit_shop(root=True, belief_label=el_paso_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_str = "casa"
        x_planroot.set_plan_label(plan_label=casa_str)
    assert (
        str(excinfo.value)
        == f"Cannot set planroot to string different than '{el_paso_str}'"
    )


def test_PlanUnit_set_plan_label_RaisesErrorWhenbelief_label_IsNone():
    # ESTABLISH
    x_planroot = planunit_shop(root=True)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_str = "casa"
        x_planroot.set_plan_label(plan_label=casa_str)
    assert (
        str(excinfo.value)
        == f"Cannot set planroot to string different than '{root_label()}'"
    )
