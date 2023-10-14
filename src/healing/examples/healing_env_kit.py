# from lw.contract import ContractUnit
from src.contract.contract import ContractUnit
from src.contract.x_func import (
    single_dir_create_if_null,
    delete_dir as x_func_delete_dir,
    copy_dir,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)
from src.contract.examples.example_contracts import (
    contract_v001 as example_contracts_contract_v001,
    contract_v002 as example_contracts_contract_v002,
    get_contract_1Task_1CE0MinutesRequired_1AcptFact as example_contracts_get_contract_1Task_1CE0MinutesRequired_1AcptFact,
    get_contract_with7amCleanTableRequired as example_contracts_get_contract_with7amCleanTableRequired,
    get_contract_base_time_example as example_contracts_get_contract_base_time_example,
    get_contract_x1_3levels_1required_1acptfacts as example_contracts_get_contract_x1_3levels_1required_1acptfacts,
)

from src.healing.healing import HealingUnit, healingunit_shop
from src.healing.examples.example_healers import (
    get_1node_contract as example_healers_get_1node_contract,
    get_7nodeJRootWithH_contract as example_healers_get_7nodeJRootWithH_contract,
    get_contract_2CleanNodesRandomWeights as example_healers_get_contract_2CleanNodesRandomWeights,
    get_contract_3CleanNodesRandomWeights as example_healers_get_contract_3CleanNodesRandomWeights,
)
from os import listdir as os_listdir, rename as os_rename, path as os_path
from pytest import fixture as pytest_fixture


def get_temp_env_kind():
    return "ex_env04"


def get_temp_env_dir():
    return f"{get_test_healings_dir()}/{get_temp_env_kind()}"


def get_test_healings_dir():
    return "src/healing/examples/healings"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_temp_env_dir()
    x_func_delete_dir(dir=env_dir)
    yield env_dir
    x_func_delete_dir(dir=env_dir)


def create_contract_file_for_healings(healing_dir: str, contract_healer: str):
    contract_x = ContractUnit(_healer=contract_healer)
    contract_dir = f"{healing_dir}/contracts"
    # file_path = f"{contract_dir}/{contract_x._healer}.json"
    # if not path.exists(file_path):
    # print(f"{file_path=} {contract_x._healer=}")

    x_func_save_file(
        dest_dir=contract_dir,
        file_title=f"{contract_x._healer}.json",
        file_text=contract_x.get_json(),
    )


def create_example_healings_list():
    return x_func_dir_files(
        dir_path=get_test_healings_dir(), include_dirs=True, include_files=False
    )


def setup_test_example_environment():
    _delete_and_set_ex3()
    _delete_and_set_ex4()
    _delete_and_set_ex5()
    _delete_and_set_ex6()


def _delete_and_set_ex3():
    healing_kind = "ex3"
    sx = healingunit_shop(kind=healing_kind, healings_dir=get_test_healings_dir())
    x_func_delete_dir(sx.get_object_root_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sx.save_public_contract(contract_x=example_healers_get_1node_contract())
    sx.save_public_contract(
        contract_x=example_contracts_get_contract_1Task_1CE0MinutesRequired_1AcptFact()
    )
    sx.save_public_contract(contract_x=example_contracts_contract_v001())
    sx.save_public_contract(contract_x=example_contracts_contract_v002())

    # sx.set_healer(healer_x=healerunit_shop(title="w1", env_dir=sx.get_object_root_dir()))
    # sx.set_healer(healer_x=healerunit_shop(title="w2", env_dir=sx.get_object_root_dir()))
    xia_text = "Xia"
    sx.create_new_healerunit(healer_title=xia_text)
    healer_text = "Mycontract"
    sx.set_healer_depotlink(
        xia_text, contract_healer=healer_text, depotlink_type="blind_trust"
    )
    # w1_obj = sx.get_healer_obj(title=w1_text)

    bob_text = "bob wurld"
    create_contract_file_for_healings(sx.get_object_root_dir(), bob_text)
    # print(f"create contract_list {w1_text=}")
    sx.create_depotlink_to_generated_contract(
        healer_title=xia_text, contract_healer=bob_text, depotlink_type="ignore"
    )
    land_text = "tim wurld"
    create_contract_file_for_healings(
        healing_dir=sx.get_object_root_dir(), contract_healer=land_text
    )
    sx.create_depotlink_to_generated_contract(
        healer_title=xia_text, contract_healer=land_text, depotlink_type="blind_trust"
    )
    # sx.create_depotlink_to_generated_contract(healer_title=w1_text, contract_healer="test9")
    # sx.create_depotlink_to_generated_contract(healer_title=w1_text, contract_healer="Bobs contract")
    sx.save_healer_file(healer_title=xia_text)
    # print(f"WHAT WHAT {sx.get_object_root_dir()}")
    # print(f"WHAT WHAT {sx.get_object_root_dir()}/healers/w1/w1.json")
    # file_text = x_func_open_file(
    #     dest_dir=f"{sx.get_object_root_dir}/healers/w1", file_title="w1.json"
    # )
    # print(f"{file_text=}")
    # print(f"{len(sx._healerunits.get(w1_text)._depotlinks)=}")
    # print(f"{sx._healerunits.get(w1_text)._depotlinks.get(bob_text)=}")
    # print(f"{sx._healerunits.get(w1_text).get_json=}")

    w2_text = "w2"
    sx.create_new_healerunit(
        healer_title=w2_text
    )  # , env_dir=sx.get_object_root_dir())
    sx.save_healer_file(healer_title=w2_text)


def _delete_and_set_ex4():
    healing_kind = "ex4"
    sx = healingunit_shop(kind=healing_kind, healings_dir=get_test_healings_dir())
    x_func_delete_dir(sx.get_object_root_dir())
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.save_public_contract(example_healers_get_7nodeJRootWithH_contract())
    sx.save_public_contract(example_contracts_get_contract_with7amCleanTableRequired())
    sx.save_public_contract(example_contracts_get_contract_base_time_example())
    sx.save_public_contract(
        example_contracts_get_contract_x1_3levels_1required_1acptfacts()
    )


def _delete_and_set_ex5():
    healing_kind = "ex5"
    sx = healingunit_shop(kind=healing_kind, healings_dir=get_test_healings_dir())
    x_func_delete_dir(sx.get_object_root_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    # ethical code ernie
    # ethical code steve
    # ethical code Jessica
    # ethical code Francine
    # ethical code Clay
    contract_1 = example_healers_get_contract_2CleanNodesRandomWeights(_healer="ernie")
    contract_2 = example_healers_get_contract_2CleanNodesRandomWeights(_healer="steve")
    contract_3 = example_healers_get_contract_2CleanNodesRandomWeights(
        _healer="jessica"
    )
    contract_4 = example_healers_get_contract_2CleanNodesRandomWeights(
        _healer="francine"
    )
    contract_5 = example_healers_get_contract_2CleanNodesRandomWeights(_healer="clay")

    sx.save_public_contract(contract_x=contract_1)
    sx.save_public_contract(contract_x=contract_2)
    sx.save_public_contract(contract_x=contract_3)
    sx.save_public_contract(contract_x=contract_4)
    sx.save_public_contract(contract_x=contract_5)

    sx.create_new_healerunit(healer_title=contract_1._healer)
    sx.create_new_healerunit(healer_title=contract_2._healer)
    sx.create_new_healerunit(healer_title=contract_3._healer)
    sx.create_new_healerunit(healer_title=contract_4._healer)
    sx.create_new_healerunit(healer_title=contract_5._healer)

    sx.set_healer_depotlink(
        contract_1._healer, contract_2._healer, "blind_trust", 3, 3.1
    )
    sx.set_healer_depotlink(
        contract_1._healer, contract_3._healer, "blind_trust", 7, 7.1
    )
    sx.set_healer_depotlink(
        contract_1._healer, contract_4._healer, "blind_trust", 4, 4.1
    )
    sx.set_healer_depotlink(
        contract_1._healer, contract_5._healer, "blind_trust", 5, 5.1
    )

    sx.set_healer_depotlink(
        contract_2._healer, contract_1._healer, "blind_trust", 3, 3.1
    )
    sx.set_healer_depotlink(
        contract_2._healer, contract_3._healer, "blind_trust", 7, 7.1
    )
    sx.set_healer_depotlink(
        contract_2._healer, contract_4._healer, "blind_trust", 4, 4.1
    )
    icx = example_healers_get_contract_3CleanNodesRandomWeights()
    sx.set_healer_depotlink(
        contract_2._healer, contract_5._healer, "ignore", 5, 5.1, icx
    )

    sx.set_healer_depotlink(
        contract_3._healer, contract_1._healer, "blind_trust", 3, 3.1
    )
    sx.set_healer_depotlink(
        contract_3._healer, contract_2._healer, "blind_trust", 7, 7.1
    )
    sx.set_healer_depotlink(
        contract_3._healer, contract_4._healer, "blind_trust", 4, 4.1
    )
    sx.set_healer_depotlink(
        contract_3._healer, contract_5._healer, "blind_trust", 5, 5.1
    )

    sx.set_healer_depotlink(
        contract_4._healer, contract_1._healer, "blind_trust", 3, 3.1
    )
    sx.set_healer_depotlink(
        contract_4._healer, contract_2._healer, "blind_trust", 7, 7.1
    )
    sx.set_healer_depotlink(
        contract_4._healer, contract_3._healer, "blind_trust", 4, 4.1
    )
    sx.set_healer_depotlink(
        contract_4._healer, contract_5._healer, "blind_trust", 5, 5.1
    )

    sx.set_healer_depotlink(
        contract_5._healer, contract_1._healer, "blind_trust", 3, 3.1
    )
    sx.set_healer_depotlink(
        contract_5._healer, contract_2._healer, "blind_trust", 7, 7.1
    )
    sx.set_healer_depotlink(
        contract_5._healer, contract_3._healer, "blind_trust", 4, 4.1
    )
    sx.set_healer_depotlink(
        contract_5._healer, contract_4._healer, "blind_trust", 5, 5.1
    )

    sx.save_healer_file(healer_title=contract_1._healer)
    sx.save_healer_file(healer_title=contract_2._healer)
    sx.save_healer_file(healer_title=contract_3._healer)
    sx.save_healer_file(healer_title=contract_4._healer)
    sx.save_healer_file(healer_title=contract_5._healer)


def _delete_and_set_ex6():
    healing_kind = "ex6"
    sx = healingunit_shop(kind=healing_kind, healings_dir=get_test_healings_dir())
    x_func_delete_dir(sx.get_object_root_dir())
    sx.create_dirs_if_null(in_memory_bank=False)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_contract = ContractUnit(_healer=sal_text)
    sal_contract.add_partyunit(title=bob_text, creditor_weight=2)
    sal_contract.add_partyunit(title=tom_text, creditor_weight=7)
    sal_contract.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=sal_contract)

    bob_contract = ContractUnit(_healer=bob_text)
    bob_contract.add_partyunit(title=sal_text, creditor_weight=3)
    bob_contract.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_contract(contract_x=bob_contract)

    tom_contract = ContractUnit(_healer=tom_text)
    tom_contract.add_partyunit(title=sal_text, creditor_weight=2)
    sx.save_public_contract(contract_x=tom_contract)

    ava_contract = ContractUnit(_healer=ava_text)
    ava_contract.add_partyunit(title=elu_text, creditor_weight=2)
    sx.save_public_contract(contract_x=ava_contract)

    elu_contract = ContractUnit(_healer=elu_text)
    elu_contract.add_partyunit(title=ava_text, creditor_weight=19)
    elu_contract.add_partyunit(title=sal_text, creditor_weight=1)
    sx.save_public_contract(contract_x=elu_contract)

    sx.refresh_bank_metrics()
    sx.set_river_sphere_for_contract(contract_healer=sal_text, max_flows_count=100)


def create_example_healing(healing_kind: str):
    sx = healingunit_shop(kind=healing_kind, healings_dir=get_test_healings_dir())
    sx.create_dirs_if_null(in_memory_bank=True)


def delete_dir_example_healing(healing_obj: HealingUnit):
    x_func_delete_dir(healing_obj.get_object_root_dir())


def rename_example_healing(healing_obj: HealingUnit, new_title):
    # base_dir = healing_obj.get_object_root_dir()
    base_dir = "src/healing/examples/healings"
    src_dir = f"{base_dir}/{healing_obj.kind}"
    dst_dir = f"{base_dir}/{new_title}"
    os_rename(src=src_dir, dst=dst_dir)
    healing_obj.set_healingunit_kind(kind=new_title)


class InvalidHealingCopyException(Exception):
    pass


def copy_evaluation_healing(src_kind: str, dest_kind: str):
    base_dir = "src/healing/examples/healings"
    new_dir = f"{base_dir}/{dest_kind}"
    if os_path.exists(new_dir):
        raise InvalidHealingCopyException(
            f"Cannot copy healing to '{new_dir}' directory because '{new_dir}' exists."
        )
    # base_dir = healing_obj.get_object_root_dir()
    src_dir = f"{base_dir}/{src_kind}"
    dest_dir = f"{base_dir}/{dest_kind}"
    copy_dir(src_dir=src_dir, dest_dir=dest_dir)
