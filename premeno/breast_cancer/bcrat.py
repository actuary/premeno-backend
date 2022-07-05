import math
import pickle
from dataclasses import dataclass
from typing import Optional


@dataclass
class BCRAT:
    age_start: Optional[float]
    age_end: Optional[float]
    no_of_biopsies: Optional[int]
    hyperplasia: Optional[int]
    age_menarche: Optional[float]
    age_at_first_child: Optional[float]
    no_of_relatives: Optional[int]
    race: Optional[str]


class ValidationError:
    pass


class Subject:
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
            self._age_start < 20
            or self._age_start >= 90
            or self._age_start >= self._age_end
        ):
            return None
        return self._age_start

    @property
    def age_end(self) -> Optional[float]:
        if self._age_end > 90 or self._age_start >= self._age_end:
            return None
        return self._age_end

    @property
    def no_of_biopsies_cat(self) -> Optional[int]:
        no_of_biopsies_cat = -1

        if self._no_of_biopsies in (0, 99) and self._hyperplasia != 99:
            no_of_biopsies_cat = None

        if 0 < self._no_of_biopsies < 99 and self._hyperplasia not in (0, 1, 99):
            no_of_biopsies_cat = None

        if no_of_biopsies_cat == -1 and self._no_of_biopsies in (0, 99):
            no_of_biopsies_cat = 0

        if no_of_biopsies_cat == -1 and self._no_of_biopsies == 1:
            no_of_biopsies_cat = 1

        if no_of_biopsies_cat == -1 and 2 <= self._no_of_biopsies < 99:
            no_of_biopsies_cat = 2

        if self._race in [3, 5] and self._no_of_biopsies in (0, 99):
            no_of_biopsies_cat = 0

        if self._race in [3, 5] and no_of_biopsies_cat and no_of_biopsies_cat >= 2:
            no_of_biopsies_cat = 1

        return no_of_biopsies_cat

    @property
    def age_at_menarche_cat(self) -> Optional[int]:
        age_menarche_cat = None

        if (14 <= self._age_menarche <= self._age_start) or self._age_menarche == 99:
            age_menarche_cat = 0

        if 12 <= self._age_menarche < 14:
            age_menarche_cat = 1

        if 0 < self._age_menarche < 12:
            age_menarche_cat = 2

        if self._age_menarche > self._age_start and self._age_menarche != 99:
            age_menarche_cat = None

        if self._race == 2 and age_menarche_cat == 2:
            age_menarche_cat = 1

        if self._race == 3:
            age_menarche_cat = 0

        return age_menarche_cat

    @property
    def age_at_first_child_cat(self) -> Optional[int]:
        age_at_first_child_cat = None

        if self._age_at_first_child < 20 or self._age_at_first_child == 99:
            age_at_first_child_cat = 0

        if 20 <= self._age_at_first_child < 25:
            age_at_first_child_cat = 1

        if 25 <= self._age_at_first_child < 30 or self._age_at_first_child == 98:
            age_at_first_child_cat = 2

        if 30 <= self._age_at_first_child < 98:
            age_at_first_child_cat = 3

        if self._age_menarche != 99 and self._age_at_first_child < self._age_menarche:
            age_at_first_child_cat = None

        if self._age_start < self._age_at_first_child < 98:
            age_at_first_child_cat = None

        if self._race == 2:
            age_at_first_child_cat = 0

        if (
            self._race in (3, 5)
            and self._age_at_first_child != 98
            and age_at_first_child_cat == 2
        ):
            age_at_first_child_cat = 1

        if self._race in (3, 5) and age_at_first_child_cat == 3:
            age_at_first_child_cat = 2

        return age_at_first_child_cat

    @property
    def no_of_relatives_cat(self) -> Optional[int]:
        no_of_relatives_cat = None

        if self._no_of_relatives == 0 or self._no_of_relatives == 99:
            no_of_relatives_cat = 0

        if self._no_of_relatives == 1:
            no_of_relatives_cat = 1

        if 2 <= self._no_of_relatives < 99:
            no_of_relatives_cat = 2

        if 6 <= self._race <= 11 and no_of_relatives_cat == 2:
            no_of_relatives_cat = 1

        if self._race in (3, 5) and no_of_relatives_cat == 2:
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
        if self.no_of_biopsies_cat is None:
            relative_risk_factor = None

        if self.no_of_biopsies_cat is not None and self.no_of_biopsies_cat == 0:
            relative_risk_factor = 1.00

        if self.no_of_biopsies_cat is not None and self.no_of_biopsies_cat > 0:
            if self._hyperplasia == 0:
                relative_risk_factor = 0.93
            elif self._hyperplasia == 1:
                relative_risk_factor = 1.82
            elif self._hyperplasia == 99:
                relative_risk_factor = 1.00

        if self._no_of_biopsies in (0, 99) and self._hyperplasia != 99:
            relative_risk_factor = None

        if 0 < self._no_of_biopsies < 99 and self._hyperplasia not in (0, 1, 99):
            relative_risk_factor = None

        return relative_risk_factor

    @property
    def is_valid(self) -> bool:
        return True


def recode_number_of_biopsies(no_of_biopsies, hyperplasia, race):
    no_of_biopsies_cat = -1

    if (no_of_biopsies == 0 or no_of_biopsies == 99) and hyperplasia != 99:
        no_of_biopsies_cat = None

    if no_of_biopsies > 0 and no_of_biopsies < 99 and hyperplasia not in (0, 1, 99):
        no_of_biopsies_cat = None

    if no_of_biopsies_cat == -1 and no_of_biopsies in (0, 99):
        no_of_biopsies_cat = 0

    if no_of_biopsies_cat == -1 and no_of_biopsies == 1:
        no_of_biopsies_cat = 1

    if no_of_biopsies_cat == -1 and 2 <= no_of_biopsies < 99:
        no_of_biopsies_cat = 2

    if race in [3, 5] and no_of_biopsies in (0, 99):
        no_of_biopsies_cat = 0

    if race in [3, 5] and no_of_biopsies_cat and no_of_biopsies_cat >= 2:
        no_of_biopsies_cat = 1

    return no_of_biopsies_cat


def recode_age_menarche(age_menarche, age_start, race):
    age_menarche_cat = None

    if (14 <= age_menarche <= age_start) or age_menarche == 99:
        age_menarche_cat = 0

    if 12 <= age_menarche < 14:
        age_menarche_cat = 1

    if 0 < age_menarche < 12:
        age_menarche_cat = 2

    if age_menarche > age_start and age_menarche != 99:
        age_menarche_cat = None

    if race == 2 and age_menarche_cat == 2:
        age_menarche_cat = 1

    if race == 3:
        age_menarche_cat = 0

    return age_menarche_cat


def recode_age_first_child(age_at_first_child, age_menarche, age_start, race):
    age_at_first_child_cat = None

    if age_at_first_child < 20 or age_at_first_child == 99:
        age_at_first_child_cat = 0

    if 20 <= age_at_first_child < 25:
        age_at_first_child_cat = 1

    if 25 <= age_at_first_child < 30 or age_at_first_child == 98:
        age_at_first_child_cat = 2

    if 30 <= age_at_first_child < 98:
        age_at_first_child_cat = 3

    if age_menarche != 99 and age_at_first_child < age_menarche:
        age_at_first_child_cat = None

    if age_start < age_at_first_child < 98:
        age_at_first_child_cat = None

    if race == 2:
        age_at_first_child_cat = 0

    if race in (3, 5) and age_at_first_child != 98 and age_at_first_child_cat == 2:
        age_at_first_child_cat = 1

    if race in (3, 5) and age_at_first_child_cat == 3:
        age_at_first_child_cat = 2

    return age_at_first_child_cat


def recode_no_of_relatives(no_of_relatives, race):
    no_of_relatives_cat = None

    if no_of_relatives == 0 or no_of_relatives == 99:
        no_of_relatives_cat = 0

    if no_of_relatives == 1:
        no_of_relatives_cat = 1

    if 2 <= no_of_relatives < 99:
        no_of_relatives_cat = 2

    if 6 <= race <= 11 and no_of_relatives_cat == 2:
        no_of_relatives_cat = 1

    if race in (3, 5) and no_of_relatives_cat == 2:
        no_of_relatives_cat = 1

    return no_of_relatives_cat


def recode_race(race):
    if race not in range(1, 12):
        return None

    return race


def calculate_relative_risk_factor(hyperplasia, no_of_biopsies, no_of_biopsies_cat):
    relative_risk_factor = None
    if no_of_biopsies_cat is None:
        relative_risk_factor = None

    if no_of_biopsies_cat is not None and no_of_biopsies_cat == 0:
        relative_risk_factor = 1.00

    if no_of_biopsies_cat is not None and no_of_biopsies_cat > 0:
        if hyperplasia == 0:
            relative_risk_factor = 0.93
        elif hyperplasia == 1:
            relative_risk_factor = 1.82
        elif hyperplasia == 99:
            relative_risk_factor = 1.00

    if (no_of_biopsies == 0 or no_of_biopsies == 99) and hyperplasia != 99:
        relative_risk_factor = None

    if no_of_biopsies > 0 and no_of_biopsies < 99 and hyperplasia not in (0, 1, 99):
        relative_risk_factor = None

    return relative_risk_factor


def recode_hyperplasia(hyperplasia, number_of_biopsies_cat, number_of_biopsies):
    recoded_hyper_plasia = hyperplasia
    if (number_of_biopsies == 0 or number_of_biopsies == 99) and hyperplasia != 99:
        recoded_hyper_plasia = None

    if (
        number_of_biopsies > 0
        and number_of_biopsies < 99
        and hyperplasia not in (0, 1, 99)
    ):
        recoded_hyper_plasia = None

    if number_of_biopsies_cat is None or hyperplasia is None:
        recoded_hyper_plasia = None

    return recoded_hyper_plasia


def recode_age_start(age_start, age_end):
    if age_start < 20 or age_start >= 90 or age_start >= age_end:
        return None
    return age_start


def recode_age_end(age_start, age_end):
    if age_end > 90 or age_start >= age_end:
        return None
    return age_end


def char_race(Race):
    CharRace = "??"

    race_to_char = {
        1: "Wh",
        2: "AA",
        3: "HU",
        4: "NA",
        5: "HF",
        6: "Ch",
        7: "Ja",
        8: "Fi",
        9: "Hw",
        10: "oP",
        11: "oA",
    }

    if Race in race_to_char.keys():
        CharRace = race_to_char[Race]

    return CharRace


@dataclass
class BCRAT_Factors:
    T1: Optional[int]
    T2: Optional[int]
    NB_Cat: Optional[int]
    AM_Cat: Optional[int]
    AF_Cat: Optional[int]
    NR_Cat: Optional[int]
    R_Hyp: Optional[float]
    HypPlas: Optional[float]
    Race: Optional[int]

    @property
    def is_valid(self) -> bool:
        return (
            self.T1 is not None
            and self.T2 is not None
            and self.NB_Cat is not None
            and self.AM_Cat is not None
            and self.AF_Cat is not None
            and self.NR_Cat is not None
            and self.R_Hyp is not None
            and self.HypPlas is not None
            and self.Race is not None
            and self.T2 > self.T1
        )

    @property
    def to_csv_row(self) -> str:
        return f"{self.T1},{self.T2},{self.NB_Cat},{self.AM_Cat},{self.AF_Cat},{self.NR_Cat},{self.R_Hyp},{self.HypPlas},{self.Race},{self.is_valid}\n"


def recode_check_v2(data):
    T1 = recode_age_start(data.T1, data.T2)
    T2 = recode_age_end(data.T1, data.T2)
    NB_Cat = recode_number_of_biopsies(data.N_Biop, data.HypPlas, data.Race)
    AM_Cat = recode_age_menarche(data.AgeMen, data.T1, data.Race)
    AF_Cat = recode_age_first_child(data.Age1st, data.AgeMen, data.T1, data.Race)
    NR_Cat = recode_no_of_relatives(data.N_Rels, data.Race)
    HypPlas = recode_hyperplasia(data.HypPlas, NB_Cat, data.N_Biop)
    R_Hyp = calculate_relative_risk_factor(data.HypPlas, data.N_Biop, NB_Cat)
    Race = recode_race(data.Race)

    return BCRAT_Factors(T1, T2, NB_Cat, AM_Cat, AF_Cat, NR_Cat, R_Hyp, HypPlas, Race)


def convert_row_to_BCRAT(row):
    return BCRAT(
        row.T1,
        row.T2,
        row.N_Biop,
        row.HypPlas,
        row.AgeMen,
        row.Age1st,
        row.N_Rels,
        row.Race,
    )


def relativeRisk(
    race, numberOfBiopies, ageFirstChild, ageMenarche, numberRelatives, rHyp
):
    betas = {
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
            0.0000000000,
            0.2318368334,
            0.166685441,
            0.0000000000,
            0.0000000000,
        ],
        "other_hispanic": [
            0.4798624017,
            0.2593922322,
            0.4669246218,
            0.9076679727,
            0.0000000000,
            0.0000000000,
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

    beta = betas[race]
    lp1 = (
        numberOfBiopies * beta[0]
        + ageMenarche * beta[1]
        + ageFirstChild * beta[2]
        + numberRelatives * beta[3]
        + ageFirstChild * numberRelatives * beta[5]
        + math.log(rHyp)
    )
    lp2 = lp1 + numberOfBiopies * beta[4]

    return (math.exp(lp1), math.exp(lp2))


def save_object(obj, filename):
    with open(filename, "wb") as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
    obj = None
    with open(filename, "rb") as file:
        obj = pickle.load(file)

    return obj


if __name__ == "__main__":
    pass
