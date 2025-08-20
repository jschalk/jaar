from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import (
    get_0_if_None,
    get_dict_from_json,
    get_empty_set_if_None,
    get_json_from_dict,
)
from src.a00_data_toolbox.file_toolbox import (
    create_path,
    get_dir_file_strs,
    open_file,
    set_dir,
)
from src.a01_term_logic.term import (
    BeliefName,
    CoinLabel,
    EventInt,
    PartnerName,
    default_knot_if_None,
)
from src.a02_finance_logic.finance_config import (
    BitNum,
    FundIota,
    FundNum,
    PennyNum,
    default_fund_iota_if_None,
    default_RespectBit_if_None,
    filter_penny,
)
from src.a06_belief_logic.belief_main import BeliefUnit, beliefunit_shop
from src.a07_timeline_logic.timeline_main import (
    TimeLinePoint,
    TimeLineUnit,
    add_newtimeline_planunit,
    timelineunit_shop,
)
from src.a11_bud_logic.bud import (
    BrokerUnit,
    BudUnit,
    TranBook,
    TranUnit,
    brokerunit_shop,
    get_brokerunit_from_dict,
    get_tranbook_from_dict,
    tranbook_shop,
)
from src.a11_bud_logic.cell import cellunit_shop
from src.a12_hub_toolbox.a12_path import create_cell_dir_path, create_coin_json_path
from src.a12_hub_toolbox.hub_tool import (
    cellunit_save_to_dir,
    gut_file_exists,
    open_gut_file,
    open_job_file,
    save_gut_file,
    save_job_file,
)
from src.a12_hub_toolbox.keep_tool import create_treasury_db_file, save_duty_belief
from src.a13_belief_listen_logic.basis_beliefs import create_listen_basis
from src.a13_belief_listen_logic.listen_main import (
    listen_to_agendas_create_init_job_from_guts,
    listen_to_debtors_roll_jobs_into_job,
)


def get_default_job_listen_count() -> int:
    return 3


class budunit_Exception(Exception):
    pass


class set_paypurchase_Exception(Exception):
    pass


class set_offi_time_max_Exception(Exception):
    pass


@dataclass
class CoinUnit:
    """Data pipelines:
    pipeline1: packs->gut
    pipeline2: gut->dutys
    pipeline3: duty->vision
    pipeline4: vision->job
    pipeline5: gut->job (direct)
    pipeline6: gut->vision->job (through visions)
    pipeline7: packs->job (could be 5 of 6)
    """

    coin_label: CoinLabel = None
    coin_mstr_dir: str = None
    timeline: TimeLineUnit = None
    brokerunits: dict[BeliefName, BrokerUnit] = None
    paybook: TranBook = None
    offi_times: set[TimeLinePoint] = None
    knot: str = None
    fund_iota: FundIota = None
    respect_bit: BitNum = None
    penny: PennyNum = None
    job_listen_rotations: int = None
    _offi_time_max: TimeLinePoint = None
    _coin_dir: str = None
    _beliefs_dir: str = None
    _packs_dir: str = None
    _all_tranbook: TranBook = None

    # directory setup
    def _set_coin_dirs(self):
        coins_dir = create_path(self.coin_mstr_dir, "coins")
        self._coin_dir = create_path(coins_dir, self.coin_label)
        self._beliefs_dir = create_path(self._coin_dir, "beliefs")
        self._packs_dir = create_path(self._coin_dir, "packs")
        set_dir(x_path=self._coin_dir)
        set_dir(x_path=self._beliefs_dir)
        set_dir(x_path=self._packs_dir)

    def _get_belief_dir(self, belief_name) -> str:
        return create_path(self._beliefs_dir, belief_name)

    def _get_belief_folder_names(self) -> set:
        beliefs = get_dir_file_strs(
            self._beliefs_dir, include_dirs=True, include_files=False
        )
        return sorted(list(beliefs.keys()))

    # belief management
    def _set_all_healer_dutys(self, belief_name: BeliefName):
        x_gut = open_gut_file(self.coin_mstr_dir, self.coin_label, belief_name)
        x_gut.cash_out()
        for healer_name, healer_dict in x_gut._healers_dict.items():
            for keep_rope in healer_dict.keys():
                create_treasury_db_file(
                    self.coin_mstr_dir,
                    belief_name=belief_name,
                    coin_label=self.coin_label,
                    keep_rope=keep_rope,
                    knot=self.knot,
                )
                save_duty_belief(
                    coin_mstr_dir=self.coin_mstr_dir,
                    belief_name=healer_name,
                    coin_label=self.coin_label,
                    keep_rope=keep_rope,
                    knot=None,
                    duty_belief=x_gut,
                )

    # job belief management
    def create_empty_belief_from_coin(self, belief_name: BeliefName) -> BeliefUnit:
        return beliefunit_shop(
            belief_name,
            self.coin_label,
            knot=self.knot,
            fund_iota=self.fund_iota,
            respect_bit=self.respect_bit,
            penny=self.penny,
        )

    def create_gut_file_if_none(self, belief_name: BeliefName) -> None:
        if not gut_file_exists(self.coin_mstr_dir, self.coin_label, belief_name):
            empty_belief = self.create_empty_belief_from_coin(belief_name)
            save_gut_file(self.coin_mstr_dir, empty_belief)

    def create_init_job_from_guts(self, belief_name: BeliefName) -> None:
        self.create_gut_file_if_none(belief_name)
        x_gut = open_gut_file(self.coin_mstr_dir, self.coin_label, belief_name)
        x_job = create_listen_basis(x_gut)
        listen_to_agendas_create_init_job_from_guts(self.coin_mstr_dir, x_job)
        save_job_file(self.coin_mstr_dir, x_job)

    def rotate_job(self, belief_name: BeliefName) -> BeliefUnit:
        x_job = open_job_file(self.coin_mstr_dir, self.coin_label, belief_name)
        x_job.cash_out()
        # # if beliefunit has healers create job from healers.
        # create beliefunit from debtors roll
        return listen_to_debtors_roll_jobs_into_job(
            self.coin_mstr_dir, self.coin_label, belief_name
        )

    def generate_all_jobs(self) -> None:
        belief_names = self._get_belief_folder_names()
        for belief_name in belief_names:
            self.create_init_job_from_guts(belief_name)

        for _ in range(self.job_listen_rotations):
            for belief_name in belief_names:
                save_job_file(self.coin_mstr_dir, self.rotate_job(belief_name))

    def get_job_file_belief(self, belief_name: BeliefName) -> BeliefUnit:
        return open_job_file(self.coin_mstr_dir, self.coin_label, belief_name)

    # brokerunits
    def set_brokerunit(self, x_brokerunit: BrokerUnit) -> None:
        self.brokerunits[x_brokerunit.belief_name] = x_brokerunit

    def brokerunit_exists(self, x_belief_name: BeliefName) -> bool:
        return self.brokerunits.get(x_belief_name) != None

    def get_brokerunit(self, x_belief_name: BeliefName) -> BrokerUnit:
        return self.brokerunits.get(x_belief_name)

    def del_brokerunit(self, x_belief_name: BeliefName) -> None:
        self.brokerunits.pop(x_belief_name)

    def add_budunit(
        self,
        belief_name: BeliefName,
        bud_time: TimeLinePoint,
        quota: int,
        allow_prev_to_offi_time_max_entry: bool = False,
        celldepth: int = None,
    ):
        self._offi_time_max = get_0_if_None(self._offi_time_max)
        if bud_time < self._offi_time_max and not allow_prev_to_offi_time_max_entry:
            exception_str = f"Cannot set budunit because bud_time {bud_time} is less than CoinUnit._offi_time_max {self._offi_time_max}."
            raise budunit_Exception(exception_str)
        if self.brokerunit_exists(belief_name) is False:
            self.set_brokerunit(brokerunit_shop(belief_name))
        x_brokerunit = self.get_brokerunit(belief_name)
        x_brokerunit.add_bud(bud_time, quota, celldepth)

    def get_budunit(self, belief_name: BeliefName, bud_time: TimeLinePoint) -> BudUnit:
        if not self.get_brokerunit(belief_name):
            return None
        x_brokerunit = self.get_brokerunit(belief_name)
        return x_brokerunit.get_bud(bud_time)

    def to_dict(self, include_paybook: bool = True) -> dict:
        x_dict = {
            "coin_label": self.coin_label,
            "coin_mstr_dir": self.coin_mstr_dir,
            "knot": self.knot,
            "fund_iota": self.fund_iota,
            "penny": self.penny,
            "brokerunits": self._get_brokerunits_dict(),
            "respect_bit": self.respect_bit,
            "timeline": self.timeline.to_dict(),
            "offi_times": list(self.offi_times),
        }
        if include_paybook:
            x_dict["paybook"] = self.paybook.to_dict()
        return x_dict

    def get_json(self) -> str:
        return get_json_from_dict(self.to_dict())

    def _get_brokerunits_dict(self) -> dict[BeliefName, dict]:
        return {
            x_bud.belief_name: x_bud.to_dict() for x_bud in self.brokerunits.values()
        }

    def get_brokerunits_bud_times(self) -> set[TimeLinePoint]:
        all_budunit_bud_times = set()
        for x_brokerunit in self.brokerunits.values():
            all_budunit_bud_times.update(x_brokerunit.get_bud_times())
        return all_budunit_bud_times

    def set_paypurchase(self, x_paypurchase: TranUnit):
        self.paybook.set_tranunit(
            tranunit=x_paypurchase,
            blocked_tran_times=self.get_brokerunits_bud_times(),
            _offi_time_max=self._offi_time_max,
        )

    def add_paypurchase(
        self,
        belief_name: BeliefName,
        partner_name: PartnerName,
        tran_time: TimeLinePoint,
        amount: FundNum,
        blocked_tran_times: set[TimeLinePoint] = None,
        _offi_time_max: TimeLinePoint = None,
    ) -> None:
        self.paybook.add_tranunit(
            belief_name=belief_name,
            partner_name=partner_name,
            tran_time=tran_time,
            amount=amount,
            blocked_tran_times=blocked_tran_times,
            _offi_time_max=_offi_time_max,
        )

    def paypurchase_exists(
        self, src: BeliefName, dst: PartnerName, x_tran_time: TimeLinePoint
    ) -> bool:
        return self.paybook.tranunit_exists(src, dst, x_tran_time)

    def get_paypurchase(
        self, src: BeliefName, dst: PartnerName, x_tran_time: TimeLinePoint
    ) -> TranUnit:
        return self.paybook.get_tranunit(src, dst, x_tran_time)

    def del_paypurchase(
        self, src: BeliefName, dst: PartnerName, x_tran_time: TimeLinePoint
    ) -> TranUnit:
        return self.paybook.del_tranunit(src, dst, x_tran_time)

    # def set_offi_time(self, offi_time: TimeLinePoint):
    #     self.offi_time = offi_time
    #     if self._offi_time_max < self.offi_time:
    #         self._offi_time_max = self.offi_time

    def set_offi_time_max(self, x_offi_time_max: TimeLinePoint):
        x_tran_times = self.paybook.get_tran_times()
        if x_tran_times != set() and max(x_tran_times) >= x_offi_time_max:
            exception_str = f"Cannot set _offi_time_max {x_offi_time_max}, paypurchase with greater tran_time exists"
            raise set_offi_time_max_Exception(exception_str)
        # if self.offi_time > x_offi_time_max:
        #     exception_str = f"Cannot set _offi_time_max={x_offi_time_max} because it is less than offi_time={self.offi_time}"
        #     raise set_offi_time_max_Exception(exception_str)
        self._offi_time_max = x_offi_time_max

    # def set_offi_time(
    #     self, offi_time: TimeLinePoint, _offi_time_max: TimeLinePoint
    # ):
    #     self.set_offi_time(offi_time)
    #     self.set_offi_time_max(_offi_time_max)

    def set_all_tranbook(self) -> None:
        x_tranunits = copy_deepcopy(self.paybook.tranunits)
        x_tranbook = tranbook_shop(self.coin_label, x_tranunits)
        for belief_name, x_brokerunit in self.brokerunits.items():
            for x_bud_time, x_budunit in x_brokerunit.buds.items():
                for partner_name, x_amount in x_budunit._bud_partner_nets.items():
                    x_tranbook.add_tranunit(
                        belief_name, partner_name, x_bud_time, x_amount
                    )
        self._all_tranbook = x_tranbook

    def create_buds_root_cells(
        self,
        ote1_dict: dict[BeliefName, dict[TimeLinePoint, EventInt]],
    ) -> None:
        for belief_name, brokerunit in self.brokerunits.items():
            for bud_time in brokerunit.buds.keys():
                self._create_bud_root_cell(belief_name, ote1_dict, bud_time)

    def _create_bud_root_cell(
        self,
        belief_name: BeliefName,
        ote1_dict: dict[BeliefName, dict[TimeLinePoint, EventInt]],
        bud_time: TimeLinePoint,
    ) -> None:
        past_event_int = _get_ote1_max_past_event_int(belief_name, ote1_dict, bud_time)
        budunit = self.get_budunit(belief_name, bud_time)
        cellunit = cellunit_shop(
            bud_belief_name=belief_name,
            ancestors=[],
            event_int=past_event_int,
            celldepth=budunit.celldepth,
            quota=budunit.quota,
            penny=self.penny,
        )
        root_cell_dir = create_cell_dir_path(
            self.coin_mstr_dir, self.coin_label, belief_name, bud_time, []
        )
        cellunit_save_to_dir(root_cell_dir, cellunit)

    def get_timeline_config(self) -> dict:
        return self.timeline.to_dict()

    def add_timeline_to_gut(self, belief_name: BeliefName) -> None:
        """Adds the timeline to the gut file for the given belief."""
        x_gut = open_gut_file(self.coin_mstr_dir, self.coin_label, belief_name)
        add_newtimeline_planunit(x_gut, self.get_timeline_config())
        save_gut_file(self.coin_mstr_dir, x_gut)

    def add_timeline_to_guts(self) -> None:
        """Adds the timeline to all gut files."""
        belief_names = self._get_belief_folder_names()
        for belief_name in belief_names:
            self.add_timeline_to_gut(belief_name)


def _get_ote1_max_past_event_int(
    belief_name: str, ote1_dict: dict[str, dict[str, int]], bud_time: int
) -> EventInt:
    """Using the grab most recent ote1 event int before a given bud_time"""
    ote1_belief_dict = ote1_dict.get(belief_name)
    if not ote1_belief_dict:
        return None
    event_timepoints = set(ote1_belief_dict.keys())
    if past_timepoints := {tp for tp in event_timepoints if int(tp) <= bud_time}:
        max_past_timepoint = max(past_timepoints)
        return ote1_belief_dict.get(max_past_timepoint)


def coinunit_shop(
    coin_label: CoinLabel,
    coin_mstr_dir: str,
    timeline: TimeLineUnit = None,
    offi_times: set[TimeLinePoint] = None,
    knot: str = None,
    fund_iota: float = None,
    respect_bit: float = None,
    penny: float = None,
    job_listen_rotations: int = None,
) -> CoinUnit:
    if timeline is None:
        timeline = timelineunit_shop()
    if not job_listen_rotations:
        job_listen_rotations = get_default_job_listen_count()
    x_coinunit = CoinUnit(
        coin_label=coin_label,
        coin_mstr_dir=coin_mstr_dir,
        timeline=timeline,
        brokerunits={},
        paybook=tranbook_shop(coin_label),
        offi_times=get_empty_set_if_None(offi_times),
        knot=default_knot_if_None(knot),
        fund_iota=default_fund_iota_if_None(fund_iota),
        respect_bit=default_RespectBit_if_None(respect_bit),
        penny=filter_penny(penny),
        _all_tranbook=tranbook_shop(coin_label),
        job_listen_rotations=job_listen_rotations,
    )
    if x_coinunit.coin_mstr_dir:
        x_coinunit._set_coin_dirs()
    return x_coinunit


def _get_brokerunits_from_dict(
    brokerunits_dict: dict,
) -> dict[BeliefName, BrokerUnit]:
    return {
        x_belief_name: get_brokerunit_from_dict(brokerunit_dict)
        for x_belief_name, brokerunit_dict in brokerunits_dict.items()
    }


def get_from_dict(coin_dict: dict) -> CoinUnit:
    x_coin_label = coin_dict.get("coin_label")
    x_coin = coinunit_shop(
        coin_label=x_coin_label,
        coin_mstr_dir=coin_dict.get("coin_mstr_dir"),
        offi_times=set(coin_dict.get("offi_times")),
        knot=coin_dict.get("knot"),
        fund_iota=coin_dict.get("fund_iota"),
        respect_bit=coin_dict.get("respect_bit"),
        penny=coin_dict.get("penny"),
    )
    coin_dict_timeline_value = coin_dict.get("timeline")
    if coin_dict_timeline_value:
        x_coin.timeline = timelineunit_shop(coin_dict_timeline_value)
    else:
        x_coin.timeline = timelineunit_shop(None)
    x_coin.brokerunits = _get_brokerunits_from_dict(coin_dict.get("brokerunits"))
    x_coin.paybook = get_tranbook_from_dict(coin_dict.get("paybook"))
    return x_coin


def get_from_json(x_coin_json: str) -> CoinUnit:
    return get_from_dict(get_dict_from_json(x_coin_json))


def get_default_path_coinunit(coin_mstr_dir: str, coin_label: CoinLabel) -> CoinUnit:
    coin_json_path = create_coin_json_path(coin_mstr_dir, coin_label)
    x_coinunit = get_from_json(open_file(coin_json_path))
    x_coinunit.coin_mstr_dir = coin_mstr_dir
    x_coinunit._set_coin_dirs()
    return x_coinunit
