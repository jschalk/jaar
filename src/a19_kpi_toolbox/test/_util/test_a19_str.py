from src.a19_kpi_toolbox.test._util.a19_str import vow_kpi001_acct_nets_str


def test_str_functions_ReturnsObj():
    # ESTABLISH / WHEN / THEN

    assert vow_kpi001_acct_nets_str() == "vow_kpi001_acct_nets"
