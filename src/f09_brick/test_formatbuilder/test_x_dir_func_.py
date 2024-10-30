from src.f01_road.road import create_road
from src.f04_gift.atom_config import (
    acct_id_str,
    fiscal_id_str,
    credit_belief_str,
    base_str,
    type_AcctID_str,
)
from src.f08_filter.filter import bridgeunit_shop, filterunit_shop
from src.f09_brick.dir_func import (
    filter_single_column_dataframe,
    filter_all_columns_dataframe,
    get_dataframe_filterable_columns,
)
from src.f08_filter.examples.example_filters import (
    get_casa_maison_filterunit_set_by_otx_to_inx,
    get_casa_maison_filterunit_set_by_explicit_label,
    get_casa_maison_road_otx_dt,
    get_casa_maison_road_inx_dt,
)
from pandas import DataFrame
from copy import deepcopy as copy_deepcopy


def test_get_dataframe_filterable_columns_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    x_dt = DataFrame()
    assert get_dataframe_filterable_columns(x_dt) == set()
    x_dt = DataFrame(columns=[acct_id_str()])
    assert get_dataframe_filterable_columns(x_dt) == {acct_id_str()}
    x_dt = DataFrame(columns=[acct_id_str(), credit_belief_str()])
    assert get_dataframe_filterable_columns(x_dt) == {acct_id_str()}
    x_dt = DataFrame(columns=[base_str(), acct_id_str(), credit_belief_str()])
    assert get_dataframe_filterable_columns(x_dt) == {acct_id_str(), base_str()}
    x_dt = DataFrame(columns=["calc_swim", acct_id_str(), credit_belief_str()])
    assert get_dataframe_filterable_columns(x_dt) == {acct_id_str()}


def test_filter_single_column_dataframe_ReturnsObj_Scenario0_AcctID_EmptyDataFrame():
    # ESTABLISH
    acct_id_bridgeunit = bridgeunit_shop("acct_id")
    empty_dt = DataFrame(columns=[acct_id_str()])

    # WHEN
    gen_dt = filter_single_column_dataframe(empty_dt, acct_id_bridgeunit, acct_id_str())

    # THEN
    assert gen_dt.to_csv() == empty_dt.to_csv()


def test_filter_single_column_dataframe_SetsParameterAttrs_Scenario0_AcctID_5rows():
    # ESTABLISH
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    acct_id_bridgeunit = bridgeunit_shop(type_AcctID_str())
    acct_id_bridgeunit.set_otx_to_inx(xio_otx, xio_inx)
    acct_id_bridgeunit.set_otx_to_inx(sue_otx, sue_inx)
    acct_id_bridgeunit.set_otx_to_inx(bob_otx, bob_inx)
    otx_dt = DataFrame(columns=[acct_id_str()])
    otx_dt.loc[0] = [zia_otx]
    otx_dt.loc[1] = [sue_otx]
    otx_dt.loc[2] = [bob_otx]
    otx_dt.loc[3] = [xio_otx]
    otx_dt = otx_dt.reset_index(drop=True)
    old_otx_dt = copy_deepcopy(otx_dt)
    print(f"{otx_dt=}")

    # WHEN
    filter_single_column_dataframe(otx_dt, acct_id_bridgeunit, acct_id_str())

    # THEN
    assert otx_dt.iloc[0][acct_id_str()] == zia_otx
    assert otx_dt.iloc[1][acct_id_str()] == sue_inx
    assert otx_dt.to_csv() != old_otx_dt.to_csv()
    inx_dt = DataFrame(columns=[acct_id_str()])
    inx_dt.loc[0] = zia_otx
    inx_dt.loc[1] = sue_inx
    inx_dt.loc[2] = bob_inx
    inx_dt.loc[3] = xio_inx
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    assert otx_dt.to_csv() == inx_dt.to_csv()


def test_filter_single_column_dataframe_SetsParameterAttrs_Scenario1_AcctID_5rowsMultipleColumns():
    # ESTABLISH
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    acct_id_bridgeunit = bridgeunit_shop(type_AcctID_str())
    acct_id_bridgeunit.set_otx_to_inx(xio_otx, xio_inx)
    acct_id_bridgeunit.set_otx_to_inx(sue_otx, sue_inx)
    acct_id_bridgeunit.set_otx_to_inx(bob_otx, bob_inx)
    otx_dt = DataFrame(columns=[fiscal_id_str(), acct_id_str(), credit_belief_str()])
    otx_dt.loc[0] = ["ZZ", zia_otx, 12]
    otx_dt.loc[1] = ["ZZ", sue_otx, 12]
    otx_dt.loc[2] = ["ZZ", bob_otx, 12]
    otx_dt.loc[3] = ["ZZ", xio_otx, 12]
    otx_dt = otx_dt.reset_index(drop=True)
    old_otx_dt = copy_deepcopy(otx_dt)
    print(f"{otx_dt=}")

    # WHEN
    filter_single_column_dataframe(otx_dt, acct_id_bridgeunit, acct_id_str())

    # THEN
    assert otx_dt.iloc[0][acct_id_str()] == zia_otx
    assert otx_dt.iloc[1][acct_id_str()] == sue_inx
    assert otx_dt.to_csv() != old_otx_dt.to_csv()
    inx_dt = DataFrame(columns=[fiscal_id_str(), acct_id_str(), credit_belief_str()])
    inx_dt.loc[0] = ["ZZ", zia_otx, 12]
    inx_dt.loc[1] = ["ZZ", sue_inx, 12]
    inx_dt.loc[2] = ["ZZ", bob_inx, 12]
    inx_dt.loc[3] = ["ZZ", xio_inx, 12]
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    assert otx_dt.to_csv() == inx_dt.to_csv()


def test_filter_all_columns_dataframe_SetsParameterAttrs_Scenario0_AcctID():
    # ESTABLISH
    yao_str = "Yao"
    xio_otx = "Xio"
    sue_otx = "Sue"
    bob_otx = "Bob"
    zia_otx = "Zia"
    xio_inx = "Xioita"
    sue_inx = "Suita"
    bob_inx = "Bobita"
    yao_filterunit = filterunit_shop(yao_str)
    yao_filterunit.set_otx_to_inx(type_AcctID_str(), xio_otx, xio_inx)
    yao_filterunit.set_otx_to_inx(type_AcctID_str(), sue_otx, sue_inx)
    yao_filterunit.set_otx_to_inx(type_AcctID_str(), bob_otx, bob_inx)
    otx_dt = DataFrame(columns=[fiscal_id_str(), acct_id_str(), credit_belief_str()])
    otx_dt.loc[0] = ["ZZ", zia_otx, 12]
    otx_dt.loc[1] = ["ZZ", sue_otx, 12]
    otx_dt.loc[2] = ["ZZ", bob_otx, 12]
    otx_dt.loc[3] = ["ZZ", xio_otx, 12]
    otx_dt = otx_dt.reset_index(drop=True)
    old_otx_dt = copy_deepcopy(otx_dt)
    print(f"{otx_dt=}")

    # WHEN
    filter_all_columns_dataframe(otx_dt, yao_filterunit)

    # THEN
    assert otx_dt.iloc[0][acct_id_str()] == zia_otx
    assert otx_dt.iloc[1][acct_id_str()] == sue_inx
    assert otx_dt.to_csv() != old_otx_dt.to_csv()
    inx_dt = DataFrame(columns=[fiscal_id_str(), acct_id_str(), credit_belief_str()])
    inx_dt.loc[0] = ["ZZ", zia_otx, 12]
    inx_dt.loc[1] = ["ZZ", sue_inx, 12]
    inx_dt.loc[2] = ["ZZ", bob_inx, 12]
    inx_dt.loc[3] = ["ZZ", xio_inx, 12]
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    assert otx_dt.to_csv() == inx_dt.to_csv()


def test_filter_all_columns_dataframe_SetsParameterAttrs_Scenario1_RodeUnit_get_casa_maison_filterunit_set_by_otx_to_inx():
    # ESTABLISH
    otx_music45_str = "music45"
    inx_music87_str = "music87"
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_road = create_road(otx_music45_str, casa_otx_str)
    casa_inx_road = create_road(inx_music87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_road = create_road(casa_otx_road, clean_otx_str)
    clean_inx_road = create_road(casa_inx_road, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_road = create_road(clean_otx_road, sweep_str)
    sweep_inx_road = create_road(clean_inx_road, sweep_str)
    yao_filterunit = get_casa_maison_filterunit_set_by_otx_to_inx()
    otx_dt = get_casa_maison_road_otx_dt()
    old_otx_dt = copy_deepcopy(otx_dt)
    assert otx_dt.iloc[0][base_str()] == otx_music45_str
    assert otx_dt.iloc[1][base_str()] == casa_otx_road
    assert otx_dt.iloc[2][base_str()] == clean_otx_road
    assert otx_dt.iloc[3][base_str()] == sweep_otx_road
    print(f"{otx_dt=}")

    # WHEN
    filter_all_columns_dataframe(otx_dt, yao_filterunit)

    # THEN
    assert otx_dt.iloc[0][base_str()] == inx_music87_str
    assert otx_dt.iloc[1][base_str()] == casa_inx_road
    assert otx_dt.iloc[2][base_str()] == clean_inx_road
    assert otx_dt.iloc[3][base_str()] == sweep_inx_road
    assert otx_dt.to_csv() != old_otx_dt.to_csv()
    inx_dt = get_casa_maison_road_inx_dt()
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    assert otx_dt.to_csv() == inx_dt.to_csv()


def test_filter_all_columns_dataframe_SetsParameterAttrs_Scenario2_RodeUnit_get_casa_maison_filterunit_set_by_explicit_label():
    # ESTABLISH
    otx_music45_str = "music45"
    inx_music87_str = "music87"
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_road = create_road(otx_music45_str, casa_otx_str)
    casa_inx_road = create_road(inx_music87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_road = create_road(casa_otx_road, clean_otx_str)
    clean_inx_road = create_road(casa_inx_road, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_road = create_road(clean_otx_road, sweep_str)
    sweep_inx_road = create_road(clean_inx_road, sweep_str)
    yao_filterunit = get_casa_maison_filterunit_set_by_explicit_label()
    # print(f"{yao_filterunit=}")
    otx_dt = get_casa_maison_road_otx_dt()
    old_otx_dt = copy_deepcopy(otx_dt)
    assert otx_dt.iloc[0][base_str()] == otx_music45_str
    assert otx_dt.iloc[1][base_str()] == casa_otx_road
    assert otx_dt.iloc[2][base_str()] == clean_otx_road
    assert otx_dt.iloc[3][base_str()] == sweep_otx_road
    print(f"Before {otx_dt=}")
    print("")

    # WHEN
    filter_all_columns_dataframe(otx_dt, yao_filterunit)

    # THEN
    print("")
    print(f"After  {otx_dt=}")
    assert otx_dt.iloc[0][base_str()] == inx_music87_str
    assert otx_dt.iloc[1][base_str()] == casa_inx_road
    assert otx_dt.iloc[2][base_str()] == clean_inx_road
    assert otx_dt.iloc[3][base_str()] == sweep_inx_road
    assert otx_dt.to_csv() != old_otx_dt.to_csv()
    inx_dt = get_casa_maison_road_inx_dt()
    print(f"{str(otx_dt.to_csv())=}")
    print(f"{str(inx_dt.to_csv())=}")
    assert otx_dt.to_csv() == inx_dt.to_csv()
