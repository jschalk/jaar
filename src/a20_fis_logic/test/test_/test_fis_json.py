from src.a00_data_toolbox.file_toolbox import create_path
from src.a20_fis_logic.fis import fisunit_shop
from src.a20_fis_logic.test._util.a20_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_FisUnit_get_dict_ReturnsObj_Scenario0MinimalParameters():
    # ESTABLISH
    fiss2_dir = create_path(get_module_temp_dir(), "fiss2")
    five_fis_id = "five"
    x_fis = fisunit_shop(five_fis_id, fiss2_dir)

    # WHEN
    x_fis_dict = x_fis.get_dict()

    # THEN
    assert x_fis_dict
    assert set(x_fis_dict.keys()) == {
        "fis_id",
        "fis_time_pnigh",
    }
    assert x_fis_dict.get("fis_id") == five_fis_id
    assert x_fis_dict.get("fis_time_pnigh") == 0


def test_FisUnit_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    fiss2_dir = create_path(get_module_temp_dir(), "fiss2")
    five_fis_id = "five"
    fis2_time_pnigh = 55
    accord45_str = "accord45"
    fis2_bankunits = {"accord45"}
    x_fis = fisunit_shop(
        fis_id=five_fis_id,
        fiss_dir=fiss2_dir,
        fis_time_pnigh=fis2_time_pnigh,
        _bankunits=fis2_bankunits,
    )

    # WHEN
    x_fis_dict = x_fis.get_dict()

    # THEN
    assert x_fis_dict
    assert x_fis_dict.get("fis_id") == five_fis_id
    assert x_fis_dict.get("fis_time_pnigh") == fis2_time_pnigh
