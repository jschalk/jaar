from src.agenda.examples.example_agendas import (
    agenda_v002 as ex_agenda_v002,
)
from src.econ.econ import econunit_shop
from src.econ.examples.example_clerks import (
    get_6node_agenda as example_get_6node_agenda,
    get_agenda_2CleanNodesRandomWeights,
    get_agenda_3CleanNodesRandomWeights,
)
from src.econ.examples.econ_env_kit import (
    get_temp_env_econ_id,
    get_test_econ_dir,
    env_dir_setup_cleanup,
)


def test_EconUnit_get_refreshed_job_ReturnsCorrectAgendaObjScenario1(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_econ_id(), get_test_econ_dir())
    input_agenda = example_get_6node_agenda()
    x_econ.save_job_agenda_to_forum(input_agenda)
    # x_econ.save_job_agenda_to_forum(ex_cxs_get_agenda_1Task_1CE0MinutesReason_1Belief())
    # x_econ.save_job_agenda_to_forum(ex_cxs_agenda_v001())
    xia_text = "Xia"
    x_econ.create_new_clerkunit(clerk_id=xia_text)
    x_econ.set_clerk_depotlink(
        xia_text, input_agenda._owner_id, depotlink_type="blind_trust"
    )
    x_econ.save_clerkunit_file(clerk_id=xia_text)
    xia_healer = x_econ.get_clerkunit(clerk_id=xia_text)
    # print(f"{xia_healer._role._partys.keys()=}")

    # WHEN
    output_agenda = x_econ.get_refreshed_job(clerk_id=xia_text)
    # input agenda must be melded to itself to create originunits
    input_agenda.meld(input_agenda)
    input_agenda.set_owner_id(new_owner_id=xia_text)
    input_agenda._originunit.set_originlink(party_id=xia_text, weight=1)

    # THEN
    a_text = "A"
    c_text = "C"
    c_road = input_agenda.make_l1_road(c_text)
    d_text = "D"
    d_road = output_agenda.make_road(c_road, d_text)
    print(f"{output_agenda._owner_id=}")
    print(f"{output_agenda._idea_dict.keys()=}")
    output_agenda_d_idea = output_agenda.get_idea_obj(d_road)
    # print(f" {output_agenda_d_idea._weight=} {len(input_agenda._idearoot._kids)=} ")
    assert output_agenda != None
    assert len(input_agenda._idearoot._kids) == 2
    # idea_a = output_agenda.get_idea_obj("A")
    # idea_b = output_agenda.get_idea_obj("B")
    # for idea_kid_x1 in input_agenda._idearoot._kids.values():
    #     print(f"{idea_kid_x1._label=}")
    #     output_agenda_counterpart_x1 = output_agenda.get_idea_obj(idea_kid_x1._label)
    #     for idea_kid_x2 in idea_kid_x1._kids.values():
    #         output_agenda_counterpart_x2 = output_agenda_counterpart_x1._get_kid(
    #             idea_kid_x2._label
    #         )
    #         print(
    #             f"{idea_kid_x2._label=} {idea_kid_x2._weight=} {output_agenda_counterpart_x2._weight=}"
    #         )
    #         # assert output_agenda_counterpart_x2 == idea_kid_x2
    #         assert output_agenda_counterpart_x2._label == idea_kid_x2._label

    #     print(
    #         f"{idea_kid_x1._label=} {idea_kid_x1._weight=} {output_agenda_counterpart_x1._weight=}"
    #     )
    #     assert output_agenda_counterpart_x1._label == idea_kid_x1._label
    # assert output_agenda._idearoot._kids == input_agenda._idearoot._kids
    assert output_agenda._idearoot._beliefunits == {}
    assert output_agenda._idearoot._beliefunits == input_agenda._idearoot._beliefunits
    assert list(output_agenda._partys.keys()) == [xia_text, a_text]
    assert output_agenda._partys != input_agenda._partys
    assert list(output_agenda._groups.keys()) == [xia_text, a_text]
    assert output_agenda._groups != input_agenda._groups
    print(f"{output_agenda._originunit=}")
    print(f"{input_agenda._originunit=}")
    assert output_agenda._originunit == input_agenda._originunit

    b_text = "B"
    b_road = output_agenda.make_l1_road(b_text)
    print(f"{output_agenda.get_idea_obj(b_road)._originunit=}")
    print(f"{input_agenda.get_idea_obj(b_road)._originunit=}")
    assert output_agenda._idearoot == input_agenda._idearoot


def test_EconUnit_get_refreshed_job_ReturnsCorrectAgendaObjScenario2(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_econ_id(), get_test_econ_dir())
    x1_agenda = example_get_6node_agenda()
    x2_agenda = ex_agenda_v002()

    x_econ.save_job_agenda_to_forum(x1_agenda)
    x_econ.save_job_agenda_to_forum(x2_agenda)
    # x_econ.save_job_agenda_to_forum(ex_cxs_get_agenda_1Task_1CE0MinutesReason_1Belief())
    # x_econ.save_job_agenda_to_forum(ex_cxs_agenda_v001())
    xia_text = "Xia"
    x_econ.create_new_clerkunit(clerk_id=xia_text)
    x_econ.set_clerk_depotlink(xia_text, x1_agenda._owner_id, "blind_trust")
    x_econ.set_clerk_depotlink(xia_text, x2_agenda._owner_id, "blind_trust")
    x_econ.save_clerkunit_file(clerk_id=xia_text)
    xia_healer = x_econ.get_clerkunit(clerk_id=xia_text)
    print(f"{xia_healer._role._partys.keys()=}")

    # WHEN
    output_agenda = x_econ.get_refreshed_job(clerk_id=xia_text)

    # THEN
    output_agenda_d_road = f"{output_agenda._world_id},C,D"
    output_agenda_d_idea = output_agenda.get_idea_obj(output_agenda_d_road)
    print(f" {output_agenda_d_idea._weight=} ")
    assert output_agenda != None
    # for idea_kid_x1 in x1_agenda._idearoot._kids.values():
    #     output_agenda_counterpart_x1 = output_agenda.get_idea_obj(idea_kid_x1._label)
    #     for idea_kid_x2 in idea_kid_x1._kids.values():
    #         output_agenda_counterpart_x2 = output_agenda_counterpart_x1._get_kid(
    #             idea_kid_x2._label
    #         )
    #         print(
    #             f"{idea_kid_x2._label=} {idea_kid_x2._weight=} {output_agenda_counterpart_x2._weight=}"
    #         )
    #         # assert output_agenda_counterpart_x2 == idea_kid_x2
    #         assert output_agenda_counterpart_x2._label == idea_kid_x2._label

    #     print(
    #         f"{idea_kid_x1._label=} {idea_kid_x1._weight=} {output_agenda_counterpart_x1._weight=}"
    #     )
    #     assert output_agenda_counterpart_x1._label == idea_kid_x1._label
    # assert output_agenda._idearoot._kids == x1_agenda._idearoot._kids
    assert len(output_agenda._idearoot._beliefunits) == 9
    assert len(output_agenda._idearoot._beliefunits) == len(
        x2_agenda._idearoot._beliefunits
    )
    assert len(output_agenda._partys) == 3
    assert len(output_agenda._partys) != len(x1_agenda._partys)
    assert output_agenda._partys != x1_agenda._partys
    assert len(output_agenda._groups) == 3
    assert set(output_agenda._groups.keys()) == {"A", "Xia", "Bob"}
    assert output_agenda._idearoot != x1_agenda._idearoot
    assert output_agenda._idearoot != x2_agenda._idearoot


def test_ClerkUnit_refresh_depotlinks_CorrectlyPullsAllForumAgendas(
    env_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_test_econ_dir()
    econ_id = get_temp_env_econ_id()
    x_econ = econunit_shop(econ_id=econ_id, econ_dir=env_dir)
    x_econ.set_econ_dirs(in_memory_treasury=True)
    # ux = clerkunit_shop(owner_id=healer1_text, env_dir=env_dir)

    ernie_text = "ernie"
    jessi_text = "jessi"
    steve_text = "steve"
    ernie_agenda = get_agenda_2CleanNodesRandomWeights(_owner_id=ernie_text)
    jessi_agenda = get_agenda_2CleanNodesRandomWeights(_owner_id=jessi_text)
    old_steve_agenda = get_agenda_2CleanNodesRandomWeights(_owner_id=steve_text)
    x_econ.save_job_agenda_to_forum(ernie_agenda)
    x_econ.save_job_agenda_to_forum(jessi_agenda)
    x_econ.save_job_agenda_to_forum(old_steve_agenda)
    x_econ.create_new_clerkunit(clerk_id=ernie_text)
    x_econ.create_new_clerkunit(clerk_id=jessi_text)
    # x_econ.create_new_clerkunit(clerk_id=steve_text)
    ux_ernie = x_econ.get_clerkunit(clerk_id=ernie_text)
    ux_jessi = x_econ.get_clerkunit(clerk_id=jessi_text)
    # ux_steve = x_econ.get_clerkunit(clerk_id=steve_text)
    ux_ernie.set_depot_agenda(x_agenda=jessi_agenda, depotlink_type="blind_trust")
    ux_ernie.set_depot_agenda(x_agenda=old_steve_agenda, depotlink_type="blind_trust")
    ux_jessi.set_depot_agenda(x_agenda=ernie_agenda, depotlink_type="blind_trust")
    ux_jessi.set_depot_agenda(x_agenda=old_steve_agenda, depotlink_type="blind_trust")
    # ux_steve.set_depot_agenda(x_agenda=ernie_agenda, depotlink_type="blind_trust")
    # ux_steve.set_depot_agenda(x_agenda=jessi_agenda, depotlink_type="blind_trust")
    assert len(ux_ernie.get_remelded_output_agenda().get_idea_dict()) == 4
    assert len(ux_jessi.get_remelded_output_agenda().get_idea_dict()) == 4
    # assert len(ux_steve.get_remelded_output_agenda().get_idea_dict()) == 4
    new_steve_agenda = get_agenda_3CleanNodesRandomWeights(_owner_id="steve")
    x_econ.save_job_agenda_to_forum(new_steve_agenda)
    # print(f"{env_dir=} {ux._forum_dir=}")
    # for file_name in dir_files(dir_path=env_dir):
    #     print(f"{ux._forum_dir=} {file_name=}")

    # for file_name in dir_files(dir_path=ux._forum_dir):
    #     print(f"{ux._forum_dir=} {file_name=}")

    # WHEN
    x_econ.reload_all_clerkunits_job_agendas()

    # THEN
    assert len(ux_ernie.get_remelded_output_agenda().get_idea_dict()) == 5
    assert len(ux_jessi.get_remelded_output_agenda().get_idea_dict()) == 5
