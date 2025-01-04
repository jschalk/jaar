from src.f00_instrument.dict_toolbox import extract_csv_headers
from src.f04_gift.atom_config import acct_name_str, cmty_title_str, owner_name_str
from src.f09_brick.brick import (
    get_csv_cmty_title_owner_name_metrics,
    cmty_title_owner_name_nested_csv_dict,
)


def test_extract_csv_headers_ReturnsObj():
    # ESTABLISH
    x_csv = """cmty_title,owner_name,acct_name,credit_belief,debtit_belief
accord56,Sue,Bob,13,29
accord56,Sue,Sue,11,23
accord56,Sue,Yao,41,37
"""

    # WHEN
    x_headers, x_csv = extract_csv_headers(x_csv)

    # THEN
    credit_belief_str = "credit_belief"
    debtit_belief_str = "debtit_belief"
    assert x_headers == [
        cmty_title_str(),
        owner_name_str(),
        acct_name_str(),
        credit_belief_str,
        debtit_belief_str,
    ]


def test_extract_csv_headers_RemovesHeaders_csv():
    # ESTABLISH
    x_csv = """cmty_title,owner_name,acct_name,credit_belief,debtit_belief
accord56,Sue,Bob,13,29
accord56,Sue,Sue,11,23
accord56,Sue,Yao,41,37
"""

    # WHEN
    x_headers, new_csv = extract_csv_headers(x_csv)

    # THEN
    print(f"{new_csv=}")
    headerless_csv = """accord56,Sue,Bob,13,29
accord56,Sue,Sue,11,23
accord56,Sue,Yao,41,37
"""
    assert new_csv == headerless_csv


def test_get_csv_cmty_title_owner_name_metrics_ReturnsObj_Scenario2():
    # ESTABLISH
    accord_cmty_title = "accord56"
    sue_str = "Sue"
    bob_str = "Bob"
    headerless_csv = f"""{accord_cmty_title},{sue_str},Bob,13,29
{accord_cmty_title},{sue_str},Sue,11,23
{accord_cmty_title},{sue_str},Yao,41,37
{accord_cmty_title},{sue_str},Zia,41,37
{accord_cmty_title},{bob_str},Yao,41,37
"""

    # WHEN
    u_dict = get_csv_cmty_title_owner_name_metrics(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")

    assert u_dict != {accord_cmty_title: {sue_str: 1}}
    assert u_dict == {accord_cmty_title: {sue_str: 4, bob_str: 1}}


def test_cmty_title_owner_name_nested_csv_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    accord_cmty_title = "accord56"
    sue_str = "Sue"
    bob_str = "Bob"
    headerless_csv = f"""face_x,event_x,{accord_cmty_title},{sue_str},Bob,13,29
,,{accord_cmty_title},{sue_str},Sue,11,23
,,{accord_cmty_title},{sue_str},Yao,41,37
,,{accord_cmty_title},{sue_str},Zia,41,37
,,{accord_cmty_title},{bob_str},Yao,41,37
"""

    # WHEN
    u_dict = cmty_title_owner_name_nested_csv_dict(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")
    static_sue_csv = f"""face_x,event_x,{accord_cmty_title},{sue_str},Bob,13,29
,,{accord_cmty_title},{sue_str},Sue,11,23
,,{accord_cmty_title},{sue_str},Yao,41,37
,,{accord_cmty_title},{sue_str},Zia,41,37
"""
    static_bob_csv = f""",,{accord_cmty_title},{bob_str},Yao,41,37
"""
    generated_owner_name_dict = u_dict.get(accord_cmty_title)
    assert generated_owner_name_dict
    assert list(generated_owner_name_dict.keys()) == [sue_str, bob_str]
    generated_bob_csv = generated_owner_name_dict.get(bob_str)
    assert generated_bob_csv == static_bob_csv
    generated_sue_csv = generated_owner_name_dict.get(sue_str)
    assert generated_sue_csv == static_sue_csv
    owner_name_csv_dict = {sue_str: static_sue_csv, bob_str: static_bob_csv}
    assert u_dict == {accord_cmty_title: owner_name_csv_dict}
