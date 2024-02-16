from src._prime.road import default_road_delimiter_if_none
from src.world.world import WorldUnit, worldunit_shop
from src.world.examples.world_env_kit import (
    get_test_worlds_dir,
    worlds_dir_setup_cleanup,
)

from src.world.person import personunit_shop
from pytest import raises as pytest_raises


def test_WorldUnit_exists(worlds_dir_setup_cleanup):
    dallas_text = "dallas"
    dallas_world = WorldUnit(world_id=dallas_text, worlds_dir=get_test_worlds_dir())
    assert dallas_world.world_id == dallas_text
    assert dallas_world.worlds_dir == get_test_worlds_dir()
    assert dallas_world._persons_dir is None
    assert dallas_world._personunits is None
    assert dallas_world._deals_dir is None
    assert dallas_world._dealunits is None
    assert dallas_world._max_deal_uid is None
    assert dallas_world._road_delimiter is None


def test_worldunit_shop_ReturnsWorldUnit(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    dallas_world = worldunit_shop(
        world_id=dallas_text, worlds_dir=get_test_worlds_dir()
    )

    # THEN
    assert dallas_world.world_id == dallas_text
    assert dallas_world.worlds_dir == get_test_worlds_dir()
    assert dallas_world._persons_dir != None
    assert dallas_world._personunits == {}
    assert dallas_world._deals_dir != None
    assert dallas_world._dealunits == {}
    assert dallas_world._max_deal_uid == 0
    assert dallas_world._road_delimiter == default_road_delimiter_if_none()


def test_worldunit_shop_ReturnsWorldUnitWith_road_delimiter(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    slash_text = "/"

    # WHEN
    dallas_world = worldunit_shop(
        world_id=dallas_text,
        worlds_dir=get_test_worlds_dir(),
        _road_delimiter=slash_text,
    )

    # THEN
    assert dallas_world._road_delimiter == slash_text


def test_WorldUnit__set_world_dirs_SetsPersonDir(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    dallas_world = WorldUnit(world_id=dallas_text, worlds_dir=get_test_worlds_dir())
    assert dallas_world._persons_dir is None

    # WHEN
    dallas_world._set_world_dirs()

    # THEN
    assert dallas_world._world_dir == f"{get_test_worlds_dir()}/{dallas_text}"
    assert dallas_world._persons_dir == f"{get_test_worlds_dir()}/{dallas_text}/persons"
    assert dallas_world._deals_dir == f"{get_test_worlds_dir()}/{dallas_text}/deals"


def test_worldunit_shop_SetsWorldsDirs(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    dallas_world = worldunit_shop(
        world_id=dallas_text, worlds_dir=get_test_worlds_dir()
    )

    # THEN
    assert dallas_world.world_id == dallas_text
    assert dallas_world._world_dir == f"{get_test_worlds_dir()}/{dallas_text}"
    assert dallas_world._persons_dir == f"{dallas_world._world_dir}/persons"


def test_WorldUnit__set_person_in_memory_CorrectlySetsPerson(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    dallas_world = worldunit_shop(
        world_id=dallas_text, worlds_dir=get_test_worlds_dir()
    )
    assert dallas_world._personunits == {}

    # WHEN
    luca_text = "Luca"
    luca_person = personunit_shop(person_id=luca_text)
    dallas_world._set_person_in_memory(personunit=luca_person)

    # THEN
    assert dallas_world._personunits != {}
    assert len(dallas_world._personunits) == 1
    assert dallas_world._personunits[luca_text] == luca_person
    assert dallas_world._world_dir == f"{get_test_worlds_dir()}/{dallas_text}"
    assert dallas_world._persons_dir == f"{dallas_world._world_dir}/persons"


def test_WorldUnit_personunit_exists_ReturnsCorrectBool(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    dallas_world = worldunit_shop(
        world_id=dallas_text, worlds_dir=get_test_worlds_dir()
    )
    assert dallas_world._personunits == {}

    # WHEN / THEN
    luca_text = "Luca"
    assert dallas_world.personunit_exists(luca_text) == False

    # WHEN / THEN
    luca_person = personunit_shop(person_id=luca_text)
    dallas_world._set_person_in_memory(personunit=luca_person)
    assert dallas_world.personunit_exists(luca_text)


def test_WorldUnit_add_personunit_CorrectlySetsPerson(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    slash_text = "/"
    dallas_world = worldunit_shop(dallas_text, get_test_worlds_dir(), slash_text)
    luca_text = "Luca"
    luca_person_dir = f"{dallas_world._persons_dir}/{luca_text}"

    # WHEN
    dallas_world.add_personunit(luca_text)

    # THEN
    assert dallas_world._personunits[luca_text] != None
    print(f"{get_test_worlds_dir()=}")
    print(f"      {luca_person_dir=}")
    dallas_world_luca_dir = dallas_world._personunits[luca_text].person_dir
    print(f"     {dallas_world_luca_dir=}")
    assert dallas_world._personunits[luca_text].person_dir == luca_person_dir
    assert dallas_world._personunits[luca_text]._road_delimiter == slash_text
    luca_person_obj = personunit_shop(
        person_id=luca_text,
        world_id=dallas_text,
        worlds_dir=dallas_world.worlds_dir,
        _road_delimiter=slash_text,
    )
    assert dallas_world._personunits[luca_text].worlds_dir == luca_person_obj.worlds_dir
    assert dallas_world._personunits[luca_text].world_id == luca_person_obj.world_id
    assert dallas_world._personunits[luca_text] == luca_person_obj


def test_WorldUnit_add_personunit_RaisesErrorIfPersonExists(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    dallas_world = worldunit_shop(
        world_id=dallas_text, worlds_dir=get_test_worlds_dir()
    )
    luca_text = "Luca"
    luca_person_dir = f"{dallas_world._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(
        person_id=luca_text,
        world_id=dallas_text,
        worlds_dir=dallas_world.worlds_dir,
    )
    dallas_world.add_personunit(luca_text)
    assert dallas_world._personunits[luca_text] != None
    assert dallas_world._personunits[luca_text].person_dir == luca_person_dir
    assert dallas_world._personunits[luca_text] == luca_person_obj

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        dallas_world.add_personunit(luca_text)
    assert str(excinfo.value) == f"add_personunit fail: {luca_text} already exists"


def test_WorldUnit__set_person_in_memory_CorrectlyCreatesObj(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    dallas_world = worldunit_shop(
        world_id=dallas_text, worlds_dir=get_test_worlds_dir()
    )
    luca_text = "Luca"
    assert dallas_world.personunit_exists(luca_text) == False

    # WHEN
    luca_person_dir = f"{dallas_world._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(
        person_id=luca_text,
        world_id=dallas_world.world_id,
        worlds_dir=dallas_world.worlds_dir,
    )
    dallas_world._set_person_in_memory(luca_person_obj)

    # THEN
    assert dallas_world.personunit_exists(luca_text)
    assert dallas_world._personunits.get(luca_text).person_dir == luca_person_dir
    assert dallas_world._personunits.get(luca_text) == luca_person_obj


# def test_WorldUnit__set_person_in_memory_CorrectlyReplacesObj(worlds_dir_setup_cleanup):
#     # GIVEN
#     dallas_text = "dallas"
#     dallas_world = worldunit_shop(world_id=dallas_text, worlds_dir=get_test_worlds_dir())
#     luca_text = "Luca"
#     world.add_personunit(luca_text)
#     luca_person = world.get_personunit_from_memory(luca_text)
#     assert world.personunit_exists(luca_text)

#     # WHEN
#     luca_person_dir = f"{world._persons_dir}/{luca_text}"
#     world._set_person_in_memory(
#         personunit_shop(person_id=luca_text, worlds_dir=dallas_world._world_dir
#     )


def test_WorldUnit_get_personunit_from_memory_ReturnsPerson(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    dallas_text = "dallas"
    dallas_world = worldunit_shop(
        world_id=dallas_text, worlds_dir=get_test_worlds_dir()
    )
    luca_text = "Luca"
    luca_person_dir = f"{dallas_world._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(
        person_id=luca_text,
        world_id=dallas_world.world_id,
        worlds_dir=dallas_world.worlds_dir,
    )
    dallas_world.add_personunit(luca_text)

    # WHEN
    luca_gotten_obj = dallas_world.get_personunit_from_memory(luca_text)

    # THEN
    assert luca_gotten_obj != None
    assert luca_gotten_obj.person_dir == luca_person_dir
    assert luca_gotten_obj == luca_person_obj


def test_WorldUnit_get_personunit_from_memory_ReturnsNone(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    dallas_text = "dallas"
    dallas_world = worldunit_shop(
        world_id=dallas_text, worlds_dir=get_test_worlds_dir()
    )
    luca_text = "Luca"

    # WHEN
    luca_gotten_obj = dallas_world.get_personunit_from_memory(luca_text)

    # THEN
    assert luca_gotten_obj is None


def test_WorldUnit_get_person_gut_ReturnsCorrectObj(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    dallas_world = worldunit_shop(dallas_text, get_test_worlds_dir())
    luca_text = "Luca"
    dallas_world.add_personunit(luca_text)
    luca_person = dallas_world.get_personunit_from_memory(luca_text)
    bob_text = "Bob"
    luca_gut = luca_person.get_gut_file_agenda()
    luca_gut.add_partyunit(bob_text)
    luca_person._save_agenda_to_gut_path(luca_gut)

    # WHEN
    gen_luca_gut = dallas_world.get_person_gut(luca_text)

    # THEN
    assert gen_luca_gut != None
    assert gen_luca_gut.get_party(bob_text) != None