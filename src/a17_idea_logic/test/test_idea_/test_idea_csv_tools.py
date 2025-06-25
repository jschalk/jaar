from src.a17_idea_logic.idea import (
    belief_label_owner_name_nested_csv_dict,
    get_csv_belief_label_owner_name_metrics,
)


def test_get_csv_belief_label_owner_name_metrics_ReturnsObj_Scenario2():
    # ESTABLISH
    accord_belief_label = "accord56"
    sue_str = "Sue"
    bob_str = "Bob"
    headerless_csv = f"""{accord_belief_label},{sue_str},Bob,13,29
{accord_belief_label},{sue_str},Sue,11,23
{accord_belief_label},{sue_str},Yao,41,37
{accord_belief_label},{sue_str},Zia,41,37
{accord_belief_label},{bob_str},Yao,41,37
"""

    # WHEN
    u_dict = get_csv_belief_label_owner_name_metrics(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")

    assert u_dict != {accord_belief_label: {sue_str: 1}}
    assert u_dict == {accord_belief_label: {sue_str: 4, bob_str: 1}}


def test_belief_label_owner_name_nested_csv_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    accord_belief_label = "accord56"
    sue_str = "Sue"
    bob_str = "Bob"
    headerless_csv = f"""face_x,event_x,{accord_belief_label},{sue_str},Bob,13,29
,,{accord_belief_label},{sue_str},Sue,11,23
,,{accord_belief_label},{sue_str},Yao,41,37
,,{accord_belief_label},{sue_str},Zia,41,37
,,{accord_belief_label},{bob_str},Yao,41,37
"""

    # WHEN
    u_dict = belief_label_owner_name_nested_csv_dict(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")
    static_sue_csv = f"""face_x,event_x,{accord_belief_label},{sue_str},Bob,13,29
,,{accord_belief_label},{sue_str},Sue,11,23
,,{accord_belief_label},{sue_str},Yao,41,37
,,{accord_belief_label},{sue_str},Zia,41,37
"""
    static_bob_csv = f""",,{accord_belief_label},{bob_str},Yao,41,37
"""
    generated_owner_name_dict = u_dict.get(accord_belief_label)
    assert generated_owner_name_dict
    assert list(generated_owner_name_dict.keys()) == [sue_str, bob_str]
    generated_bob_csv = generated_owner_name_dict.get(bob_str)
    assert generated_bob_csv == static_bob_csv
    generated_sue_csv = generated_owner_name_dict.get(sue_str)
    assert generated_sue_csv == static_sue_csv
    owner_name_csv_dict = {sue_str: static_sue_csv, bob_str: static_bob_csv}
    assert u_dict == {accord_belief_label: owner_name_csv_dict}
