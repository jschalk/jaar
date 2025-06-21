from src.a12_hub_toolbox.test._util.a12_str import (
    bank_mstr_dir_str,
    bank_ote1_agg_str,
    gut_str,
    job_str,
)


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert gut_str() == "gut"
    assert job_str() == "job"
    assert bank_ote1_agg_str() == "bank_ote1_agg"
    assert bank_mstr_dir_str() == "bank_mstr_dir"
