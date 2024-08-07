from src._road.road import (
    default_road_delimiter_if_none,
    create_road_from_nodes,
    create_road,
    get_default_real_id_roadnode as root_label,
)
from src._road.finance import (
    default_bit_if_none,
    default_penny_if_none,
    default_fund_coin_if_none,
    validate_fund_pool,
)
from src._road.jaar_config import (
    get_gifts_folder,
    get_test_reals_dir,
    get_rootpart_of_econ_dir,
    get_real_id_if_None,
)
from src.bud.bud import budunit_shop
from src.listen.hubunit import HubUnit, hubunit_shop, get_econ_path
from src.listen.examples.example_listen_buds import get_budunit_with_4_levels
from src.listen.examples.listen_env import (
    get_listen_temp_env_dir as env_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_get_econ_path_ReturnsCorrectObj():
    # ESTABLISH
    sue_text = "Sue"
    peru_text = "peru"
    sue_hubunit = hubunit_shop(None, real_id=peru_text, owner_id=sue_text)
    texas_text = "texas"
    dallas_text = "dallas"
    elpaso_text = "el paso"
    kern_text = "kern"
    idearoot = get_rootpart_of_econ_dir()
    texas_road = create_road_from_nodes([idearoot, texas_text])
    dallas_road = create_road_from_nodes([idearoot, texas_text, dallas_text])
    elpaso_road = create_road_from_nodes([idearoot, texas_text, elpaso_text])
    kern_road = create_road_from_nodes([idearoot, texas_text, elpaso_text, kern_text])

    # WHEN
    texas_path = get_econ_path(sue_hubunit, texas_road)
    dallas_path = get_econ_path(sue_hubunit, dallas_road)
    elpaso_path = get_econ_path(sue_hubunit, elpaso_road)
    kern_path = get_econ_path(sue_hubunit, kern_road)

    # THEN
    idearoot_dir = f"{sue_hubunit.econs_dir()}/{get_rootpart_of_econ_dir()}"
    print(f"{kern_road=}")
    print(f"{idearoot_dir=}")
    assert texas_path == f"{idearoot_dir}/{texas_text}"
    assert dallas_path == f"{idearoot_dir}/{texas_text}/{dallas_text}"
    assert elpaso_path == f"{idearoot_dir}/{texas_text}/{elpaso_text}"
    assert kern_path == f"{idearoot_dir}/{texas_text}/{elpaso_text}/{kern_text}"

    # WHEN / THEN
    diff_root_texas_road = create_road_from_nodes([peru_text, texas_text])
    diff_root_dallas_road = create_road_from_nodes([peru_text, texas_text, dallas_text])
    diff_root_elpaso_road = create_road_from_nodes([peru_text, texas_text, elpaso_text])
    assert texas_path == get_econ_path(sue_hubunit, diff_root_texas_road)
    assert dallas_path == get_econ_path(sue_hubunit, diff_root_dallas_road)
    assert elpaso_path == get_econ_path(sue_hubunit, diff_root_elpaso_road)


def test_HubUnit_Exists():
    # ESTABLISH / WHEN
    x_hubunit = HubUnit()

    # THEN
    assert x_hubunit.reals_dir is None
    assert x_hubunit.real_id is None
    assert x_hubunit.owner_id is None
    assert x_hubunit.econ_road is None
    assert x_hubunit.road_delimiter is None
    assert x_hubunit.fund_pool is None
    assert x_hubunit.fund_coin is None
    assert x_hubunit.bit is None
    assert x_hubunit.penny is None
    assert x_hubunit.econ_money_magnitude is None


def test_HubUnit_RaisesError_econ_road_DoesNotExist():
    # ESTABLISH
    bob_text = "Bob"
    bob_hubunit = HubUnit(bob_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_hubunit.econ_dir()
    assert (
        str(excinfo.value)
        == f"HubUnit '{bob_text}' cannot save to econ_dir because it does not have econ_road."
    )


def test_hubunit_shop_ReturnsCorrectObj():
    # ESTABLISH
    x_reals_dir = "src/real/examples"
    x_real_id = "music"
    sue_text = "Sue"
    x_road_delimiter = "/"
    x_fund_pool = 13000
    x_fund_coin = 13
    x_bit = 9
    x_penny = 3
    x_money_magnitude = 900

    # WHEN
    x_hubunit = hubunit_shop(
        reals_dir=x_reals_dir,
        real_id=x_real_id,
        owner_id=sue_text,
        econ_road=None,
        road_delimiter=x_road_delimiter,
        fund_pool=x_fund_pool,
        fund_coin=x_fund_coin,
        bit=x_bit,
        penny=x_penny,
        econ_money_magnitude=x_money_magnitude,
    )

    # THEN
    assert x_hubunit.reals_dir == x_reals_dir
    assert x_hubunit.real_id == x_real_id
    assert x_hubunit.owner_id == sue_text
    assert x_hubunit.road_delimiter == x_road_delimiter
    assert x_hubunit.fund_pool == x_fund_pool
    assert x_hubunit.fund_coin == x_fund_coin
    assert x_hubunit.bit == x_bit
    assert x_hubunit.penny == x_penny
    assert x_hubunit.econ_money_magnitude == x_money_magnitude
    assert x_hubunit.real_dir() == f"{x_reals_dir}/{x_real_id}"
    assert x_hubunit.owners_dir() == f"{x_hubunit.real_dir()}/owners"
    assert x_hubunit.owner_dir() == f"{x_hubunit.owners_dir()}/{sue_text}"
    assert x_hubunit.econs_dir() == f"{x_hubunit.owner_dir()}/econs"
    assert x_hubunit.atoms_dir() == f"{x_hubunit.owner_dir()}/atoms"
    assert x_hubunit.voice_dir() == f"{x_hubunit.owner_dir()}/voice"
    assert x_hubunit.action_dir() == f"{x_hubunit.owner_dir()}/action"
    assert x_hubunit.gifts_dir() == f"{x_hubunit.owner_dir()}/{get_gifts_folder()}"
    assert x_hubunit.voice_file_name() == f"{sue_text}.json"
    x_voice_file_path = f"{x_hubunit.voice_dir()}/{x_hubunit.voice_file_name()}"
    assert x_hubunit.voice_file_path() == x_voice_file_path
    assert x_hubunit.action_file_name() == f"{sue_text}.json"
    x_actionpath = f"{x_hubunit.action_dir()}/{x_hubunit.action_file_name()}"
    assert x_hubunit.action_path() == x_actionpath


def test_hubunit_shop_ReturnsCorrectObjWhenEmpty():
    # ESTABLISH
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)

    # WHEN
    sue_hubunit = hubunit_shop(None, None, sue_text, texas_road)

    # THEN
    assert sue_hubunit.reals_dir == get_test_reals_dir()
    assert sue_hubunit.real_id == get_real_id_if_None()
    assert sue_hubunit.real_dir() == f"{get_test_reals_dir()}/{get_real_id_if_None()}"
    assert sue_hubunit.owner_id == sue_text
    assert sue_hubunit.road_delimiter == default_road_delimiter_if_none()
    assert sue_hubunit.fund_pool == validate_fund_pool()
    assert sue_hubunit.fund_coin == default_fund_coin_if_none()
    assert sue_hubunit.bit == default_bit_if_none()
    assert sue_hubunit.penny == default_penny_if_none()
    assert sue_hubunit.owners_dir() == f"{sue_hubunit.real_dir()}/owners"
    x_hubunit = hubunit_shop(None, None, sue_text)
    assert sue_hubunit.econ_road == texas_road
    assert sue_hubunit.econ_dir() == get_econ_path(x_hubunit, texas_road)
    bob_text = "Bob"
    assert sue_hubunit.dutys_dir() == f"{sue_hubunit.econ_dir()}/dutys"
    assert sue_hubunit.jobs_dir() == f"{sue_hubunit.econ_dir()}/jobs"
    assert sue_hubunit.grades_dir() == f"{sue_hubunit.econ_dir()}/grades"
    sue_dutys_dir = sue_hubunit.dutys_dir()
    sue_jobs_dir = sue_hubunit.jobs_dir()
    sue_grades_dir = sue_hubunit.grades_dir()
    assert sue_hubunit.duty_path(bob_text) == f"{sue_dutys_dir}/{bob_text}.json"
    assert sue_hubunit.job_path(bob_text) == f"{sue_jobs_dir}/{bob_text}.json"
    assert sue_hubunit.grade_path(bob_text) == f"{sue_grades_dir}/{bob_text}.json"
    treasury_file_name = "treasury.db"
    treasury_file_path = f"{sue_hubunit.econ_dir()}/{treasury_file_name}"
    assert sue_hubunit.treasury_file_name() == treasury_file_name
    assert sue_hubunit.treasury_db_path() == treasury_file_path


def test_hubunit_shop_RaisesErrorIf_owner_id_Contains_road_delimiter():
    # ESTABLISH
    slash_text = "/"
    bob_text = f"Bob{slash_text}Sue"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        hubunit_shop(None, None, owner_id=bob_text, road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_HubUnit_save_file_voice_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text)
    assert os_path_exists(sue_hubunit.voice_file_path()) is False

    # WHEN
    sue_hubunit.save_file_voice(file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_hubunit.voice_file_path())


def test_HubUnit_voice_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # ESTABLISH
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text)
    assert sue_hubunit.voice_file_exists() is False

    # WHEN
    sue_hubunit.save_file_voice(file_text="fooboo", replace=True)

    # THEN
    assert sue_hubunit.voice_file_exists()


def test_HubUnit_open_file_voice_OpensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text)
    example_text = "fooboo"
    sue_hubunit.save_file_voice(example_text, replace=True)

    # WHEN / THEN
    assert sue_hubunit.open_file_voice() == example_text


def test_HubUnit_save_file_action_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text)
    assert os_path_exists(sue_hubunit.action_path()) is False

    # WHEN
    sue_hubunit.save_file_action(file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_hubunit.action_path())


def test_HubUnit_action_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # ESTABLISH
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text)
    assert sue_hubunit.action_file_exists() is False

    # WHEN
    sue_hubunit.save_file_action(file_text="fooboo", replace=True)

    # THEN
    assert sue_hubunit.action_file_exists()


def test_HubUnit_open_file_action_OpensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text)
    example_text = "fooboo"
    sue_hubunit.save_file_action(example_text, replace=True)

    # WHEN / THEN
    assert sue_hubunit.open_file_action() == example_text


def test_HubUnit_save_voice_bud_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels()
    sue_text = sue_budunit._owner_id
    real_id = root_label()
    sue_hubunit = hubunit_shop(env_dir(), real_id, sue_text, None)

    print(f"{sue_hubunit.voice_file_path()=}")
    assert sue_hubunit.voice_file_exists() is False

    # WHEN
    sue_hubunit.save_voice_bud(sue_budunit)

    # THEN
    assert sue_hubunit.voice_file_exists()


def test_HubUnit_save_voice_bud_RaisesErrorWhenBud_action_id_IsWrong(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_text = "Sue"

    real_id = root_label()
    sue_hubunit = hubunit_shop(env_dir(), real_id, sue_text, None)

    # WHEN / THEN
    yao_text = "Yao"
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_voice_bud(budunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"BudUnit with owner_id '{yao_text}' cannot be saved as owner_id '{sue_text}''s voice bud."
    )


def test_HubUnit_get_voice_bud_OpensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels()
    sue_text = sue_budunit._owner_id
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, texas_road)
    sue_hubunit.save_voice_bud(sue_budunit)

    # WHEN / THEN
    assert sue_hubunit.get_voice_bud().get_dict() == sue_budunit.get_dict()


def test_HubUnit_save_action_bud_CorrectlySavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels()
    sue_text = sue_budunit._owner_id

    real_id = root_label()
    sue_hubunit = hubunit_shop(env_dir(), real_id, sue_text, None)

    print(f"{sue_hubunit.action_path()=}")
    assert sue_hubunit.action_file_exists() is False

    # WHEN
    sue_hubunit.save_action_bud(sue_budunit)

    # THEN
    assert sue_hubunit.action_file_exists()


def test_HubUnit_get_action_bud_OpensFile(env_dir_setup_cleanup):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels()
    sue_text = sue_budunit._owner_id
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text, texas_road)
    sue_hubunit.save_action_bud(sue_budunit)

    # WHEN / THEN
    assert sue_hubunit.get_action_bud().get_dict() == sue_budunit.get_dict()


def test_HubUnit_get_action_bud_ReturnsNoneIfFileDoesNotExist(env_dir_setup_cleanup):
    # ESTABLISH
    sue_budunit = get_budunit_with_4_levels()
    sue_text = sue_budunit._owner_id
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text)

    # WHEN / THEN
    assert sue_hubunit.get_action_bud() is None


def test_HubUnit_save_action_bud_RaisesErrorWhenBud_action_id_IsWrong(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_text = "Sue"

    real_id = root_label()
    sue_hubunit = hubunit_shop(env_dir(), real_id, sue_text, None)

    # WHEN / THEN
    yao_text = "Yao"
    with pytest_raises(Exception) as excinfo:
        sue_hubunit.save_action_bud(budunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"BudUnit with owner_id '{yao_text}' cannot be saved as owner_id '{sue_text}''s action bud."
    )
