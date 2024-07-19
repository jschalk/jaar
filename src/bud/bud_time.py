from src.bud.hreg_time import HregTimeIdeaSource
from src.bud.idea import ideaunit_shop
from src.bud.bud import BudUnit


def add_time_hreg_ideaunit(x_budunit: BudUnit) -> BudUnit:
    time_road = x_budunit.make_l1_road(time_str())
    time_idea = ideaunit_shop(time_str())
    x_budunit.add_l1_idea(time_idea)

    # tech_road branch
    tech_road = x_budunit.make_road(time_road, tech_str())
    tech_idea = ideaunit_shop(tech_str())
    x_budunit.add_idea(tech_idea, time_road)

    # year 365
    year365_road = x_budunit.make_road(tech_road, year365_str())
    year365_idea = ideaunit_shop(year365_str())
    x_budunit.add_idea(year365_idea, tech_road)
    x_budunit.add_idea(ideaunit_shop(f"1-{Jan()}"), year365_road)
    x_budunit.add_idea(ideaunit_shop(f"2-{Feb28()}"), year365_road)
    x_budunit.add_idea(ideaunit_shop(f"3-{Mar()}"), year365_road)
    x_budunit.add_idea(ideaunit_shop(f"4-{Apr()}"), year365_road)
    x_budunit.add_idea(ideaunit_shop(f"5-{May()}"), year365_road)
    x_budunit.add_idea(ideaunit_shop(f"6-{Jun()}"), year365_road)
    x_budunit.add_idea(ideaunit_shop(f"7-{Jul()}"), year365_road)
    x_budunit.add_idea(ideaunit_shop(f"8-{Aug()}"), year365_road)
    x_budunit.add_idea(ideaunit_shop(f"9-{Sep()}"), year365_road)
    x_budunit.add_idea(ideaunit_shop(f"10-{Oct()}"), year365_road)
    x_budunit.add_idea(ideaunit_shop(f"11-{Nov()}"), year365_road)
    x_budunit.add_idea(ideaunit_shop(f"12-{Dec()}"), year365_road)

    # year 366
    year366_road = x_budunit.make_road(tech_road, year366_str())
    year366_idea = ideaunit_shop(year366_str())
    x_budunit.add_idea(year366_idea, tech_road)
    x_budunit.add_idea(ideaunit_shop(f"1-{Jan()}"), year366_road)
    x_budunit.add_idea(ideaunit_shop(f"2-{Feb29()}"), year366_road)
    x_budunit.add_idea(ideaunit_shop(f"3-{Mar()}"), year366_road)
    x_budunit.add_idea(ideaunit_shop(f"4-{Apr()}"), year366_road)
    x_budunit.add_idea(ideaunit_shop(f"5-{May()}"), year366_road)
    x_budunit.add_idea(ideaunit_shop(f"6-{Jun()}"), year366_road)
    x_budunit.add_idea(ideaunit_shop(f"7-{Jul()}"), year366_road)
    x_budunit.add_idea(ideaunit_shop(f"8-{Aug()}"), year366_road)
    x_budunit.add_idea(ideaunit_shop(f"9-{Sep()}"), year366_road)
    x_budunit.add_idea(ideaunit_shop(f"10-{Oct()}"), year366_road)
    x_budunit.add_idea(ideaunit_shop(f"11-{Nov()}"), year366_road)
    x_budunit.add_idea(ideaunit_shop(f"12-{Dec()}"), year366_road)

    # day_road
    tech_day_road = x_budunit.make_road(tech_road, day_str())
    tech_day_idea = ideaunit_shop(day_str())
    x_budunit.add_idea(tech_day_idea, tech_road)
    x_budunit.add_idea(ideaunit_shop("0-12am"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("1-1am"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("2-2am"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("3-3am"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("4-4am"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("5-5am"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("6-6am"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("7-7am"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("8-8am"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("9-9am"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("10-10am"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("11-11am"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("12-12pm"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("13-1pm"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("14-2pm"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("15-3pm"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("16-4pm"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("17-5pm"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("18-6pm"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("19-7pm"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("20-8pm"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("21-9pm"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("22-10pm"), tech_day_road)
    x_budunit.add_idea(ideaunit_shop("23-11pm"), tech_day_road)

    # week_road
    week_road = x_budunit.make_road(tech_road, week_str())
    week_idea = ideaunit_shop(week_str())
    x_budunit.add_idea(week_idea, tech_road)
    Sun_road = x_budunit.make_road(week_road, get_Sun())
    Mon_road = x_budunit.make_road(week_road, get_Mon())
    Tue_road = x_budunit.make_road(week_road, get_Tue())
    Wed_road = x_budunit.make_road(week_road, get_Wed())
    Thu_road = x_budunit.make_road(week_road, get_Thu())
    Fri_road = x_budunit.make_road(week_road, get_Fri())
    Sat_road = x_budunit.make_road(week_road, get_Sat())
    Sun_idea = ideaunit_shop(get_Sun())
    Mon_idea = ideaunit_shop(get_Mon())
    Tue_idea = ideaunit_shop(get_Tue())
    Wed_idea = ideaunit_shop(get_Wed())
    Thu_idea = ideaunit_shop(get_Thu())
    Fri_idea = ideaunit_shop(get_Fri())
    Sat_idea = ideaunit_shop(get_Sat())
    x_budunit.add_idea(Sun_idea, week_road)
    x_budunit.add_idea(Mon_idea, week_road)
    x_budunit.add_idea(Tue_idea, week_road)
    x_budunit.add_idea(Wed_idea, week_road)
    x_budunit.add_idea(Thu_idea, week_road)
    x_budunit.add_idea(Fri_idea, week_road)
    x_budunit.add_idea(Sat_idea, week_road)

    # hour_road
    hour_road = x_budunit.make_road(tech_road, hour_str())
    hour_idea = ideaunit_shop(hour_str())
    x_budunit.add_idea(hour_idea, tech_road)
    x_budunit.add_idea(ideaunit_shop("0-:00"), hour_road)
    x_budunit.add_idea(ideaunit_shop("1-:01"), hour_road)
    x_budunit.add_idea(ideaunit_shop("2-:02"), hour_road)
    x_budunit.add_idea(ideaunit_shop("3-:03"), hour_road)
    x_budunit.add_idea(ideaunit_shop("4-:04"), hour_road)
    x_budunit.add_idea(ideaunit_shop("5-:05"), hour_road)
    x_budunit.add_idea(ideaunit_shop("6-:06"), hour_road)
    x_budunit.add_idea(ideaunit_shop("7-:07"), hour_road)
    x_budunit.add_idea(ideaunit_shop("8-:08"), hour_road)
    x_budunit.add_idea(ideaunit_shop("9-:09"), hour_road)
    x_budunit.add_idea(ideaunit_shop("10-:10"), hour_road)
    x_budunit.add_idea(ideaunit_shop("11-:11"), hour_road)
    x_budunit.add_idea(ideaunit_shop("12-:12"), hour_road)
    x_budunit.add_idea(ideaunit_shop("13-:13"), hour_road)
    x_budunit.add_idea(ideaunit_shop("14-:14"), hour_road)
    x_budunit.add_idea(ideaunit_shop("15-:15"), hour_road)
    x_budunit.add_idea(ideaunit_shop("16-:16"), hour_road)
    x_budunit.add_idea(ideaunit_shop("17-:17"), hour_road)
    x_budunit.add_idea(ideaunit_shop("18-:18"), hour_road)
    x_budunit.add_idea(ideaunit_shop("19-:19"), hour_road)
    x_budunit.add_idea(ideaunit_shop("20-:20"), hour_road)
    x_budunit.add_idea(ideaunit_shop("21-:21"), hour_road)
    x_budunit.add_idea(ideaunit_shop("22-:22"), hour_road)
    x_budunit.add_idea(ideaunit_shop("23-:23"), hour_road)
    x_budunit.add_idea(ideaunit_shop("24-:24"), hour_road)
    x_budunit.add_idea(ideaunit_shop("25-:25"), hour_road)
    x_budunit.add_idea(ideaunit_shop("26-:26"), hour_road)
    x_budunit.add_idea(ideaunit_shop("27-:27"), hour_road)
    x_budunit.add_idea(ideaunit_shop("28-:28"), hour_road)
    x_budunit.add_idea(ideaunit_shop("29-:29"), hour_road)
    x_budunit.add_idea(ideaunit_shop("30-:30"), hour_road)
    x_budunit.add_idea(ideaunit_shop("31-:31"), hour_road)
    x_budunit.add_idea(ideaunit_shop("32-:32"), hour_road)
    x_budunit.add_idea(ideaunit_shop("33-:33"), hour_road)
    x_budunit.add_idea(ideaunit_shop("34-:34"), hour_road)
    x_budunit.add_idea(ideaunit_shop("35-:35"), hour_road)
    x_budunit.add_idea(ideaunit_shop("36-:36"), hour_road)
    x_budunit.add_idea(ideaunit_shop("37-:37"), hour_road)
    x_budunit.add_idea(ideaunit_shop("38-:38"), hour_road)
    x_budunit.add_idea(ideaunit_shop("39-:39"), hour_road)
    x_budunit.add_idea(ideaunit_shop("40-:40"), hour_road)
    x_budunit.add_idea(ideaunit_shop("41-:41"), hour_road)
    x_budunit.add_idea(ideaunit_shop("42-:42"), hour_road)
    x_budunit.add_idea(ideaunit_shop("43-:43"), hour_road)
    x_budunit.add_idea(ideaunit_shop("44-:44"), hour_road)
    x_budunit.add_idea(ideaunit_shop("45-:45"), hour_road)
    x_budunit.add_idea(ideaunit_shop("46-:46"), hour_road)
    x_budunit.add_idea(ideaunit_shop("47-:47"), hour_road)
    x_budunit.add_idea(ideaunit_shop("48-:48"), hour_road)
    x_budunit.add_idea(ideaunit_shop("49-:49"), hour_road)
    x_budunit.add_idea(ideaunit_shop("50-:50"), hour_road)
    x_budunit.add_idea(ideaunit_shop("51-:51"), hour_road)
    x_budunit.add_idea(ideaunit_shop("52-:52"), hour_road)
    x_budunit.add_idea(ideaunit_shop("53-:53"), hour_road)
    x_budunit.add_idea(ideaunit_shop("54-:54"), hour_road)
    x_budunit.add_idea(ideaunit_shop("55-:55"), hour_road)
    x_budunit.add_idea(ideaunit_shop("56-:56"), hour_road)
    x_budunit.add_idea(ideaunit_shop("57-:57"), hour_road)
    x_budunit.add_idea(ideaunit_shop("58-:58"), hour_road)
    x_budunit.add_idea(ideaunit_shop("59-:59"), hour_road)

    # month_road branch
    month_road = x_budunit.make_road(tech_road, month_str())
    month_idea = ideaunit_shop(month_str())
    x_budunit.add_idea(month_idea, tech_road)
    x_budunit.add_idea(ideaunit_shop(Jan()), month_road)
    x_budunit.add_idea(ideaunit_shop(Feb28()), month_road)
    x_budunit.add_idea(ideaunit_shop(Feb29()), month_road)
    x_budunit.add_idea(ideaunit_shop(Mar()), month_road)
    x_budunit.add_idea(ideaunit_shop(Apr()), month_road)
    x_budunit.add_idea(ideaunit_shop(May()), month_road)
    x_budunit.add_idea(ideaunit_shop(Jun()), month_road)
    x_budunit.add_idea(ideaunit_shop(Jul()), month_road)
    x_budunit.add_idea(ideaunit_shop(Aug()), month_road)
    x_budunit.add_idea(ideaunit_shop(Sep()), month_road)
    x_budunit.add_idea(ideaunit_shop(Oct()), month_road)
    x_budunit.add_idea(ideaunit_shop(Nov()), month_road)
    x_budunit.add_idea(ideaunit_shop(Dec()), month_road)
    Jan_road = x_budunit.make_road(month_road, Jan())
    Feb28_road = x_budunit.make_road(month_road, Feb28())
    Feb29_road = x_budunit.make_road(month_road, Feb29())
    Mar_road = x_budunit.make_road(month_road, Mar())
    Apr_road = x_budunit.make_road(month_road, Apr())
    May_road = x_budunit.make_road(month_road, May())
    Jun_road = x_budunit.make_road(month_road, Jun())
    Jul_road = x_budunit.make_road(month_road, Jul())
    Aug_road = x_budunit.make_road(month_road, Aug())
    Sep_road = x_budunit.make_road(month_road, Sep())
    Oct_road = x_budunit.make_road(month_road, Oct())
    Nov_road = x_budunit.make_road(month_road, Nov())
    Dec_road = x_budunit.make_road(month_road, Dec())
    x_budunit.add_idea(ideaunit_shop(days_str()), Jan_road)
    x_budunit.add_idea(ideaunit_shop(days_str()), Feb28_road)
    x_budunit.add_idea(ideaunit_shop(days_str()), Feb29_road)
    x_budunit.add_idea(ideaunit_shop(days_str()), Mar_road)
    x_budunit.add_idea(ideaunit_shop(days_str()), Apr_road)
    x_budunit.add_idea(ideaunit_shop(days_str()), May_road)
    x_budunit.add_idea(ideaunit_shop(days_str()), Jun_road)
    x_budunit.add_idea(ideaunit_shop(days_str()), Jul_road)
    x_budunit.add_idea(ideaunit_shop(days_str()), Aug_road)
    x_budunit.add_idea(ideaunit_shop(days_str()), Sep_road)
    x_budunit.add_idea(ideaunit_shop(days_str()), Oct_road)
    x_budunit.add_idea(ideaunit_shop(days_str()), Nov_road)
    x_budunit.add_idea(ideaunit_shop(days_str()), Dec_road)

    # year4_noleap_road branch
    year4_noleap_road = x_budunit.make_road(tech_road, year4_no__leap_str())
    year4_noleap_idea = ideaunit_shop(year4_no__leap_str())
    x_budunit.add_idea(year4_noleap_idea, tech_road)
    x_budunit.add_idea(ideaunit_shop(year1_str()), year4_noleap_road)
    x_budunit.add_idea(ideaunit_shop(year2_str()), year4_noleap_road)
    x_budunit.add_idea(ideaunit_shop(year3_str()), year4_noleap_road)
    x_budunit.add_idea(ideaunit_shop(year4_str()), year4_noleap_road)

    # year4_withleap_road branch
    year4_withleap_road = x_budunit.make_road(tech_road, year4_withleap_str())
    year4_withleap_idea = ideaunit_shop(year4_withleap_str())
    x_budunit.add_idea(year4_withleap_idea, tech_road)
    x_budunit.add_idea(ideaunit_shop(year1_str()), year4_withleap_road)
    x_budunit.add_idea(ideaunit_shop(year2_str()), year4_withleap_road)
    x_budunit.add_idea(ideaunit_shop(year3_str()), year4_withleap_road)
    x_budunit.add_idea(ideaunit_shop(year4_str()), year4_withleap_road)

    # c400_road branch
    c400_road = x_budunit.make_road(tech_road, c400_str())
    c400_idea = ideaunit_shop(c400_str())
    x_budunit.add_idea(c400_idea, tech_road)
    node_0_100_road = x_budunit.make_road(c400_road, node_0_100_str())
    node_1_4_road = x_budunit.make_road(c400_road, node_1_4_str())
    node_1_96_road = x_budunit.make_road(c400_road, node_1_96_str())
    node_2_4_road = x_budunit.make_road(c400_road, node_2_4_str())
    node_2_96_road = x_budunit.make_road(c400_road, node_2_96_str())
    node_3_4_road = x_budunit.make_road(c400_road, node_3_4_str())
    node_3_96_road = x_budunit.make_road(c400_road, node_3_96_str())
    node_0_100_idea = ideaunit_shop(node_0_100_str())
    node_1_4_idea = ideaunit_shop(node_1_4_str())
    node_1_96_idea = ideaunit_shop(node_1_96_str())
    node_2_4_idea = ideaunit_shop(node_2_4_str())
    node_2_96_idea = ideaunit_shop(node_2_96_str())
    node_3_4_idea = ideaunit_shop(node_3_4_str())
    node_3_96_idea = ideaunit_shop(node_3_96_str())
    x_budunit.add_idea(node_0_100_idea, c400_road)
    x_budunit.add_idea(node_1_4_idea, c400_road)
    x_budunit.add_idea(node_1_96_idea, c400_road)
    x_budunit.add_idea(node_2_4_idea, c400_road)
    x_budunit.add_idea(node_2_96_idea, c400_road)
    x_budunit.add_idea(node_3_4_idea, c400_road)
    x_budunit.add_idea(node_3_96_idea, c400_road)
    x_budunit.add_idea(ideaunit_shop(year4_withleap_str()), node_0_100_road)
    x_budunit.add_idea(ideaunit_shop(year4_no__leap_str()), node_1_4_road)
    x_budunit.add_idea(ideaunit_shop(year4_withleap_str()), node_1_96_road)
    x_budunit.add_idea(ideaunit_shop(year4_no__leap_str()), node_2_4_road)
    x_budunit.add_idea(ideaunit_shop(year4_withleap_str()), node_2_96_road)
    x_budunit.add_idea(ideaunit_shop(year4_no__leap_str()), node_3_4_road)
    x_budunit.add_idea(ideaunit_shop(year4_withleap_str()), node_3_96_road)

    # jajatime_str branch
    jajatime_idea = ideaunit_shop(get_jajatime_text(), time_road)
    jaja_road = x_budunit.make_road(time_road, get_jajatime_text())
    x_budunit.add_idea(jajatime_idea, time_road)

    # years_road
    years_road = x_budunit.make_road(jaja_road, years_str())
    print(f"{years_road=}")
    jaja_years_idea = ideaunit_shop(years_str())
    x_budunit.add_idea(jaja_years_idea, jaja_road)
    yr2010_road = x_budunit.make_road(years_road, yr2010min_str())
    yr2011_road = x_budunit.make_road(years_road, yr2011min_str())
    yr2012_road = x_budunit.make_road(years_road, yr2012min_str())
    yr2013_road = x_budunit.make_road(years_road, yr2013min_str())
    yr2014_road = x_budunit.make_road(years_road, yr2014min_str())
    yr2015_road = x_budunit.make_road(years_road, yr2015min_str())
    yr2016_road = x_budunit.make_road(years_road, yr2016min_str())
    yr2017_road = x_budunit.make_road(years_road, yr2017min_str())
    yr2018_road = x_budunit.make_road(years_road, yr2018min_str())
    yr2019_road = x_budunit.make_road(years_road, yr2019min_str())
    yr2020_road = x_budunit.make_road(years_road, yr2020min_str())
    yr2021_road = x_budunit.make_road(years_road, yr2021min_str())
    yr2022_road = x_budunit.make_road(years_road, yr2022min_str())
    yr2023_road = x_budunit.make_road(years_road, yr2023min_str())
    yr2024_road = x_budunit.make_road(years_road, yr2024min_str())
    yr2025_road = x_budunit.make_road(years_road, yr2025min_str())
    yr2026_road = x_budunit.make_road(years_road, yr2026min_str())
    yr2027_road = x_budunit.make_road(years_road, yr2027min_str())
    yr2028_road = x_budunit.make_road(years_road, yr2028min_str())
    yr2029_road = x_budunit.make_road(years_road, yr2029min_str())
    yr2030_road = x_budunit.make_road(years_road, yr2030min_str())
    idea_2010 = ideaunit_shop(yr2010min_str())  # [1057158720, 1057684320]
    idea_2011 = ideaunit_shop(yr2011min_str())  # [1057684320, 1058209920]
    idea_2012 = ideaunit_shop(yr2012min_str())  # [1058209920, 1058736960]
    idea_2013 = ideaunit_shop(yr2013min_str())  # [1058736960, 1059262560]
    idea_2014 = ideaunit_shop(yr2014min_str())  # [1059262560, 1059788160]
    idea_2015 = ideaunit_shop(yr2015min_str())  # [1059788160, 1060313760]
    idea_2016 = ideaunit_shop(yr2016min_str())  # [1060313760, 1060840800]
    idea_2017 = ideaunit_shop(yr2017min_str())  # [1060840800, 1061366400]
    idea_2018 = ideaunit_shop(yr2018min_str())  # [1061366400, 1061892000]
    idea_2019 = ideaunit_shop(yr2019min_str())  # [1061892000, 1062417600]
    idea_2020 = ideaunit_shop(yr2020min_str())  # [1062417600, 1062944640]
    idea_2021 = ideaunit_shop(yr2021min_str())  # [1062944640, 1063470240]
    idea_2022 = ideaunit_shop(yr2022min_str())  # [1063470240, 1063995840]
    idea_2023 = ideaunit_shop(yr2023min_str())  # [1063995840, 1064521440]
    idea_2024 = ideaunit_shop(yr2024min_str())  # [1064521440, 1065048480]
    idea_2025 = ideaunit_shop(yr2025min_str())  # [1065048480, 1065574080]
    idea_2026 = ideaunit_shop(yr2026min_str())  # [1065574080, 1066099680]
    idea_2027 = ideaunit_shop(yr2027min_str())  # [1066099680, 1066625280]
    idea_2028 = ideaunit_shop(yr2028min_str())  # [1066625280, 1067152320]
    idea_2029 = ideaunit_shop(yr2029min_str())  # [1067152320, 1067677920]
    idea_2030 = ideaunit_shop(yr2030min_str())  # [1067677920, 1068203520]
    x_budunit.add_idea(idea_2010, years_road)
    x_budunit.add_idea(idea_2011, years_road)
    x_budunit.add_idea(idea_2012, years_road)
    x_budunit.add_idea(idea_2013, years_road)
    x_budunit.add_idea(idea_2014, years_road)
    x_budunit.add_idea(idea_2015, years_road)
    x_budunit.add_idea(idea_2016, years_road)
    x_budunit.add_idea(idea_2017, years_road)
    x_budunit.add_idea(idea_2018, years_road)
    x_budunit.add_idea(idea_2019, years_road)
    x_budunit.add_idea(idea_2020, years_road)
    x_budunit.add_idea(idea_2021, years_road)
    x_budunit.add_idea(idea_2022, years_road)
    x_budunit.add_idea(idea_2023, years_road)
    x_budunit.add_idea(idea_2024, years_road)
    x_budunit.add_idea(idea_2025, years_road)
    x_budunit.add_idea(idea_2026, years_road)
    x_budunit.add_idea(idea_2027, years_road)
    x_budunit.add_idea(idea_2028, years_road)
    x_budunit.add_idea(idea_2029, years_road)
    x_budunit.add_idea(idea_2030, years_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2010_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2011_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2012_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2013_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2014_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2015_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2016_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2017_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2018_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2019_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2020_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2021_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2022_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2023_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2024_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2025_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2026_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2027_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2028_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2029_road)
    x_budunit.add_idea(ideaunit_shop(morph_str()), yr2030_road)
    yr2010mor_road = x_budunit.make_road(yr2010_road, morph_str())
    yr2011mor_road = x_budunit.make_road(yr2011_road, morph_str())
    yr2012mor_road = x_budunit.make_road(yr2012_road, morph_str())
    yr2013mor_road = x_budunit.make_road(yr2013_road, morph_str())
    yr2014mor_road = x_budunit.make_road(yr2014_road, morph_str())
    yr2015mor_road = x_budunit.make_road(yr2015_road, morph_str())
    yr2016mor_road = x_budunit.make_road(yr2016_road, morph_str())
    yr2017mor_road = x_budunit.make_road(yr2017_road, morph_str())
    yr2018mor_road = x_budunit.make_road(yr2018_road, morph_str())
    yr2019mor_road = x_budunit.make_road(yr2019_road, morph_str())
    yr2020mor_road = x_budunit.make_road(yr2020_road, morph_str())
    yr2021mor_road = x_budunit.make_road(yr2021_road, morph_str())
    yr2022mor_road = x_budunit.make_road(yr2022_road, morph_str())
    yr2023mor_road = x_budunit.make_road(yr2023_road, morph_str())
    yr2024mor_road = x_budunit.make_road(yr2024_road, morph_str())
    yr2025mor_road = x_budunit.make_road(yr2025_road, morph_str())
    yr2026mor_road = x_budunit.make_road(yr2026_road, morph_str())
    yr2027mor_road = x_budunit.make_road(yr2027_road, morph_str())
    yr2028mor_road = x_budunit.make_road(yr2028_road, morph_str())
    yr2029mor_road = x_budunit.make_road(yr2029_road, morph_str())
    yr2030mor_road = x_budunit.make_road(yr2030_road, morph_str())
    x_budunit.add_idea(ideaunit_shop(yr2010yr_str()), yr2010mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2011yr_str()), yr2011mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2012yr_str()), yr2012mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2013yr_str()), yr2013mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2014yr_str()), yr2014mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2015yr_str()), yr2015mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2016yr_str()), yr2016mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2017yr_str()), yr2017mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2018yr_str()), yr2018mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2019yr_str()), yr2019mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2020yr_str()), yr2020mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2021yr_str()), yr2021mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2022yr_str()), yr2022mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2023yr_str()), yr2023mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2024yr_str()), yr2024mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2025yr_str()), yr2025mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2026yr_str()), yr2026mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2027yr_str()), yr2027mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2028yr_str()), yr2028mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2029yr_str()), yr2029mor_road)
    x_budunit.add_idea(ideaunit_shop(yr2030yr_str()), yr2030mor_road)

    jaja_c400_idea = ideaunit_shop(c400_str())
    x_budunit.add_idea(jaja_c400_idea, jaja_road)
    jaja_c400s_idea = ideaunit_shop(c400s_str())
    x_budunit.add_idea(jaja_c400s_idea, jaja_road)
    jaja_day_idea = ideaunit_shop(day_str())
    x_budunit.add_idea(jaja_day_idea, jaja_road)
    jaja_days_idea = ideaunit_shop(days_str())
    x_budunit.add_idea(jaja_days_idea, jaja_road)
    jaja_week_idea = ideaunit_shop(week_str())
    x_budunit.add_idea(jaja_week_idea, jaja_road)
    jaja_weeks_idea = ideaunit_shop(weeks_str())
    x_budunit.add_idea(jaja_weeks_idea, jaja_road)

    return x_budunit


def years_str() -> str:
    return "years"


def year4_no__leap_str() -> str:
    return "4year wo leap"


def year4_withleap_str() -> str:
    return "4year with leap"


def year365_str() -> str:
    return "365 year"


def year366_str() -> str:
    return "366 year"


def month_str() -> str:
    return "month"


def day_str() -> str:
    return "day"


def hour_str() -> str:
    return "hour"


def weekday_idea_str() -> str:
    return "weekday_idea"


def time_str() -> str:
    return "time"


def tech_str() -> str:
    return "tech"


def min_str() -> str:
    return "minutes"


def get_jajatime_text():
    return "jajatime"


def get_Sun():
    return "Sunday"


def get_Mon():
    return "Monday"


def get_Tue():
    return "Tuesday"


def get_Wed():
    return "Wednesday"


def get_Thu():
    return "Thursday"


def get_Fri():
    return "Friday"


def get_Sat():
    return "Saturday"


def c400_str():
    return "400 year segment"


def c400s_str():
    return f"{c400_str()}s"


def week_str():
    return "week"


def weeks_str():
    return f"{week_str()}s"


def day_str():
    return "day"


def days_str():
    return f"{day_str()}s"


def Jan():
    return "Jan"


def Feb28():
    return "Feb28"


def Feb29():
    return "Feb29"


def Mar():
    return "Mar"


def Apr():
    return "Apr"


def May():
    return "May"


def Jun():
    return "Jun"


def Jul():
    return "Jul"


def Aug():
    return "Aug"


def Sep():
    return "Sep"


def Oct():
    return "Oct"


def Nov():
    return "Nov"


def Dec():
    return "Dec"


def year_str() -> str:
    return "years"


def year1_str() -> str:
    return "1-year"


def year2_str() -> str:
    return "2-year"


def year3_str() -> str:
    return "3-year"


def year4_str() -> str:
    return "4-year"


def _get_jajatime_week_legible_text(x_budunit: BudUnit, open: int, divisor: int) -> str:
    x_hregidea = HregTimeIdeaSource(x_budunit._road_delimiter)
    open_in_week = open % divisor
    time_road = x_budunit.make_l1_road("time")
    tech_road = x_budunit.make_road(time_road, "tech")
    week_road = x_budunit.make_road(tech_road, "week")
    weekday_ideas_dict = x_budunit.get_idea_ranged_kids(week_road, open_in_week)
    weekday_idea_node = None
    # for idea in weekday_ideas_dict.values():
    #     weekday_idea_node = idea

    # if divisor == 10080:
    #     return f"every {weekday_idea_node._label} at {x_hregidea.readable_1440_time(min1440=open % 1440)}"
    # num_with_letter_ending = x_hregidea.get_number_with_letter_ending(
    #     num=divisor // 10080
    # )
    # return f"every {num_with_letter_ending} {weekday_idea_node._label} at {x_hregidea.readable_1440_time(min1440=open % 1440)}"


def node_0_100_str() -> str:
    return "0-100-25 leap years"


def node_1_4_str() -> str:
    return "100-104-0 leap years"


def node_1_96_str() -> str:
    return "104-200-24 leap years"


def node_2_4_str() -> str:
    return "200-204-0 leap years"


def node_2_96_str() -> str:
    return "204-300-24 leap years"


def node_3_4_str() -> str:
    return "300-304-0 leap years"


def node_3_96_str() -> str:
    return "304-400-24 leap years"


def yr2010min_str() -> str:
    return "2010 by minute"


def yr2011min_str() -> str:
    return "2011 by minute"


def yr2012min_str() -> str:
    return "2012 by minute"


def yr2013min_str() -> str:
    return "2013 by minute"


def yr2014min_str() -> str:
    return "2014 by minute"


def yr2015min_str() -> str:
    return "2015 by minute"


def yr2016min_str() -> str:
    return "2016 by minute"


def yr2017min_str() -> str:
    return "2017 by minute"


def yr2018min_str() -> str:
    return "2018 by minute"


def yr2019min_str() -> str:
    return "2019 by minute"


def yr2020min_str() -> str:
    return "2020 by minute"


def yr2021min_str() -> str:
    return "2021 by minute"


def yr2022min_str() -> str:
    return "2022 by minute"


def yr2023min_str() -> str:
    return "2023 by minute"


def yr2024min_str() -> str:
    return "2024 by minute"


def yr2025min_str() -> str:
    return "2025 by minute"


def yr2026min_str() -> str:
    return "2026 by minute"


def yr2027min_str() -> str:
    return "2027 by minute"


def yr2028min_str() -> str:
    return "2028 by minute"


def yr2029min_str() -> str:
    return "2029 by minute"


def yr2030min_str() -> str:
    return "2030 by minute"


def morph_str() -> str:
    return "morph"


def yr2010yr_str() -> str:
    return "2010 as year"


def yr2011yr_str() -> str:
    return "2011 as year"


def yr2012yr_str() -> str:
    return "2012 as year"


def yr2013yr_str() -> str:
    return "2013 as year"


def yr2014yr_str() -> str:
    return "2014 as year"


def yr2015yr_str() -> str:
    return "2015 as year"


def yr2016yr_str() -> str:
    return "2016 as year"


def yr2017yr_str() -> str:
    return "2017 as year"


def yr2018yr_str() -> str:
    return "2018 as year"


def yr2019yr_str() -> str:
    return "2019 as year"


def yr2020yr_str() -> str:
    return "2020 as year"


def yr2021yr_str() -> str:
    return "2021 as year"


def yr2022yr_str() -> str:
    return "2022 as year"


def yr2023yr_str() -> str:
    return "2023 as year"


def yr2024yr_str() -> str:
    return "2024 as year"


def yr2025yr_str() -> str:
    return "2025 as year"


def yr2026yr_str() -> str:
    return "2026 as year"


def yr2027yr_str() -> str:
    return "2027 as year"


def yr2028yr_str() -> str:
    return "2028 as year"


def yr2029yr_str() -> str:
    return "2029 as year"


def yr2030yr_str() -> str:
    return "2030 as year"
