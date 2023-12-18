from src.world.concern import create_cultureaddress, create_concernunit, create_urgeunit


def get_farm_concernunit():
    texas_cultureaddress = create_cultureaddress("Luca", "Texas")
    food_text = "food"
    good_text = "farm food"
    bad_text = "cheap food"
    farm_text = "cultivate"
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    return create_concernunit(
        cultureaddress=texas_cultureaddress,
        why=food_text,
        good=good_text,
        bad=bad_text,
        action=farm_text,
        positive=well_text,
        negative=poor_text,
    )


def get_farm_urgeunit():
    bob_text = "Bob"
    real_text = "Real Farmers"
    farm_urgeunit = create_urgeunit(
        get_farm_concernunit(), bob_text, actor_group=real_text
    )
    yao_text = "Yao"
    farm_urgeunit.add_actor_pid(yao_text)
    return farm_urgeunit