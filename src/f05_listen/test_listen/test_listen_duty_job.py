from src.f01_road.road import (
    RoadUnit,
    create_road,
    get_default_fiscal_id_ideaunit,
    IdeaUnit,
)
from src.f02_bud.item import itemunit_shop
from src.f02_bud.bud import BudUnit, budunit_shop
from src.f05_listen.hubunit import hubunit_shop, HubUnit
from src.f05_listen.listen import listen_to_owner_jobs, create_job_file_from_duty_file
from src.f05_listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
    get_texas_hubunit,
)


def casa_str() -> str:
    return "casa"


def cook_str() -> str:
    return "cook"


def eat_str() -> str:
    return "eat"


def hungry_str() -> str:
    return "hungry"


def full_str() -> str:
    return "full"


def sanitation_str():
    return "sanitation"


def clean_str():
    return "clean"


def dirty_str():
    return "dirty"


def sweep_str():
    return "sweep"


def run_str():
    return "run"


def casa_road() -> RoadUnit:
    return create_road(get_default_fiscal_id_ideaunit(), casa_str())


def cook_road() -> RoadUnit:
    return create_road(casa_road(), cook_str())


def eat_road() -> RoadUnit:
    return create_road(casa_road(), eat_str())


def hungry_road() -> RoadUnit:
    return create_road(eat_road(), hungry_str())


def full_road() -> RoadUnit:
    return create_road(eat_road(), full_str())


def sanitation_road() -> RoadUnit:
    return create_road(casa_road(), sanitation_str())


def clean_road() -> RoadUnit:
    return create_road(sanitation_road(), clean_str())


def dirty_road() -> RoadUnit:
    return create_road(sanitation_road(), dirty_str())


def sweep_road() -> RoadUnit:
    return create_road(casa_road(), sweep_str())


def run_road() -> RoadUnit:
    return create_road(casa_road(), run_str())


def get_example_yao_bud() -> BudUnit:
    yao_str = "Yao"
    zia_str = "Zia"
    bob_str = "Bob"
    yao_speaker = budunit_shop(yao_str, get_default_fiscal_id_ideaunit())
    yao_speaker.set_item(itemunit_shop(run_str()), casa_road())
    yao_speaker.add_acctunit(yao_str, debtit_belief=10)
    yao_speaker.add_acctunit(zia_str, debtit_belief=30)
    yao_speaker.add_acctunit(bob_str, debtit_belief=40)
    yao_speaker.set_acct_respect(80)
    return yao_speaker


def get_example_yao_job1_speaker() -> BudUnit:
    yao_str = "Yao"
    yao_speaker = get_example_yao_bud()
    yao_speaker.del_item_obj(run_road())
    yao_speaker.set_acct_respect(40)
    yao_speaker.set_item(itemunit_shop(cook_str(), pledge=True), casa_road())
    yao_speaker.set_item(itemunit_shop(hungry_str()), eat_road())
    yao_speaker.set_item(itemunit_shop(full_str()), eat_road())
    cook_itemunit = yao_speaker.get_item_obj(cook_road())
    cook_itemunit.teamunit.set_teamlink(yao_str)
    yao_speaker.edit_reason(cook_road(), eat_road(), hungry_road())
    yao_speaker.set_fact(eat_road(), hungry_road())
    return yao_speaker


def get_example_yao_job2_speaker() -> BudUnit:
    yao_str = "Yao"
    yao_speaker = get_example_yao_bud()
    yao_speaker.del_item_obj(run_road())
    yao_speaker.set_acct_respect(30)
    yao_speaker.set_item(itemunit_shop(cook_str(), pledge=True), casa_road())
    yao_speaker.set_item(itemunit_shop(hungry_str()), eat_road())
    yao_speaker.set_item(itemunit_shop(full_str()), eat_road())
    cook_itemunit = yao_speaker.get_item_obj(cook_road())
    cook_itemunit.teamunit.set_teamlink(yao_str)
    yao_speaker.edit_reason(cook_road(), eat_road(), hungry_road())
    yao_speaker.set_fact(eat_road(), hungry_road())

    yao_speaker.set_item(itemunit_shop(sweep_str(), pledge=True), casa_road())
    yao_speaker.set_item(itemunit_shop(dirty_str()), sanitation_road())
    yao_speaker.set_item(itemunit_shop(clean_str()), sanitation_road())
    yao_speaker.edit_reason(sweep_road(), sanitation_road(), dirty_road())
    yao_speaker.set_fact(sweep_road(), dirty_road())
    return yao_speaker


def get_example_yao_job3_speaker() -> BudUnit:
    yao_speaker = get_example_yao_bud()
    yao_speaker.del_item_obj(run_road())
    yao_speaker.set_acct_respect(10)
    yao_speaker.set_item(itemunit_shop(sweep_str(), pledge=True), casa_road())
    yao_speaker.set_item(itemunit_shop(dirty_str()), sanitation_road())
    yao_speaker.set_item(itemunit_shop(clean_str()), sanitation_road())
    yao_speaker.edit_reason(sweep_road(), sanitation_road(), dirty_road())
    yao_speaker.set_fact(sweep_road(), dirty_road())
    return yao_speaker


def get_usa_road() -> RoadUnit:
    return create_road(get_default_fiscal_id_ideaunit(), "USA")


def get_iowa_str() -> IdeaUnit:
    return "Iowa"


def get_ohio_str() -> IdeaUnit:
    return "Ohio"


def get_utah_str() -> IdeaUnit:
    return "Utah"


def get_swim_str() -> IdeaUnit:
    return "swim"


def get_location_str() -> IdeaUnit:
    return "location"


def get_in_mer_str() -> IdeaUnit:
    return "in_mer"


def get_on_land_str() -> IdeaUnit:
    return "on_land"


def get_iowa_road() -> RoadUnit:
    return create_road(get_usa_road(), get_iowa_str())


def get_ohio_road() -> RoadUnit:
    return create_road(get_usa_road(), get_ohio_str())


def get_utah_road() -> RoadUnit:
    return create_road(get_usa_road(), get_utah_str())


def get_swim_road() -> RoadUnit:
    return create_road(get_default_fiscal_id_ideaunit(), get_swim_str())


def get_location_road() -> RoadUnit:
    return create_road(get_default_fiscal_id_ideaunit(), get_location_str())


def get_in_mer_road() -> RoadUnit:
    return create_road(get_location_road(), get_in_mer_str())


def get_on_land_road() -> RoadUnit:
    return create_road(get_location_road(), get_on_land_str())


def get_yao_ohio_hubunit() -> HubUnit:
    yao_bud = get_example_yao_bud()
    return hubunit_shop(
        fiscals_dir=env_dir(),
        fiscal_id=yao_bud._fiscal_id,
        owner_id=yao_bud._owner_id,
        keep_road=get_ohio_road(),
        # pipeline_voice_final_str(),
    )


def get_yao_iowa_hubunit() -> HubUnit:
    yao_bud = get_example_yao_bud()
    return hubunit_shop(
        fiscals_dir=env_dir(),
        fiscal_id=yao_bud._fiscal_id,
        owner_id=yao_bud._owner_id,
        keep_road=get_iowa_road(),
        # pipeline_voice_final_str(),
    )


def get_zia_utah_hubunit() -> HubUnit:
    yao_bud = get_example_yao_bud()
    return hubunit_shop(
        fiscals_dir=env_dir(),
        fiscal_id=yao_bud._fiscal_id,
        owner_id="Zia",
        keep_road=get_utah_road(),
        # pipeline_voice_final_str(),
    )


def get_example_yao_voice_with_3_healers():
    yao_voice = get_example_yao_bud()
    yao_str = yao_voice.get_acct("Yao").acct_id
    bob_str = yao_voice.get_acct("Bob").acct_id
    zia_str = yao_voice.get_acct("Zia").acct_id
    iowa_item = itemunit_shop(get_iowa_str(), problem_bool=True)
    ohio_item = itemunit_shop(get_ohio_str(), problem_bool=True)
    utah_item = itemunit_shop(get_utah_str(), problem_bool=True)
    iowa_item.healerlink.set_healer_id(get_yao_iowa_hubunit().owner_id)
    ohio_item.healerlink.set_healer_id(get_yao_ohio_hubunit().owner_id)
    utah_item.healerlink.set_healer_id(get_zia_utah_hubunit().owner_id)
    yao_voice.set_item(iowa_item, get_usa_road())
    yao_voice.set_item(ohio_item, get_usa_road())
    yao_voice.set_item(utah_item, get_usa_road())

    return yao_voice


# def test_listen_to_owner_jobs_Pipeline_Scenario0(env_dir_setup_cleanup):
#     # ESTABLISH
#     # yao0_voice with 3 debotors of different credit_beliefs
#     # yao_job1 with 1 task, fact that doesn't make that task active
#     # yao_job2 with 2 tasks, one is equal fact that makes task active
#     # yao_job3 with 1 new task, fact stays with it

#     yao_voice0 = get_example_yao_voice_with_3_healers()
#     yao_voice0.del_item_obj(run_road())
#     yao_voice0.set_l1_item(itemunit_shop(get_location_str()))
#     yao_voice0.set_item(itemunit_shop(get_in_mer_str()), get_location_road())
#     yao_voice0.set_item(itemunit_shop(get_on_land_str()), get_location_road())
#     yao_voice0.set_l1_item(itemunit_shop(get_swim_str(), pledge=True))
#     yao_voice0.edit_reason(get_swim_road(), get_location_road(), get_in_mer_road())
#     yao_voice0.settle_bud()
#     assert yao_voice0._keep_dict.get(get_iowa_road())
#     assert yao_voice0._keep_dict.get(get_ohio_road())
#     assert yao_voice0._keep_dict.get(get_utah_road())
#     assert len(yao_voice0._keep_dict) == 3
#     print(f"{yao_voice0._item_dict.keys()=}")

#     yao_str = yao_voice0._owner_id
#     yao_job1 = get_example_yao_job1_speaker()
#     yao_job2 = get_example_yao_job2_speaker()
#     yao_job3 = get_example_yao_job3_speaker()
#     yao_iowa_hubunit = get_yao_iowa_hubunit()
#     yao_ohio_hubunit = get_yao_ohio_hubunit()
#     zia_utah_hubunit = get_zia_utah_hubunit()
#     # delete_dir(yao_iowa_hubunit.owners_dir())
#     assert yao_iowa_hubunit.voice_file_exists() is False
#     assert yao_iowa_hubunit.final_file_exists() is False
#     assert yao_iowa_hubunit.job_file_exists(yao_str) is False
#     assert yao_ohio_hubunit.job_file_exists(yao_str) is False
#     assert zia_utah_hubunit.job_file_exists(yao_str) is False
#     yao_iowa_hubunit.save_voice_bud(yao_voice0)
#     yao_iowa_hubunit.save_job_bud(yao_job1)
#     yao_ohio_hubunit.save_job_bud(yao_job2)
#     zia_utah_hubunit.save_job_bud(yao_job3)
#     assert yao_iowa_hubunit.voice_file_exists()
#     assert yao_iowa_hubunit.job_file_exists(yao_str)
#     assert yao_ohio_hubunit.job_file_exists(yao_str)
#     assert zia_utah_hubunit.job_file_exists(yao_str)

#     # WHEN
#     assert yao_iowa_hubunit.final_file_exists() is False
#     listen_to_owner_jobs(yao_iowa_hubunit)
#     assert yao_iowa_hubunit.final_file_exists()

#     yao_final = yao_iowa_hubunit.get_final_bud()
#     yao_final.settle_bud()
#     assert yao_final._accts.keys() == yao_voice0._accts.keys()
#     assert yao_final.get_acct(yao_str)._irrational_debtit_belief == 0
#     yao_final_accts = yao_final.get_dict().get("_accts")
#     yao_voice0_accts = yao_voice0.get_dict().get("_accts")
#     yao_final_bob = yao_final_accts.get("Bob")
#     yao_voice0_bob = yao_voice0_accts.get("Bob")
#     print(f"{yao_final_bob=}")
#     print(f"{yao_voice0_bob=}")
#     assert yao_final_bob == yao_voice0_bob
#     assert yao_final_accts.keys() == yao_voice0_accts.keys()
#     assert yao_final_accts == yao_voice0_accts
#     assert len(yao_final.get_dict().get("_accts")) == 3
#     assert len(yao_final._item_dict) == 10
#     print(f"{yao_final._item_dict.keys()=}")
#     print(f"{yao_final.get_factunits_dict().keys()=}")
#     assert yao_final.item_exists(cook_road())
#     assert yao_final.item_exists(clean_road())
#     assert yao_final.item_exists(run_road()) is False
#     assert len(yao_final._itemroot.factunits) == 2
#     assert yao_final != yao_voice0


def test_listen_to_owner_jobs_Pipeline_Scenario1_yao_voice_CanOnlyReferenceItself(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    # yao0_voice with 3 debotors of different credit_beliefs
    # yao_job1 with 1 task, fact that doesn't make that task active
    # yao_job2 with 2 tasks, one is equal fact that makes task active
    # yao_job3 with 1 new task, fact stays with it

    yao_voice0 = get_example_yao_voice_with_3_healers()
    yao_voice0.set_l1_item(itemunit_shop(get_location_str()))
    yao_voice0.set_item(itemunit_shop(get_in_mer_str()), get_location_road())
    yao_voice0.set_item(itemunit_shop(get_on_land_str()), get_location_road())
    yao_voice0.set_l1_item(itemunit_shop(get_swim_str(), pledge=True))
    yao_voice0.edit_reason(get_swim_road(), get_location_road(), get_in_mer_road())
    yao_voice0.set_fact(get_location_road(), get_in_mer_road())
    print(f"{yao_voice0.get_fact(get_location_road())=}")
    yao_voice0.del_item_obj(run_road())
    assert yao_voice0._keep_dict.get(get_iowa_road())
    assert yao_voice0._keep_dict.get(get_ohio_road())
    assert yao_voice0._keep_dict.get(get_utah_road())
    yao_voice0.settle_bud()
    assert len(yao_voice0._keep_dict) == 3
    # print(f"{yao_voice0._item_dict.keys()=}")

    yao_str = yao_voice0._owner_id
    yao_job1 = get_example_yao_job1_speaker()
    yao_job2 = get_example_yao_job2_speaker()
    yao_job3 = get_example_yao_job3_speaker()
    yao_iowa_hubunit = get_yao_iowa_hubunit()
    yao_ohio_hubunit = get_yao_ohio_hubunit()
    zia_utah_hubunit = get_zia_utah_hubunit()
    # delete_dir(yao_iowa_hubunit.owners_dir())
    assert yao_iowa_hubunit.voice_file_exists() is False
    assert yao_iowa_hubunit.final_file_exists() is False
    assert yao_iowa_hubunit.job_file_exists(yao_str) is False
    assert yao_ohio_hubunit.job_file_exists(yao_str) is False
    assert zia_utah_hubunit.job_file_exists(yao_str) is False
    print(f"{yao_voice0.get_fact(get_location_road())=}")
    yao_iowa_hubunit.save_voice_bud(yao_voice0)
    # yao_iowa_hubunit.save_job_bud(yao_job1)
    # yao_ohio_hubunit.save_job_bud(yao_job2)
    # zia_utah_hubunit.save_job_bud(yao_job3)
    assert yao_iowa_hubunit.voice_file_exists()
    assert yao_iowa_hubunit.job_file_exists(yao_str) is False
    assert yao_ohio_hubunit.job_file_exists(yao_str) is False
    assert zia_utah_hubunit.job_file_exists(yao_str) is False

    # WHEN
    assert yao_iowa_hubunit.final_file_exists() is False
    listen_to_owner_jobs(yao_iowa_hubunit)
    assert yao_iowa_hubunit.final_file_exists()

    yao_final = yao_iowa_hubunit.get_final_bud()
    yao_final.settle_bud()
    assert yao_final._accts.keys() == yao_voice0._accts.keys()
    assert yao_final.get_acct(yao_str)._irrational_debtit_belief == 0
    yao_final_accts = yao_final.get_dict().get("_accts")
    yao_voice0_accts = yao_voice0.get_dict().get("_accts")
    yao_final_bob = yao_final_accts.get("Bob")
    yao_voice0_bob = yao_voice0_accts.get("Bob")
    print(f"{yao_final_bob=}")
    print(f"{yao_voice0_bob=}")
    assert yao_final_bob == yao_voice0_bob
    assert yao_final_accts.keys() == yao_voice0_accts.keys()
    assert yao_final_accts == yao_voice0_accts
    assert len(yao_final.get_dict().get("_accts")) == 3
    assert len(yao_final._item_dict) == 4
    print(f"{yao_final._item_dict.keys()=}")
    print(f"{yao_final.get_factunits_dict().keys()=}")
    assert yao_final.item_exists(cook_road()) is False
    assert yao_final.item_exists(clean_road()) is False
    assert yao_final.item_exists(run_road()) is False
    assert yao_final.item_exists(get_swim_road())
    assert yao_final.item_exists(get_in_mer_road())
    assert yao_final.item_exists(get_on_land_road()) is False
    assert yao_final.get_fact(get_location_road()) is not None
    assert yao_final.get_fact(get_location_road()).pick == get_in_mer_road()
    assert len(yao_final.get_agenda_dict()) == 1
    assert len(yao_final._itemroot.factunits) == 1
    assert yao_final != yao_voice0


def test_create_job_file_from_duty_file_CreatesEmptyJob(env_dir_setup_cleanup):
    # ESTABLISH
    yao_str = "Yao"
    yao_duty = budunit_shop(yao_str)
    sue_texas_hubunit = get_texas_hubunit()
    sue_texas_hubunit.save_duty_bud(yao_duty)
    assert sue_texas_hubunit.job_file_exists(yao_str) is False

    # WHEN
    create_job_file_from_duty_file(sue_texas_hubunit, yao_str)

    # ESTABLISH
    assert sue_texas_hubunit.job_file_exists(yao_str)
    yao_job = sue_texas_hubunit.get_job_bud(yao_str)
    assert yao_job._owner_id is not None
    assert yao_job._owner_id == yao_str
    assert yao_job.get_dict() == yao_duty.get_dict()
