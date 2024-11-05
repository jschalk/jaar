from src.f00_instrument.dict_tool import extract_csv_headers
from src.f04_gift.atom_config import acct_id_str, fiscal_id_str, owner_id_str
from src.f09_brick.brick import (
    get_csv_fiscal_id_owner_id_metrics,
    fiscal_id_owner_id_nested_csv_dict,
)


def test_extract_csv_headers_ReturnsObj():
    # ESTABLISH
    x_csv = """fiscal_id,owner_id,acct_id,credit_belief,debtit_belief
music56,Sue,Bob,13,29
music56,Sue,Sue,11,23
music56,Sue,Yao,41,37
"""

    # WHEN
    x_headers, x_csv = extract_csv_headers(x_csv)

    # THEN
    credit_belief_str = "credit_belief"
    debtit_belief_str = "debtit_belief"
    assert x_headers == [
        fiscal_id_str(),
        owner_id_str(),
        acct_id_str(),
        credit_belief_str,
        debtit_belief_str,
    ]


def test_extract_csv_headers_RemovesHeaders_csv():
    # ESTABLISH
    x_csv = """fiscal_id,owner_id,acct_id,credit_belief,debtit_belief
music56,Sue,Bob,13,29
music56,Sue,Sue,11,23
music56,Sue,Yao,41,37
"""

    # WHEN
    x_headers, new_csv = extract_csv_headers(x_csv)

    # THEN
    print(f"{new_csv=}")
    headerless_csv = """music56,Sue,Bob,13,29
music56,Sue,Sue,11,23
music56,Sue,Yao,41,37
"""
    assert new_csv == headerless_csv


def test_get_csv_fiscal_id_owner_id_metrics_ReturnsObj_Scenario2():
    # ESTABLISH
    music_fiscal_id = "music56"
    sue_str = "Sue"
    bob_str = "Bob"
    headerless_csv = f"""{music_fiscal_id},{sue_str},Bob,13,29
{music_fiscal_id},{sue_str},Sue,11,23
{music_fiscal_id},{sue_str},Yao,41,37
{music_fiscal_id},{sue_str},Zia,41,37
{music_fiscal_id},{bob_str},Yao,41,37
"""

    # WHEN
    u_dict = get_csv_fiscal_id_owner_id_metrics(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")

    assert u_dict != {music_fiscal_id: {sue_str: 1}}
    assert u_dict == {music_fiscal_id: {sue_str: 4, bob_str: 1}}


def test_fiscal_id_owner_id_nested_csv_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    music_fiscal_id = "music56"
    sue_str = "Sue"
    bob_str = "Bob"
    headerless_csv = f"""face_x,eon_x,{music_fiscal_id},{sue_str},Bob,13,29
,,{music_fiscal_id},{sue_str},Sue,11,23
,,{music_fiscal_id},{sue_str},Yao,41,37
,,{music_fiscal_id},{sue_str},Zia,41,37
,,{music_fiscal_id},{bob_str},Yao,41,37
"""

    # WHEN
    u_dict = fiscal_id_owner_id_nested_csv_dict(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")
    static_sue_csv = f"""face_x,eon_x,{music_fiscal_id},{sue_str},Bob,13,29
,,{music_fiscal_id},{sue_str},Sue,11,23
,,{music_fiscal_id},{sue_str},Yao,41,37
,,{music_fiscal_id},{sue_str},Zia,41,37
"""
    static_bob_csv = f""",,{music_fiscal_id},{bob_str},Yao,41,37
"""
    generated_owner_id_dict = u_dict.get(music_fiscal_id)
    assert generated_owner_id_dict
    assert list(generated_owner_id_dict.keys()) == [sue_str, bob_str]
    generated_bob_csv = generated_owner_id_dict.get(bob_str)
    assert generated_bob_csv == static_bob_csv
    generated_sue_csv = generated_owner_id_dict.get(sue_str)
    assert generated_sue_csv == static_sue_csv
    owner_id_csv_dict = {sue_str: static_sue_csv, bob_str: static_bob_csv}
    assert u_dict == {music_fiscal_id: owner_id_csv_dict}
