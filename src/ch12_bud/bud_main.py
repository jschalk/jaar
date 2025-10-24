from dataclasses import dataclass
from src.ch01_py.dict_toolbox import (
    create_csv,
    del_in_nested_dict,
    exists_in_nested_dict,
    get_0_if_None,
    get_empty_dict_if_None,
    get_empty_set_if_None,
    get_from_nested_dict,
    set_in_nested_dict,
)
from src.ch02_allot.allot import default_pool_num
from src.ch12_bud._ref.ch12_semantic_types import (
    BeliefName,
    EpochTime,
    FundNum,
    MomentLabel,
    VoiceName,
)


class calc_magnitudeException(Exception):
    pass


class tran_time_Exception(Exception):
    pass


DEFAULT_CELLDEPTH = 2


@dataclass
class TranUnit:
    src: BeliefName = None
    dst: VoiceName = None
    tran_time: EpochTime = None
    amount: FundNum = None


def tranunit_shop(
    src: BeliefName, dst: VoiceName, tran_time: EpochTime, amount: FundNum
) -> TranUnit:
    return TranUnit(src=src, dst=dst, tran_time=tran_time, amount=amount)


@dataclass
class TranBook:
    moment_label: MomentLabel = None
    tranunits: dict[BeliefName, dict[VoiceName, dict[EpochTime, FundNum]]] = None
    _voices_net: dict[BeliefName, dict[VoiceName, FundNum]] = None

    def set_tranunit(
        self,
        tranunit: TranUnit,
        blocked_tran_times: set[EpochTime] = None,
        offi_time_max: EpochTime = None,
    ):
        self.add_tranunit(
            belief_name=tranunit.src,
            voice_name=tranunit.dst,
            tran_time=tranunit.tran_time,
            amount=tranunit.amount,
            blocked_tran_times=blocked_tran_times,
            offi_time_max=offi_time_max,
        )

    def add_tranunit(
        self,
        belief_name: BeliefName,
        voice_name: VoiceName,
        tran_time: EpochTime,
        amount: FundNum,
        blocked_tran_times: set[EpochTime] = None,
        offi_time_max: EpochTime = None,
    ):
        if tran_time in get_empty_set_if_None(blocked_tran_times):
            exception_str = (
                f"Cannot set tranunit for tran_time={tran_time}, EpochTime is blocked"
            )
            raise tran_time_Exception(exception_str)
        if offi_time_max != None and tran_time >= offi_time_max:
            exception_str = f"Cannot set tranunit for tran_time={tran_time}, EpochTime is greater than current time={offi_time_max}"
            raise tran_time_Exception(exception_str)
        x_keylist = [belief_name, voice_name, tran_time]
        set_in_nested_dict(self.tranunits, x_keylist, amount)

    def tranunit_exists(
        self, src: BeliefName, dst: VoiceName, tran_time: EpochTime
    ) -> bool:
        return get_from_nested_dict(self.tranunits, [src, dst, tran_time], True) != None

    def get_tranunit(
        self, src: BeliefName, dst: VoiceName, tran_time: EpochTime
    ) -> TranUnit:
        x_amount = get_from_nested_dict(self.tranunits, [src, dst, tran_time], True)
        if x_amount != None:
            return tranunit_shop(src, dst, tran_time, x_amount)

    def get_amount(
        self, src: BeliefName, dst: VoiceName, tran_time: EpochTime
    ) -> TranUnit:
        return get_from_nested_dict(self.tranunits, [src, dst, tran_time], True)

    def del_tranunit(
        self, src: BeliefName, dst: VoiceName, tran_time: EpochTime
    ) -> TranUnit:
        x_keylist = [src, dst, tran_time]
        if exists_in_nested_dict(self.tranunits, x_keylist):
            del_in_nested_dict(self.tranunits, x_keylist)

    def get_tran_times(self) -> set[EpochTime]:
        x_set = set()
        for dst_dict in self.tranunits.values():
            for tran_time_dict in dst_dict.values():
                x_set.update(set(tran_time_dict.keys()))
        return x_set

    def get_beliefs_voices_net(
        self,
    ) -> dict[BeliefName, dict[VoiceName, FundNum]]:
        beliefs_voices_net_dict = {}
        for belief_name, belief_dict in self.tranunits.items():
            for voice_name, voice_dict in belief_dict.items():
                if beliefs_voices_net_dict.get(belief_name) is None:
                    beliefs_voices_net_dict[belief_name] = {}
                belief_net_dict = beliefs_voices_net_dict.get(belief_name)
                belief_net_dict[voice_name] = sum(voice_dict.values())
        return beliefs_voices_net_dict

    def get_voices_net_dict(self) -> dict[VoiceName, FundNum]:
        voices_net_dict = {}
        for belief_dict in self.tranunits.values():
            for voice_name, voice_dict in sorted(belief_dict.items()):
                if voices_net_dict.get(voice_name) is None:
                    voices_net_dict[voice_name] = sum(voice_dict.values())
                else:
                    voices_net_dict[voice_name] += sum(voice_dict.values())
        return voices_net_dict

    def _get_voices_headers(self) -> list:
        return ["voice_name", "net_amount"]

    def _get_voices_net_array(self) -> list[list]:
        x_plans = self.get_voices_net_dict().items()
        return [[voice_name, net_amount] for voice_name, net_amount in x_plans]

    def get_voices_net_csv(self) -> str:
        return create_csv(self._get_voices_headers(), self._get_voices_net_array())

    def join(self, x_tranbook):
        sorted_tranunits = sorted(
            x_tranbook.tranunits.items(),
            key=lambda x: next(iter(next(iter(x[1].values())).keys())),
        )
        for src_voice_name, dst_dict in sorted_tranunits:
            for dst_voice_name, tran_time_dict in dst_dict.items():
                for x_tran_time, x_amount in tran_time_dict.items():
                    self.add_tranunit(
                        src_voice_name, dst_voice_name, x_tran_time, x_amount
                    )

    def to_dict(
        self,
    ) -> dict[MomentLabel, dict[BeliefName, dict[VoiceName, dict[EpochTime, FundNum]]]]:
        """Returns dict that is serializable to JSON."""

        return {"moment_label": self.moment_label, "tranunits": self.tranunits}


def tranbook_shop(
    x_moment_label: MomentLabel,
    x_tranunits: dict[BeliefName, dict[VoiceName, dict[EpochTime, FundNum]]] = None,
):
    return TranBook(
        moment_label=x_moment_label,
        tranunits=get_empty_dict_if_None(x_tranunits),
        _voices_net={},
    )


def get_tranbook_from_dict(x_dict: dict) -> TranBook:
    x_tranunits = x_dict.get("tranunits")
    new_tranunits = {}
    for x_belief_name, x_voice_dict in x_tranunits.items():
        for x_voice_name, x_tran_time_dict in x_voice_dict.items():
            for x_tran_time, x_amount in x_tran_time_dict.items():
                x_key_list = [x_belief_name, x_voice_name, int(x_tran_time)]
                set_in_nested_dict(new_tranunits, x_key_list, x_amount)
    return tranbook_shop(x_dict.get("moment_label"), new_tranunits)


@dataclass
class BudUnit:
    bud_time: EpochTime = None
    quota: FundNum = None
    celldepth: int = None  # non-negative
    _magnitude: FundNum = None  # how much of the actual quota is distributed
    _bud_voice_nets: dict[VoiceName, FundNum] = None  # ledger of bud outcome

    def set_bud_voice_net(self, x_voice_name: VoiceName, bud_voice_net: FundNum):
        self._bud_voice_nets[x_voice_name] = bud_voice_net

    def bud_voice_net_exists(self, x_voice_name: VoiceName) -> bool:
        return self._bud_voice_nets.get(x_voice_name) != None

    def get_bud_voice_net(self, x_voice_name: VoiceName) -> FundNum:
        return self._bud_voice_nets.get(x_voice_name)

    def del_bud_voice_net(self, x_voice_name: VoiceName):
        self._bud_voice_nets.pop(x_voice_name)

    def calc_magnitude(self):
        bud_voice_nets = self._bud_voice_nets.values()
        x_cred_sum = sum(da_net for da_net in bud_voice_nets if da_net > 0)
        x_debt_sum = sum(da_net for da_net in bud_voice_nets if da_net < 0)
        if x_cred_sum + x_debt_sum != 0:
            exception_str = f"magnitude cannot be calculated: debt_bud_voice_net={x_debt_sum}, cred_bud_voice_net={x_cred_sum}"
            raise calc_magnitudeException(exception_str)
        self._magnitude = x_cred_sum

    def to_dict(self) -> dict[str,]:
        """Returns dict that is serializable to JSON."""

        x_dict = {"bud_time": self.bud_time, "quota": self.quota}
        if self._bud_voice_nets:
            x_dict["bud_voice_nets"] = self._bud_voice_nets
        if self._magnitude:
            x_dict["magnitude"] = self._magnitude
        if self.celldepth != DEFAULT_CELLDEPTH:
            x_dict["celldepth"] = self.celldepth
        return x_dict


def budunit_shop(
    bud_time: EpochTime,
    quota: FundNum = None,
    bud_voice_nets: dict[VoiceName, FundNum] = None,
    magnitude: FundNum = None,
    celldepth: int = None,
) -> BudUnit:
    if quota is None:
        quota = default_pool_num()
    if celldepth is None:
        celldepth = DEFAULT_CELLDEPTH

    return BudUnit(
        bud_time=bud_time,
        quota=quota,
        celldepth=celldepth,
        _bud_voice_nets=get_empty_dict_if_None(bud_voice_nets),
        _magnitude=get_0_if_None(magnitude),
    )


@dataclass
class BeliefBudHistory:
    belief_name: BeliefName = None
    buds: dict[EpochTime, BudUnit] = None
    # calculated fields
    _sum_budunit_quota: FundNum = None
    _sum_voice_bud_nets: int = None
    _bud_time_min: EpochTime = None
    _bud_time_max: EpochTime = None

    def set_bud(self, x_bud: BudUnit):
        self.buds[x_bud.bud_time] = x_bud

    def add_bud(self, x_bud_time: EpochTime, x_quota: FundNum, celldepth: int = None):
        budunit = budunit_shop(bud_time=x_bud_time, quota=x_quota, celldepth=celldepth)
        self.set_bud(budunit)

    def bud_exists(self, x_bud_time: EpochTime) -> bool:
        return self.buds.get(x_bud_time) != None

    def get_bud(self, x_bud_time: EpochTime) -> BudUnit:
        return self.buds.get(x_bud_time)

    def del_bud(self, x_bud_time: EpochTime):
        self.buds.pop(x_bud_time)

    def get_2d_array(self) -> list[list]:
        return [
            [self.belief_name, x_bud.bud_time, x_bud.quota]
            for x_bud in self.buds.values()
        ]

    def get_headers(self) -> list:
        return ["belief_name", "bud_time", "quota"]

    def to_dict(self) -> dict:
        """Returns dict that is serializable to JSON."""

        return {"belief_name": self.belief_name, "buds": self._get_buds_dict()}

    def _get_buds_dict(self) -> dict:
        return {x_bud.bud_time: x_bud.to_dict() for x_bud in self.buds.values()}

    def get_bud_times(self) -> set[EpochTime]:
        return set(self.buds.keys())

    def get_tranbook(self, moment_label: MomentLabel) -> TranBook:
        x_tranbook = tranbook_shop(moment_label)
        for x_bud_time, x_bud in self.buds.items():
            for dst_voice_name, x_quota in x_bud._bud_voice_nets.items():
                x_tranbook.add_tranunit(
                    belief_name=self.belief_name,
                    voice_name=dst_voice_name,
                    tran_time=x_bud_time,
                    amount=x_quota,
                )
        return x_tranbook


def beliefbudhistory_shop(belief_name: BeliefName) -> BeliefBudHistory:
    return BeliefBudHistory(belief_name=belief_name, buds={}, _sum_voice_bud_nets={})


def get_budunit_from_dict(x_dict: dict) -> BudUnit:
    x_bud_time = x_dict.get("bud_time")
    x_quota = x_dict.get("quota")
    x_bud_net = x_dict.get("bud_voice_nets")
    x_magnitude = x_dict.get("magnitude")
    x_celldepth = x_dict.get("celldepth")
    return budunit_shop(
        x_bud_time, x_quota, x_bud_net, x_magnitude, celldepth=x_celldepth
    )


def get_beliefbudhistory_from_dict(x_dict: dict) -> BeliefBudHistory:
    x_belief_name = x_dict.get("belief_name")
    x_beliefbudhistory = beliefbudhistory_shop(x_belief_name)
    x_beliefbudhistory.buds = get_buds_from_dict(x_dict.get("buds"))
    return x_beliefbudhistory


def get_buds_from_dict(buds_dict: dict) -> dict[EpochTime, BudUnit]:
    x_dict = {}
    for x_bud_dict in buds_dict.values():
        x_budunit = get_budunit_from_dict(x_bud_dict)
        x_dict[x_budunit.bud_time] = x_budunit
    return x_dict
