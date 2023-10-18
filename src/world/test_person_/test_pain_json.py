from src.world.pain import painunit_shop, fixlink_shop, healerlink_shop


def test_fixlink_get_dict_ReturnsCorrectDict():
    # GIVEN
    diet_text = "diet"
    diet_weight = 5
    diet_fixlink = fixlink_shop(handle=diet_text, weight=diet_weight)

    # WHEN
    diet_dict = diet_fixlink.get_dict()

    # THEN
    assert diet_dict == {"handle": diet_text, "weight": diet_weight}


def test_healerlink_get_dict_ReturnsCorrectDict():
    # GIVEN
    yao_text = "yao"
    yao_weight = 5
    yao_healerlink = healerlink_shop(person_name=yao_text, weight=yao_weight)
    diet_text = "diet"
    diet_weight = 7
    diet_fixlink = fixlink_shop(handle=diet_text, weight=diet_weight)
    yao_healerlink.set_fixlink(diet_fixlink)
    diet_fix = yao_healerlink.get_fixlink(diet_text)
    assert diet_fix != None
    assert diet_fix.handle == diet_text

    # WHEN
    yao_dict = yao_healerlink.get_dict()

    # THEN
    assert yao_dict == {
        "person_name": yao_text,
        "weight": yao_weight,
        "_fixlinks": {diet_text: {"handle": diet_text, "weight": diet_weight}},
    }


def test_painunit_get_dict_ReturnsCorrectDict():
    # GIVEN
    fear_text = "fear"
    fear_weight = 13
    fear_painunit = painunit_shop(genus=fear_text, weight=fear_weight)

    yao_text = "yao"
    yao_weight = 7
    yao_healerlink = healerlink_shop(person_name=yao_text, weight=yao_weight)

    diet_text = "diet"
    diet_weight = 3
    diet_fixlink = fixlink_shop(handle=diet_text, weight=diet_weight)
    yao_healerlink.set_fixlink(diet_fixlink)

    fear_painunit.set_healerlink(yao_healerlink)

    # WHEN
    fear_dict = fear_painunit.get_dict()

    # THEN
    print(f"{fear_dict.keys()=}")
    assert len(fear_dict) == 3
    x_healerlinks_dict = fear_dict.get("_healerlinks")
    print(f"{x_healerlinks_dict=}")
    assert len(x_healerlinks_dict) == 1
    yao_healerlink = x_healerlinks_dict.get(yao_text)
    yao_fixlinks_dict = yao_healerlink.get("_fixlinks")
    print(f"{yao_fixlinks_dict=}")
    assert len(yao_fixlinks_dict) == 1
    assert len(fear_dict.get("_healerlinks")) == 1
    assert fear_dict.get("genus") == fear_text
    diet_fixlink_dict = yao_fixlinks_dict.get(diet_text)
    assert diet_fixlink_dict == {"handle": diet_text, "weight": diet_weight}
    assert yao_fixlinks_dict == {
        diet_text: {"handle": diet_text, "weight": diet_weight}
    }

    assert x_healerlinks_dict == {
        yao_text: {
            "person_name": yao_text,
            "weight": yao_weight,
            "_fixlinks": {diet_text: {"handle": diet_text, "weight": diet_weight}},
        }
    }
    assert fear_dict == {
        "genus": fear_text,
        "weight": fear_weight,
        "_healerlinks": {
            yao_text: {
                "person_name": yao_text,
                "weight": yao_weight,
                "_fixlinks": {diet_text: {"handle": diet_text, "weight": diet_weight}},
            }
        },
    }
