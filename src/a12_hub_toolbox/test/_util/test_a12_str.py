from src.a12_hub_toolbox.test._util.a12_str import coin_mstr_dir_str, gut_str, job_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert gut_str() == "gut"
    assert job_str() == "job"
    assert coin_mstr_dir_str() == "coin_mstr_dir"
