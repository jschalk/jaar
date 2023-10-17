# from lw.deal import DealUnit
from src.deal.deal import DealUnit
from src.deal.x_func import (
    single_dir_create_if_null,
    delete_dir as x_func_delete_dir,
    copy_dir,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)
from src.deal.examples.example_deals import (
    deal_v001 as example_deals_deal_v001,
    deal_v002 as example_deals_deal_v002,
    get_deal_1Task_1CE0MinutesRequired_1AcptFact as example_deals_get_deal_1Task_1CE0MinutesRequired_1AcptFact,
    get_deal_with7amCleanTableRequired as example_deals_get_deal_with7amCleanTableRequired,
    get_deal_base_time_example as example_deals_get_deal_base_time_example,
    get_deal_x1_3levels_1required_1acptfacts as example_deals_get_deal_x1_3levels_1required_1acptfacts,
)

from src.cure.cure import CureUnit, cureunit_shop
from src.cure.examples.example_healers import (
    get_1node_deal as example_healers_get_1node_deal,
    get_7nodeJRootWithH_deal as example_healers_get_7nodeJRootWithH_deal,
    get_deal_2CleanNodesRandomWeights as example_healers_get_deal_2CleanNodesRandomWeights,
    get_deal_3CleanNodesRandomWeights as example_healers_get_deal_3CleanNodesRandomWeights,
)
from os import listdir as os_listdir, rename as os_rename, path as os_path
from pytest import fixture as pytest_fixture


def get_temp_env_handle():
    return "ex_env04"


def get_temp_env_dir():
    return f"{get_test_cures_dir()}/{get_temp_env_handle()}"


def get_test_cures_dir():
    return "src/cure/examples/cures"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_temp_env_dir()
    x_func_delete_dir(dir=env_dir)
    yield env_dir
    x_func_delete_dir(dir=env_dir)


def create_deal_file_for_cures(cure_dir: str, deal_healer: str):
    deal_x = DealUnit(_healer=deal_healer)
    deal_dir = f"{cure_dir}/deals"
    # file_path = f"{deal_dir}/{deal_x._healer}.json"
    # if not path.exists(file_path):
    # print(f"{file_path=} {deal_x._healer=}")

    x_func_save_file(
        dest_dir=deal_dir,
        file_title=f"{deal_x._healer}.json",
        file_text=deal_x.get_json(),
    )


def create_example_cures_list():
    return x_func_dir_files(
        dir_path=get_test_cures_dir(), include_dirs=True, include_files=False
    )


def setup_test_example_environment():
    _delete_and_set_ex3()
    _delete_and_set_ex4()
    _delete_and_set_ex5()
    _delete_and_set_ex6()


def _delete_and_set_ex3():
    cure_handle = "ex3"
    x_cure = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    x_func_delete_dir(x_cure.get_object_root_dir())
    x_cure.create_dirs_if_null(in_memory_bank=True)

    x_cure.save_public_deal(deal_x=example_healers_get_1node_deal())
    x_cure.save_public_deal(
        deal_x=example_deals_get_deal_1Task_1CE0MinutesRequired_1AcptFact()
    )
    x_cure.save_public_deal(deal_x=example_deals_deal_v001())
    x_cure.save_public_deal(deal_x=example_deals_deal_v002())

    # x_cure.set_healer(x_healing=healingunit_shop(title="w1", env_dir=x_cure.get_object_root_dir()))
    # x_cure.set_healer(x_healing=healingunit_shop(title="w2", env_dir=x_cure.get_object_root_dir()))
    xia_text = "Xia"
    x_cure.create_new_healingunit(healing_title=xia_text)
    healer_text = "Mydeal"
    x_cure.set_healer_depotlink(
        xia_text, deal_healer=healer_text, depotlink_type="blind_trust"
    )
    # w1_obj = x_cure.get_healingunit(title=w1_text)

    bob_text = "bob wurld"
    create_deal_file_for_cures(x_cure.get_object_root_dir(), bob_text)
    # print(f"create deal_list {w1_text=}")
    x_cure.create_depotlink_to_generated_deal(
        healing_title=xia_text, deal_healer=bob_text, depotlink_type="ignore"
    )
    land_text = "tim wurld"
    create_deal_file_for_cures(
        cure_dir=x_cure.get_object_root_dir(), deal_healer=land_text
    )
    x_cure.create_depotlink_to_generated_deal(
        healing_title=xia_text, deal_healer=land_text, depotlink_type="blind_trust"
    )
    # x_cure.create_depotlink_to_generated_deal(healing_title=w1_text, deal_healer="test9")
    # x_cure.create_depotlink_to_generated_deal(healing_title=w1_text, deal_healer="Bobs deal")
    x_cure.save_healingunit_file(healing_title=xia_text)
    # print(f"WHAT WHAT {x_cure.get_object_root_dir()}")
    # print(f"WHAT WHAT {x_cure.get_object_root_dir()}/healingunits/w1/w1.json")
    # file_text = x_func_open_file(
    #     dest_dir=f"{x_cure.get_object_root_dir}/healingunits/w1", file_title="w1.json"
    # )
    # print(f"{file_text=}")
    # print(f"{len(x_cure._healingunits.get(w1_text)._depotlinks)=}")
    # print(f"{x_cure._healingunits.get(w1_text)._depotlinks.get(bob_text)=}")
    # print(f"{x_cure._healingunits.get(w1_text).get_json=}")

    w2_text = "w2"
    x_cure.create_new_healingunit(healing_title=w2_text)
    # , env_dir=x_cure.get_object_root_dir())
    x_cure.save_healingunit_file(healing_title=w2_text)


def _delete_and_set_ex4():
    cure_handle = "ex4"
    x_cure = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    x_func_delete_dir(x_cure.get_object_root_dir())
    x_cure.create_dirs_if_null(in_memory_bank=True)
    x_cure.save_public_deal(example_healers_get_7nodeJRootWithH_deal())
    x_cure.save_public_deal(example_deals_get_deal_with7amCleanTableRequired())
    x_cure.save_public_deal(example_deals_get_deal_base_time_example())
    x_cure.save_public_deal(example_deals_get_deal_x1_3levels_1required_1acptfacts())


def _delete_and_set_ex5():
    cure_handle = "ex5"
    x_cure = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    x_func_delete_dir(x_cure.get_object_root_dir())
    x_cure.create_dirs_if_null(in_memory_bank=True)

    # ethical code ernie
    # ethical code steve
    # ethical code Jessica
    # ethical code Francine
    # ethical code Clay
    deal_1 = example_healers_get_deal_2CleanNodesRandomWeights(_healer="ernie")
    deal_2 = example_healers_get_deal_2CleanNodesRandomWeights(_healer="steve")
    deal_3 = example_healers_get_deal_2CleanNodesRandomWeights(_healer="jessica")
    deal_4 = example_healers_get_deal_2CleanNodesRandomWeights(_healer="francine")
    deal_5 = example_healers_get_deal_2CleanNodesRandomWeights(_healer="clay")

    x_cure.save_public_deal(deal_x=deal_1)
    x_cure.save_public_deal(deal_x=deal_2)
    x_cure.save_public_deal(deal_x=deal_3)
    x_cure.save_public_deal(deal_x=deal_4)
    x_cure.save_public_deal(deal_x=deal_5)

    x_cure.create_new_healingunit(healing_title=deal_1._healer)
    x_cure.create_new_healingunit(healing_title=deal_2._healer)
    x_cure.create_new_healingunit(healing_title=deal_3._healer)
    x_cure.create_new_healingunit(healing_title=deal_4._healer)
    x_cure.create_new_healingunit(healing_title=deal_5._healer)

    x_cure.set_healer_depotlink(deal_1._healer, deal_2._healer, "blind_trust", 3, 3.1)
    x_cure.set_healer_depotlink(deal_1._healer, deal_3._healer, "blind_trust", 7, 7.1)
    x_cure.set_healer_depotlink(deal_1._healer, deal_4._healer, "blind_trust", 4, 4.1)
    x_cure.set_healer_depotlink(deal_1._healer, deal_5._healer, "blind_trust", 5, 5.1)

    x_cure.set_healer_depotlink(deal_2._healer, deal_1._healer, "blind_trust", 3, 3.1)
    x_cure.set_healer_depotlink(deal_2._healer, deal_3._healer, "blind_trust", 7, 7.1)
    x_cure.set_healer_depotlink(deal_2._healer, deal_4._healer, "blind_trust", 4, 4.1)
    x_deal = example_healers_get_deal_3CleanNodesRandomWeights()
    x_cure.set_healer_depotlink(
        deal_2._healer, deal_5._healer, "ignore", 5, 5.1, x_deal
    )

    x_cure.set_healer_depotlink(deal_3._healer, deal_1._healer, "blind_trust", 3, 3.1)
    x_cure.set_healer_depotlink(deal_3._healer, deal_2._healer, "blind_trust", 7, 7.1)
    x_cure.set_healer_depotlink(deal_3._healer, deal_4._healer, "blind_trust", 4, 4.1)
    x_cure.set_healer_depotlink(deal_3._healer, deal_5._healer, "blind_trust", 5, 5.1)

    x_cure.set_healer_depotlink(deal_4._healer, deal_1._healer, "blind_trust", 3, 3.1)
    x_cure.set_healer_depotlink(deal_4._healer, deal_2._healer, "blind_trust", 7, 7.1)
    x_cure.set_healer_depotlink(deal_4._healer, deal_3._healer, "blind_trust", 4, 4.1)
    x_cure.set_healer_depotlink(deal_4._healer, deal_5._healer, "blind_trust", 5, 5.1)

    x_cure.set_healer_depotlink(deal_5._healer, deal_1._healer, "blind_trust", 3, 3.1)
    x_cure.set_healer_depotlink(deal_5._healer, deal_2._healer, "blind_trust", 7, 7.1)
    x_cure.set_healer_depotlink(deal_5._healer, deal_3._healer, "blind_trust", 4, 4.1)
    x_cure.set_healer_depotlink(deal_5._healer, deal_4._healer, "blind_trust", 5, 5.1)

    x_cure.save_healingunit_file(healing_title=deal_1._healer)
    x_cure.save_healingunit_file(healing_title=deal_2._healer)
    x_cure.save_healingunit_file(healing_title=deal_3._healer)
    x_cure.save_healingunit_file(healing_title=deal_4._healer)
    x_cure.save_healingunit_file(healing_title=deal_5._healer)


def _delete_and_set_ex6():
    cure_handle = "ex6"
    x_cure = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    x_func_delete_dir(x_cure.get_object_root_dir())
    x_cure.create_dirs_if_null(in_memory_bank=False)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_deal = DealUnit(_healer=sal_text)
    sal_deal.add_partyunit(title=bob_text, creditor_weight=2)
    sal_deal.add_partyunit(title=tom_text, creditor_weight=7)
    sal_deal.add_partyunit(title=ava_text, creditor_weight=1)
    x_cure.save_public_deal(deal_x=sal_deal)

    bob_deal = DealUnit(_healer=bob_text)
    bob_deal.add_partyunit(title=sal_text, creditor_weight=3)
    bob_deal.add_partyunit(title=ava_text, creditor_weight=1)
    x_cure.save_public_deal(deal_x=bob_deal)

    tom_deal = DealUnit(_healer=tom_text)
    tom_deal.add_partyunit(title=sal_text, creditor_weight=2)
    x_cure.save_public_deal(deal_x=tom_deal)

    ava_deal = DealUnit(_healer=ava_text)
    ava_deal.add_partyunit(title=elu_text, creditor_weight=2)
    x_cure.save_public_deal(deal_x=ava_deal)

    elu_deal = DealUnit(_healer=elu_text)
    elu_deal.add_partyunit(title=ava_text, creditor_weight=19)
    elu_deal.add_partyunit(title=sal_text, creditor_weight=1)
    x_cure.save_public_deal(deal_x=elu_deal)

    x_cure.refresh_bank_metrics()
    x_cure.set_river_sphere_for_deal(deal_healer=sal_text, max_flows_count=100)


def create_example_cure(cure_handle: str):
    x_cure = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    x_cure.create_dirs_if_null(in_memory_bank=True)


def delete_dir_example_cure(cure_obj: CureUnit):
    x_func_delete_dir(cure_obj.get_object_root_dir())


def rename_example_cure(cure_obj: CureUnit, new_title):
    # base_dir = cure_obj.get_object_root_dir()
    base_dir = "src/cure/examples/cures"
    src_dir = f"{base_dir}/{cure_obj.handle}"
    dst_dir = f"{base_dir}/{new_title}"
    os_rename(src=src_dir, dst=dst_dir)
    cure_obj.set_cureunit_handle(handle=new_title)


class InvalidCureCopyException(Exception):
    pass


def copy_evaluation_cure(src_handle: str, dest_handle: str):
    base_dir = "src/cure/examples/cures"
    new_dir = f"{base_dir}/{dest_handle}"
    if os_path.exists(new_dir):
        raise InvalidCureCopyException(
            f"Cannot copy cure to '{new_dir}' directory because '{new_dir}' exists."
        )
    # base_dir = cure_obj.get_object_root_dir()
    src_dir = f"{base_dir}/{src_handle}"
    dest_dir = f"{base_dir}/{dest_handle}"
    copy_dir(src_dir=src_dir, dest_dir=dest_dir)
