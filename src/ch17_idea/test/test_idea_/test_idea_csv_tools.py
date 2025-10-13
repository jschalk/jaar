from src.ch17_idea.idea_main import (
    get_csv_moment_label_belief_name_metrics,
    moment_label_belief_name_nested_csv_dict,
)


def test_get_csv_moment_label_belief_name_metrics_ReturnsObj_Scenario2():
    # ESTABLISH
    amy_moment_label = "amy56"
    sue_str = "Sue"
    bob_str = "Bob"
    headerless_csv = f"""{amy_moment_label},{sue_str},Bob,13,29
{amy_moment_label},{sue_str},Sue,11,23
{amy_moment_label},{sue_str},Yao,41,37
{amy_moment_label},{sue_str},Zia,41,37
{amy_moment_label},{bob_str},Yao,41,37
"""

    # WHEN
    u_dict = get_csv_moment_label_belief_name_metrics(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")

    assert u_dict != {amy_moment_label: {sue_str: 1}}
    assert u_dict == {amy_moment_label: {sue_str: 4, bob_str: 1}}


def test_moment_label_belief_name_nested_csv_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    amy_moment_label = "amy56"
    sue_str = "Sue"
    bob_str = "Bob"
    headerless_csv = f"""face_x,spark_x,{amy_moment_label},{sue_str},Bob,13,29
,,{amy_moment_label},{sue_str},Sue,11,23
,,{amy_moment_label},{sue_str},Yao,41,37
,,{amy_moment_label},{sue_str},Zia,41,37
,,{amy_moment_label},{bob_str},Yao,41,37
"""

    # WHEN
    u_dict = moment_label_belief_name_nested_csv_dict(headerless_csv=headerless_csv)

    # THEN
    # print(f"{u_dict=}")
    static_sue_csv = f"""face_x,spark_x,{amy_moment_label},{sue_str},Bob,13,29
,,{amy_moment_label},{sue_str},Sue,11,23
,,{amy_moment_label},{sue_str},Yao,41,37
,,{amy_moment_label},{sue_str},Zia,41,37
"""
    static_bob_csv = f""",,{amy_moment_label},{bob_str},Yao,41,37
"""
    generated_belief_name_dict = u_dict.get(amy_moment_label)
    assert generated_belief_name_dict
    assert list(generated_belief_name_dict.keys()) == [sue_str, bob_str]
    generated_bob_csv = generated_belief_name_dict.get(bob_str)
    assert generated_bob_csv == static_bob_csv
    generated_sue_csv = generated_belief_name_dict.get(sue_str)
    assert generated_sue_csv == static_sue_csv
    belief_name_csv_dict = {sue_str: static_sue_csv, bob_str: static_bob_csv}
    assert u_dict == {amy_moment_label: belief_name_csv_dict}
