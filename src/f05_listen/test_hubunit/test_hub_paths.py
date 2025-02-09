from src.f00_instrument.file import create_path
from src.f01_road.jaar_config import (
    get_gifts_folder,
    get_test_fiscals_dir,
    get_rootpart_of_keep_dir,
    get_fiscal_title_if_None,
    get_owners_folder,
)
from src.f02_bud.bud import budunit_shop
from src.f05_listen.hub_paths import (
    create_fiscal_json_path,
    fiscal_agenda_list_report_path,
    create_timeline_dir_path,
    create_timepoint_dir_path,
    create_deal_path,
    create_budpoint_dir_path,
    create_events_owner_dir_path,
    create_voice_path,
    create_forecast_path,
)
from src.f05_listen.examples.example_listen_buds import get_budunit_with_4_levels
from src.f05_listen.examples.listen_env import (
    get_listen_temp_env_dir as env_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_create_fiscal_json_path_ReturnObj() -> str:
    # ESTABLISH
    x_fiscal_mstr_dir = env_dir()
    a23_str = "accord23"

    # WHEN
    gen_a23_json_path = create_fiscal_json_path(x_fiscal_mstr_dir, a23_str)

    # THEN
    fiscals_dir = create_path(x_fiscal_mstr_dir, "fiscals")
    a23_path = create_path(fiscals_dir, a23_str)
    expected_a23_json_path = create_path(a23_path, "fiscal.json")
    assert gen_a23_json_path == expected_a23_json_path


def test_fiscal_agenda_list_report_path_ReturnObj() -> str:
    # ESTABLISH
    fiscal_mstr_dir = env_dir()
    a23_str = "accord23"

    # WHEN
    gen_a23_full_report_path = fiscal_agenda_list_report_path(fiscal_mstr_dir, a23_str)

    # THEN
    fiscals_dir = create_path(fiscal_mstr_dir, "fiscals")
    a23_path = create_path(fiscals_dir, a23_str)
    expected_a23_agenda_full_path = create_path(a23_path, "agenda_full_listing.csv")
    assert gen_a23_full_report_path == expected_a23_agenda_full_path


def test_create_timeline_dir_path_ReturnObj() -> str:
    # ESTABLISH
    x_fiscals_dir = env_dir()
    accord23_str = "accord23"
    sue_str = "Sue"

    # WHEN
    timeline_dir = create_timeline_dir_path(x_fiscals_dir, accord23_str, sue_str)

    # THEN
    accord23_dir = create_path(x_fiscals_dir, accord23_str)
    owners_dir = create_path(accord23_dir, get_owners_folder())
    sue_dir = create_path(owners_dir, sue_str)
    expected_timeline_dir = create_path(sue_dir, "timeline")
    assert timeline_dir == expected_timeline_dir


def test_create_timepoint_dir_path_ReturnObj() -> str:
    # ESTABLISH
    x_fiscals_dir = env_dir()
    accord23_str = "accord23"
    sue_str = "Sue"
    timepoint7 = 7

    # WHEN
    generated_timepoint_dir = create_timepoint_dir_path(
        x_fiscals_dir, accord23_str, sue_str, timepoint7
    )

    # THEN
    accord23_dir = create_path(x_fiscals_dir, accord23_str)
    owners_dir = create_path(accord23_dir, get_owners_folder())
    sue_dir = create_path(owners_dir, sue_str)
    timeline_dir = create_path(sue_dir, "timeline")
    expected_timepoint_dir = create_path(timeline_dir, timepoint7)
    assert generated_timepoint_dir == expected_timepoint_dir


def test_create_deal_path_ReturnObj() -> str:
    # ESTABLISH
    x_fiscals_dir = env_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    timepoint7 = 7

    # WHEN
    gen_deal_path = create_deal_path(x_fiscals_dir, a23_str, sue_str, timepoint7)

    # THEN
    accord23_dir = create_path(x_fiscals_dir, a23_str)
    owners_dir = create_path(accord23_dir, get_owners_folder())
    sue_dir = create_path(owners_dir, sue_str)
    timeline_dir = create_path(sue_dir, "timeline")
    timepoint_dir = create_path(timeline_dir, timepoint7)
    expected_deal_path_dir = create_path(timepoint_dir, "deal.json")
    assert gen_deal_path == expected_deal_path_dir


def test_create_budpoint_dir_path_ReturnObj() -> str:
    # ESTABLISH
    x_fiscals_dir = env_dir()
    a23_str = "accord23"
    sue_str = "Sue"
    timepoint7 = 7

    # WHEN
    gen_budpoint_path = create_budpoint_dir_path(
        x_fiscals_dir, a23_str, sue_str, timepoint7
    )

    # THEN
    accord23_dir = create_path(x_fiscals_dir, a23_str)
    owners_dir = create_path(accord23_dir, get_owners_folder())
    sue_dir = create_path(owners_dir, sue_str)
    timeline_dir = create_path(sue_dir, "timeline")
    timepoint_dir = create_path(timeline_dir, timepoint7)
    expected_budpoint_path_dir = create_path(timepoint_dir, "budpoint.json")
    assert gen_budpoint_path == expected_budpoint_path_dir


def test_create_events_owner_dir_path_ReturnObj() -> str:
    # ESTABLISH
    x_fiscals_dir = env_dir()
    accord23_str = "accord23"
    bob_str = "Bob"
    event3 = 3
    event7 = 7

    # WHEN
    gen_a23_e3_bud_path = create_events_owner_dir_path(
        x_fiscals_dir, accord23_str, bob_str, event3
    )

    # THEN
    a23_dir = create_path(x_fiscals_dir, accord23_str)
    a23_events_dir = create_path(a23_dir, "events")
    a23_bob_dir = create_path(a23_events_dir, bob_str)
    a23_bob_e3_dir = create_path(a23_bob_dir, event3)
    # bud_filename = "bud.json"
    # expected_a23_e3_bud_path = create_path(a23_bob_e3_dir, bud_filename)
    assert gen_a23_e3_bud_path == a23_bob_e3_dir


def test_create_voice_path_ReturnObj() -> str:
    # ESTABLISH
    x_fiscals_dir = env_dir()
    a23_str = "accord23"
    bob_str = "Bob"

    # WHEN
    gen_a23_e3_bud_path = create_voice_path(x_fiscals_dir, a23_str, bob_str)

    # THEN
    a23_dir = create_path(x_fiscals_dir, a23_str)
    a23_owners_dir = create_path(a23_dir, "owners")
    a23_bob_dir = create_path(a23_owners_dir, bob_str)
    a23_bob_voice_dir = create_path(a23_bob_dir, "voice")
    expected_a23_bob_voice_json_path = create_path(a23_bob_voice_dir, f"{bob_str}.json")
    # bud_filename = "bud.json"
    # expected_a23_e3_bud_path = create_path(a23_bob_e3_dir, bud_filename)
    assert gen_a23_e3_bud_path == expected_a23_bob_voice_json_path


def test_create_forecast_path_ReturnObj() -> str:
    # ESTABLISH
    x_fiscals_dir = env_dir()
    a23_str = "accord23"
    bob_str = "Bob"

    # WHEN
    gen_a23_e3_bud_path = create_forecast_path(x_fiscals_dir, a23_str, bob_str)

    # THEN
    a23_dir = create_path(x_fiscals_dir, a23_str)
    a23_owners_dir = create_path(a23_dir, "owners")
    a23_bob_dir = create_path(a23_owners_dir, bob_str)
    a23_bob_forecast_dir = create_path(a23_bob_dir, "forecast")
    expected_a23_bob_forecast_json_path = create_path(
        a23_bob_forecast_dir, f"{bob_str}.json"
    )
    # bud_filename = "bud.json"
    # expected_a23_e3_bud_path = create_path(a23_bob_e3_dir, bud_filename)
    assert gen_a23_e3_bud_path == expected_a23_bob_forecast_json_path
