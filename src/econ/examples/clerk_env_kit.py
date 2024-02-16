# from os import listdir as os_listdir
from src._road.road import WorkerID
from src.agenda.agenda import agendaunit_shop
from src.instrument.file import delete_dir, save_file
from pytest import fixture as pytest_fixture


def get_temp_clerkunit_dir() -> str:
    return f"src/econ/examples/{get_temp_econ_id()}"


def get_temp_econ_id() -> str:
    return "ex_env"


@pytest_fixture()
def clerk_dir_setup_cleanup():
    worker_id_dir = get_temp_clerkunit_dir()
    delete_dir(dir=worker_id_dir)
    yield worker_id_dir
    delete_dir(dir=worker_id_dir)


def create_agenda_file(agenda_clerkunit_dir: str, worker_id: WorkerID):
    x_agenda = agendaunit_shop(_worker_id=worker_id)
    # file_path = f"{agenda_clerkunit_dir}/{x_agenda._worker_id}.json"
    # # if not path.exists(file_path):
    # print(f"{file_path=} {x_agenda._worker_id=}")
    # with open(f"{file_path}", "w") as f:
    #     print(f" saving {x_agenda._worker_id=} to {file_path=}")
    #     f.write(x_agenda.get_json())
    save_file(
        dest_dir=agenda_clerkunit_dir,
        file_name=f"{x_agenda._worker_id}.json",
        file_text=x_agenda.get_json(),
    )
    # print(f"print all {agenda_dir=} {os_listdir(path=agenda_dir)}")
    # for file_path_y in os_listdir(path=agenda_dir):
    #     print(f"{file_path_y}")
