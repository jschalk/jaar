from src.a00_data_toolbox.file_toolbox import (
    create_directory_path,
    create_path,
    get_json_filename,
)
from src.a01_term_logic.rope import get_all_rope_labels, rebuild_rope
from src.a01_term_logic.term import BeliefName, CoinLabel, LabelTerm

COIN_FILENAME = "coin.json"
BUDUNIT_FILENAME = "budunit.json"
CELLNODE_FILENAME = "cell.json"
CELL_MANDATE_FILENAME = "cell_partner_mandate_ledger.json"
BELIEFPOINT_FILENAME = "beliefpoint.json"
BELIEFEVENT_FILENAME = "belief.json"
EVENT_ALL_PACK_FILENAME = "all_pack.json"
EVENT_EXPRESSED_PACK_FILENAME = "expressed_pack.json"


def treasury_filename() -> str:
    return "treasury.db"


def create_coin_dir_path(coin_mstr_dir: str, coin_label: LabelTerm) -> str:
    """Returns path: coin_mstr_dir\\coins\\coin_label"""
    coins_dir = create_path(coin_mstr_dir, "coins")
    return create_path(coins_dir, coin_label)


def create_coin_json_path(coin_mstr_dir: str, coin_label: LabelTerm) -> str:
    """Returns path: coin_mstr_dir\\coins\\coin_label\\coin.json"""
    coins_dir = create_path(coin_mstr_dir, "coins")
    coin_path = create_path(coins_dir, coin_label)
    return create_path(coin_path, "coin.json")


def create_coin_beliefs_dir_path(coin_mstr_dir: str, coin_label: LabelTerm) -> str:
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs"""
    coins_dir = create_path(coin_mstr_dir, "coins")
    coin_dir = create_path(coins_dir, coin_label)
    return create_path(coin_dir, "beliefs")


def create_belief_dir_path(
    coin_mstr_dir: str, coin_label: LabelTerm, belief_name: BeliefName
) -> str:
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name"""

    coins_dir = create_path(coin_mstr_dir, "coins")
    coin_dir = create_path(coins_dir, coin_label)
    beliefs_dir = create_path(coin_dir, "beliefs")
    return create_path(beliefs_dir, belief_name)


def create_keeps_dir_path(
    coin_mstr_dir: str, coin_label: LabelTerm, belief_name: BeliefName
) -> str:
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\keeps"""
    coins_dir = create_path(coin_mstr_dir, "coins")
    coin_dir = create_path(coins_dir, coin_label)
    beliefs_dir = create_path(coin_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_name)
    return create_path(belief_dir, "keeps")


class _keep_ropeMissingException(Exception):
    pass


def create_keep_rope_path(
    coin_mstr_dir: str,
    belief_name: BeliefName,
    coin_label: CoinLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> str:
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\keeps\\planroot\\level1_label"""
    if keep_rope is None:
        raise _keep_ropeMissingException(
            f"'{belief_name}' cannot save to keep_path because it does not have keep_rope."
        )

    keep_root = "planroot"
    keep_rope = rebuild_rope(keep_rope, coin_label, keep_root)
    x_list = get_all_rope_labels(keep_rope, knot)
    keep_sub_path = create_directory_path(x_list=[*x_list])
    keeps_dir = create_keeps_dir_path(coin_mstr_dir, coin_label, belief_name)
    return create_path(keeps_dir, keep_sub_path)


def create_keep_dutys_path(
    coin_mstr_dir: str,
    belief_name: BeliefName,
    coin_label: CoinLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> str:
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\keeps\\level1\\dutys"""
    x_keep_path = create_keep_rope_path(
        coin_mstr_dir, belief_name, coin_label, keep_rope, knot
    )
    return create_path(x_keep_path, "dutys")


def create_keep_duty_path(
    coin_mstr_dir: str,
    belief_name: BeliefName,
    coin_label: CoinLabel,
    keep_rope: LabelTerm,
    knot: str,
    duty_belief: BeliefName,
) -> str:
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\keeps\\level1\\dutys\\duty_belief.json"""
    x_dutys_path = create_keep_dutys_path(
        coin_mstr_dir, belief_name, coin_label, keep_rope, knot
    )
    return create_path(x_dutys_path, get_json_filename(duty_belief))


def create_keep_visions_path(
    coin_mstr_dir: str,
    belief_name: BeliefName,
    coin_label: CoinLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> str:
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\keeps\\level1\\visions"""
    x_keep_path = create_keep_rope_path(
        coin_mstr_dir, belief_name, coin_label, keep_rope, knot
    )
    return create_path(x_keep_path, "visions")


def create_keep_grades_path(
    coin_mstr_dir: str,
    belief_name: BeliefName,
    coin_label: CoinLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> str:
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\keeps\\level1\\grades"""
    x_keep_path = create_keep_rope_path(
        coin_mstr_dir, belief_name, coin_label, keep_rope, knot
    )
    return create_path(x_keep_path, "grades")


def create_treasury_db_path(
    coin_mstr_dir: str,
    belief_name: BeliefName,
    coin_label: CoinLabel,
    keep_rope: LabelTerm,
    knot: str,
) -> str:
    "Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\keeps\\level1\\treasury.db"
    keep_path = create_keep_rope_path(
        coin_mstr_dir=coin_mstr_dir,
        belief_name=belief_name,
        coin_label=coin_label,
        keep_rope=keep_rope,
        knot=knot,
    )
    return create_path(keep_path, treasury_filename())


def create_atoms_dir_path(
    coin_mstr_dir: str, coin_label: LabelTerm, belief_name: BeliefName
) -> str:
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\atoms"""
    coins_dir = create_path(coin_mstr_dir, "coins")
    coin_dir = create_path(coins_dir, coin_label)
    beliefs_dir = create_path(coin_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_name)
    return create_path(belief_dir, "atoms")


def create_packs_dir_path(
    coin_mstr_dir: str, coin_label: LabelTerm, belief_name: BeliefName
) -> str:
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\packs"""
    coins_dir = create_path(coin_mstr_dir, "coins")
    coin_dir = create_path(coins_dir, coin_label)
    beliefs_dir = create_path(coin_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_name)
    return create_path(belief_dir, "packs")


def create_buds_dir_path(
    coin_mstr_dir: str, coin_label: LabelTerm, belief_name: BeliefName
) -> str:
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\buds"""
    coins_dir = create_path(coin_mstr_dir, "coins")
    coin_dir = create_path(coins_dir, coin_label)
    beliefs_dir = create_path(coin_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_name)
    return create_path(belief_dir, "buds")


def create_bud_dir_path(
    coin_mstr_dir: str,
    coin_label: LabelTerm,
    belief_name: BeliefName,
    bud_time: int,
):
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\buds\n\\bud_time"""
    timeline_dir = create_buds_dir_path(coin_mstr_dir, coin_label, belief_name)
    return create_path(timeline_dir, bud_time)


def create_budunit_json_path(
    coin_mstr_dir: str,
    coin_label: LabelTerm,
    belief_name: BeliefName,
    bud_time: int,
) -> str:
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\buds\n\\bud_time\\budunit.json"""
    timepoint_dir = create_bud_dir_path(
        coin_mstr_dir, coin_label, belief_name, bud_time
    )
    return create_path(timepoint_dir, "budunit.json")


def create_beliefpoint_path(
    coin_mstr_dir: str,
    coin_label: LabelTerm,
    belief_name: BeliefName,
    bud_time: int,
) -> str:
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\buds\n\\bud_time\\beliefpoint.json"""
    timepoint_dir = create_bud_dir_path(
        coin_mstr_dir, coin_label, belief_name, bud_time
    )
    return create_path(timepoint_dir, "beliefpoint.json")


def create_cell_dir_path(
    coin_mstr_dir: str,
    coin_label: LabelTerm,
    belief_name: BeliefName,
    bud_time: int,
    bud_ancestors: list[BeliefName],
):
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\buds\n\\bud_time\\ledger_belief1\\ledger_belief2\\ledger_belief3"""
    bud_celldepth_dir = create_bud_dir_path(
        coin_mstr_dir, coin_label, belief_name, bud_time
    )
    if bud_ancestors is None:
        bud_ancestors = []
    for ledger_belief in bud_ancestors:
        bud_celldepth_dir = create_path(bud_celldepth_dir, ledger_belief)
    return bud_celldepth_dir


def create_cell_json_path(
    coin_mstr_dir: str,
    coin_label: LabelTerm,
    belief_name: BeliefName,
    bud_time: int,
    bud_ancestors: list[BeliefName] = None,
):
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\buds\n\\bud_time\\ledger_belief1\\ledger_belief2\\ledger_belief3\\cell.json"""
    cell_dir = create_cell_dir_path(
        coin_mstr_dir, coin_label, belief_name, bud_time, bud_ancestors
    )
    return create_path(cell_dir, "cell.json")


def create_cell_partner_mandate_ledger_path(
    coin_mstr_dir: str,
    coin_label: LabelTerm,
    belief_name: BeliefName,
    bud_time: int,
    bud_ancestors: list[BeliefName] = None,
):
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\buds\n\\bud_time\\ledger_belief1\\ledger_belief2\\ledger_belief3\\cell_partner_mandate_ledger.json"""
    cell_dir = create_cell_dir_path(
        coin_mstr_dir, coin_label, belief_name, bud_time, bud_ancestors
    )
    return create_path(cell_dir, "cell_partner_mandate_ledger.json")


def create_belief_event_dir_path(
    coin_mstr_dir: str,
    coin_label: LabelTerm,
    belief_name: BeliefName,
    event_int: int,
):
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\events\\event_int"""
    coins_dir = create_path(coin_mstr_dir, "coins")
    coin_dir = create_path(coins_dir, coin_label)
    beliefs_dir = create_path(coin_dir, "beliefs")
    coin_belief_dir = create_path(beliefs_dir, belief_name)
    coin_events_dir = create_path(coin_belief_dir, "events")
    return create_path(coin_events_dir, event_int)


def create_beliefevent_path(
    coin_mstr_dir: str,
    coin_label: LabelTerm,
    belief_name: BeliefName,
    event_int: int,
):
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\events\\event_int\\belief.json"""
    belief_event_dir_path = create_belief_event_dir_path(
        coin_mstr_dir, coin_label, belief_name, event_int
    )
    belief_filename = "belief.json"
    return create_path(belief_event_dir_path, belief_filename)


def create_event_all_pack_path(
    coin_mstr_dir: str,
    coin_label: LabelTerm,
    belief_name: BeliefName,
    event_int: int,
):
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\events\\event_int\\all_pack.json"""
    belief_event_dir_path = create_belief_event_dir_path(
        coin_mstr_dir, coin_label, belief_name, event_int
    )
    all_pack_filename = "all_pack.json"
    return create_path(belief_event_dir_path, all_pack_filename)


def create_event_expressed_pack_path(
    coin_mstr_dir: str,
    coin_label: LabelTerm,
    belief_name: BeliefName,
    event_int: int,
):
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\events\\event_int\\expressed_pack.json"""
    belief_event_dir_path = create_belief_event_dir_path(
        coin_mstr_dir, coin_label, belief_name, event_int
    )
    expressed_pack_filename = "expressed_pack.json"
    return create_path(belief_event_dir_path, expressed_pack_filename)


def create_gut_path(coin_mstr_dir: str, coin_label: LabelTerm, belief_name: BeliefName):
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\gut\\belief_name.json"""
    coins_dir = create_path(coin_mstr_dir, "coins")
    coin_dir = create_path(coins_dir, coin_label)
    beliefs_dir = create_path(coin_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_name)
    gut_dir = create_path(belief_dir, "gut")
    return create_path(gut_dir, f"{belief_name}.json")


def create_job_path(coin_mstr_dir: str, coin_label: LabelTerm, belief_name: BeliefName):
    """Returns path: coin_mstr_dir\\coins\\coin_label\\beliefs\\belief_name\\job\\belief_name.json"""
    coins_dir = create_path(coin_mstr_dir, "coins")
    coin_dir = create_path(coins_dir, coin_label)
    beliefs_dir = create_path(coin_dir, "beliefs")
    belief_dir = create_path(beliefs_dir, belief_name)
    job_dir = create_path(belief_dir, "job")
    return create_path(job_dir, f"{belief_name}.json")
