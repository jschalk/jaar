from src.world.pain import painunit_shop, healerlink_shop


def test_painunit_set_relative_weight_SetsCorrectly():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)
    assert fear_painunit._relative_weight is None

    # WHEN
    x_relative_weight = 0.45
    fear_painunit.set_relative_weight(x_relative_weight)

    # THEN
    assert fear_painunit._relative_weight == x_relative_weight


def test_painunit_set_person_importance_SetsCorrectly():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)
    assert fear_painunit._person_importance is None

    # WHEN
    x_person_importance = 0.45
    fear_painunit.set_person_importance(x_person_importance)

    # THEN
    assert fear_painunit._person_importance == x_person_importance


def test_painunit_set_healerlinks_weight_metrics_SetsCorrectly():
    # GIVEN
    fear_text = "fear"
    fear_painunit = painunit_shop(kind=fear_text)
    fear_painunit._person_importance = 0.25

    yao_text = "Yao"
    sue_text = "Sue"
    tim_text = "Tim"

    fear_painunit.set_healerlink(healerlink_shop(yao_text, weight=15))
    fear_painunit.set_healerlink(healerlink_shop(sue_text, weight=3))
    fear_painunit.set_healerlink(healerlink_shop(tim_text, weight=2))

    yao_healerlink = fear_painunit.get_healerlink(yao_text)
    sue_healerlink = fear_painunit.get_healerlink(sue_text)
    tim_healerlink = fear_painunit.get_healerlink(tim_text)
    assert yao_healerlink._relative_weight is None
    assert sue_healerlink._relative_weight is None
    assert tim_healerlink._relative_weight is None
    assert yao_healerlink._person_importance is None
    assert sue_healerlink._person_importance is None
    assert tim_healerlink._person_importance is None

    # WHEN
    fear_painunit.set_healerlinks_weight_metrics()

    # THEN
    assert yao_healerlink._relative_weight == 0.75
    assert sue_healerlink._relative_weight == 0.15
    assert tim_healerlink._relative_weight == 0.10
    assert yao_healerlink._person_importance == 0.1875
    assert sue_healerlink._person_importance == 0.0375
    assert tim_healerlink._person_importance == 0.025
