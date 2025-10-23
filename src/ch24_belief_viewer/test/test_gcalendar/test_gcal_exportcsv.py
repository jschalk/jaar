from csv import DictReader as csv_DictReader
from datetime import datetime
from io import StringIO as io_StringIO
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch14_epoch.epoch_main import add_epoch_planunit, get_default_epoch_config_dict
from src.ch24_belief_viewer.gcalendar import (
    create_gcalendar_csv,
    create_gcalendar_events_list,
    gcal_readble_percent,
)
from src.ch24_belief_viewer.test._util.ch24_examples import ExampleValuesRef as wx
from src.ref.keywords import Ch24Keywords as kw


def test_gcal_readble_percent_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert gcal_readble_percent(1.0) == "100%"
    """Ensure trailing zeros and decimal points are removed properly."""
    assert gcal_readble_percent(0.5) == "50%"
    assert gcal_readble_percent(0.505) == "50.5%"
    assert gcal_readble_percent(0.5001) == "50.01%"
    """Ensure extremely small numbers use scientific notation."""
    result = gcal_readble_percent(1e-10)
    assert "e" in result
    assert result.endswith("%")
    """Ensure custom precision works correctly."""
    assert gcal_readble_percent(0.123456, precision=1) == "12.3%"
    assert gcal_readble_percent(0.123456, precision=4) == "12.3456%"
    assert gcal_readble_percent(0.00123456, precision=4) == "0.1235%"
    assert gcal_readble_percent(0.0000123456, precision=4) == "1.23e-03%"
    assert gcal_readble_percent(0.000123456) == "0.01%"


def test_create_gcalendar_events_list_ReturnsObj_Scenario0_Empty():
    # ESTABLISH
    sue_belief = beliefunit_shop(wx.sue, wx.a23)
    apr7 = datetime(2010, 5, 7, 9)
    print(f"{apr7=}")

    # WHEN
    sue_gcal_events = create_gcalendar_events_list(sue_belief, apr7)

    # THEN
    assert sue_gcal_events == []


def test_BeliefUnit_cashout_SetsAttr_ScenarioX_SingleBranch_fund_ratio():
    # ESTABLISH
    sue_belief = beliefunit_shop(wx.sue, wx.a23)
    sue_belief.add_plan(wx.mop_rope, pledge=True, star=1)
    mop_plan = sue_belief.get_plan_obj(wx.mop_rope)
    assert not sue_belief.planroot.fund_onset
    assert not sue_belief.planroot.fund_cease
    assert not sue_belief.planroot.fund_ratio
    assert not mop_plan.fund_onset
    assert not mop_plan.fund_cease
    assert not mop_plan.fund_ratio

    # WHEN
    sue_belief.cashout()

    # THEN
    assert sue_belief.planroot.fund_onset == 0
    assert sue_belief.planroot.fund_cease == 1000000000.0
    assert sue_belief.planroot.fund_ratio == 1.0
    assert mop_plan.fund_onset == 0
    assert mop_plan.fund_cease == sue_belief.fund_pool
    assert mop_plan.fund_ratio
    assert mop_plan.fund_ratio == 1.0


def test_create_gcalendar_events_list_ReturnsObj_Scenario1_1AllDayPledge():
    # ESTABLISH
    sue_belief = beliefunit_shop(wx.sue, wx.a23)
    sue_belief.add_plan(wx.mop_rope, pledge=True, star=1)
    apr7 = datetime(2010, 5, 7, 9)
    print(f"{apr7=}")

    # WHEN
    sue_gcal_events = create_gcalendar_events_list(sue_belief, apr7)

    # THEN
    gcal_tobe_description = f"""1. {wx.mop_str} (100%)
"""
    description_str = "Description"
    expected_apr7str = "05/07/2010"
    expected_event_dict = {
        "Subject": "Pledges",
        "Start Date": expected_apr7str,
        "End Date": expected_apr7str,
        "All Day Event": "True",
        description_str: gcal_tobe_description,
    }
    init_gcal_event = sue_gcal_events[0]
    assert len(sue_gcal_events) == 1
    assert init_gcal_event.keys() == expected_event_dict.keys()
    assert init_gcal_event.get(description_str) == gcal_tobe_description
    assert sue_gcal_events == [expected_event_dict]


def test_create_gcalendar_events_list_ReturnsObj_Scenario2_3AllDayPledge():
    # ESTABLISH
    sue_belief = beliefunit_shop(wx.sue, wx.a23)
    sue_belief.add_plan(wx.mop_rope, pledge=True, star=2)
    sue_belief.add_plan(wx.sweep_rope, pledge=True, star=1)
    sue_belief.add_plan(wx.scrub_rope, pledge=True, star=1)
    apr7 = datetime(2010, 5, 7, 9)
    print(f"{apr7=}")

    # WHEN
    sue_gcal_events = create_gcalendar_events_list(sue_belief, apr7)

    # THEN
    gcal_tobe_description = f"""1. {wx.mop_str} (50%)
2. {wx.scrub_str} (25%)
3. {wx.sweep_str} (25%)
"""
    description_str = "Description"
    start_date_str = "Start Date"
    expected_apr7str = "05/07/2010"
    expected_event_dict = {
        "Subject": "Pledges",
        start_date_str: expected_apr7str,
        "End Date": expected_apr7str,
        "All Day Event": "True",
        description_str: gcal_tobe_description,
    }
    init_gcal_event = sue_gcal_events[0]
    assert len(sue_gcal_events) == 1
    assert init_gcal_event.keys() == expected_event_dict.keys()
    assert init_gcal_event.get(description_str) == gcal_tobe_description
    assert init_gcal_event.get(start_date_str) == expected_apr7str
    print(sue_gcal_events)
    print([expected_event_dict])
    assert sue_gcal_events == [expected_event_dict]


# -[ ] Build the concept of time zones into the interpretation (trans late) module, try out if the translation can be used for numbers
# def test_create_gcalendar_events_list_ReturnsObj_Scenario3_OneEpoch_pledge():
#     # ESTABLISH
#     sue_belief = beliefunit_shop(wx.sue, wx.a23)
#     sue_belief.add_plan(wx.mop_rope, pledge=True, star=2)
#     default_epoch_config = get_default_epoch_config_dict()
#     add_epoch_planunit(sue_belief, default_epoch_config)
#     sue_belief.edit_reason(wx.mop_rope, reason_context=, reason_case=)
#     apr7 = datetime(2010, 5, 7, 9)
#     print(f"{apr7=}")

#     # WHEN
#     sue_gcal_events = create_gcalendar_events_list(sue_belief, apr7)

#     # THEN
#     gcal_tobe_description = f"""1. {wx.mop_str} (50%)
# 2. {wx.scrub_str} (25%)
# 3. {wx.sweep_str} (25%)
# """
#     description_str = "Description"
#     start_date_str = "Start Date"
#     expected_apr7str = "05/07/2010"
#     expected_event_dict = {
#         "Subject": "Pledges",
#         start_date_str: expected_apr7str,
#         "End Date": expected_apr7str,
#         "All Day Event": "True",
#         description_str: gcal_tobe_description,
#     }
#     init_gcal_event = sue_gcal_events[0]
#     assert len(sue_gcal_events) == 1
#     assert init_gcal_event.keys() == expected_event_dict.keys()
#     assert init_gcal_event.get(description_str) == gcal_tobe_description
#     assert init_gcal_event.get(start_date_str) == expected_apr7str
#     print(sue_gcal_events)
#     print([expected_event_dict])
#     assert sue_gcal_events == [expected_event_dict]


def test_create_gcalendar_csv_ReturnsObj():
    # ESTABLISH
    events = [
        {
            "Subject": "Team Meeting",
            "Start Date": "10/08/2025",
            "Start Time": "09:00:00",
            "End Date": "10/08/2025",
            "End Time": "10:00:00",
            "All Day Event": "False",
            "Description": "Quarterly planning session",
        },
        {
            "Subject": "All Hands Day",
            "Start Date": "10/10/2025",
            "End Date": "10/10/2025",
            "All Day Event": "True",
            "Description": "Company-wide offsite",
        },
    ]

    # WHEN
    csv_str = create_gcalendar_csv(events)

    # THEN
    # Assert CSV contains expected headers and data
    assert isinstance(csv_str, str)
    header_str = (
        "Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description"
    )
    assert header_str in csv_str
    assert "Team Meeting" in csv_str
    assert "All Hands Day" in csv_str
    assert "Company-wide offsite" in csv_str

    # Parse it back to verify structure
    reader = list(csv_DictReader(io_StringIO(csv_str)))
    assert reader[0]["All Day Event"] == "False"
    assert reader[1]["All Day Event"] == "True"
    assert reader[1]["Start Time"] == ""  # blank for all-day event
