from enum import Enum
from dataclasses import dataclass

from premeno.risk_api.canrisk.utils import header_line

class OralContraStatus(Enum):
    Never = 'N'
    Former = 'F'
    Current = 'C'


@dataclass
class OralContraceptiveData:
    years_of_use: int 
    status: OralContraStatus = OralContraStatus.Never

    def __str__(self) -> str:
        if self.status != OralContraStatus.Never:
            return f"{self.status.value}:{self.years_of_use}"
        else:
            return self.status.value


class MhtStatus(Enum):
    Never = 'N'
    Former = 'F'
    Oestrogen = 'E'
    Combined = 'C' # or other


@dataclass 
class RiskFactors:
    age_at_menarche: int
    number_of_children: int
    age_at_first_live_birth: int
    oral_contraceptive_use: OralContraceptiveData
    mht_use: MhtStatus
    height_cm: int
    bmi: float
    alcohol_grams: float
    age_at_menopause: int

    def _first_live_birth_header(self) -> str:
        if self.number_of_children == 0:
            return ""

        return f"{header_line('First_live_birth', self.age_at_first_live_birth)}\n"

    def _age_at_menopause_header(self) -> str:
        if self.age_at_menopause == 0:
            return ""
        return f"{header_line('menopause', self.age_at_menopause)}\n"

    def make_header(self) -> str:
        return (f"{header_line('menarche', self.age_at_menarche)}\n"
                f"{header_line('parity', self.number_of_children)}\n"
                f"{self._first_live_birth_header()}"
                f"{header_line('oc_use', self.oral_contraceptive_use)}\n"
                f"{header_line('mht_use', self.mht_use.value)}\n"
                f"{header_line('BMI', self.bmi)}\n"
                f"{header_line('alcohol', self.alcohol_grams)}\n"
                f"{self._age_at_menopause_header()}"
                f"{header_line('height', self.height_cm)}\n")
