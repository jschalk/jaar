from src.f00_instrument.file import create_path
from src.f01_road.jaar_config import (
    get_gifts_folder,
    get_test_fiscals_dir,
    get_rootpart_of_keep_dir,
    get_fiscal_title_if_None,
    get_owners_folder,
)
from src.f02_bud.bud import budunit_shop
from src.f05_listen.hub_tool import create_timeline_dir, create_deal_path
from src.f05_listen.examples.example_listen_buds import get_budunit_with_4_levels
from src.f05_listen.examples.listen_env import (
    get_listen_temp_env_dir as env_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_create_timeline_dir_ReturnObj() -> str:
    # ESTABLISH
    x_fiscals_dir = env_dir()
    accord23_str = ("accord23",)
    sue_str = "Sue"

    # WHEN
    timeline_dir = create_timeline_dir(x_fiscals_dir, accord23_str, sue_str)

    # THEN
    accord23_dir = create_path(x_fiscals_dir, accord23_str)
    owners_dir = create_path(accord23_dir, get_owners_folder())
    sue_dir = create_path(owners_dir, sue_str)
    expected_timeline_dir = create_path(sue_dir, "timeline")
    assert timeline_dir == expected_timeline_dir


def test_create_deal_path_ReturnObj() -> str:
    # ESTABLISH
    x_fiscals_dir = env_dir()
    a23_str = ("accord23",)
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
