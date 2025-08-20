from src.a12_hub_toolbox.test._util.a12_str import gut_str, job_str, moment_mstr_dir_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert gut_str() == "gut"
    assert job_str() == "job"
    assert moment_mstr_dir_str() == "moment_mstr_dir"
