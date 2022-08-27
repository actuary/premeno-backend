from typing import Optional

from premeno.risk_api.gail.errors import FactorError, RecodingError
from premeno.risk_api.gail.race import ASIANS, ETHNIC_GROUP_TO_RACE, HISPANICS, Race
from premeno.risk_api.questionnaire import (
    BiopsyStatus,
    HyperplasiaStatus,
    Questionnaire,
)

_MIN_AGE = 25  # BCRAT mention 35 but use 25 in their package. Instead, we'll use 25
_MAX_AGE = 80


class GailFactors:
    def __init__(
        self,
        age: float,
        number_of_biopsies: int,
        age_at_menarche: int,
        age_at_first_child: int,
        number_of_relatives: int,
        relative_risk_factor: float,
        race: Race,
    ) -> None:
        if age < _MIN_AGE or age >= _MAX_AGE:
            raise FactorError(f"Age must be between {_MIN_AGE} and {_MAX_AGE}")
        self.age = age

        if not 0 <= number_of_biopsies <= 2:
            raise FactorError("Biopsies factor should be between 0 and 2")

        self.number_of_biopsies = number_of_biopsies

        if not 0 <= age_at_menarche <= 2:
            raise FactorError("Age at menarche factor should be between 0 and 2")

        self.age_at_menarche = age_at_menarche

        if not 0 <= age_at_first_child <= 3:
            raise FactorError("Age at first child factor should be between 0 and 3")

        self.age_at_first_child = age_at_first_child

        if not 0 <= number_of_relatives <= 2:
            raise FactorError("Number of relatives factor should be between 0 and 2")

        self.number_of_relatives = number_of_relatives

        if not 0 < relative_risk_factor:
            raise FactorError("Relative risk factor should be positive")

        self.relative_risk_factor = relative_risk_factor
        self.race = race

    @classmethod
    def from_questionnaire(cls, data: Questionnaire) -> "GailFactors":
        race = ETHNIC_GROUP_TO_RACE[data.ethnic_group]
        biops = recode_number_of_biopsies(data.number_of_biopsies, race)
        menarche = recode_age_at_menarche(data.age_at_menarche, race)
        first_child = recode_age_at_first_child(
            data.nulliparous, data.age_at_first_child, race
        )

        num_rels = recode_number_of_relatives(
            data.number_of_relatives_with_cancer, race
        )
        rr_fac = hyperplasia_relative_risk(
            data.number_of_biopsies, data.biopsies_with_hyperplasia, race
        )

        return GailFactors(
            data.age, biops, menarche, first_child, num_rels, rr_fac, race
        )


def recode_number_of_biopsies(number_of_biopsies: BiopsyStatus, race: Race) -> int:
    """Recodes number of biopsies from 0 to 2"""
    if number_of_biopsies in (BiopsyStatus.UNKNOWN, BiopsyStatus.NONE):
        return 0

    elif number_of_biopsies == BiopsyStatus.ONE or race in HISPANICS:
        # hispanic RR model from San Fran Bay Area Breast Cancer Study (SFBCS):
        #         (1) groups N_Biop ge 2 with N_Biop eq 1
        return 1

    elif number_of_biopsies == BiopsyStatus.MULTIPLE:
        return 2

    # should have covered all, so won't happen unless mistake
    raise RecodingError("Failed to recode number of biopsies")  # pragma: no cover


def recode_age_at_menarche(age_at_menarche: Optional[int], race: Race) -> int:
    """
    Recodes age_at_menarche from 0 to 2. Assumes valid age at menarche (
    i.e. less than current age and not negative) as validated by questionnaire
    """
    if (
        age_at_menarche is None
        or age_at_menarche >= 14
        or race == Race.HISPANIC_AMERICAN_US
    ):
        # hispanic RR model from San Fran Bay Area Breast Cancer Study (SFBCS):
        #         (2) eliminates  AgeMen from model for US Born hispanic women
        return 0

    elif age_at_menarche >= 12 or (
        age_at_menarche < 12 and race == Race.AFRICAN_AMERICAN
    ):
        # african-american RR model from CARE study:
        #         (2) groups AgeMen=2 with AgeMen=1;
        return 1

    elif age_at_menarche < 12:
        return 2

    # should have covered all scenarios
    raise RecodingError("Failed to recode age at menarche")  # pragma: no cover


def recode_age_at_first_child(
    nulliparous: bool, age_at_first_child: Optional[int], race: Race
) -> int:
    """Recodes age at first child from 0 to 3. Assumes
    valid age at first child - as validated by Questionnaire
    """

    if race == Race.AFRICAN_AMERICAN:
        # african-american RR model from CARE study:
        #       (1) eliminates Age1st from model;
        return 0

    elif nulliparous:
        return 2

    elif age_at_first_child is None or age_at_first_child < 20:
        return 0

    elif age_at_first_child < 25 or (age_at_first_child < 30 and race in HISPANICS):
        # hispanic RR model from San Fran Bay Area Breast Cancer Study (SFBCS):
        #         (3) group Age1st=25-29 with Age1st=20-24 and code as 1
        return 1

    elif age_at_first_child < 30 or race in HISPANICS:
        # hispanic RR model from San Fran Bay Area Breast Cancer Study (SFBCS):
        #         (3) for   Age1st=30+, 98 (nulliparous)       code as 2
        return 2

    else:
        return 3


def recode_number_of_relatives(number_of_relatives: int, race: Race) -> int:
    """Recodes the number of relatives from 0 to 2"""

    if number_of_relatives == 0 or number_of_relatives is None:
        # Unknown number of relatives lumped in with 0 (not allowed anyway for mo)
        return 0

    elif number_of_relatives == 1 or race in (HISPANICS + ASIANS):
        # for asian-americans cat 2 is pooled with cat 1
        # hispanic RR model from San Fran Bay Area Breast Cancer Study (SFBCS):
        #         (4) groups N_Rels=2 with N_Rels=1;
        return 1

    else:
        return 2


def hyperplasia_relative_risk(
    number_of_biopsies: BiopsyStatus, hyperplasia: HyperplasiaStatus, race: Race
) -> float:
    """Returns the hyperplasia relative risk multiplicative factor"""

    number_of_biopsies_fac = recode_number_of_biopsies(number_of_biopsies, race)

    if number_of_biopsies_fac == 0 or hyperplasia == HyperplasiaStatus.UNKNOWN:
        return 1.00
    elif hyperplasia == HyperplasiaStatus.NONE:
        return 0.93
    elif hyperplasia == HyperplasiaStatus.SOME:
        return 1.82
    else:
        # can't happen unless enums change
        raise RecodingError("Failed to recode relative risk factor")  # pragma: no cover
