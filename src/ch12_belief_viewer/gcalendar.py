from csv import DictWriter as csv_DictWriter
from datetime import datetime
from io import StringIO as io_StringIO
from src.ch07_belief_logic.belief_main import BeliefUnit, get_sorted_plan_list


def gcal_readble_percent(value: float, precision=2):
    """
    Convert a float into a readable percentage string.
    Handles very small and large values gracefully.
    """
    if value is None:
        return "0%"

    percent = value * 100

    if 0 < abs(percent) < 0.01:
        return f"{percent:.2e}%"

    formatted = f"{percent:.{precision}f}".rstrip("0").rstrip(".")
    return f"{formatted}%"


def create_gcalendar_events_list(x_belief: BeliefUnit, day: datetime) -> list[dict]:
    agenda_plans_dict = x_belief.get_agenda_dict()
    agenda_list = get_sorted_plan_list(agenda_plans_dict)
    gcal_tobe_description = ""
    for item_rank, agenda_item in enumerate(agenda_list, start=1):
        item_fund_ratio_str = gcal_readble_percent(agenda_item.fund_ratio)
        gcal_tobe_description += (
            f"{item_rank}. {agenda_item.plan_label} ({item_fund_ratio_str})\n"
        )
    all_day_events = {
        "Subject": "Pledges",
        "Start Date": day.strftime("%m/%d/%Y"),
        "End Date": day.strftime("%m/%d/%Y"),
        "All Day Event": "True",
        "Description": gcal_tobe_description,
    }
    return [all_day_events] if gcal_tobe_description else []


def create_gcalendar_csv(events: list[dict]) -> str:
    """Create a Google Calendar-compatible CSV file."""
    fieldnames = [
        "Subject",
        "Start Date",
        "Start Time",
        "End Date",
        "End Time",
        "All Day Event",
        "Description",
    ]

    # Use StringIO to build in memory
    output = io_StringIO()
    writer = csv_DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(events)

    return output.getvalue()
