from dataclasses import dataclass, field
from typing import Optional

from premeno.risk_api.canrisk.pedigree import PedigreeEntry, Sex
from premeno.risk_api.canrisk.risk_factors import (
    MhtStatus,
    OralContraceptiveData,
    OralContraStatus,
    RiskFactors,
)
from premeno.risk_api.canrisk.utils import header_line
from premeno.risk_api.questionnaire import OralContraceptiveUse, Questionnaire
from premeno.risk_api.utils import alcohol_grams_per_day, calculate_bmi


def make_family(
    pedigree: PedigreeEntry,
    age_at_first_child: Optional[int],
    mother_age_at_diagnosis: Optional[int],
    sisters_ages_at_diagnosis: list[int],
) -> list[PedigreeEntry]:
    """ """
    family = [
        pedigree,
        pedigree.husband(),
        pedigree.mother(mother_age_at_diagnosis),
        pedigree.father(),
    ]

    family.extend(pedigree.calculate_sisters(sisters_ages_at_diagnosis))
    if age_at_first_child is not None:
        family.append(pedigree.child(age_at_first_child, 1))

    return family


@dataclass
class CanRiskFile:
    risk_factors: RiskFactors
    pedigrees: list[PedigreeEntry] = field(default_factory=list)

    def _version_info(self) -> str:
        return "CanRisk 2.0"

    def __str__(self) -> str:

        pedigree_file = "\n".join([str(person) for person in self.pedigrees])
        return (
            f"{header_line(self._version_info(), None)}\n"
            f"{self.risk_factors.make_header()}"
            f"{header_line(PedigreeEntry.header(), None)}\n"
            f"{pedigree_file}"
        )


""" Convert from questionnaire status to one expected by canrisk """
ORAL_CONTRACEPTIVE_MAPPING = {
    OralContraceptiveUse.NEVER: OralContraStatus.Never,
    OralContraceptiveUse.EVER: OralContraStatus.Former,
}


def create_canrisk_file(data: Questionnaire, mht_status: MhtStatus) -> CanRiskFile:
    """Creates can risk file from given mht status"""

    risk_factors = RiskFactors(
        data.age_at_menarche,
        data.number_of_children,
        data.age_at_first_child,
        OralContraceptiveData(
            5, ORAL_CONTRACEPTIVE_MAPPING[data.oral_contraception_use]
        ),
        mht_status,
        round(data.height),
        calculate_bmi(data.height, data.weight),
        alcohol_grams_per_day(data.alcohol_use),
        0,
    )

    pedigree = PedigreeEntry(
        "me", True, "me", Sex.Female, int(data.age), data.year_of_birth, "dad", "mum"
    )

    family = make_family(
        pedigree,
        data.age_at_first_child,
        data.mother_age_at_diagnosis,
        data.sisters_ages_at_diagnosis,
    )
    return CanRiskFile(risk_factors, family)
