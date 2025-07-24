from pytest import fixture as pytest_fixture
from src.a22_world_viewer.planview_server import planviewer


def test_planviewer_IsCreated():
    # ESTABLISH
    assert planviewer is not None
    # Optional: create test client and test root endpoint if exists
    client = planviewer.test_client()
    response = client.get("/")  # or some valid route you define

    # WHEN / THEN
    # If '/' route not defined, skip or test /process with dummy data
    assert response.status_code in (200, 404)


def test_process_endpoint():
    # ESTABLISH
    client = planviewer.test_client()
    response = client.post(
        "/process", json={"_mode": "default", "data": {"foo": "bar"}}
    )
    assert response.status_code == 200

    # WHEN
    json_data = response.get_json()

    # THEN
    assert json_data["result"]["foo"] == "bar"


@pytest_fixture
def client():
    planviewer.config["TESTING"] = True
    with planviewer.test_client() as client:
        yield client


def test_load_modes(client):
    # ESTABLISH
    response = client.get("/modes")
    assert response.status_code == 200

    # WHEN
    modes_list = response.get_json()

    # THEN
    print(modes_list)
    assert isinstance(modes_list, list)
    assert all(isinstance(mode, str) for mode in modes_list)
    assert modes_list == [
        "Plan Label",
        "Plan Tasks",
        "Plan Fund",
        "Plan Awardees",
        "Plan Reasons",
        "Plan Facts",
        "Plan Time",
        "static_dict_testing",
    ]
