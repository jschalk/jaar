from src.f04_gift.atom_config import (
    acct_id_str,
    fiscal_id_str,
    credit_belief_str,
    base_str,
    type_AcctID_str,
)
from src.f09_filter.bridge import bridgekind_shop, bridgeunit_shop
from src.f09_filter.filter import (
    filter_single_column_dataframe,
    filter_all_columns_dataframe,
    get_dataframe_filterable_columns,
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
    acct_id_bridgekind = bridgekind_shop("acct_id")
    empty_dt = DataFrame(columns=[acct_id_str()])

    # WHEN
    gen_dt = filter_single_column_dataframe(empty_dt, acct_id_bridgekind, acct_id_str())

    # THEN
    assert gen_dt.to_csv() == empty_dt.to_csv()


def test_filter_single_column_dataframe_SetsParameterAttrs_Scenario0_AcctID_5rows():
    # ESTABLISH
    xio_src = "Xio"
    sue_src = "Sue"
    bob_src = "Bob"
    zia_src = "Zia"
    xio_dst = "Xioita"
    sue_dst = "Suita"
    bob_dst = "Bobita"
    acct_id_bridgekind = bridgekind_shop(type_AcctID_str())
    acct_id_bridgekind.set_src_to_dst(xio_src, xio_dst)
    acct_id_bridgekind.set_src_to_dst(sue_src, sue_dst)
    acct_id_bridgekind.set_src_to_dst(bob_src, bob_dst)
    src_dt = DataFrame(columns=[acct_id_str()])
    src_dt.loc[0] = [zia_src]
    src_dt.loc[1] = [sue_src]
    src_dt.loc[2] = [bob_src]
    src_dt.loc[3] = [xio_src]
    src_dt = src_dt.reset_index(drop=True)
    old_src_dt = copy_deepcopy(src_dt)
    print(f"{src_dt=}")

    # WHEN
    filter_single_column_dataframe(src_dt, acct_id_bridgekind, acct_id_str())

    # THEN
    assert src_dt.iloc[0][acct_id_str()] == zia_src
    assert src_dt.iloc[1][acct_id_str()] == sue_dst
    assert src_dt.to_csv() != old_src_dt.to_csv()
    dst_dt = DataFrame(columns=[acct_id_str()])
    dst_dt.loc[0] = zia_src
    dst_dt.loc[1] = sue_dst
    dst_dt.loc[2] = bob_dst
    dst_dt.loc[3] = xio_dst
    print(f"{str(src_dt.to_csv())=}")
    print(f"{str(dst_dt.to_csv())=}")
    assert src_dt.to_csv() == dst_dt.to_csv()


def test_filter_single_column_dataframe_SetsParameterAttrs_Scenario1_AcctID_5rowsMultipleColumns():
    # ESTABLISH
    xio_src = "Xio"
    sue_src = "Sue"
    bob_src = "Bob"
    zia_src = "Zia"
    xio_dst = "Xioita"
    sue_dst = "Suita"
    bob_dst = "Bobita"
    acct_id_bridgekind = bridgekind_shop(type_AcctID_str())
    acct_id_bridgekind.set_src_to_dst(xio_src, xio_dst)
    acct_id_bridgekind.set_src_to_dst(sue_src, sue_dst)
    acct_id_bridgekind.set_src_to_dst(bob_src, bob_dst)
    src_dt = DataFrame(columns=[fiscal_id_str(), acct_id_str(), credit_belief_str()])
    src_dt.loc[0] = ["ZZ", zia_src, 12]
    src_dt.loc[1] = ["ZZ", sue_src, 12]
    src_dt.loc[2] = ["ZZ", bob_src, 12]
    src_dt.loc[3] = ["ZZ", xio_src, 12]
    src_dt = src_dt.reset_index(drop=True)
    old_src_dt = copy_deepcopy(src_dt)
    print(f"{src_dt=}")

    # WHEN
    filter_single_column_dataframe(src_dt, acct_id_bridgekind, acct_id_str())

    # THEN
    assert src_dt.iloc[0][acct_id_str()] == zia_src
    assert src_dt.iloc[1][acct_id_str()] == sue_dst
    assert src_dt.to_csv() != old_src_dt.to_csv()
    dst_dt = DataFrame(columns=[fiscal_id_str(), acct_id_str(), credit_belief_str()])
    dst_dt.loc[0] = ["ZZ", zia_src, 12]
    dst_dt.loc[1] = ["ZZ", sue_dst, 12]
    dst_dt.loc[2] = ["ZZ", bob_dst, 12]
    dst_dt.loc[3] = ["ZZ", xio_dst, 12]
    print(f"{str(src_dt.to_csv())=}")
    print(f"{str(dst_dt.to_csv())=}")
    assert src_dt.to_csv() == dst_dt.to_csv()


def test_filter_all_columns_dataframe_SetsParameterAttrs():
    # ESTABLISH
    yao_str = "Yao"
    xio_src = "Xio"
    sue_src = "Sue"
    bob_src = "Bob"
    zia_src = "Zia"
    xio_dst = "Xioita"
    sue_dst = "Suita"
    bob_dst = "Bobita"
    yao_bridgeunit = bridgeunit_shop(yao_str)
    yao_bridgeunit.set_src_to_dst(type_AcctID_str(), xio_src, xio_dst)
    yao_bridgeunit.set_src_to_dst(type_AcctID_str(), sue_src, sue_dst)
    yao_bridgeunit.set_src_to_dst(type_AcctID_str(), bob_src, bob_dst)
    src_dt = DataFrame(columns=[fiscal_id_str(), acct_id_str(), credit_belief_str()])
    src_dt.loc[0] = ["ZZ", zia_src, 12]
    src_dt.loc[1] = ["ZZ", sue_src, 12]
    src_dt.loc[2] = ["ZZ", bob_src, 12]
    src_dt.loc[3] = ["ZZ", xio_src, 12]
    src_dt = src_dt.reset_index(drop=True)
    old_src_dt = copy_deepcopy(src_dt)
    print(f"{src_dt=}")

    # WHEN
    filter_all_columns_dataframe(src_dt, yao_bridgeunit)

    # THEN
    assert src_dt.iloc[0][acct_id_str()] == zia_src
    assert src_dt.iloc[1][acct_id_str()] == sue_dst
    assert src_dt.to_csv() != old_src_dt.to_csv()
    dst_dt = DataFrame(columns=[fiscal_id_str(), acct_id_str(), credit_belief_str()])
    dst_dt.loc[0] = ["ZZ", zia_src, 12]
    dst_dt.loc[1] = ["ZZ", sue_dst, 12]
    dst_dt.loc[2] = ["ZZ", bob_dst, 12]
    dst_dt.loc[3] = ["ZZ", xio_dst, 12]
    print(f"{str(src_dt.to_csv())=}")
    print(f"{str(dst_dt.to_csv())=}")
    assert src_dt.to_csv() == dst_dt.to_csv()
