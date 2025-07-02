from src.a10_owner_calc.test._util.a10_str import jmetrics_str, owner_groupunit_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert jmetrics_str() == "jmetrics"
    assert owner_groupunit_str() == "owner_groupunit"
