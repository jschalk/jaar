# from os import listdir as os_listdir
from pytest import fixture as pytest_fixture
from src.agenda.agenda import agendaunit_shop
from src.tools.file import delete_dir, save_file


def get_temp_clerkunit_dir() -> str:
    return f"src/economy/examples/{get_temp_economy_id()}"


def get_temp_economy_id() -> str:
    return "ex_env"


@pytest_fixture()
def clerk_dir_setup_cleanup():
    healer_dir = get_temp_clerkunit_dir()
    delete_dir(dir=healer_dir)
    yield healer_dir
    delete_dir(dir=healer_dir)


def create_agenda_file(agenda_clerkunit_dir: str, agenda_healer: str):
    agenda_x = agendaunit_shop(_healer=agenda_healer)
    # file_path = f"{agenda_clerkunit_dir}/{agenda_x._healer}.json"
    # # if not path.exists(file_path):
    # print(f"{file_path=} {agenda_x._healer=}")
    # with open(f"{file_path}", "w") as f:
    #     print(f" saving {agenda_x._healer=} to {file_path=}")
    #     f.write(agenda_x.get_json())
    save_file(
        dest_dir=agenda_clerkunit_dir,
        file_name=f"{agenda_x._healer}.json",
        file_text=agenda_x.get_json(),
    )
    # print(f"print all {agenda_dir=} {os_listdir(path=agenda_dir)}")
    # for file_path_y in os_listdir(path=agenda_dir):
    #     print(f"{file_path_y}")
