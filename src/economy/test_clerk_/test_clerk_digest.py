from src.agenda.agenda import agendaunit_shop, originunit_shop
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as example_agendas_get_agenda_with_4_levels,
)
from src.tools.file import open_file, count_files
from src.economy.clerk import clerkunit_shop
from src.economy.examples.example_clerks import (
    get_2node_agenda as example_healers_get_2node_agenda,
    get_7nodeJRoot_agenda as example_healers_get_7nodeJRoot_agenda,
)
from src.economy.examples.clerk_env_kit import (
    clerk_dir_setup_cleanup,
    get_temp_clerkunit_dir,
    get_temp_economy_id,
)
from os import path as os_path
from pytest import raises as pytest_raises


# def test_healer_save_contract_agenda_CreateStartingAgendaFile(
#     clerk_dir_setup_cleanup,
# ):
#     # GIVEN
#     lai_pid = "Lai"
#     env_dir = get_temp_clerkunit_dir()
#     lai_agenda = clerkunit_shop(pid=lai_pid, env_dir=env_dir)
#     lai_contract_file_name = lai_agenda._contract_file_name
#     with pytest_raises(Exception) as excinfo:
#         open_file(lai_agenda._clerkunit_dir, lai_contract_file_name)
#     assert (
#         str(excinfo.value)
#         == f"Could not load file {lai_agenda._contract_file_path} (2, 'No such file or directory')"
#     )

#     # WHEN
#     lai_agenda.save_contract_agenda(
#         agenda_x=example_agendas_get_agenda_with_4_levels()
#     )

#     # THEN
#     assert open_file(lai_agenda._clerkunit_dir, lai_contract_file_name) != None


def test_healeropen_contract_agenda_WhenStartingAgendaFileDoesNotExists(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    env_dir = get_temp_clerkunit_dir()
    economy_id_text = get_temp_economy_id()
    x_clerk = clerkunit_shop(pid=tim_text, env_dir=env_dir, economy_id=economy_id_text)

    # WHEN
    contract_agenda = x_clerk.open_contract_agenda()
    assert contract_agenda != None
    assert contract_agenda._economy_id == economy_id_text

    # THEN
    x_agenda = agendaunit_shop(_healer=tim_text)
    x_agenda.set_economy_id(get_temp_economy_id())
    x_agenda.set_agenda_metrics()
    # x_idearoot = ideaunit_shop(_root=True, _label=gio_text, _parent_road="")
    # x_idearoot._agenda_importance = 1
    # x_idearoot._level = 0
    # x_idearoot._ancestor_promise_count = 0
    # x_idearoot._descendant_promise_count = 0
    # x_idearoot._all_party_credit = True
    # x_idearoot._all_party_debt = True

    assert contract_agenda._idearoot == x_agenda._idearoot
    assert contract_agenda._idearoot._acptfactunits == {}
    assert list(contract_agenda._partys.keys()) == [tim_text]
    assert list(contract_agenda._groups.keys()) == [tim_text]


def test_healer_save_contract_agenda_contractPersonIDMustBeHealer(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    gio_text = "Gio"
    env_dir = get_temp_clerkunit_dir()
    x_clerk = clerkunit_shop(gio_text, env_dir, get_temp_economy_id())
    x_agenda = example_agendas_get_agenda_with_4_levels()
    assert x_agenda._healer != gio_text

    # WHEN
    x_clerk.save_contract_agenda(x_agenda=x_agenda)

    # THEN
    assert x_clerk.open_contract_agenda()._healer == x_clerk._clerk_cid


def test_healer_open_contract_agenda_WhenStartingAgendaFileExists(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    gio_text = "Gio"
    x_clerk = clerkunit_shop(gio_text, get_temp_clerkunit_dir(), get_temp_economy_id())
    x_clerk.save_contract_agenda(x_agenda=example_agendas_get_agenda_with_4_levels())

    # WHEN
    assert x_clerk.open_contract_agenda() != None
    contract_agenda = x_clerk.open_contract_agenda()

    # THEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    x_agenda.set_healer(new_healer=gio_text)
    x_agenda.set_agenda_metrics()

    assert contract_agenda._idearoot._kids == x_agenda._idearoot._kids
    assert contract_agenda._idearoot == x_agenda._idearoot
    assert contract_agenda._idearoot._acptfactunits == {}
    assert contract_agenda._partys == {}
    assert contract_agenda._groups == {}
    assert contract_agenda._healer == x_clerk._clerk_cid


def test_healer_erase_contract_agenda_file_DeletesFileCorrectly(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    gio_text = "Gio"
    env_dir = get_temp_clerkunit_dir()
    x_clerk = clerkunit_shop(gio_text, env_dir, get_temp_economy_id())
    x_clerk.save_contract_agenda(example_agendas_get_agenda_with_4_levels())
    file_name = x_clerk._contract_file_name
    assert open_file(x_clerk._clerkunit_dir, file_name) != None

    # WHEN
    x_clerk.erase_contract_agenda_file()

    # THEN
    with pytest_raises(Exception) as excinfo:
        open_file(x_clerk._clerkunit_dir, file_name)
    assert (
        str(excinfo.value)
        == f"Could not load file {x_clerk._clerkunit_dir}/contract_agenda.json (2, 'No such file or directory')"
    )


def test_clerkunit_save_agenda_to_digest_SavesFileCorrectly(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    clerk_cid = "healer1"
    env_dir = get_temp_clerkunit_dir()
    x_clerk = clerkunit_shop(clerk_cid, env_dir, get_temp_economy_id())
    x_clerk.create_core_dir_and_files()
    x_agenda = example_healers_get_2node_agenda()
    src_agenda_healer = x_agenda._healer
    assert count_files(x_clerk._agendas_digest_dir) == 0

    # WHEN
    x_clerk.save_agenda_to_digest(x_agenda, src_agenda_healer=src_agenda_healer)

    # THEN
    x_agenda_file_name = f"{x_agenda._healer}.json"
    digest_file_path = f"{x_clerk._agendas_digest_dir}/{x_agenda_file_name}"
    print(f"Saving to {digest_file_path=}")
    assert os_path.exists(digest_file_path)
    # for path_x in os_scandir(x_clerk._agendas_digest_dir):
    #     print(f"{path_x=}")
    assert count_files(x_clerk._agendas_digest_dir) == 1
    digest_x_agenda_json = open_file(
        dest_dir=x_clerk._agendas_digest_dir,
        file_name=f"{src_agenda_healer}.json",
    )
    assert digest_x_agenda_json == x_agenda.get_json()


def test_presonunit__set_depotlink_CorrectlySets_blind_trust_DigestAgenda(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    env_dir = get_temp_clerkunit_dir()
    sue_agenda = clerkunit_shop(sue_text, env_dir, get_temp_economy_id())
    sue_agenda.create_core_dir_and_files()
    x_agenda = example_healers_get_2node_agenda()
    src_agenda_healer = x_agenda._healer
    assert count_files(sue_agenda._agendas_digest_dir) == 0
    print(f"{x_agenda._economy_id=}")

    # WHEN
    sue_agenda.set_depot_agenda(x_agenda=x_agenda, depotlink_type="blind_trust")

    # THEN
    x_agenda_file_name = f"{x_agenda._healer}.json"
    digest_file_path = f"{sue_agenda._agendas_digest_dir}/{x_agenda_file_name}"
    print(f"Saving to {digest_file_path=}")
    assert os_path.exists(digest_file_path)
    # for path_x in os_scandir(sue_agenda._agendas_digest_dir):
    #     print(f"{path_x=}")
    assert count_files(sue_agenda._agendas_digest_dir) == 1
    digest_x_agenda_json = open_file(
        dest_dir=sue_agenda._agendas_digest_dir,
        file_name=f"{src_agenda_healer}.json",
    )
    assert digest_x_agenda_json == x_agenda.get_json()


def test_healer_get_remelded_output_agenda_withEmptyDigestDict(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    clerk_cid_x = "boots3"
    x_clerk = clerkunit_shop(
        clerk_cid_x, get_temp_clerkunit_dir(), get_temp_economy_id()
    )
    x_clerk.create_core_dir_and_files()
    x_agenda_output_before = x_clerk.get_remelded_output_agenda()
    assert str(type(x_agenda_output_before)).find(".agenda.AgendaUnit'>")
    assert x_agenda_output_before._healer == clerk_cid_x
    assert x_agenda_output_before._idearoot._label == get_temp_economy_id()
    # x_clerk.set_digested_agenda(agenda_x=agendaunit_shop(_healer="digested1"))

    # WHEN
    sx_output_after = x_clerk.get_remelded_output_agenda()

    # THEN
    healer_agenda_x = agendaunit_shop(_healer=clerk_cid_x, _weight=0.0)
    healer_agenda_x.set_economy_id(get_temp_economy_id())
    healer_agenda_x._idearoot._parent_road = ""
    healer_agenda_x.set_agenda_metrics()

    assert str(type(sx_output_after)).find(".agenda.AgendaUnit'>")
    assert sx_output_after._weight == healer_agenda_x._weight
    assert (
        sx_output_after._idearoot._parent_road == healer_agenda_x._idearoot._parent_road
    )
    assert (
        sx_output_after._idearoot._acptfactunits
        == healer_agenda_x._idearoot._acptfactunits
    )
    assert sx_output_after._idearoot == healer_agenda_x._idearoot


def test_healer_get_remelded_output_agenda_with1DigestedAgenda(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    env_dir = get_temp_clerkunit_dir()
    yao_clerk = clerkunit_shop(yao_text, env_dir, get_temp_economy_id())
    yao_clerk.create_core_dir_and_files()
    x_agenda_output_before = yao_clerk.get_remelded_output_agenda()
    assert str(type(x_agenda_output_before)).find(".agenda.AgendaUnit'>")
    assert x_agenda_output_before._healer == yao_text
    assert x_agenda_output_before._idearoot._label == get_temp_economy_id()
    input_agenda = example_healers_get_2node_agenda()
    input_agenda.meld(input_agenda)
    input_idearoot = input_agenda._idearoot
    input_b_idea = input_idearoot.get_kid("B")
    assert input_b_idea._agenda_economy_id == get_temp_economy_id()
    yao_clerk.set_depot_agenda(x_agenda=input_agenda, depotlink_type="blind_trust")

    # WHEN
    new_output_agenda = yao_clerk.get_remelded_output_agenda()

    # THEN
    assert str(type(new_output_agenda)).find(".agenda.AgendaUnit'>")

    assert new_output_agenda._weight == 0
    assert new_output_agenda._weight != input_agenda._weight
    assert new_output_agenda._economy_id == input_agenda._economy_id
    sx_idearoot = new_output_agenda._idearoot
    assert sx_idearoot._agenda_economy_id == input_idearoot._agenda_economy_id
    assert sx_idearoot._parent_road == input_idearoot._parent_road
    assert sx_idearoot._acptfactunits == input_idearoot._acptfactunits
    new_output_agenda_b_idea = sx_idearoot.get_kid("B")
    assert new_output_agenda_b_idea._parent_road == input_b_idea._parent_road
    assert (
        new_output_agenda_b_idea._agenda_economy_id == input_b_idea._agenda_economy_id
    )
    assert new_output_agenda._idearoot._kids == input_agenda._idearoot._kids
    assert sx_idearoot._kids_total_weight == input_idearoot._kids_total_weight
    assert sx_idearoot == input_idearoot
    assert new_output_agenda._healer != input_agenda._healer
    assert new_output_agenda != input_agenda


# def test_healer_set_digested_agenda_with2Groups(clerk_dir_setup_cleanup):
#     # GIVEN
#     env_dir = get_temp_clerkunit_dir()
#     x_clerk = clerkunit_shop(pid="test8", env_dir=env_dir)
#     x_agenda_output_before = x_clerk.get_remelded_output_agenda()
#     assert str(type(x_agenda_output_before)).find(".agenda.AgendaUnit'>")
#     assert x_agenda_output_before._groups == {}
#     assert x_agenda_output_before._partys == {}
#     assert x_agenda_output_before._acptfacts == {}

#     src1 = "test1"
#     src1_road = f"{src1}"
#     s1 = agendaunit_shop(_healer=src1)

#     ceci_text = "Ceci"
#     s1.set_partyunit(partyunit=PartyUnit(pid=ceci_text))
#     swim_text = "swimmers"
#     swim_group = BraUnit(pid=swim_text)
#     swim_group.set_partylink(partylink=partylink_shop(pid=ceci_text))
#     s1.set_groupunit(y_groupunit=swim_group)

#     yaya_text = "yaya"
#     yaya_road = f"{src1},{yaya_text}"
#     s1.add_idea(ideaunit_shop(yaya_text), parent_road=src1_road)
#     s1.set_acptfact(base=yaya_road, acptfact=yaya_road)

#     assert s1._groups.get(swim_text).pid == swim_text
#     assert s1._partys.get(ceci_text).pid == ceci_text
#     assert s1._idearoot._label == src1
#     assert s1._acptfacts.get(yaya_road).base == yaya_road

#     # WHEN
#     x_clerk.set_single_digested_agenda(_agenda_healer="test1", digest_agenda_x=s1)
#     new_output_agenda = x_clerk.get_remelded_output_agenda()

#     # THEN
#     assert str(type(new_output_agenda)).find(".agenda.AgendaUnit'>")
#     assert new_output_agenda._acptfacts == s1._acptfacts
#     assert new_output_agenda._partys == s1._partys
#     assert new_output_agenda._groups == s1._groups
#     assert new_output_agenda._weight == s1._weight
#     assert new_output_agenda._weight == s1._weight
#     assert new_output_agenda._idearoot._parent_road == s1._idearoot._parent_road
#     assert new_output_agenda._idearoot._acptfactunits == s1._idearoot._acptfactunits
#     assert new_output_agenda._idearoot._kids == s1._idearoot._kids
#     assert new_output_agenda._idearoot._kids_total_weight == s1._idearoot._kids_total_weight
#     assert new_output_agenda._idearoot == s1._idearoot
#     assert new_output_agenda._label != s1._label
#     assert new_output_agenda != s1


def test_healer_contract_agenda_CorrectlysHasOriginLinksWithHealerAsSource(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    # clerkunit with contract_agenda and no other depot agendas
    yao_text = "Yao"
    contract_origin_weight = 1
    yao_originunit = originunit_shop()
    yao_originunit.set_originlink(pid=yao_text, weight=contract_origin_weight)
    contract_agenda_x = example_healers_get_7nodeJRoot_agenda()
    contract_agenda_x.set_healer(yao_text)

    assert contract_agenda_x._idearoot._originunit == originunit_shop()
    assert contract_agenda_x._idearoot._originunit != yao_originunit

    x_clerk = clerkunit_shop(yao_text, get_temp_clerkunit_dir(), get_temp_economy_id())
    x_clerk.create_core_dir_and_files()
    x_clerk.save_contract_agenda(x_agenda=contract_agenda_x)

    # WHEN
    output_agenda_x = x_clerk.get_remelded_output_agenda()

    # THEN
    print(f"{output_agenda_x._economy_id=} {output_agenda_x._idearoot._label=}")
    print(f"{output_agenda_x._idearoot._kids.keys()=}")
    assert output_agenda_x._idearoot._originunit == originunit_shop()
    a_road = output_agenda_x.make_road(output_agenda_x._economy_id, "A")
    c_road = output_agenda_x.make_road(output_agenda_x._economy_id, "C")
    d_road = output_agenda_x.make_road(c_road, "D")
    print(f"{d_road=}")
    d_idea = output_agenda_x.get_idea_obj(d_road)
    assert d_idea._originunit == yao_originunit

    print(f"{output_agenda_x._originunit=}")
    assert output_agenda_x._originunit == yao_originunit

    output_originlink = output_agenda_x._originunit._links.get(yao_text)
    assert output_originlink.pid == yao_text
    assert output_originlink.weight == contract_origin_weight
