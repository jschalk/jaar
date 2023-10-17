# from os import listdir as os_listdir
from pytest import fixture as pytest_fixture
from src.deal.deal import DealUnit
from src.deal.x_func import delete_dir, save_file as x_func_save_file


def get_temp_healingunit_dir() -> str:
    return f"src/cure/examples/{get_temp_cure_handle()}"


def get_temp_cure_handle() -> str:
    return "ex_env"


@pytest_fixture()
def healer_dir_setup_cleanup():
    healer_dir = get_temp_healingunit_dir()
    delete_dir(dir=healer_dir)
    yield healer_dir
    delete_dir(dir=healer_dir)


def create_deal_file(deal_healingunit_dir: str, deal_healer: str):
    deal_x = DealUnit(_healer=deal_healer)
    # file_path = f"{deal_healingunit_dir}/{deal_x._healer}.json"
    # # if not path.exists(file_path):
    # print(f"{file_path=} {deal_x._healer=}")
    # with open(f"{file_path}", "w") as f:
    #     print(f" saving {deal_x._healer=} to {file_path=}")
    #     f.write(deal_x.get_json())
    x_func_save_file(
        dest_dir=deal_healingunit_dir,
        file_title=f"{deal_x._healer}.json",
        file_text=deal_x.get_json(),
    )
    # print(f"print all {deal_dir=} {os_listdir(path=deal_dir)}")
    # for file_path_y in os_listdir(path=deal_dir):
    #     print(f"{file_path_y}")
