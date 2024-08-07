from src.span.csv_tool import (
    extract_csv_headers,
    get_csv_real_id_owner_id_metrics,
    create_filtered_csv_dict,
)
from src.span.examples.span_env import span_env_setup_cleanup


def test_extract_csv_headers_ReturnsEmptyObj():
    # ESTABLISH
    x_csv = ""

    # WHEN
    x_headers = extract_csv_headers(x_csv)

    # THEN
    assert x_headers == []


def test_extract_csv_headers_ReturnsObj():
    # ESTABLISH
    x_csv = """real_id,owner_id,acct_id,credit_score,debtit_score
music56,Sue,Bob,13,29
music56,Sue,Sue,11,23
music56,Sue,Yao,41,37
"""

    # WHEN
    x_headers, x_csv = extract_csv_headers(x_csv)

    # THEN
    real_id_text = "real_id"
    owner_id_text = "owner_id"
    acct_id_text = "acct_id"
    credit_score_text = "credit_score"
    debtit_score_text = "debtit_score"
    assert x_headers == [
        real_id_text,
        owner_id_text,
        acct_id_text,
        credit_score_text,
        debtit_score_text,
    ]


def test_extract_csv_headers_RemovesHeaders_csv():
    # ESTABLISH
    x_csv = """real_id,owner_id,acct_id,credit_score,debtit_score
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


def test_get_csv_real_id_owner_id_list_ReturnsEmptyObj():
    # ESTABLISH
    headerless_csv = ""

    # WHEN
    x_dict = get_csv_real_id_owner_id_metrics(headerless_csv=headerless_csv)

    # THEN
    assert x_dict == {}


def test_get_csv_real_id_owner_id_list_ReturnsObj_Scenario1():
    # ESTABLISH
    music_real_id = "music56"
    yao_text = "Yao"
    headerless_csv = f"""{music_real_id},{yao_text},Bob,13,29
"""

    # WHEN
    x_dict = get_csv_real_id_owner_id_metrics(headerless_csv=headerless_csv)

    # THEN
    assert x_dict == {music_real_id: {yao_text: 1}}


def test_get_csv_real_id_owner_id_list_ReturnsObj_Scenario2():
    # ESTABLISH
    music_real_id = "music56"
    sue_text = "Sue"
    bob_text = "Bob"
    headerless_csv = f"""{music_real_id},{sue_text},Bob,13,29
{music_real_id},{sue_text},Sue,11,23
{music_real_id},{sue_text},Yao,41,37
{music_real_id},{sue_text},Zia,41,37
{music_real_id},{bob_text},Yao,41,37
"""

    # WHEN
    u_dict = get_csv_real_id_owner_id_metrics(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")

    assert u_dict != {music_real_id: {sue_text: 1}}
    assert u_dict == {music_real_id: {sue_text: 4, bob_text: 1}}


def test_get_csv_real_id_owner_id_list_ReturnsObj_Scenario2():
    # ESTABLISH
    music_real_id = "music56"
    sue_text = "Sue"
    bob_text = "Bob"
    headerless_csv = f"""{music_real_id},{sue_text},Bob,13,29
{music_real_id},{sue_text},Sue,11,23
{music_real_id},{sue_text},Yao,41,37
{music_real_id},{sue_text},Zia,41,37
{music_real_id},{bob_text},Yao,41,37
"""

    # WHEN
    u_dict = get_csv_real_id_owner_id_metrics(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")

    assert u_dict != {music_real_id: {sue_text: 1}}
    assert u_dict == {music_real_id: {sue_text: 4, bob_text: 1}}


def test_create_filtered_csv_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    music_real_id = "music56"
    sue_text = "Sue"
    bob_text = "Bob"
    headerless_csv = f"""{music_real_id},{sue_text},Bob,13,29
{music_real_id},{sue_text},Sue,11,23
{music_real_id},{sue_text},Yao,41,37
{music_real_id},{sue_text},Zia,41,37
{music_real_id},{bob_text},Yao,41,37
"""

    # WHEN
    u_dict = create_filtered_csv_dict(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")
    static_sue_csv = f"""{music_real_id},{sue_text},Bob,13,29
{music_real_id},{sue_text},Sue,11,23
{music_real_id},{sue_text},Yao,41,37
{music_real_id},{sue_text},Zia,41,37
"""
    static_bob_csv = f"""{music_real_id},{bob_text},Yao,41,37
"""
    generated_owner_id_dict = u_dict.get(music_real_id)
    assert generated_owner_id_dict
    assert list(generated_owner_id_dict.keys()) == [sue_text, bob_text]
    generated_bob_csv = generated_owner_id_dict.get(bob_text)
    assert generated_bob_csv == static_bob_csv
    generated_sue_csv = generated_owner_id_dict.get(sue_text)
    assert generated_sue_csv == static_sue_csv
    owner_id_csv_dict = {sue_text: static_sue_csv, bob_text: static_bob_csv}
    assert u_dict == {music_real_id: owner_id_csv_dict}
