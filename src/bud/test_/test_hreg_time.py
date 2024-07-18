from src.bud.hreg_time import HregTimeIdeaSource


def test_HregTimeIdeaSource_Exists():
    # ESTABLISH
    slash_text = "/"

    # WHEN
    x_hregtimeideasource = HregTimeIdeaSource(slash_text)

    # THEN
    assert x_hregtimeideasource.delimiter == slash_text


# def test_get_jajatime_week_legible_text_ReturnsObj():


# def _get_jajatime_week_legible_text(x_budunit: BudUnit, open: int, divisor: int) -> str:
#     x_hregidea = HregTimeIdeaSource(self._road_delimiter)
#     open_in_week = open % divisor
#     time_road = self.make_l1_road("time")
#     tech_road = self.make_road(time_road, "tech")
#     week_road = self.make_road(tech_road, "week")
#     weekday_ideas_dict = self.get_idea_ranged_kids(
#         idea_road=week_road, begin=open_in_week
#     )
#     weekday_idea_node = None
#     for idea in weekday_ideas_dict.values():
#         weekday_idea_node = idea

#     if divisor == 10080:
#         return f"every {weekday_idea_node._label} at {x_hregidea.readable_1440_time(min1440=open % 1440)}"
#     num_with_letter_ending = x_hregidea.get_number_with_letter_ending(
#         num=divisor // 10080
#     )
#     return f"every {num_with_letter_ending} {weekday_idea_node._label} at {x_hregidea.readable_1440_time(min1440=open % 1440)}"
