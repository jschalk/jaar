from src.agent.tool import ToolKid
from src.agent.required import (
    acptfactunit_shop,
    sufffactunit_shop,
    RequiredUnit,
    acptfactunit_shop,
)
from src.agent.agent import AgentUnit, get_from_json
from src.agent.x_func import open_file as x_func_open_file
from src.agent.examples.get_agent_examples_dir import get_agent_examples_dir


def agent_v001() -> AgentUnit:
    return get_from_json(
        x_func_open_file(
            dest_dir=get_agent_examples_dir(), file_name="example_agent1.json"
        )
    )


def agent_v001_with_large_agenda() -> AgentUnit:
    a1 = agent_v001()
    day_minute_text = "day_minute"
    day_minute_road = f"{a1._desc},{day_minute_text}"
    month_week_text = "month_week"
    month_week_road = f"{a1._desc},{month_week_text}"
    nations_text = "Nation-States"
    nations_road = f"{a1._desc},{nations_text}"
    mood_text = "Moods"
    mood_road = f"{a1._desc},{mood_text}"
    aaron_text = "Aaron Donald sphere"
    aaron_road = f"{a1._desc},{aaron_text}"
    # internet_text = "Internet"
    # internet_road = f"{a1._desc},{internet_text}"
    year_month_text = "year_month"
    year_month_road = f"{a1._desc},{year_month_text}"
    season_text = "Seasons"
    season_road = f"{a1._desc},{season_text}"
    ced_week_text = "ced_week"
    ced_week_road = f"{a1._desc},{ced_week_text}"
    # water_text = "WaterBeing"
    # water_road = f"{a1._desc},{water_text}"
    weekdays_text = "weekdays"
    weekdays_road = f"{a1._desc},{weekdays_text}"
    # movie_text = "No Movie playing"
    # movie_road = f"{a1._desc},{movie_text}"

    a1.set_acptfact(base=aaron_road, pick=aaron_road)
    a1.set_acptfact(base=ced_week_road, pick=ced_week_road, open=0, nigh=53)
    a1.set_acptfact(base=day_minute_road, pick=day_minute_road, open=0, nigh=1399)
    # a1.set_acptfact(base=internet, pick=internet)
    a1.set_acptfact(base=month_week_road, pick=month_week_road, open=0, nigh=5)
    a1.set_acptfact(base=mood_road, pick=mood_road)
    # a1.set_acptfact(base=movie, pick=movie)
    a1.set_acptfact(base=nations_road, pick=nations_road)
    a1.set_acptfact(base=season_road, pick=season_road)
    a1.set_acptfact(base=year_month_road, pick=year_month_road, open=0, nigh=12)
    # a1.set_acptfact(base=water, pick=water)
    a1.set_acptfact(base=weekdays_road, pick=weekdays_road)

    return a1


def agent_v002() -> AgentUnit:
    return get_from_json(
        x_func_open_file(
            dest_dir=get_agent_examples_dir(), file_name="example_agent2.json"
        )
    )


def get_agent_with_4_levels() -> AgentUnit:
    src_road = "src"
    agent_x = AgentUnit(_weight=10, _desc=src_road)

    work = "work"
    tool_kid_work = ToolKid(_weight=30, _desc=work, promise=True)
    agent_x.add_tool(tool_kid=tool_kid_work, walk=src_road)

    cat = "feed cat"
    tool_kid_feedcat = ToolKid(_weight=30, _desc=cat, promise=True)
    agent_x.add_tool(tool_kid=tool_kid_feedcat, walk=src_road)

    week_text = "weekdays"
    week_road = f"{src_road},{week_text}"
    tool_kid_weekdays = ToolKid(_weight=40, _desc=week_text)
    agent_x.add_tool(tool_kid=tool_kid_weekdays, walk=src_road)

    sun_text = "Sunday"
    mon_text = "Monday"
    tue_text = "Tuesday"
    wed_text = "Wednesday"
    thu_text = "Thursday"
    fri_text = "Friday"
    sat_text = "Saturday"

    tool_grandkidU = ToolKid(_weight=20, _desc=sun_text)
    tool_grandkidM = ToolKid(_weight=20, _desc=mon_text)
    tool_grandkidT = ToolKid(_weight=20, _desc=tue_text)
    tool_grandkidW = ToolKid(_weight=20, _desc=wed_text)
    tool_grandkidR = ToolKid(_weight=30, _desc=thu_text)
    tool_grandkidF = ToolKid(_weight=40, _desc=fri_text)
    tool_grandkidA = ToolKid(_weight=50, _desc=sat_text)

    agent_x.add_tool(tool_grandkidU, week_road)
    agent_x.add_tool(tool_grandkidM, week_road)
    agent_x.add_tool(tool_grandkidT, week_road)
    agent_x.add_tool(tool_grandkidW, week_road)
    agent_x.add_tool(tool_grandkidR, week_road)
    agent_x.add_tool(tool_grandkidF, week_road)
    agent_x.add_tool(tool_grandkidA, week_road)

    states_text = "nation-state"
    states_road = f"{src_road},{states_text}"
    tool_kid_states = ToolKid(_weight=30, _desc=states_text)
    agent_x.add_tool(tool_kid=tool_kid_states, walk=f"{src_road}")

    usa_text = "USA"
    usa_road = f"{states_road},{usa_text}"
    france_text = "France"
    brazil_text = "Brazil"
    tool_grandkid_usa = ToolKid(_weight=50, _desc=usa_text)
    tool_grandkid_france = ToolKid(_weight=50, _desc=france_text)
    tool_grandkid_brazil = ToolKid(_weight=50, _desc=brazil_text)
    agent_x.add_tool(tool_grandkid_france, states_road)
    agent_x.add_tool(tool_grandkid_brazil, states_road)
    agent_x.add_tool(tool_grandkid_usa, states_road)

    texas_text = "Texas"
    oregon_text = "Oregon"
    tool_grandgrandkid_usa_texas = ToolKid(_weight=50, _desc=texas_text)
    tool_grandgrandkid_usa_oregon = ToolKid(_weight=50, _desc=oregon_text)
    agent_x.add_tool(tool_grandgrandkid_usa_texas, usa_road)
    agent_x.add_tool(tool_grandgrandkid_usa_oregon, usa_road)
    return agent_x


def get_agent_with_4_levels_and_2requireds() -> AgentUnit:
    agent_x = get_agent_with_4_levels()
    week_road = f"{agent_x._desc},weekdays"
    wed_text = "Wednesday"
    wed_road = f"{week_road},{wed_text}"
    wed_sufffact = sufffactunit_shop(need=wed_road)

    nation_road = f"{agent_x._desc},nation-state"
    usa_road = f"{nation_road},USA"
    usa_sufffact_x = sufffactunit_shop(need=usa_road)
    work_wk_required = RequiredUnit(
        base=week_road, sufffacts={wed_sufffact.need: wed_sufffact}
    )
    nation_required = RequiredUnit(
        base=nation_road, sufffacts={usa_sufffact_x.need: usa_sufffact_x}
    )
    work_text = "work"
    work_road = f"{agent_x._desc},{work_text}"
    agent_x.edit_tool_attr(road=work_road, required=work_wk_required)
    agent_x.edit_tool_attr(road=work_road, required=nation_required)
    return agent_x


def get_agent_with_4_levels_and_2requireds_2acptfacts() -> AgentUnit:
    agent_x = get_agent_with_4_levels_and_2requireds()
    wednesday = f"{agent_x._desc},weekdays,Wednesday"
    weekday = f"{agent_x._desc},weekdays"
    states = f"{agent_x._desc},nation-state"
    usa_road = f"{agent_x._desc},nation-state,USA"
    agent_x.set_acptfact(base=weekday, pick=wednesday)
    agent_x.set_acptfact(base=states, pick=usa_road)
    return agent_x


def get_agent_with7amCleanTableRequired() -> AgentUnit:
    agent_x = get_agent_with_4_levels_and_2requireds_2acptfacts()
    src = agent_x._desc
    timetech = "timetech"
    day_24hr = "24hr day"
    am = "am"
    pm = "pm"
    tool_timeline = ToolKid(_weight=40, _desc=timetech)
    tool_24hr_day = ToolKid(_weight=40, _desc=day_24hr, _begin=0.0, _close=24.0)
    tool_am = ToolKid(_weight=50, _desc=am, _begin=0, _close=12)
    tool_01 = ToolKid(_weight=50, _desc="1", _begin=1, _close=2)
    tool_02 = ToolKid(_weight=50, _desc="2", _begin=2, _close=3)
    tool_03 = ToolKid(_weight=50, _desc="3", _begin=3, _close=4)
    tool_pm = ToolKid(_weight=50, _desc=pm, _begin=12, _close=24)

    time_road = f"{src},{timetech}"
    day24hr_road = f"{time_road},{day_24hr}"
    am_road = f"{day_24hr},{am}"
    agent_x.add_tool(tool_timeline, src)
    agent_x.add_tool(tool_24hr_day, time_road)
    agent_x.add_tool(tool_am, day24hr_road)
    agent_x.add_tool(tool_pm, day24hr_road)
    agent_x.add_tool(tool_01, am_road)  # tool_am
    agent_x.add_tool(tool_02, am_road)  # tool_am
    agent_x.add_tool(tool_03, am_road)  # tool_am

    housework = "housework"
    house_road = f"{src},{housework}"
    clean_table = "clean table"
    clean_road = f"{house_road},{clean_table}"
    remove_dish = "remove dishs"
    get_soap = "get soap"
    get_soap_road = f"{clean_road},{get_soap}"
    remove_dish = "remove dishs"
    tool_housework = ToolKid(_weight=40, _desc=housework)
    tool_cleantable = ToolKid(_weight=40, _desc=clean_table, promise=True)
    tool_tabledishs = ToolKid(_weight=40, _desc=remove_dish, promise=True)
    tool_tablesoap = ToolKid(_weight=40, _desc=get_soap, promise=True)
    tool_grabsoap = ToolKid(_weight=40, _desc="grab soap", promise=True)

    agent_x.add_tool(tool_kid=tool_housework, walk=src)
    agent_x.add_tool(tool_kid=tool_cleantable, walk=house_road)
    agent_x.add_tool(tool_kid=tool_tabledishs, walk=clean_road)
    agent_x.add_tool(tool_kid=tool_tablesoap, walk=clean_road)
    agent_x.add_tool(tool_kid=tool_grabsoap, walk=get_soap_road)

    clean_table_7am_base = day24hr_road
    clean_table_7am_sufffact_road = day24hr_road
    clean_table_7am_sufffact_open = 7.0
    clean_table_7am_sufffact_nigh = 7.0
    clean_table_7am_sufffact_x = sufffactunit_shop(
        need=clean_table_7am_sufffact_road,
        open=clean_table_7am_sufffact_open,
        nigh=clean_table_7am_sufffact_nigh,
    )
    clean_table_7am_required = RequiredUnit(
        base=clean_table_7am_base,
        sufffacts={clean_table_7am_sufffact_x.need: clean_table_7am_sufffact_x},
    )
    agent_x.edit_tool_attr(
        road=f"{agent_x._desc},housework,clean table", required=clean_table_7am_required
    )
    agent_x.edit_tool_attr(
        road=f"{agent_x._desc},work", required=clean_table_7am_required
    )
    return agent_x


def get_agent_1Task_1CE0MinutesRequired_1AcptFact() -> AgentUnit:
    lw_desc = "test45"
    agent_x = AgentUnit(_weight=10, _desc=lw_desc)
    ced_min_desc = "CE0_minutes"
    ced_minutes = ToolKid(_desc=ced_min_desc)
    ced_road = f"{lw_desc},{ced_min_desc}"
    agent_x.add_tool(tool_kid=ced_minutes, walk=lw_desc)
    mail_desc = "obtain mail"
    mail_task = ToolKid(_desc=mail_desc, promise=True)
    agent_x.add_tool(tool_kid=mail_task, walk=lw_desc)

    sufffact_x = sufffactunit_shop(need=ced_road, open=80, nigh=90)
    x_task_required = RequiredUnit(
        base=sufffact_x.need, sufffacts={sufffact_x.need: sufffact_x}
    )
    mail_road = f"{lw_desc},{mail_desc}"
    agent_x.edit_tool_attr(road=mail_road, required=x_task_required)

    x_acptfact = acptfactunit_shop(base=ced_road, pick=ced_road, open=85, nigh=95)
    # print(
    #     f"1Task_1CE0MinutesRequired_1AcptFact 2. {len(agent_x._toolroot._kids)=} {x_acptfact.base=}"
    # )
    agent_x.set_acptfact(
        base=x_acptfact.base,
        pick=x_acptfact.pick,
        open=x_acptfact.open,
        nigh=x_acptfact.nigh,
    )
    # print(f"1Task_1CE0MinutesRequired_1AcptFact 3. {len(agent_x._toolroot._kids)=}")

    return agent_x


def get_agent_x1_3levels_1required_1acptfacts() -> AgentUnit:
    prom = "prom"
    x_agent = AgentUnit(_weight=10, _desc=prom)
    tool_kid_shave = ToolKid(_weight=30, _desc="shave", promise=True)
    x_agent.add_tool(tool_kid=tool_kid_shave, walk=prom)
    weekdays = "weekdays"
    tool_kid_weekdays = ToolKid(_weight=40, _desc=weekdays)
    x_agent.add_tool(tool_kid=tool_kid_weekdays, walk=prom)

    tool_grandkidU = ToolKid(_weight=20, _desc="Sunday")
    tool_grandkidM = ToolKid(_weight=20, _desc="Monday")
    week_road = f"{prom},{weekdays}"
    x_agent.add_tool(tool_kid=tool_grandkidU, walk=week_road)
    x_agent.add_tool(tool_kid=tool_grandkidM, walk=week_road)

    shave_base = "prom,weekdays"
    shave_sufffact_road = "prom,weekdays,Monday"
    shave_sufffact_x = sufffactunit_shop(need=shave_sufffact_road)
    shave_required = RequiredUnit(
        base=shave_base,
        sufffacts={shave_sufffact_x.need: shave_sufffact_x},
    )

    x_agent.edit_tool_attr(road="prom,shave", required=shave_required)
    x_agent.set_acptfact(base="prom,weekdays", pick="prom,weekdays,Sunday")
    acptfactunit_x = acptfactunit_shop(
        base="prom,weekdays", pick="prom,weekdays,Sunday,church"
    )
    x_agent.edit_tool_attr(road="prom,shave", acptfactunit=acptfactunit_x)
    return x_agent


def get_agent_base_time_example() -> AgentUnit:
    g_src = "src"
    g_lw = AgentUnit(_desc=g_src)
    plant = "plant"
    x_tool = ToolKid(_desc=plant)
    g_lw.add_tool(x_tool, walk=g_src)

    return g_lw


def get_agent_irrational_example() -> AgentUnit:
    # this agent has no conclusive agenda because 2 promise tools are in contradiction
    # "egg first" is true when "chicken first" is false
    # "chicken first" is true when "egg first" is true
    # Step 0: if chicken._active_status == True, egg._active_status is set to False
    # Step 1: if egg._active_status == False, chicken._active_status is set to False
    # Step 2: if chicken._active_status == False, egg._active_status is set to True
    # Step 3: if egg._active_status == True, chicken._active_status is set to True
    # Step 4: back to step 0.
    # after agent_x.set_agent_metrics these should be true:
    # 1. agent_x._irrational == True
    # 2. agent_x._tree_traverse_count = agent_x._max_tree_traverse

    src_road = "src"
    agent_x = AgentUnit(_weight=10, _desc=src_road)
    agent_x.set_max_tree_traverse(3)

    egg_text = "egg first"
    egg_road = f"{src_road},{egg_text}"
    agent_x.add_tool(tool_kid=ToolKid(_desc=egg_text), walk=src_road)

    chicken_text = "chicken first"
    chicken_road = f"{src_road},{chicken_text}"
    agent_x.add_tool(tool_kid=ToolKid(_desc=chicken_text), walk=src_road)

    # set egg promise is True when chicken first is False
    agent_x.edit_tool_attr(
        road=egg_road,
        promise=True,
        required_base=chicken_road,
        required_suff_tool_active_status=True,
    )

    # set chick promise is True when egg first is False
    agent_x.edit_tool_attr(
        road=chicken_road,
        promise=True,
        required_base=egg_road,
        required_suff_tool_active_status=False,
    )

    return agent_x
