from src._road.road import RoadUnit, create_road, get_default_real_id_roadnode, RoadNode
from src._world.idea import ideaunit_shop
from src._world.world import WorldUnit, worldunit_shop
from src.listen.hubunit import hubunit_shop, HubUnit
from src.listen.listen import listen_to_owner_jobs, create_job_file_from_duty_file
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
    get_texas_hubunit,
)


def casa_text() -> str:
    return "casa"


def cook_text() -> str:
    return "cook"


def eat_text() -> str:
    return "eat"


def hungry_text() -> str:
    return "hungry"


def full_text() -> str:
    return "full"


def sanitation_text():
    return "sanitation"


def clean_text():
    return "clean"


def dirty_text():
    return "dirty"


def sweep_text():
    return "sweep"


def run_text():
    return "run"


def casa_road() -> RoadUnit:
    return create_road(get_default_real_id_roadnode(), casa_text())


def cook_road() -> RoadUnit:
    return create_road(casa_road(), cook_text())


def eat_road() -> RoadUnit:
    return create_road(casa_road(), eat_text())


def hungry_road() -> RoadUnit:
    return create_road(eat_road(), hungry_text())


def full_road() -> RoadUnit:
    return create_road(eat_road(), full_text())


def sanitation_road() -> RoadUnit:
    return create_road(casa_road(), sanitation_text())


def clean_road() -> RoadUnit:
    return create_road(sanitation_road(), clean_text())


def dirty_road() -> RoadUnit:
    return create_road(sanitation_road(), dirty_text())


def sweep_road() -> RoadUnit:
    return create_road(casa_road(), sweep_text())


def run_road() -> RoadUnit:
    return create_road(casa_road(), run_text())


def get_example_yao_world() -> WorldUnit:
    yao_text = "Yao"
    zia_text = "Zia"
    bob_text = "Bob"
    yao_speaker = worldunit_shop(yao_text, get_default_real_id_roadnode())
    yao_speaker.add_idea(ideaunit_shop(run_text()), casa_road())
    yao_speaker.add_charunit(yao_text, debtor_weight=10)
    yao_speaker.add_charunit(zia_text, debtor_weight=30)
    yao_speaker.add_charunit(bob_text, debtor_weight=40)
    yao_speaker.set_char_pool(80)
    return yao_speaker


def get_example_yao_job1_speaker() -> WorldUnit:
    yao_text = "Yao"
    yao_speaker = get_example_yao_world()
    yao_speaker.del_idea_obj(run_road())
    yao_speaker.set_char_pool(40)
    yao_speaker.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    yao_speaker.add_idea(ideaunit_shop(hungry_text()), eat_road())
    yao_speaker.add_idea(ideaunit_shop(full_text()), eat_road())
    cook_ideaunit = yao_speaker.get_idea_obj(cook_road())
    cook_ideaunit._cultureunit.set_belieflink(yao_text)
    yao_speaker.edit_reason(cook_road(), eat_road(), hungry_road())
    yao_speaker.set_fact(eat_road(), hungry_road())
    return yao_speaker


def get_example_yao_job2_speaker() -> WorldUnit:
    yao_text = "Yao"
    yao_speaker = get_example_yao_world()
    yao_speaker.del_idea_obj(run_road())
    yao_speaker.set_char_pool(30)
    yao_speaker.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    yao_speaker.add_idea(ideaunit_shop(hungry_text()), eat_road())
    yao_speaker.add_idea(ideaunit_shop(full_text()), eat_road())
    cook_ideaunit = yao_speaker.get_idea_obj(cook_road())
    cook_ideaunit._cultureunit.set_belieflink(yao_text)
    yao_speaker.edit_reason(cook_road(), eat_road(), hungry_road())
    yao_speaker.set_fact(eat_road(), hungry_road())

    yao_speaker.add_idea(ideaunit_shop(sweep_text(), pledge=True), casa_road())
    yao_speaker.add_idea(ideaunit_shop(dirty_text()), sanitation_road())
    yao_speaker.add_idea(ideaunit_shop(clean_text()), sanitation_road())
    yao_speaker.edit_reason(sweep_road(), sanitation_road(), dirty_road())
    yao_speaker.set_fact(sweep_road(), dirty_road())
    return yao_speaker


def get_example_yao_job3_speaker() -> WorldUnit:
    yao_speaker = get_example_yao_world()
    yao_speaker.del_idea_obj(run_road())
    yao_speaker.set_char_pool(10)
    yao_speaker.add_idea(ideaunit_shop(sweep_text(), pledge=True), casa_road())
    yao_speaker.add_idea(ideaunit_shop(dirty_text()), sanitation_road())
    yao_speaker.add_idea(ideaunit_shop(clean_text()), sanitation_road())
    yao_speaker.edit_reason(sweep_road(), sanitation_road(), dirty_road())
    yao_speaker.set_fact(sweep_road(), dirty_road())
    return yao_speaker


def get_usa_road() -> RoadUnit:
    return create_road(get_default_real_id_roadnode(), "USA")


def get_iowa_text() -> RoadNode:
    return "Iowa"


def get_ohio_text() -> RoadNode:
    return "Ohio"


def get_utah_text() -> RoadNode:
    return "Utah"


def get_swim_text() -> RoadNode:
    return "swim"


def get_location_text() -> RoadNode:
    return "location"


def get_in_ocean_text() -> RoadNode:
    return "in_ocean"


def get_on_land_text() -> RoadNode:
    return "on_land"


def get_iowa_road() -> RoadUnit:
    return create_road(get_usa_road(), get_iowa_text())


def get_ohio_road() -> RoadUnit:
    return create_road(get_usa_road(), get_ohio_text())


def get_utah_road() -> RoadUnit:
    return create_road(get_usa_road(), get_utah_text())


def get_swim_road() -> RoadUnit:
    return create_road(get_default_real_id_roadnode(), get_swim_text())


def get_location_road() -> RoadUnit:
    return create_road(get_default_real_id_roadnode(), get_location_text())


def get_in_ocean_road() -> RoadUnit:
    return create_road(get_location_road(), get_in_ocean_text())


def get_on_land_road() -> RoadUnit:
    return create_road(get_location_road(), get_on_land_text())


def get_yao_ohio_hubunit() -> HubUnit:
    yao_world = get_example_yao_world()
    return hubunit_shop(
        reals_dir=env_dir(),
        real_id=yao_world._real_id,
        owner_id=yao_world._owner_id,
        econ_road=get_ohio_road(),
        # pipeline_voice_action_text(),
    )


def get_yao_iowa_hubunit() -> HubUnit:
    yao_world = get_example_yao_world()
    return hubunit_shop(
        reals_dir=env_dir(),
        real_id=yao_world._real_id,
        owner_id=yao_world._owner_id,
        econ_road=get_iowa_road(),
        # pipeline_voice_action_text(),
    )


def get_zia_utah_hubunit() -> HubUnit:
    yao_world = get_example_yao_world()
    return hubunit_shop(
        reals_dir=env_dir(),
        real_id=yao_world._real_id,
        owner_id="Zia",
        econ_road=get_utah_road(),
        # pipeline_voice_action_text(),
    )


def get_example_yao_voice_with_3_healers():
    yao_voice = get_example_yao_world()
    yao_text = yao_voice.get_char("Yao").char_id
    bob_text = yao_voice.get_char("Bob").char_id
    zia_text = yao_voice.get_char("Zia").char_id
    iowa_idea = ideaunit_shop(get_iowa_text(), _problem_bool=True)
    ohio_idea = ideaunit_shop(get_ohio_text(), _problem_bool=True)
    utah_idea = ideaunit_shop(get_utah_text(), _problem_bool=True)
    iowa_idea._healerhold.set_belief_id(get_yao_iowa_hubunit().owner_id)
    ohio_idea._healerhold.set_belief_id(get_yao_ohio_hubunit().owner_id)
    utah_idea._healerhold.set_belief_id(get_zia_utah_hubunit().owner_id)
    yao_voice.add_idea(iowa_idea, get_usa_road())
    yao_voice.add_idea(ohio_idea, get_usa_road())
    yao_voice.add_idea(utah_idea, get_usa_road())

    return yao_voice


def test_listen_to_owner_jobs_Pipeline_Scenario0(env_dir_setup_cleanup):
    # GIVEN
    # yao0_voice with 3 debotors of different credor_weights
    # yao_job1 with 1 task, fact that doesn't make that task active
    # yao_job2 with 2 tasks, one is equal fact that makes task active
    # yao_job3 with 1 new task, fact stays with it

    yao_voice0 = get_example_yao_voice_with_3_healers()
    yao_voice0.del_idea_obj(run_road())
    yao_voice0.add_l1_idea(ideaunit_shop(get_location_text()))
    yao_voice0.add_idea(ideaunit_shop(get_in_ocean_text()), get_location_road())
    yao_voice0.add_idea(ideaunit_shop(get_on_land_text()), get_location_road())
    yao_voice0.add_l1_idea(ideaunit_shop(get_swim_text(), pledge=True))
    yao_voice0.edit_reason(get_swim_road(), get_location_road(), get_in_ocean_road())
    yao_voice0.calc_world_metrics()
    assert yao_voice0._econ_dict.get(get_iowa_road())
    assert yao_voice0._econ_dict.get(get_ohio_road())
    assert yao_voice0._econ_dict.get(get_utah_road())
    assert len(yao_voice0._econ_dict) == 3
    print(f"{yao_voice0._idea_dict.keys()=}")

    yao_text = yao_voice0._owner_id
    yao_job1 = get_example_yao_job1_speaker()
    yao_job2 = get_example_yao_job2_speaker()
    yao_job3 = get_example_yao_job3_speaker()
    yao_iowa_hubunit = get_yao_iowa_hubunit()
    yao_ohio_hubunit = get_yao_ohio_hubunit()
    zia_utah_hubunit = get_zia_utah_hubunit()
    # delete_dir(yao_iowa_hubunit.owners_dir())
    assert yao_iowa_hubunit.voice_file_exists() is False
    assert yao_iowa_hubunit.action_file_exists() is False
    assert yao_iowa_hubunit.job_file_exists(yao_text) is False
    assert yao_ohio_hubunit.job_file_exists(yao_text) is False
    assert zia_utah_hubunit.job_file_exists(yao_text) is False
    yao_iowa_hubunit.save_voice_world(yao_voice0)
    yao_iowa_hubunit.save_job_world(yao_job1)
    yao_ohio_hubunit.save_job_world(yao_job2)
    zia_utah_hubunit.save_job_world(yao_job3)
    assert yao_iowa_hubunit.voice_file_exists()
    assert yao_iowa_hubunit.job_file_exists(yao_text)
    assert yao_ohio_hubunit.job_file_exists(yao_text)
    assert zia_utah_hubunit.job_file_exists(yao_text)

    # WHEN
    assert yao_iowa_hubunit.action_file_exists() is False
    listen_to_owner_jobs(yao_iowa_hubunit)
    assert yao_iowa_hubunit.action_file_exists()

    yao_action = yao_iowa_hubunit.get_action_world()
    yao_action.calc_world_metrics()
    assert yao_action._chars.keys() == yao_voice0._chars.keys()
    assert yao_action.get_char(yao_text)._irrational_debtor_weight == 0
    assert yao_action.get_beliefunits_dict() == yao_voice0.get_beliefunits_dict()
    assert len(yao_action._idea_dict) == 10
    print(f"{yao_action._idea_dict.keys()=}")
    print(f"{yao_action.get_factunits_dict().keys()=}")
    assert yao_action.idea_exists(cook_road())
    assert yao_action.idea_exists(clean_road())
    assert yao_action.idea_exists(run_road()) is False
    assert len(yao_action._idearoot._factunits) == 2
    assert yao_action != yao_voice0


def test_listen_to_owner_jobs_Pipeline_Scenario1_yao_voice_CanOnlyReferenceItself(
    env_dir_setup_cleanup,
):
    # GIVEN
    # yao0_voice with 3 debotors of different credor_weights
    # yao_job1 with 1 task, fact that doesn't make that task active
    # yao_job2 with 2 tasks, one is equal fact that makes task active
    # yao_job3 with 1 new task, fact stays with it

    yao_voice0 = get_example_yao_voice_with_3_healers()
    yao_voice0.add_l1_idea(ideaunit_shop(get_location_text()))
    yao_voice0.add_idea(ideaunit_shop(get_in_ocean_text()), get_location_road())
    yao_voice0.add_idea(ideaunit_shop(get_on_land_text()), get_location_road())
    yao_voice0.add_l1_idea(ideaunit_shop(get_swim_text(), pledge=True))
    yao_voice0.edit_reason(get_swim_road(), get_location_road(), get_in_ocean_road())
    yao_voice0.set_fact(get_location_road(), get_in_ocean_road())
    print(f"{yao_voice0.get_fact(get_location_road())=}")
    yao_voice0.del_idea_obj(run_road())
    assert yao_voice0._econ_dict.get(get_iowa_road())
    assert yao_voice0._econ_dict.get(get_ohio_road())
    assert yao_voice0._econ_dict.get(get_utah_road())
    yao_voice0.calc_world_metrics()
    assert len(yao_voice0._econ_dict) == 3
    # print(f"{yao_voice0._idea_dict.keys()=}")

    yao_text = yao_voice0._owner_id
    yao_job1 = get_example_yao_job1_speaker()
    yao_job2 = get_example_yao_job2_speaker()
    yao_job3 = get_example_yao_job3_speaker()
    yao_iowa_hubunit = get_yao_iowa_hubunit()
    yao_ohio_hubunit = get_yao_ohio_hubunit()
    zia_utah_hubunit = get_zia_utah_hubunit()
    # delete_dir(yao_iowa_hubunit.owners_dir())
    assert yao_iowa_hubunit.voice_file_exists() is False
    assert yao_iowa_hubunit.action_file_exists() is False
    assert yao_iowa_hubunit.job_file_exists(yao_text) is False
    assert yao_ohio_hubunit.job_file_exists(yao_text) is False
    assert zia_utah_hubunit.job_file_exists(yao_text) is False
    print(f"{yao_voice0.get_fact(get_location_road())=}")
    yao_iowa_hubunit.save_voice_world(yao_voice0)
    # yao_iowa_hubunit.save_job_world(yao_job1)
    # yao_ohio_hubunit.save_job_world(yao_job2)
    # zia_utah_hubunit.save_job_world(yao_job3)
    assert yao_iowa_hubunit.voice_file_exists()
    assert yao_iowa_hubunit.job_file_exists(yao_text) is False
    assert yao_ohio_hubunit.job_file_exists(yao_text) is False
    assert zia_utah_hubunit.job_file_exists(yao_text) is False

    # WHEN
    assert yao_iowa_hubunit.action_file_exists() is False
    listen_to_owner_jobs(yao_iowa_hubunit)
    assert yao_iowa_hubunit.action_file_exists()

    yao_action = yao_iowa_hubunit.get_action_world()
    yao_action.calc_world_metrics()
    assert yao_action._chars.keys() == yao_voice0._chars.keys()
    assert yao_action.get_char(yao_text)._irrational_debtor_weight == 0
    assert yao_action.get_beliefunits_dict() == yao_voice0.get_beliefunits_dict()
    assert len(yao_action._idea_dict) == 4
    print(f"{yao_action._idea_dict.keys()=}")
    print(f"{yao_action.get_factunits_dict().keys()=}")
    assert yao_action.idea_exists(cook_road()) is False
    assert yao_action.idea_exists(clean_road()) is False
    assert yao_action.idea_exists(run_road()) is False
    assert yao_action.idea_exists(get_swim_road())
    assert yao_action.idea_exists(get_in_ocean_road())
    assert yao_action.idea_exists(get_on_land_road()) is False
    assert yao_action.get_fact(get_location_road()) != None
    assert yao_action.get_fact(get_location_road()).pick == get_in_ocean_road()
    assert len(yao_action.get_agenda_dict()) == 1
    assert len(yao_action._idearoot._factunits) == 1
    assert yao_action != yao_voice0


def test_create_job_file_from_duty_file_CreatesEmptyJob(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_duty = worldunit_shop(yao_text)
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_world(yao_duty)
    assert sue_texas_hubunit.job_file_exists(yao_text) is False

    # WHEN
    create_job_file_from_duty_file(sue_texas_hubunit, yao_text)

    # GIVEN
    assert sue_texas_hubunit.job_file_exists(yao_text)
    yao_job = sue_texas_hubunit.get_job_world(yao_text)
    assert yao_job._owner_id != None
    assert yao_job._owner_id == yao_text
    assert yao_job.get_dict() == yao_duty.get_dict()
