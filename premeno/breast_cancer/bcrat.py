import math
from typing import Optional


class Subject:
    _betas = {
        "white": [
            0.5292641686,
            0.0940103059,
            0.2186262218,
            0.9583027845,
            -0.2880424830,
            -0.1908113865,
        ],
        "black": [0.1822121131, 0.2672530336, 0.0, 0.4757242578, -0.1119411682, 0.0],
        "hispanic": [
            0.0970783641,
            0.0,
            0.2318368334,
            0.166685441,
            0.0,
            0.0,
        ],
        "other_hispanic": [
            0.4798624017,
            0.2593922322,
            0.4669246218,
            0.9076679727,
            0.0,
            0.0,
        ],
        "other": [
            0.5292641686,
            0.0940103059,
            0.2186262218,
            0.9583027845,
            -0.2880424830,
            -0.1908113865,
        ],
        "asian": [
            0.55263612260619,
            0.07499257592975,
            0.27638268294593,
            0.79185633720481,
            0.0,
            0.0,
        ],
    }

    _races = {
        1: "white",
        2: "black",
        3: "hispanic",
        4: "other",
        5: "other_hispanic",
        6: "asian",
        7: "asian",
        8: "asian",
        9: "asian",
        10: "asian",
        11: "asian",
    }

    HISPANICS = [3, 5]
    ASIANS = [6, 7, 8, 9, 10, 11]
    UNKNOWN_RESPONSE = 99
    MIN_AGE = 20
    MAX_AGE = 90

    def __init__(
        self,
        age_start: float,
        age_end: float,
        no_of_biopsies: int,
        hyperplasia: int,
        age_menarche: int,
        age_at_first_child: int,
        no_of_relatives: int,
        race: int,
    ):
        self._age_start = age_start
        self._age_end = age_end
        self._no_of_biopsies = no_of_biopsies
        self._hyperplasia = hyperplasia
        self._age_menarche = age_menarche
        self._age_at_first_child = age_at_first_child
        self._no_of_relatives = no_of_relatives
        self._race = race

    @property
    def age_start(self) -> Optional[float]:
        if (
            self._age_start < self.MIN_AGE
            or self._age_start >= self.MAX_AGE
            or self._age_start >= self._age_end
        ):
            return None
        return self._age_start

    @property
    def age_end(self) -> Optional[float]:
        if self._age_end > self.MAX_AGE or self._age_start >= self._age_end:
            return None
        return self._age_end

    @property
    def no_of_biopsies_cat(self) -> Optional[int]:
        no_of_biopsies_cat = None

        if self._invalid_biopsy_choice(self._no_of_biopsies, self._hyperplasia):
            no_of_biopsies_cat = None

        elif no_of_biopsies_cat == None and self._no_of_biopsies in (
            0,
            self.UNKNOWN_RESPONSE,
        ):
            no_of_biopsies_cat = 0

        elif no_of_biopsies_cat == None and self._no_of_biopsies == 1:
            no_of_biopsies_cat = 1

        elif (
            no_of_biopsies_cat == None
            and 2 <= self._no_of_biopsies < self.UNKNOWN_RESPONSE
        ):
            no_of_biopsies_cat = 2

        if self._race in self.HISPANICS:
            if self._no_of_biopsies in (0, self.UNKNOWN_RESPONSE):
                no_of_biopsies_cat = 0

            if (no_of_biopsies_cat or -1) >= 2:
                no_of_biopsies_cat = 1

        return no_of_biopsies_cat

    @property
    def age_at_menarche_cat(self) -> Optional[int]:
        age_menarche_cat = None

        if self._age_menarche < 0:
            age_menarche_cat = None

        elif self._age_menarche < 12:
            age_menarche_cat = 2

        elif self._age_menarche < 14:
            age_menarche_cat = 1

        elif 14 <= self._age_menarche <= self._age_start:
            age_menarche_cat = 0

        elif self._age_menarche == self.UNKNOWN_RESPONSE:
            age_menarche_cat = 0

        if self._age_start < self._age_menarche < self.UNKNOWN_RESPONSE:
            age_menarche_cat = None

        if self._race == 2 and age_menarche_cat == 2:
            age_menarche_cat = 1

        if self._race == 3:
            age_menarche_cat = 0

        return age_menarche_cat

    @property
    def age_at_first_child_cat(self) -> Optional[int]:
        age_at_first_child_cat = None
        UNKNOWN_RESPONSE_1st = 98

        if self._age_at_first_child < 20:
            age_at_first_child_cat = 0

        elif self._age_at_first_child < 25:
            age_at_first_child_cat = 1

        elif self._age_at_first_child < 30:
            age_at_first_child_cat = 2

        elif self._age_at_first_child < UNKNOWN_RESPONSE_1st:
            age_at_first_child_cat = 3

        elif self._age_at_first_child == UNKNOWN_RESPONSE_1st:
            age_at_first_child_cat = 2

        elif self._age_at_first_child == self.UNKNOWN_RESPONSE:
            age_at_first_child_cat = 0

        if self._age_at_first_child < self._age_menarche < self.UNKNOWN_RESPONSE:
            age_at_first_child_cat = None

        if self._age_start < self._age_at_first_child < UNKNOWN_RESPONSE_1st:
            age_at_first_child_cat = None

        if self._race == 2:
            age_at_first_child_cat = 0

        if (
            self._race in self.HISPANICS
            and self._age_at_first_child != UNKNOWN_RESPONSE_1st
            and age_at_first_child_cat == 2
        ):
            age_at_first_child_cat = 1

        if self._race in self.HISPANICS and age_at_first_child_cat == 3:
            age_at_first_child_cat = 2

        return age_at_first_child_cat

    @property
    def no_of_relatives_cat(self) -> Optional[int]:
        no_of_relatives_cat = None

        if self._no_of_relatives == 0:
            no_of_relatives_cat = 0

        elif self._no_of_relatives == 1:
            no_of_relatives_cat = 1

        elif self._no_of_relatives < self.UNKNOWN_RESPONSE:
            no_of_relatives_cat = 2

        elif self._no_of_relatives == self.UNKNOWN_RESPONSE:
            no_of_relatives_cat = 0

        if self._race in self.HISPANICS + self.ASIANS and no_of_relatives_cat == 2:
            no_of_relatives_cat = 1

        return no_of_relatives_cat

    @property
    def race(self) -> Optional[int]:
        if self._race not in range(1, 12):
            return None
        return self._race

    @property
    def relative_risk_factor(self):
        relative_risk_factor = None

        if self.no_of_biopsies_cat is not None and self.no_of_biopsies_cat == 0:
            relative_risk_factor = 1.00

        if (self.no_of_biopsies_cat or 0) > 0:
            if self._hyperplasia == 0:
                relative_risk_factor = 0.93
            elif self._hyperplasia == 1:
                relative_risk_factor = 1.82
            elif self._hyperplasia == self.UNKNOWN_RESPONSE:
                relative_risk_factor = 1.00

        if self._invalid_biopsy_choice(self._no_of_biopsies, self._hyperplasia):
            relative_risk_factor = None

        return relative_risk_factor

    def _invalid_biopsy_choice(self, no_biopsies, hyperplasia) -> bool:
        return (
            (
                0 < no_biopsies < self.UNKNOWN_RESPONSE
                and hyperplasia not in (0, 1, self.UNKNOWN_RESPONSE)
            )
            or no_biopsies in (0, self.UNKNOWN_RESPONSE)
            and hyperplasia != self.UNKNOWN_RESPONSE
        )

    def is_valid(self) -> bool:
        return (
            self.age_start is not None
            and self.age_end is not None
            and self.no_of_biopsies_cat is not None
            and self.age_at_menarche_cat is not None
            and self.age_at_first_child_cat is not None
            and self.no_of_relatives_cat is not None
            and self.race is not None
        )

    def relative_risk(self) -> Optional[float]:
        if not self.is_valid():
            return None

        beta = self._betas[self._races[self.race]]  # type: ignore

        lp1 = (
            self.no_of_biopsies_cat * beta[0]  # type: ignore
            + self.age_at_menarche_cat * beta[1]  # type: ignore
            + self.age_at_first_child_cat * beta[2]  # type: ignore
            + self.no_of_relatives_cat * beta[3]  # type: ignore
            + self.age_at_first_child_cat
            * self.no_of_relatives_cat
            * beta[5]  # type: ignore
            + math.log(self.relative_risk_factor)  # type: ignore
        )  # type: ignore

        lp2 = lp1 + self.no_of_biopsies_cat * beta[4]  # type: ignore

        return (math.exp(lp1), math.exp(lp2))  # type: ignore


if __name__ == "__main__":
    pass
