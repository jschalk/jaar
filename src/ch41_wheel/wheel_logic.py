from dataclasses import dataclass

FAMU_STATUSES = {"winning", "losing", "stable", None}


class FamuStatusError(Exception):
    pass


@dataclass
class FamilyUnit:
    famu_name: str = None
    pillars: list = None
    prestige: bool = None
    linchpin: bool = None
    famu_status: str = None

    def set_famu_status(self, famu_status: str) -> None:
        if famu_status not in FAMU_STATUSES:
            error_str = f"FamilyUnit '{self.famu_name}': '{famu_status}' is not acceptable famu_status."
            raise FamuStatusError(error_str)
        self.famu_status = famu_status


def familyunit_shop(famu_name: str, famu_status: str = None) -> FamilyUnit:
    x_familyunit = FamilyUnit(
        famu_name=famu_name, pillars=[], prestige=False, linchpin=False
    )
    x_familyunit.set_famu_status(famu_status)
    return x_familyunit


@dataclass
class PillarUnit:
    pillar_name: str = None
    bearers: set[FamilyUnit] = None


def pillarunit_shop(pillar_name: str) -> PillarUnit:
    return PillarUnit(pillar_name=pillar_name, bearers={})


@dataclass
class WheelUnit:
    wheel_name: str = None
    familys: dict[FamilyUnit] = None


def wheelunit_shop(wheel_name: str) -> WheelUnit:
    return WheelUnit(wheel_name)
