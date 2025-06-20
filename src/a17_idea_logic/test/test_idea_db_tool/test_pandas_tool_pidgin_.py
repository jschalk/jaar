from copy import deepcopy as copy_deepcopy
from pandas import DataFrame
from pandas.testing import assert_frame_equal as pandas_assert_frame_equal
from src.a01_term_logic.rope import create_rope, to_rope
from src.a02_finance_logic.test._util.a02_str import vow_label_str
from src.a06_plan_logic.test._util.a06_str import (
    NameTerm_str,
    acct_name_str,
    credit_score_str,
    rcontext_str,
)
from src.a16_pidgin_logic.map import namemap_shop
from src.a16_pidgin_logic.pidgin import pidginunit_shop
from src.a16_pidgin_logic.test._util.example_pidgins import (
    get_casa_maison_pidginunit_set_by_label,
    get_casa_maison_pidginunit_set_by_otx2inx,
    get_casa_maison_rope_inx_dt,
    get_casa_maison_rope_otx_dt,
)
from src.a17_idea_logic.idea_db_tool import (
    get_dataframe_pidginable_columns,
    translate_all_columns_dataframe,
    translate_single_column_dataframe,
)


def test_get_dataframe_pidginable_columns_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    x_dt = DataFrame()
    assert get_dataframe_pidginable_columns(x_dt) == set()
    x_dt = DataFrame(columns=[acct_name_str()])
    assert get_dataframe_pidginable_columns(x_dt) == {acct_name_str()}
    x_dt = DataFrame(columns=[acct_name_str(), credit_score_str()])
    assert get_dataframe_pidginable_columns(x_dt) == {acct_name_str()}
    x_dt = DataFrame(columns=[rcontext_str(), acct_name_str(), credit_score_str()])
    assert get_dataframe_pidginable_columns(x_dt) == {acct_name_str(), rcontext_str()}
    x_dt = DataFrame(columns=["calc_swim", acct_name_str(), credit_score_str()])
    assert get_dataframe_pidginable_columns(x_dt) == {acct_name_str()}


def test_translate_single_column_dataframe_ReturnsObj_Scenario0_AcctName_EmptyDataFrame():
    # ESTABLISH
    acct_name_mapunit = namemap_shop()
    empty_dt = DataFrame(columns=[acct_name_str()])

    # WHEN
    gen_dt = translate_single_column_dataframe(
        empty_dt, acct_name_mapunit, acct_name_str()
    )

    # THEN
    pandas_assert_frame_equal(gen_dt, empty_dt)


def test_translate_single_column_dataframe_SetsParameterAttrs_Scenario0_AcctName_5rows():
    # ESTABLISH
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    acct_name_mapunit = namemap_shop()
    acct_name_mapunit.set_otx2inx(xio_otx, xio_inx)
    acct_name_mapunit.set_otx2inx(sue_otx, sue_inx)
    acct_name_mapunit.set_otx2inx(bob_otx, bob_inx)
    otx_dt = DataFrame(columns=[acct_name_str()])
    otx_dt.loc[0] = [zia_otx]
    otx_dt.loc[1] = [sue_otx]
    otx_dt.loc[2] = [bob_otx]
    otx_dt.loc[3] = [xio_otx]
    otx_dt = otx_dt.reset_index(drop=True)
    old_otx_dt = copy_deepcopy(otx_dt)
    print(f"{otx_dt=}")

    # WHEN
    translate_single_column_dataframe(otx_dt, acct_name_mapunit, acct_name_str())

    # THEN
    assert otx_dt.iloc[0][acct_name_str()] == zia_otx
    assert otx_dt.iloc[1][acct_name_str()] == sue_inx
    assert otx_dt.to_csv() != old_otx_dt.to_csv()
    inx_dt = DataFrame(columns=[acct_name_str()])
    inx_dt.loc[0] = zia_otx
    inx_dt.loc[1] = sue_inx
    inx_dt.loc[2] = bob_inx
    inx_dt.loc[3] = xio_inx
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    pandas_assert_frame_equal(otx_dt, inx_dt)
    assert otx_dt.to_csv() == inx_dt.to_csv()


def test_translate_single_column_dataframe_SetsParameterAttrs_Scenario1_AcctName_5rowsMultipleColumns():
    # ESTABLISH
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    acct_name_mapunit = namemap_shop()
    acct_name_mapunit.set_otx2inx(xio_otx, xio_inx)
    acct_name_mapunit.set_otx2inx(sue_otx, sue_inx)
    acct_name_mapunit.set_otx2inx(bob_otx, bob_inx)
    otx_dt = DataFrame(columns=[vow_label_str(), acct_name_str(), credit_score_str()])
    otx_dt.loc[0] = ["ZZ", zia_otx, 12]
    otx_dt.loc[1] = ["ZZ", sue_otx, 12]
    otx_dt.loc[2] = ["ZZ", bob_otx, 12]
    otx_dt.loc[3] = ["ZZ", xio_otx, 12]
    otx_dt = otx_dt.reset_index(drop=True)
    old_otx_dt = copy_deepcopy(otx_dt)
    print(f"{otx_dt=}")

    # WHEN
    translate_single_column_dataframe(otx_dt, acct_name_mapunit, acct_name_str())

    # THEN
    assert otx_dt.iloc[0][acct_name_str()] == zia_otx
    assert otx_dt.iloc[1][acct_name_str()] == sue_inx
    assert otx_dt.to_csv() != old_otx_dt.to_csv()
    inx_dt = DataFrame(columns=[vow_label_str(), acct_name_str(), credit_score_str()])
    inx_dt.loc[0] = ["ZZ", zia_otx, 12]
    inx_dt.loc[1] = ["ZZ", sue_inx, 12]
    inx_dt.loc[2] = ["ZZ", bob_inx, 12]
    inx_dt.loc[3] = ["ZZ", xio_inx, 12]
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    assert otx_dt.to_csv() == inx_dt.to_csv()
    pandas_assert_frame_equal(otx_dt, inx_dt)


def test_translate_all_columns_dataframe_SetsParameterAttrs_Scenario0_AcctName():
    # ESTABLISH
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    otx_dt = DataFrame(columns=[vow_label_str(), acct_name_str(), credit_score_str()])
    otx_dt.loc[0] = ["ZZ", zia_otx, 12]
    otx_dt.loc[1] = ["ZZ", sue_otx, 12]
    otx_dt.loc[2] = ["ZZ", bob_otx, 12]
    otx_dt.loc[3] = ["ZZ", xio_otx, 12]
    otx_dt = otx_dt.reset_index(drop=True)
    old_otx_dt = copy_deepcopy(otx_dt)
    print(f"{otx_dt=}")

    # WHEN
    translate_all_columns_dataframe(otx_dt, None)

    # THEN
    assert otx_dt.iloc[0][acct_name_str()] == zia_otx
    assert otx_dt.iloc[1][acct_name_str()] == sue_otx
    pandas_assert_frame_equal(otx_dt, old_otx_dt)
    inx_dt = DataFrame(columns=[vow_label_str(), acct_name_str(), credit_score_str()])
    inx_dt.loc[0] = ["ZZ", zia_otx, 12]
    inx_dt.loc[1] = ["ZZ", sue_otx, 12]
    inx_dt.loc[2] = ["ZZ", bob_otx, 12]
    inx_dt.loc[3] = ["ZZ", xio_otx, 12]
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    assert otx_dt.to_csv() == inx_dt.to_csv()
    pandas_assert_frame_equal(otx_dt, inx_dt)


def test_translate_all_columns_dataframe_SetsParameterAttrs_Scenario1_AcctName():
    # ESTABLISH
    yao_str = "Yao"
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    yao_pidginunit = pidginunit_shop(yao_str)
    yao_pidginunit.set_otx2inx(NameTerm_str(), xio_otx, xio_inx)
    yao_pidginunit.set_otx2inx(NameTerm_str(), sue_otx, sue_inx)
    yao_pidginunit.set_otx2inx(NameTerm_str(), bob_otx, bob_inx)
    otx_dt = DataFrame(columns=[vow_label_str(), acct_name_str(), credit_score_str()])
    otx_dt.loc[0] = ["ZZ", zia_otx, 12]
    otx_dt.loc[1] = ["ZZ", sue_otx, 12]
    otx_dt.loc[2] = ["ZZ", bob_otx, 12]
    otx_dt.loc[3] = ["ZZ", xio_otx, 12]
    otx_dt = otx_dt.reset_index(drop=True)
    old_otx_dt = copy_deepcopy(otx_dt)
    print(f"{otx_dt=}")

    # WHEN
    translate_all_columns_dataframe(otx_dt, yao_pidginunit)

    # THEN
    assert otx_dt.iloc[0][acct_name_str()] == zia_otx
    assert otx_dt.iloc[1][acct_name_str()] == sue_inx
    assert otx_dt.to_csv() != old_otx_dt.to_csv()
    inx_dt = DataFrame(columns=[vow_label_str(), acct_name_str(), credit_score_str()])
    inx_dt.loc[0] = ["ZZ", zia_otx, 12]
    inx_dt.loc[1] = ["ZZ", sue_inx, 12]
    inx_dt.loc[2] = ["ZZ", bob_inx, 12]
    inx_dt.loc[3] = ["ZZ", xio_inx, 12]
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    assert otx_dt.to_csv() == inx_dt.to_csv()
    pandas_assert_frame_equal(otx_dt, inx_dt)


def test_translate_all_columns_dataframe_SetsParameterAttrs_Scenario2_RodeUnit_get_casa_maison_pidginunit_set_by_otx2inx():
    # ESTABLISH
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    otx_accord45_rope = to_rope(otx_accord45_str)
    inx_accord87_rope = to_rope(inx_accord87_str)
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_rope = create_rope(otx_accord45_str, casa_otx_str)
    casa_inx_rope = create_rope(inx_accord87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_rope = create_rope(casa_otx_rope, clean_otx_str)
    clean_inx_rope = create_rope(casa_inx_rope, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_rope = create_rope(clean_otx_rope, sweep_str)
    sweep_inx_rope = create_rope(clean_inx_rope, sweep_str)
    yao_pidginunit = get_casa_maison_pidginunit_set_by_otx2inx()
    otx_dt = get_casa_maison_rope_otx_dt()
    old_otx_dt = copy_deepcopy(otx_dt)
    assert otx_dt.iloc[0][rcontext_str()] == otx_accord45_rope
    assert otx_dt.iloc[1][rcontext_str()] == casa_otx_rope
    assert otx_dt.iloc[2][rcontext_str()] == clean_otx_rope
    assert otx_dt.iloc[3][rcontext_str()] == sweep_otx_rope
    print(f"{otx_dt=}")

    # WHEN
    translate_all_columns_dataframe(otx_dt, yao_pidginunit)

    # THEN
    assert otx_dt.iloc[0][rcontext_str()] == inx_accord87_rope
    assert otx_dt.iloc[1][rcontext_str()] == casa_inx_rope
    assert otx_dt.iloc[2][rcontext_str()] == clean_inx_rope
    assert otx_dt.iloc[3][rcontext_str()] == sweep_inx_rope
    assert otx_dt.to_csv() != old_otx_dt.to_csv()
    inx_dt = get_casa_maison_rope_inx_dt()
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    assert otx_dt.to_csv() == inx_dt.to_csv()
    pandas_assert_frame_equal(otx_dt, inx_dt)


def test_translate_all_columns_dataframe_SetsParameterAttrs_Scenario3_RodeUnit_get_casa_maison_pidginunit_set_by_label():
    # ESTABLISH
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    otx_accord45_rope = to_rope(otx_accord45_str)
    inx_accord87_rope = to_rope(inx_accord87_str)
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_rope = create_rope(otx_accord45_str, casa_otx_str)
    casa_inx_rope = create_rope(inx_accord87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_rope = create_rope(casa_otx_rope, clean_otx_str)
    clean_inx_rope = create_rope(casa_inx_rope, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_rope = create_rope(clean_otx_rope, sweep_str)
    sweep_inx_rope = create_rope(clean_inx_rope, sweep_str)
    yao_pidginunit = get_casa_maison_pidginunit_set_by_label()
    # print(f"{yao_pidginunit=}")
    otx_dt = get_casa_maison_rope_otx_dt()
    old_otx_dt = copy_deepcopy(otx_dt)
    assert otx_dt.iloc[0][rcontext_str()] == otx_accord45_rope
    assert otx_dt.iloc[1][rcontext_str()] == casa_otx_rope
    assert otx_dt.iloc[2][rcontext_str()] == clean_otx_rope
    assert otx_dt.iloc[3][rcontext_str()] == sweep_otx_rope
    print(f"Before {otx_dt=}")
    print("")

    # WHEN
    translate_all_columns_dataframe(otx_dt, yao_pidginunit)

    # THEN
    print("")
    print(f"after  {otx_dt=}")
    assert otx_dt.iloc[0][rcontext_str()] == inx_accord87_rope
    assert otx_dt.iloc[1][rcontext_str()] == casa_inx_rope
    assert otx_dt.iloc[2][rcontext_str()] == clean_inx_rope
    assert otx_dt.iloc[3][rcontext_str()] == sweep_inx_rope
    assert otx_dt.to_csv() != old_otx_dt.to_csv()
    inx_dt = get_casa_maison_rope_inx_dt()
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    assert otx_dt.to_csv() == inx_dt.to_csv()
    pandas_assert_frame_equal(otx_dt, inx_dt)
