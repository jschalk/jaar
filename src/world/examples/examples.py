from src.world.lobby import (
    create_economyaddress,
    create_concernunit,
    create_lobbyunit,
)


def get_farm_concernunit():
    texas_economyaddress = create_economyaddress("Luca", "Texas")
    food_text = "food"
    good_text = "farm food"
    bad_text = "cheap food"
    farm_text = "cultivate"
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    return create_concernunit(
        economyaddress=texas_economyaddress,
        when=food_text,
        good=good_text,
        bad=bad_text,
        action=farm_text,
        positive=well_text,
        negative=poor_text,
    )


def get_farm_lobbyunit():
    bob_text = "Bob"
    real_text = "Real Farmers"
    farm_lobbyunit = create_lobbyunit(
        get_farm_concernunit(), bob_text, lobbyee_group=real_text
    )
    yao_text = "Yao"
    farm_lobbyunit.add_lobbyee_pid(yao_text)
    return farm_lobbyunit
