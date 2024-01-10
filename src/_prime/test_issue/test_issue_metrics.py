from src._prime.road import (
    get_default_economy_root_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src._prime.issue import (
    IssueUnit,
    issueunit_shop,
    create_issueunit,
    FactUnit,
    factunit_shop,
)
from pytest import raises as pytest_raises


def test_IssueUnit_is_meaningful_ReturnsCorrectBool():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)

    # WHEN / THEN
    assert len(cook_issue.factunits) == 0
    assert cook_issue.is_meaningful() == False

    # WHEN / THEN
    cheap_factunit = factunit_shop(create_road(cook_road, "cheap food"), -2)
    cook_issue.set_factunit(cheap_factunit)
    assert len(cook_issue.factunits) == 1
    assert cook_issue.is_meaningful() == False

    # WHEN / THEN
    farm_text = "farm fresh"
    farm_factunit = factunit_shop(create_road(cook_road, farm_text), 3)
    cook_issue.set_factunit(farm_factunit)
    assert len(cook_issue.factunits) == 2
    assert cook_issue.is_meaningful()

    # WHEN / THEN
    cook_issue.del_factunit(create_road(cook_road, farm_text))
    assert len(cook_issue.factunits) == 1
    assert cook_issue.is_meaningful() == False

    # WHEN / THEN
    plastic_factunit = factunit_shop(create_road(cook_road, "plastic pots"), -5)
    cook_issue.set_factunit(plastic_factunit)
    assert len(cook_issue.factunits) == 2
    assert cook_issue.is_meaningful() == False

    # WHEN / THEN
    metal_factunit = factunit_shop(create_road(cook_road, "metal pots"), 7)
    cook_issue.set_factunit(metal_factunit)
    assert len(cook_issue.factunits) == 3
    assert cook_issue.is_meaningful()


def test_IssueUnit_is_tribal_ReturnsCorrectBool():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)

    # WHEN / THEN
    assert cook_issue.is_tribal() == False

    # WHEN / THEN
    cheap_road = create_road(cook_road, "cheap food")
    cheap_factunit = factunit_shop(cheap_road, -2, love=77)
    cook_issue.set_factunit(cheap_factunit)
    assert cook_issue.is_tribal() == False

    # WHEN / THEN
    farm_text = "farm fresh"
    farm_road = create_road(cook_road, farm_text)
    farm_factunit = factunit_shop(farm_road, -2, love=-55)
    cook_issue.set_factunit(farm_factunit)
    assert cook_issue.is_tribal()

    # WHEN / THEN
    cook_issue.del_factunit(farm_road)
    assert len(cook_issue.factunits) == 1
    assert cook_issue.is_tribal() == False

    # WHEN / THEN
    plastic_road = create_road(cook_road, "plastic pots")
    plastic_factunit = factunit_shop(plastic_road, -2, love=99)
    cook_issue.set_factunit(plastic_factunit)
    assert len(cook_issue.factunits) == 2
    assert cook_issue.is_tribal() == False

    # WHEN / THEN
    metal_road = create_road(cook_road, "metal pots")
    metal_factunit = factunit_shop(metal_road, -2, love=-44)
    cook_issue.set_factunit(metal_factunit)
    assert len(cook_issue.factunits) == 3
    assert cook_issue.is_tribal()


def test_IssueUnit_is_dialectic_ReturnsCorrectBool_v1():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)

    # WHEN / THEN
    assert cook_issue.is_tribal() == False
    assert cook_issue.is_meaningful() == False
    assert cook_issue.is_dialectic() == False


def test_IssueUnit_is_dialectic_ReturnsCorrectBool_v2():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    warm_proc_road = create_road(cook_road, "warm processed food")
    cold_proc_road = create_road(cook_road, "cold processed food")
    warm_farm_road = create_road(cook_road, "warm farmed food")
    cold_farm_road = create_road(cook_road, "cold farmed food")
    cook_issue.set_factunit(factunit_shop(warm_proc_road, affect=44, love=-9))
    cook_issue.set_factunit(factunit_shop(cold_proc_road, affect=-5, love=-4))
    cook_issue.set_factunit(factunit_shop(warm_farm_road, affect=33, love=77))
    cook_issue.set_factunit(factunit_shop(cold_farm_road, affect=-7, love=88))
    assert len(cook_issue.factunits) == 4
    assert cook_issue.is_tribal()
    assert cook_issue.is_meaningful()
    assert cook_issue.is_dialectic()

    # WHEN / THEN
    cook_issue.del_factunit(cold_proc_road)
    assert len(cook_issue.factunits) == 3
    assert cook_issue.is_tribal()
    assert cook_issue.is_meaningful()
    assert cook_issue.is_dialectic() == False


def test_IssueUnit_set_metrics_SetsAttr_calc_is_meaningful_Correctly():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    assert cook_issue._calc_is_meaningful == False

    # WHEN
    cook_issue.set_metrics()
    # THEN
    assert cook_issue._calc_is_meaningful == False

    # GIVEN
    cheap_factunit = factunit_shop(create_road(cook_road, "cheap food"), -2)
    cook_issue.set_factunit(cheap_factunit, set_metrics=False)
    farm_text = "farm fresh"
    farm_factunit = factunit_shop(create_road(cook_road, farm_text), 3)
    cook_issue.set_factunit(farm_factunit, set_metrics=False)
    assert len(cook_issue.factunits) == 2
    assert cook_issue.is_meaningful()
    assert cook_issue._calc_is_meaningful == False

    # WHEN
    cook_issue.set_metrics()
    # THEN
    assert cook_issue._calc_is_meaningful


def test_IssueUnit_set_metrics_SetsAttr_calc_is_tribal_Correctly():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    assert cook_issue.is_tribal() == False
    # WHEN
    cook_issue.set_metrics()
    # THEN
    assert cook_issue.is_tribal() == False

    # WHEN / THEN
    cheap_road = create_road(cook_road, "cheap food")
    cheap_factunit = factunit_shop(cheap_road, -2, love=77)
    cook_issue.set_factunit(cheap_factunit, set_metrics=False)
    farm_text = "farm fresh"
    farm_road = create_road(cook_road, farm_text)
    farm_factunit = factunit_shop(farm_road, -2, love=-55)
    cook_issue.set_factunit(farm_factunit, set_metrics=False)
    assert cook_issue.is_tribal()
    assert cook_issue._calc_is_tribal == False
    # WHEN
    cook_issue.set_metrics()
    # THEN
    assert cook_issue._calc_is_tribal


def test_IssueUnit_set_metrics_SetsAttr_calc_is_dialectic_Correctly():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    warm_proc_road = create_road(cook_road, "warm processed food")
    cold_proc_road = create_road(cook_road, "cold processed food")
    warm_farm_road = create_road(cook_road, "warm farmed food")
    cold_farm_road = create_road(cook_road, "cold farmed food")
    warm_proc_factunit = factunit_shop(warm_proc_road, affect=44, love=-9)
    cold_proc_factunit = factunit_shop(cold_proc_road, affect=-5, love=-4)
    warm_farm_factunit = factunit_shop(warm_farm_road, affect=33, love=77)
    cold_farm_factunit = factunit_shop(cold_farm_road, affect=-7, love=88)
    cook_issue.set_factunit(warm_proc_factunit, set_metrics=False)
    cook_issue.set_factunit(cold_proc_factunit, set_metrics=False)
    cook_issue.set_factunit(warm_farm_factunit, set_metrics=False)
    cook_issue.set_factunit(cold_farm_factunit, set_metrics=False)
    assert len(cook_issue.factunits) == 4
    assert cook_issue.is_tribal()
    assert cook_issue.is_meaningful()
    assert cook_issue.is_dialectic()
    assert cook_issue._calc_is_tribal == False
    assert cook_issue._calc_is_meaningful == False
    assert cook_issue._calc_is_dialectic == False

    # WHEN
    cook_issue.set_metrics()
    # THEN
    assert cook_issue._calc_is_tribal
    assert cook_issue._calc_is_meaningful
    assert cook_issue._calc_is_dialectic

    # GIVEN
    cook_issue.del_factunit(cold_proc_road)
    assert len(cook_issue.factunits) == 3
    assert cook_issue.is_tribal()
    assert cook_issue.is_meaningful()
    assert cook_issue.is_dialectic() == False

    # WHEN
    cook_issue.set_metrics()
    # THEN
    assert cook_issue._calc_is_tribal
    assert cook_issue._calc_is_meaningful
    assert cook_issue._calc_is_dialectic == False

    # WHEN
    cook_issue.set_factunit(factunit_shop(cold_proc_road, affect=-5, love=-4))
    # THEN
    assert cook_issue._calc_is_tribal
    assert cook_issue._calc_is_meaningful
    assert cook_issue._calc_is_dialectic