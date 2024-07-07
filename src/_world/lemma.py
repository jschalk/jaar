from src._instrument.python import get_empty_dict_if_none
from src._world.reason_idea import FactUnit, RoadUnit, factunit_shop
from src._world.idea import IdeaUnit
from dataclasses import dataclass


class InvalidLemmaException(Exception):
    pass


@dataclass
class Lemma:
    src_fact: FactUnit
    calc_fact: FactUnit
    x_idea: IdeaUnit
    eval_status: bool
    eval_count: int


@dataclass
class Lemmas:
    lemmas: dict[RoadUnit, Lemma] = None

    def _get_loop_range_calc_fact_attr(
        self,
        idea_begin: float,
        idea_close: float,
        src_open: float,
        src_nigh: float,
        src_idea_begin: float,
        src_idea_close: float,
    ) -> RoadUnit:
        fact_open = None
        fact_nigh = None

        # if src_idea and fact_idea have equal range return equal src fact range
        if idea_begin == src_idea_begin and idea_close == src_idea_close:
            fact_open = src_open
            fact_nigh = src_nigh
        else:
            # create both ranges and get calc ranges for both. Return the not null one
            r1_open, r1_nigh = self._get_range_calc_fact_attr(
                idea_begin=idea_begin,
                idea_close=idea_close,
                src_open=src_idea_begin,
                src_nigh=src_nigh,
            )
            r2_open, r2_nigh = self._get_range_calc_fact_attr(
                idea_begin=idea_begin,
                idea_close=idea_close,
                src_open=src_open,
                src_nigh=src_idea_close,
            )
            # # if both are not null return r1_nigh as fact_open and r2_open as fact_nigh
            # if r1_open != None and r1_nigh != None and r2_open != None and r2_nigh != None:
            #     fact_open = r1_nigh
            #     fact_nigh = r2_open
            if r1_open != None and r1_nigh != None:
                fact_open = r1_open
                fact_nigh = r1_nigh
            elif r2_open != None and r2_nigh != None:
                fact_open = r2_open
                fact_nigh = r2_nigh

        return fact_open, fact_nigh

    def _get_range_calc_fact_attr(
        self,
        idea_begin,
        idea_close,
        src_open,
        src_nigh,
    ) -> set[float, float]:
        fact_open = None
        fact_nigh = None
        if src_open <= idea_begin and src_nigh >= idea_close:
            # if parent range contains all idea range
            fact_open = idea_begin
            fact_nigh = idea_close
        elif src_open >= idea_begin and src_nigh < idea_close:
            # if parent range exists inside idea range
            fact_open = src_open
            fact_nigh = src_nigh
        elif src_open >= idea_begin and src_open < idea_close and src_nigh > idea_close:
            # if parent range begins inside idea range and ends outside idea range
            fact_open = src_open
            fact_nigh = idea_close
        elif src_open <= idea_begin and src_nigh > idea_begin:
            fact_open = idea_begin
            fact_nigh = src_nigh
        # if src_open <= idea_begin and src_nigh >= idea_close:
        #     # if parent range contains all idea range
        #     fact_open = idea_begin
        #     fact_nigh = idea_close
        # elif src_open >= idea_begin and src_nigh < idea_close:
        #     # if parent range exists inside idea range
        #     fact_open = src_open
        #     fact_nigh = src_nigh
        # elif src_open >= idea_begin and src_open < idea_close and src_nigh > idea_close:
        #     # if parent range begins inside idea range and ends outside idea range
        #     fact_open = src_open
        #     fact_nigh = idea_close
        # elif (
        #     # if parent range begins outside idea range and ends inside idea range
        #     src_open <= idea_begin
        #     and src_nigh > idea_begin
        #     and src_nigh < idea_close
        # ):
        #     fact_open = idea_begin
        #     fact_nigh = src_nigh

        return fact_open, fact_nigh

    def _get_multipler_calc_fact_attr(
        self,
        idea_begin,
        idea_close,
        idea_numor,
        idea_denom,
        src_open,
        src_nigh,
    ) -> set[float, float]:
        return self._get_range_calc_fact_attr(
            idea_begin=idea_begin,
            idea_close=idea_close,
            src_open=src_open * idea_numor / idea_denom,
            src_nigh=src_nigh * idea_numor / idea_denom,
        )

    def _get_remainder_calc_fact_attr(
        self,
        idea_begin,
        idea_close,
        src_open,
        src_nigh,
    ):
        fact_open = None
        fact_nigh = None

        if src_nigh - src_open >= idea_close:  # - idea_begin:
            fact_open = idea_begin
            fact_nigh = idea_close
        else:
            fact_open = src_open % idea_close
            fact_nigh = src_nigh % idea_close

        return fact_open, fact_nigh

    def _create_new_fact(
        self, x_idea: IdeaUnit, src_fact: FactUnit, src_idea: IdeaUnit
    ) -> FactUnit:
        if x_idea._begin is None or x_idea._close is None:
            raise InvalidLemmaException(f"Idea {x_idea.get_road()} does not have range")

        idea_begin = x_idea._begin
        idea_close = x_idea._close
        idea_numor = x_idea._numor
        idea_denom = x_idea._denom
        idea_reest = x_idea._reest
        src_open = src_fact.open
        src_nigh = src_fact.nigh
        src_idea_begin = src_idea._begin
        src_idea_close = src_idea._close
        idea_road = x_idea.get_road()

        fact_open = None
        fact_nigh = None

        if src_open is None and src_nigh is None:
            fact_open = None
            fact_nigh = None
        elif (idea_numor is None or idea_denom is None) and src_open > src_nigh:
            fact_open, fact_nigh = self._get_loop_range_calc_fact_attr(
                idea_begin=idea_begin,
                idea_close=idea_close,
                src_open=src_open,
                src_nigh=src_nigh,
                src_idea_begin=src_idea_begin,
                src_idea_close=src_idea_close,
            )

        elif idea_numor is None or idea_denom is None:
            fact_open, fact_nigh = self._get_range_calc_fact_attr(
                idea_begin=idea_begin,
                idea_close=idea_close,
                src_open=src_open,
                src_nigh=src_nigh,
            )
        elif idea_numor != None and idea_denom != None and idea_reest in (False, None):
            fact_open, fact_nigh = self._get_multipler_calc_fact_attr(
                idea_begin=idea_begin,
                idea_close=idea_close,
                idea_numor=idea_numor,
                idea_denom=idea_denom,
                src_open=src_open,
                src_nigh=src_nigh,
            )
        elif idea_numor != None and idea_denom != None and idea_reest == True:
            fact_open, fact_nigh = self._get_remainder_calc_fact_attr(
                idea_begin=idea_begin,
                idea_close=idea_close,
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

    def is_lemmas_evaluated(self) -> bool:
        return sum(lemma.eval_status == True for lemma in self.lemmas.values()) == len(
            self.lemmas
        )

    def get_unevaluated_lemma(self) -> Lemma:
        for lemma in self.lemmas.values():
            if lemma.eval_status is False:
                # set to True
                lemma.eval_status = True
                return lemma

    # def _add_lemma_idea(
    def eval(self, x_idea: IdeaUnit, src_fact: FactUnit, src_idea: IdeaUnit):
        new_fact = self._create_new_fact(
            x_idea=x_idea, src_fact=src_fact, src_idea=src_idea
        )
        road_x = x_idea.get_road()
        if self.lemmas.get(road_x) is None:
            self.lemmas[road_x] = Lemma(
                src_fact=src_fact,
                calc_fact=new_fact,
                x_idea=x_idea,
                eval_status=False,
                eval_count=1,
            )


def lemmas_shop(lemmas: dict[RoadUnit, Lemma] = None, delimiter: str = None) -> Lemmas:
    return Lemmas(lemmas=get_empty_dict_if_none(lemmas))
