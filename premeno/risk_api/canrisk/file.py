from dataclasses import dataclass, field
from typing import List

from premeno.risk_api.canrisk.pedigree import PedigreeEntry
from premeno.risk_api.canrisk.risk_factors import RiskFactors
from premeno.risk_api.canrisk.utils import header_line


@dataclass
class CanRiskFile:
    risk_factors: RiskFactors
    pedigree: PedigreeEntry
    mother: PedigreeEntry
    father: PedigreeEntry
    sisters: List[PedigreeEntry] = field(default_factory=list)

    def _version_info(self) -> str:
        return "CanRisk 2.0"

    def _has_children(self) -> bool:
        return self.risk_factors.number_of_children > 0

    def __str__(self) -> str:
        pedigree_data = [self.pedigree, self.mother, self.father]

        if self._has_children():
            age_at_flb = self.risk_factors.age_at_first_live_birth
            no_children = self.risk_factors.number_of_children

            pedigree_data.append(self.pedigree.husband())
            pedigree_data.extend(self.pedigree.children(age_at_flb, no_children))

        pedigree_data.extend(self.sisters)

        pedigree_file = "\n".join([str(person) for person in pedigree_data])
        return (f"{header_line(self._version_info(), None)}\n"
                f"{self.risk_factors.make_header()}"
                f"{header_line(PedigreeEntry.header(), None)}\n"
                f"{pedigree_file}")
