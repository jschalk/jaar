from src._instrument.python import get_empty_dict_if_none
from src.bud.reason_idea import FactUnit, RoadUnit, factunit_shop
from src.bud.idea import IdeaUnit
from dataclasses import dataclass


class InvalidAxiomException(Exception):
    pass


@dataclass
class Axiom:
    src_fact: FactUnit
    calc_fact: FactUnit
    x_idea: IdeaUnit
    eval_status: bool
    eval_count: int


@dataclass
class Axioms:
    axioms: dict[RoadUnit, Axiom] = None

    def _get_loop_range_calc_fact_attr(
        self,
        idea_gogo_want: float,
        idea_stop_want: float,
        src_open: float,
        src_nigh: float,
        src_idea_gogo_want: float,
        src_idea_stop_want: float,
    ) -> RoadUnit:
        fact_open = None
        fact_nigh = None

        # if src_idea and fact_idea have equal range return equal src fact range
        if (
            idea_gogo_want == src_idea_gogo_want
            and idea_stop_want == src_idea_stop_want
        ):
            fact_open = src_open
            fact_nigh = src_nigh
        else:
            # create both ranges and get calc ranges for both. Return the not null one
            r1_open, r1_nigh = self._get_range_calc_fact_attr(
                idea_gogo_want=idea_gogo_want,
                idea_stop_want=idea_stop_want,
                src_open=src_idea_gogo_want,
                src_nigh=src_nigh,
            )
            r2_open, r2_nigh = self._get_range_calc_fact_attr(
                idea_gogo_want=idea_gogo_want,
                idea_stop_want=idea_stop_want,
                src_open=src_open,
                src_nigh=src_idea_stop_want,
            )
            # # if both are not null return r1_nigh as fact_open and r2_open as fact_nigh
            # if r1_open is not None and r1_nigh is not None and r2_open is not None and r2_nigh is not None:
            #     fact_open = r1_nigh
            #     fact_nigh = r2_open
            if r1_open is not None and r1_nigh is not None:
                fact_open = r1_open
                fact_nigh = r1_nigh
            elif r2_open is not None and r2_nigh is not None:
                fact_open = r2_open
                fact_nigh = r2_nigh

        return fact_open, fact_nigh

    def _get_range_calc_fact_attr(
        self,
        idea_gogo_want,
        idea_stop_want,
        src_open,
        src_nigh,
    ) -> set[float, float]:
        fact_open = None
        fact_nigh = None
        if src_open <= idea_gogo_want and src_nigh >= idea_stop_want:
            # if parent range contains all idea range
            fact_open = idea_gogo_want
            fact_nigh = idea_stop_want
        elif src_open >= idea_gogo_want and src_nigh < idea_stop_want:
            # if parent range exists inside idea range
            fact_open = src_open
            fact_nigh = src_nigh
        elif (
            src_open >= idea_gogo_want
            and src_open < idea_stop_want
            and src_nigh > idea_stop_want
        ):
            # if parent range gogo_wants inside idea range and ends outside idea range
            fact_open = src_open
            fact_nigh = idea_stop_want
        elif src_open <= idea_gogo_want and src_nigh > idea_gogo_want:
            fact_open = idea_gogo_want
            fact_nigh = src_nigh
        # if src_open <= idea_gogo_want and src_nigh >= idea_stop_want:
        #     # if parent range contains all idea range
        #     fact_open = idea_gogo_want
        #     fact_nigh = idea_stop_want
        # elif src_open >= idea_gogo_want and src_nigh < idea_stop_want:
        #     # if parent range exists inside idea range
        #     fact_open = src_open
        #     fact_nigh = src_nigh
        # elif src_open >= idea_gogo_want and src_open < idea_stop_want and src_nigh > idea_stop_want:
        #     # if parent range gogo_wants inside idea range and ends outside idea range
        #     fact_open = src_open
        #     fact_nigh = idea_stop_want
        # elif (
        #     # if parent range gogo_wants outside idea range and ends inside idea range
        #     src_open <= idea_gogo_want
        #     and src_nigh > idea_gogo_want
        #     and src_nigh < idea_stop_want
        # ):
        #     fact_open = idea_gogo_want
        #     fact_nigh = src_nigh

        return fact_open, fact_nigh

    def _get_multipler_calc_fact_attr(
        self,
        idea_gogo_want,
        idea_stop_want,
        idea_numor,
        idea_denom,
        src_open,
        src_nigh,
    ) -> set[float, float]:
        return self._get_range_calc_fact_attr(
            idea_gogo_want=idea_gogo_want,
            idea_stop_want=idea_stop_want,
            src_open=src_open * idea_numor / idea_denom,
            src_nigh=src_nigh * idea_numor / idea_denom,
        )

    def _get_remainder_calc_fact_attr(
        self,
        idea_gogo_want,
        idea_stop_want,
        src_open,
        src_nigh,
    ):
        fact_open = None
        fact_nigh = None

        if src_nigh - src_open >= idea_stop_want:  # - idea_gogo_want:
            fact_open = idea_gogo_want
            fact_nigh = idea_stop_want
        else:
            fact_open = src_open % idea_stop_want
            fact_nigh = src_nigh % idea_stop_want

        return fact_open, fact_nigh

    def _create_new_fact(
        self, x_idea: IdeaUnit, src_fact: FactUnit, src_idea: IdeaUnit
    ) -> FactUnit:  # sourcery skip: remove-redundant-if
        if x_idea._gogo_want is None or x_idea._stop_want is None:
            raise InvalidAxiomException(f"Idea {x_idea.get_road()} does not have range")

        idea_gogo_want = x_idea._gogo_want
        idea_stop_want = x_idea._stop_want
        idea_numor = x_idea._numor
        idea_denom = x_idea._denom
        idea_reest = x_idea._reest
        src_open = src_fact.open
        src_nigh = src_fact.nigh
        src_idea_gogo_want = src_idea._gogo_want
        src_idea_stop_want = src_idea._stop_want
        idea_road = x_idea.get_road()

        fact_open = None
        fact_nigh = None

        if src_open is None and src_nigh is None:
            fact_open = None
            fact_nigh = None
        elif (idea_numor is None or idea_denom is None) and src_open > src_nigh:
            fact_open, fact_nigh = self._get_loop_range_calc_fact_attr(
                idea_gogo_want=idea_gogo_want,
                idea_stop_want=idea_stop_want,
                src_open=src_open,
                src_nigh=src_nigh,
                src_idea_gogo_want=src_idea_gogo_want,
                src_idea_stop_want=src_idea_stop_want,
            )

        elif idea_numor is None or idea_denom is None:
            fact_open, fact_nigh = self._get_range_calc_fact_attr(
                idea_gogo_want=idea_gogo_want,
                idea_stop_want=idea_stop_want,
                src_open=src_open,
                src_nigh=src_nigh,
            )
        elif (
            idea_numor is not None
            and idea_denom is not None
            and idea_reest in (False, None)
        ):
            fact_open, fact_nigh = self._get_multipler_calc_fact_attr(
                idea_gogo_want=idea_gogo_want,
                idea_stop_want=idea_stop_want,
                idea_numor=idea_numor,
                idea_denom=idea_denom,
                src_open=src_open,
                src_nigh=src_nigh,
            )
        elif idea_numor is not None and idea_denom is not None and idea_reest:
            fact_open, fact_nigh = self._get_remainder_calc_fact_attr(
                idea_gogo_want=idea_gogo_want,
                idea_stop_want=idea_stop_want,
                src_open=src_open,
                src_nigh=src_nigh,
            )

        active = fact_open is not None and fact_nigh is not None
        return factunit_shop(
            base=idea_road,
            pick=idea_road,
            open=fact_open,
            nigh=fact_nigh,
        )

    def is_axioms_evaluated(self) -> bool:
        return sum(axiom.eval_status is True for axiom in self.axioms.values()) == len(
            self.axioms
        )

    def get_unevaluated_axiom(self) -> Axiom:
        for axiom in self.axioms.values():
            if axiom.eval_status is False:
                # set to True
                axiom.eval_status = True
                return axiom

    # def _add_axiom_idea(
    def eval(self, x_idea: IdeaUnit, src_fact: FactUnit, src_idea: IdeaUnit):
        new_fact = self._create_new_fact(
            x_idea=x_idea, src_fact=src_fact, src_idea=src_idea
        )
        road_x = x_idea.get_road()
        if self.axioms.get(road_x) is None:
            self.axioms[road_x] = Axiom(
                src_fact=src_fact,
                calc_fact=new_fact,
                x_idea=x_idea,
                eval_status=False,
                eval_count=1,
            )


def axioms_shop(axioms: dict[RoadUnit, Axiom] = None, delimiter: str = None) -> Axioms:
    return Axioms(axioms=get_empty_dict_if_none(axioms))
