from src.a12_hub_tools._test_util.a12_str import gut_str, job_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert gut_str() == "gut"
    assert job_str() == "job"
