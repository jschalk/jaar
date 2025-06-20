from src.a12_hub_toolbox.test._util.a12_str import (
    gut_str,
    job_str,
    vow_mstr_dir_str,
    vow_ote1_agg_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert gut_str() == "gut"
    assert job_str() == "job"
    assert vow_ote1_agg_str() == "vow_ote1_agg"
    assert vow_mstr_dir_str() == "vow_mstr_dir"
