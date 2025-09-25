from src.ch18_etl_toolbox._ref.ch18_keywords import *
from typing import Literal


def default_kpi_bundle_str() -> str:
    return "default_kpi_bundle"


def moment_kpi001_voice_nets_str() -> Literal["moment_kpi001_voice_nets"]:
    """Table name for KPI001: The net funds per voice per moment."""
    return "moment_kpi001_voice_nets"


def moment_kpi002_belief_pledges_str() -> Literal["moment_kpi002_belief_pledges"]:
    """Table name for KPI002: List of pledges per moment ."""
    return "moment_kpi002_belief_pledges"
