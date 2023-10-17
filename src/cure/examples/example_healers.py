from src.deal.deal import DealUnit, IdeaKid, assigned_unit_shop
from src.cure.healing import healingunit_shop, HealingUnit
from src.cure.examples.healer_env_kit import get_temp_cure_handle

from random import randrange


def get_1node_deal() -> DealUnit:
    a_text = "A"
    x_deal = DealUnit(_healer=a_text)
    x_deal.set_cure_handle(get_temp_cure_handle())
    x_deal.set_deal_metrics()
    return x_deal


def get_Jnode2node_deal() -> DealUnit:
    healer_text = "J"
    x_deal = DealUnit(_healer=healer_text)
    x_deal.set_cure_handle(get_temp_cure_handle())
    a_text = "A"
    idea_a = IdeaKid(_label=a_text)
    x_deal.add_idea(idea_kid=idea_a, pad=get_temp_cure_handle())
    x_deal.set_deal_metrics()
    return x_deal


def get_2node_deal() -> DealUnit:
    healer_text = "A"
    b_text = "B"
    x_deal = DealUnit(_healer=healer_text)
    x_deal.set_cure_handle(get_temp_cure_handle())
    idea_b = IdeaKid(_label=b_text)
    x_deal.add_idea(idea_kid=idea_b, pad=get_temp_cure_handle())
    x_deal.set_deal_metrics()
    return x_deal


def get_3node_deal() -> DealUnit:
    a_text = "A"
    a_road = a_text
    x_deal = DealUnit(_healer=a_text)
    x_deal.set_cure_handle(get_temp_cure_handle())
    b_text = "B"
    idea_b = IdeaKid(_label=b_text)
    c_text = "C"
    idea_c = IdeaKid(_label=c_text)
    x_deal.add_idea(idea_kid=idea_b, pad=a_road)
    x_deal.add_idea(idea_kid=idea_c, pad=a_road)
    x_deal.set_deal_metrics()
    return x_deal


def get_3node_D_E_F_deal() -> DealUnit:
    d_text = "D"
    d_road = d_text
    x_deal = DealUnit(_healer=d_text)
    x_deal.set_cure_handle(get_temp_cure_handle())
    b_text = "E"
    idea_b = IdeaKid(_label=b_text)
    c_text = "F"
    idea_c = IdeaKid(_label=c_text)
    x_deal.add_idea(idea_kid=idea_b, pad=d_road)
    x_deal.add_idea(idea_kid=idea_c, pad=d_road)
    x_deal.set_deal_metrics()
    return x_deal


def get_6node_deal() -> DealUnit:
    x_deal = DealUnit(_healer="A")
    x_deal.set_cure_handle(get_temp_cure_handle())
    idea_b = IdeaKid(_label="B")
    idea_c = IdeaKid(_label="C")
    idea_d = IdeaKid(_label="D")
    idea_e = IdeaKid(_label="E")
    idea_f = IdeaKid(_label="F")
    x_deal.add_idea(idea_kid=idea_b, pad="A")
    x_deal.add_idea(idea_kid=idea_c, pad="A")
    x_deal.add_idea(idea_kid=idea_d, pad="A,C")
    x_deal.add_idea(idea_kid=idea_e, pad="A,C")
    x_deal.add_idea(idea_kid=idea_f, pad="A,C")
    x_deal.set_deal_metrics()
    return x_deal


def get_7nodeInsertH_deal() -> DealUnit:
    x_deal = DealUnit(_healer="A")
    x_deal.set_cure_handle(get_temp_cure_handle())
    idea_b = IdeaKid(_label="B")
    idea_c = IdeaKid(_label="C")
    idea_h = IdeaKid(_label="H")
    idea_d = IdeaKid(_label="D")
    idea_e = IdeaKid(_label="E")
    idea_f = IdeaKid(_label="F")
    x_deal.add_idea(idea_kid=idea_b, pad="A")
    x_deal.add_idea(idea_kid=idea_c, pad="A")
    x_deal.add_idea(idea_kid=idea_e, pad="A,C")
    x_deal.add_idea(idea_kid=idea_f, pad="A,C")
    x_deal.add_idea(idea_kid=idea_h, pad="A,C")
    x_deal.add_idea(idea_kid=idea_d, pad="A,C,H")
    x_deal.set_deal_metrics()
    return x_deal


def get_5nodeHG_deal() -> DealUnit:
    x_deal = DealUnit(_healer="A")
    x_deal.set_cure_handle(get_temp_cure_handle())
    idea_b = IdeaKid(_label="B")
    idea_c = IdeaKid(_label="C")
    idea_h = IdeaKid(_label="H")
    idea_g = IdeaKid(_label="G")
    x_deal.add_idea(idea_kid=idea_b, pad="A")
    x_deal.add_idea(idea_kid=idea_c, pad="A")
    x_deal.add_idea(idea_kid=idea_h, pad="A,C")
    x_deal.add_idea(idea_kid=idea_g, pad="A,C")
    x_deal.set_deal_metrics()
    return x_deal


def get_7nodeJRoot_deal() -> DealUnit:
    x_deal = DealUnit(_healer="J")
    x_deal.set_cure_handle(get_temp_cure_handle())
    idea_a = IdeaKid(_label="A")
    idea_b = IdeaKid(_label="B")
    idea_c = IdeaKid(_label="C")
    idea_d = IdeaKid(_label="D")
    idea_e = IdeaKid(_label="E")
    idea_f = IdeaKid(_label="F")
    x_deal.add_idea(idea_kid=idea_a, pad="J")
    x_deal.add_idea(idea_kid=idea_b, pad="J,A")
    x_deal.add_idea(idea_kid=idea_c, pad="J,A")
    x_deal.add_idea(idea_kid=idea_d, pad="J,A,C")
    x_deal.add_idea(idea_kid=idea_e, pad="J,A,C")
    x_deal.add_idea(idea_kid=idea_f, pad="J,A,C")
    x_deal.set_deal_metrics()
    return x_deal


def get_7nodeJRootWithH_deal() -> DealUnit:
    x_deal = DealUnit(_healer="J")
    x_deal.set_cure_handle(get_temp_cure_handle())
    idea_a = IdeaKid(_label="A")
    idea_b = IdeaKid(_label="B")
    idea_c = IdeaKid(_label="C")
    idea_e = IdeaKid(_label="E")
    idea_f = IdeaKid(_label="F")
    idea_h = IdeaKid(_label="H")
    x_deal.add_idea(idea_kid=idea_a, pad="J")
    x_deal.add_idea(idea_kid=idea_b, pad="J,A")
    x_deal.add_idea(idea_kid=idea_c, pad="J,A")
    x_deal.add_idea(idea_kid=idea_e, pad="J,A,C")
    x_deal.add_idea(idea_kid=idea_f, pad="J,A,C")
    x_deal.add_idea(idea_kid=idea_h, pad="J,A,C")
    x_deal.set_deal_metrics()
    return x_deal


def get_healer_2deal(env_dir, cure_handle) -> HealingUnit:
    yao_text = "Xio"
    yao_healer = healingunit_shop(yao_text, env_dir, cure_handle)
    yao_healer.set_depot_deal(get_1node_deal(), depotlink_type="blind_trust")
    yao_healer.set_depot_deal(get_Jnode2node_deal(), depotlink_type="blind_trust")
    return yao_healer


def get_deal_2CleanNodesRandomWeights(_healer: str = None) -> DealUnit:
    healer_text = _healer if _healer != None else "ernie"
    x_deal = DealUnit(_healer=healer_text)
    casa_text = "casa"
    x_deal.add_idea(idea_kid=IdeaKid(_label=casa_text), pad="")
    casa_road = f"{x_deal._cure_handle},{casa_text}"
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    cookery_idea = IdeaKid(_label=cookery_text, _weight=randrange(1, 50), promise=True)
    bedroom_idea = IdeaKid(_label=bedroom_text, _weight=randrange(1, 50), promise=True)
    x_deal.add_idea(idea_kid=cookery_idea, pad=casa_road)
    x_deal.add_idea(idea_kid=bedroom_idea, pad=casa_road)
    x_deal.set_deal_metrics()
    return x_deal


def get_deal_3CleanNodesRandomWeights(_healer: str = None) -> DealUnit:
    healer_text = _healer if _healer != None else "ernie"
    x_deal = DealUnit(_healer=healer_text)
    casa_text = "casa"
    x_deal.add_idea(idea_kid=IdeaKid(_label=casa_text), pad="")
    casa_road = f"{x_deal._cure_handle},{casa_text}"
    cookery_text = "clean cookery"
    bedroom_text = "clean bedroom"
    hallway_text = "clean hallway"
    cookery_idea = IdeaKid(_label=cookery_text, _weight=randrange(1, 50), promise=True)
    bedroom_idea = IdeaKid(_label=bedroom_text, _weight=randrange(1, 50), promise=True)
    hallway_idea = IdeaKid(_label=hallway_text, _weight=randrange(1, 50), promise=True)
    x_deal.add_idea(idea_kid=cookery_idea, pad=casa_road)
    x_deal.add_idea(idea_kid=bedroom_idea, pad=casa_road)
    x_deal.add_idea(idea_kid=hallway_idea, pad=casa_road)
    x_deal.set_deal_metrics()
    return x_deal


def get_deal_assignment_laundry_example1() -> DealUnit:
    america_text = "America"
    america_deal = DealUnit(_healer=america_text)
    joachim_text = "Joachim"
    america_deal.add_partyunit(america_text)
    america_deal.add_partyunit(joachim_text)

    root_road = america_deal._cure_handle
    casa_text = "casa"
    casa_road = f"{root_road},{casa_text}"
    america_deal.add_idea(IdeaKid(_label=casa_text), pad=root_road)

    basket_text = "laundry basket status"
    basket_road = f"{casa_road},{basket_text}"
    america_deal.add_idea(IdeaKid(_label=basket_text), pad=casa_road)

    b_full_text = "full"
    b_full_road = f"{basket_road},{b_full_text}"
    america_deal.add_idea(IdeaKid(_label=b_full_text), pad=basket_road)

    b_smel_text = "smelly"
    b_smel_road = f"{basket_road},{b_smel_text}"
    america_deal.add_idea(IdeaKid(_label=b_smel_text), pad=basket_road)

    b_bare_text = "bare"
    b_bare_road = f"{basket_road},{b_bare_text}"
    america_deal.add_idea(IdeaKid(_label=b_bare_text), pad=basket_road)

    b_fine_text = "fine"
    b_fine_road = f"{basket_road},{b_fine_text}"
    america_deal.add_idea(IdeaKid(_label=b_fine_text), pad=basket_road)

    b_half_text = "half full"
    b_half_road = f"{basket_road},{b_half_text}"
    america_deal.add_idea(IdeaKid(_label=b_half_text), pad=basket_road)

    laundry_task_text = "do_laundry"
    laundry_task_road = f"{casa_road},{laundry_task_text}"
    america_deal.add_idea(
        IdeaKid(_label=laundry_task_text, promise=True), pad=casa_road
    )

    # make laundry requirement
    basket_idea = america_deal.get_idea_kid(road=basket_road)
    america_deal.edit_idea_attr(
        road=laundry_task_road, required_base=basket_road, required_sufffact=b_full_road
    )
    # make laundry requirement
    america_deal.edit_idea_attr(
        road=laundry_task_road, required_base=basket_road, required_sufffact=b_smel_road
    )
    # assign Joachim to task
    joachim_assignunit = assigned_unit_shop()
    joachim_assignunit.set_suffgroup(joachim_text)
    america_deal.edit_idea_attr(road=laundry_task_road, assignedunit=joachim_assignunit)
    america_deal.set_acptfact(base=basket_road, pick=b_full_road)

    return america_deal
