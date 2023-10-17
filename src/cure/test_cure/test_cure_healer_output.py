from src.oath.examples.example_oaths import (
    oath_v002 as ex_cxs_oath_v002,
)
from src.cure.cure import cureunit_shop
from src.cure.examples.example_healers import (
    get_6node_oath as example_healers_get_6node_oath,
    get_oath_2CleanNodesRandomWeights,
    get_oath_3CleanNodesRandomWeights,
)
from src.cure.examples.cure_env_kit import (
    get_temp_env_handle,
    get_test_cures_dir,
    env_dir_setup_cleanup,
)


def test_cure_get_output_oath_ReturnsCorrectOathObjScenario1(
    env_dir_setup_cleanup,
):
    # GIVEN
    sx = cureunit_shop(handle=get_temp_env_handle(), cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null(in_memory_bank=True)
    input_cx = example_healers_get_6node_oath()
    sx.save_public_oath(input_cx)
    # sx.save_public_oath(ex_cxs_get_oath_1Task_1CE0MinutesRequired_1AcptFact())
    # sx.save_public_oath(ex_cxs_oath_v001())
    xia_text = "Xia"
    sx.create_new_healingunit(healing_title=xia_text)
    sx.set_healer_depotlink(xia_text, input_cx._healer, depotlink_type="blind_trust")
    sx.save_healingunit_file(healing_title=xia_text)
    xia_healer = sx.get_healingunit(title=xia_text)
    # print(f"{xia_healer._isol._partys.keys()=}")

    # WHEN
    output_cx = sx.get_output_oath(healing_title=xia_text)
    # input oath must be melded to itself to create originunits
    input_cx.meld(input_cx)
    input_cx.set_healer(new_healer=xia_text)
    input_cx._originunit.set_originlink(title=xia_text, weight=1)

    # THEN
    a_text = "A"
    c_text = "C"
    c_road = f"{input_cx._cure_handle},{c_text}"
    d_text = "D"
    d_road = f"{c_road},{d_text}"
    print(f"{output_cx._healer=}")
    print(f"{output_cx._idea_dict.keys()=}")
    output_cx_d_idea = output_cx.get_idea_kid(d_road)
    # print(f" {output_cx_d_idea._weight=} {len(input_cx._idearoot._kids)=} ")
    assert output_cx != None
    assert len(input_cx._idearoot._kids) == 2
    # idea_a = output_cx.get_idea_kid(road="A")
    # idea_b = output_cx.get_idea_kid(road="B")
    # for idea_kid_x1 in input_cx._idearoot._kids.values():
    #     print(f"{idea_kid_x1._label=}")
    #     output_cx_counterpart_x1 = output_cx._idearoot._kids.get(idea_kid_x1._label)
    #     for idea_kid_x2 in idea_kid_x1._kids.values():
    #         output_cx_counterpart_x2 = output_cx_counterpart_x1._kids.get(
    #             idea_kid_x2._label
    #         )
    #         print(
    #             f"{idea_kid_x2._label=} {idea_kid_x2._weight=} {output_cx_counterpart_x2._weight=}"
    #         )
    #         # assert output_cx_counterpart_x2 == idea_kid_x2
    #         assert output_cx_counterpart_x2._label == idea_kid_x2._label

    #     print(
    #         f"{idea_kid_x1._label=} {idea_kid_x1._weight=} {output_cx_counterpart_x1._weight=}"
    #     )
    #     assert output_cx_counterpart_x1._label == idea_kid_x1._label
    # assert output_cx._idearoot._kids == input_cx._idearoot._kids
    assert output_cx._idearoot._acptfactunits == {}
    assert output_cx._idearoot._acptfactunits == input_cx._idearoot._acptfactunits
    assert list(output_cx._partys.keys()) == [xia_text, a_text]
    assert output_cx._partys != input_cx._partys
    assert list(output_cx._groups.keys()) == [xia_text, a_text]
    assert output_cx._groups != input_cx._groups
    print(f"{output_cx._originunit=}")
    print(f"{input_cx._originunit=}")
    assert output_cx._originunit == input_cx._originunit

    b_text = "B"
    print(f"{output_cx._idearoot._kids.get(b_text)._originunit=}")
    print(f"{input_cx._idearoot._kids.get(b_text)._originunit=}")
    assert output_cx._idearoot == input_cx._idearoot


def test_cure_get_output_oath_ReturnsCorrectOathObjScenario2(
    env_dir_setup_cleanup,
):
    # GIVEN
    sx = cureunit_shop(handle=get_temp_env_handle(), cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null(in_memory_bank=True)
    cx1 = example_healers_get_6node_oath()
    cx2 = ex_cxs_oath_v002()

    sx.save_public_oath(cx1)
    sx.save_public_oath(cx2)
    # sx.save_public_oath(ex_cxs_get_oath_1Task_1CE0MinutesRequired_1AcptFact())
    # sx.save_public_oath(ex_cxs_oath_v001())
    xia_text = "Xia"
    sx.create_new_healingunit(healing_title=xia_text)
    sx.set_healer_depotlink(xia_text, cx1._healer, depotlink_type="blind_trust")
    sx.set_healer_depotlink(xia_text, cx2._healer, depotlink_type="blind_trust")
    sx.save_healingunit_file(healing_title=xia_text)
    xia_healer = sx.get_healingunit(title=xia_text)
    print(f"{xia_healer._isol._partys.keys()=}")

    # WHEN
    output_cx = sx.get_output_oath(healing_title=xia_text)

    # THEN
    output_cx_d_road = f"{output_cx._cure_handle},C,D"
    output_cx_d_idea = output_cx.get_idea_kid(output_cx_d_road)
    print(f" {output_cx_d_idea._weight=} ")
    assert output_cx != None
    # for idea_kid_x1 in cx1._idearoot._kids.values():
    #     output_cx_counterpart_x1 = output_cx._idearoot._kids.get(idea_kid_x1._label)
    #     for idea_kid_x2 in idea_kid_x1._kids.values():
    #         output_cx_counterpart_x2 = output_cx_counterpart_x1._kids.get(
    #             idea_kid_x2._label
    #         )
    #         print(
    #             f"{idea_kid_x2._label=} {idea_kid_x2._weight=} {output_cx_counterpart_x2._weight=}"
    #         )
    #         # assert output_cx_counterpart_x2 == idea_kid_x2
    #         assert output_cx_counterpart_x2._label == idea_kid_x2._label

    #     print(
    #         f"{idea_kid_x1._label=} {idea_kid_x1._weight=} {output_cx_counterpart_x1._weight=}"
    #     )
    #     assert output_cx_counterpart_x1._label == idea_kid_x1._label
    # assert output_cx._idearoot._kids == cx1._idearoot._kids
    assert len(output_cx._idearoot._acptfactunits) == 9
    assert len(output_cx._idearoot._acptfactunits) == len(cx2._idearoot._acptfactunits)
    assert len(output_cx._partys) == 25
    assert len(output_cx._partys) == len(cx2._partys) + 2 + 1
    assert len(output_cx._groups) == 37
    assert len(output_cx._groups) == len(cx2._groups) + 2 + 1
    assert output_cx._idearoot != cx1._idearoot
    assert output_cx._idearoot != cx2._idearoot


def test_healingunit_refresh_depotlinks_CorrectlyPullsAllPublicOaths(
    env_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_test_cures_dir()
    cure_handle = get_temp_env_handle()
    sx = cureunit_shop(handle=cure_handle, cures_dir=env_dir)
    sx.create_dirs_if_null(in_memory_bank=True)
    # ux = healingunit_shop(title=healer1_text, env_dir=env_dir)

    ernie_text = "ernie"
    jessi_text = "jessi"
    steve_text = "steve"
    ernie_oath = get_oath_2CleanNodesRandomWeights(_healer=ernie_text)
    jessi_oath = get_oath_2CleanNodesRandomWeights(_healer=jessi_text)
    old_steve_cx = get_oath_2CleanNodesRandomWeights(_healer=steve_text)
    sx.save_public_oath(oath_x=ernie_oath)
    sx.save_public_oath(oath_x=jessi_oath)
    sx.save_public_oath(oath_x=old_steve_cx)
    sx.create_new_healingunit(healing_title=ernie_text)
    sx.create_new_healingunit(healing_title=jessi_text)
    # sx.create_new_healingunit(healing_title=steve_text)
    ux_ernie = sx.get_healingunit(title=ernie_text)
    ux_jessi = sx.get_healingunit(title=jessi_text)
    # ux_steve = sx.get_healingunit(title=steve_text)
    ux_ernie.set_depot_oath(oath_x=jessi_oath, depotlink_type="blind_trust")
    ux_ernie.set_depot_oath(oath_x=old_steve_cx, depotlink_type="blind_trust")
    ux_jessi.set_depot_oath(oath_x=ernie_oath, depotlink_type="blind_trust")
    ux_jessi.set_depot_oath(oath_x=old_steve_cx, depotlink_type="blind_trust")
    # ux_steve.set_depot_oath(oath_x=ernie_oath, depotlink_type="blind_trust")
    # ux_steve.set_depot_oath(oath_x=jessi_oath, depotlink_type="blind_trust")
    assert len(ux_ernie._admin.get_remelded_output_oath().get_idea_list()) == 4
    assert len(ux_jessi._admin.get_remelded_output_oath().get_idea_list()) == 4
    # assert len(ux_steve._admin.get_remelded_output_oath().get_idea_list()) == 4
    new_steve_oath = get_oath_3CleanNodesRandomWeights(_healer="steve")
    sx.save_public_oath(oath_x=new_steve_oath)
    # print(f"{env_dir=} {ux._admin._oaths_public_dir=}")
    # for file_title in x_func_dir_files(dir_path=env_dir):
    #     print(f"{ux._admin._oaths_public_dir=} {file_title=}")

    # for file_title in x_func_dir_files(dir_path=ux._admin._oaths_public_dir):
    #     print(f"{ux._admin._oaths_public_dir=} {file_title=}")

    # WHEN
    sx.reload_all_healingunits_src_oathunits()

    # THEN
    assert len(ux_ernie._admin.get_remelded_output_oath().get_idea_list()) == 5
    assert len(ux_jessi._admin.get_remelded_output_oath().get_idea_list()) == 5
