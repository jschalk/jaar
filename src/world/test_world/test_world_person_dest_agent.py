from src.world.world import WorldUnit
from src.agent.agent import AgentUnit
from src.agent.examples.example_agents import (
    get_agent_1Task_1CE0MinutesRequired_1AcptFact as ex_cxs_get_agent_1Task_1CE0MinutesRequired_1AcptFact,
    agent_v001 as ex_cxs_agent_v001,
    agent_v002 as ex_cxs_agent_v002,
)
from src.world.examples.example_persons import (
    get_1node_agent as example_persons_get_1node_agent,
    get_6node_agent as example_persons_get_6node_agent,
)
from os import path as os_path
from src.world.examples.env_tools import (
    get_temp_env_name,
    get_test_worlds_dir,
    create_person_file_for_worlds,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_world_get_person_dest_agent_from_digest_agent_files_ReturnsCorrectAgentObjScenario1(
    env_dir_setup_cleanup,
):
    # GIVEN
    ex = WorldUnit(name=get_temp_env_name(), worlds_dir=get_test_worlds_dir())
    ex.create_dirs_if_null(in_memory_bank=True)
    input_agent = example_persons_get_6node_agent()
    ex.save_agentunit_obj_to_agents_dir(input_agent)
    # ex.save_agentunit_obj_to_agents_dir(ex_cxs_get_agent_1Task_1CE0MinutesRequired_1AcptFact())
    # ex.save_agentunit_obj_to_agents_dir(ex_cxs_agent_v001())
    px_name = "test_person1"
    ex.create_new_personunit(person_name=px_name)
    ex.create_agentlink_to_saved_agent(
        person_name=px_name, agent_desc=input_agent._desc
    )
    ex.save_person_file(person_name=px_name)
    person_x_obj = ex.get_person_obj_from_world(name=px_name)
    print(f"{person_x_obj._src_agentlinks=}")

    # WHEN
    dest_agent = ex.get_person_dest_agent_from_digest_agent_files(person_name=px_name)

    # THEN
    # print(f"Before meldable= {person_x_obj._src_agentlinks} ")
    input_agent.make_meldable(person_x_obj.get_starting_digest_agent())
    # print(f"After meldable= {person_x_obj._src_agentlinks} ")

    dest_agent_d_idea = dest_agent.get_idea_kid(road="A,C,D")
    print(f" {dest_agent_d_idea._weight=} {len(input_agent._idearoot._kids)=} ")
    assert dest_agent != None
    assert len(input_agent._idearoot._kids) == 2
    # idea_a = dest_agent.get_idea_kid(road="A")
    # idea_b = dest_agent.get_idea_kid(road="B")
    # for idea_kid_x1 in input_agent._idearoot._kids.values():
    #     print(f"{idea_kid_x1._desc=}")
    #     dest_agent_counterpart_x1 = dest_agent._idearoot._kids.get(idea_kid_x1._desc)
    #     for idea_kid_x2 in idea_kid_x1._kids.values():
    #         dest_agent_counterpart_x2 = dest_agent_counterpart_x1._kids.get(
    #             idea_kid_x2._desc
    #         )
    #         print(
    #             f"{idea_kid_x2._desc=} {idea_kid_x2._weight=} {dest_agent_counterpart_x2._weight=}"
    #         )
    #         # assert dest_agent_counterpart_x2 == idea_kid_x2
    #         assert dest_agent_counterpart_x2._desc == idea_kid_x2._desc

    #     print(
    #         f"{idea_kid_x1._desc=} {idea_kid_x1._weight=} {dest_agent_counterpart_x1._weight=}"
    #     )
    #     assert dest_agent_counterpart_x1._desc == idea_kid_x1._desc
    # assert dest_agent._idearoot._kids == input_agent._idearoot._kids
    assert dest_agent._idearoot._acptfactunits == {}
    assert dest_agent._idearoot._acptfactunits == input_agent._idearoot._acptfactunits
    assert dest_agent._allys == {}
    assert dest_agent._allys == input_agent._allys
    assert dest_agent._groups == {}
    assert dest_agent._groups == input_agent._groups
    assert dest_agent._idearoot == input_agent._idearoot


def test_world_get_person_dest_agent_from_digest_agent_files_ReturnsCorrectAgentObjScenario2(
    env_dir_setup_cleanup,
):
    # GIVEN
    ex = WorldUnit(name=get_temp_env_name(), worlds_dir=get_test_worlds_dir())
    ex.create_dirs_if_null(in_memory_bank=True)
    agent1 = example_persons_get_6node_agent()
    agent2 = ex_cxs_agent_v002()

    ex.save_agentunit_obj_to_agents_dir(agent1)
    ex.save_agentunit_obj_to_agents_dir(agent2)
    # ex.save_agentunit_obj_to_agents_dir(ex_cxs_get_agent_1Task_1CE0MinutesRequired_1AcptFact())
    # ex.save_agentunit_obj_to_agents_dir(ex_cxs_agent_v001())
    px_name = "test_person1"
    ex.create_new_personunit(person_name=px_name)
    ex.create_agentlink_to_saved_agent(px_name, agent1._desc)
    ex.create_agentlink_to_saved_agent(px_name, agent2._desc)
    ex.save_person_file(person_name=px_name)
    person_x_obj = ex.get_person_obj_from_world(name=px_name)
    print(f"{person_x_obj._src_agentlinks=}")

    # WHEN
    dest_agent = ex.get_person_dest_agent_from_digest_agent_files(person_name=px_name)

    # THEN
    # print(f"Before meldable= {person_x_obj._src_agentlinks} ")
    agent1.make_meldable(person_x_obj.get_starting_digest_agent())
    # print(f"After meldable= {person_x_obj._src_agentlinks} ")

    dest_agent_d_idea = dest_agent.get_idea_kid(road="A,C,D")
    print(f" {dest_agent_d_idea._weight=} ")
    assert dest_agent != None
    # for idea_kid_x1 in agent1._idearoot._kids.values():
    #     dest_agent_counterpart_x1 = dest_agent._idearoot._kids.get(idea_kid_x1._desc)
    #     for idea_kid_x2 in idea_kid_x1._kids.values():
    #         dest_agent_counterpart_x2 = dest_agent_counterpart_x1._kids.get(
    #             idea_kid_x2._desc
    #         )
    #         print(
    #             f"{idea_kid_x2._desc=} {idea_kid_x2._weight=} {dest_agent_counterpart_x2._weight=}"
    #         )
    #         # assert dest_agent_counterpart_x2 == idea_kid_x2
    #         assert dest_agent_counterpart_x2._desc == idea_kid_x2._desc

    #     print(
    #         f"{idea_kid_x1._desc=} {idea_kid_x1._weight=} {dest_agent_counterpart_x1._weight=}"
    #     )
    #     assert dest_agent_counterpart_x1._desc == idea_kid_x1._desc
    # assert dest_agent._idearoot._kids == agent1._idearoot._kids
    assert len(dest_agent._idearoot._acptfactunits) == 9
    assert len(dest_agent._idearoot._acptfactunits) == len(
        agent2._idearoot._acptfactunits
    )
    assert len(dest_agent._allys) == 22
    assert len(dest_agent._allys) == len(agent2._allys)
    assert len(dest_agent._groups) == 34
    assert len(dest_agent._groups) == len(agent2._groups)
    assert dest_agent._idearoot != agent1._idearoot
    assert dest_agent._idearoot != agent2._idearoot
