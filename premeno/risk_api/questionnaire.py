from datetime import date, datetime, timedelta
from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator


class EthnicGroup(Enum):
    WHITE = "white"
    OTHER = "other"


class EducationLevel(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    COLLEGE = "college"
    UNIVERSITY = "uni"


class SmokingUse(Enum):
    NEVER = "never"
    PAST = "past"
    CURRENT = "current"


class OralContraceptiveUse(Enum):
    NEVER = "n"
    EVER = "y"


class MhtFormulation(Enum):
    NONE = "none"
    OESTROGEN = "e"
    COMBINED = "e+p"


class BiopsyStatus(Enum):
    NONE = 0
    ONE = 1
    MULTIPLE = 2
    UNKNOWN = 3


class HyperplasiaStatus(Enum):
    NONE = 0
    SOME = 1
    UNKNOWN = 3


def age_from_date(date_of_birth: date, to_date: date = date.today()) -> float:
    """ """
    return (to_date - date_of_birth) / timedelta(days=365.2425)


class Questionnaire(BaseModel):
    """Stores the questionnaire responses. Validates and transforms passed JSON data"""

    date_of_birth: date
    height: float
    weight: float
    ethnic_group: EthnicGroup
    education: EducationLevel
    alcohol_use: float
    smoking: SmokingUse
    mht: MhtFormulation
    age_at_menarche: int
    nulliparous: bool  # No children
    age_at_first_child: Optional[int]  # None means unknown
    oral_contraception_use: OralContraceptiveUse
    number_of_biopsies: BiopsyStatus
    biopsies_with_hyperplasia: HyperplasiaStatus
    mother_age_at_diagnosis: Optional[int]  # None means not diagnosed of BC
    sisters_ages_at_diagnosis: list[int]  # Empty means no diagnoses of BC
    questionnaire_date: date = date.today()

    @property
    def age(self) -> float:
        return age_from_date(self.date_of_birth, self.questionnaire_date)

    @property
    def year_of_birth(self) -> int:
        return self.date_of_birth.year

    @property
    def number_of_children(self) -> int:
        return 0 if self.nulliparous else 1

    @property
    def number_of_relatives_with_cancer(self) -> int:
        if self.mother_age_at_diagnosis is not None:
            return 1 + len(self.sisters_ages_at_diagnosis)

        return len(self.sisters_ages_at_diagnosis)

    @property
    def number_of_sisters_with_cancer(self) -> int:
        return len(self.sisters_ages_at_diagnosis)

    @validator("date_of_birth", pre=True)
    def date_of_birth_age_convert(cls, v) -> date:
        dob = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f%z").date()
        age = age_from_date(dob)
        if not 35 <= age <= 70:
            raise ValueError("Age must be between 35 and 70")

        return dob

    @validator("height")
    def height_range(cls, v) -> float:
        if not 50 <= v <= 250:
            raise ValueError("Height must be between 50cm and 250cm")

        return v

    @validator("weight")
    def weight_range(cls, v) -> float:
        if not 10 <= v <= 700:
            raise ValueError("Weight must be between 10kg and 700kg")

        return v

    @validator("age_at_menarche")
    def check_age_at_menarche(cls, v, values) -> int:
        if not 0 < v < age_from_date(values.get("date_of_birth")):
            raise ValueError("Age at menarche must be between 0 years and current age")
        return v

    @validator("age_at_first_child", pre=True)
    def check_age_at_first_child_null(cls, v) -> Optional[int]:
        if v == "":
            return None

        return int(v)

    @validator("age_at_first_child")
    def check_age_at_first_child_valid(cls, v, values) -> Optional[int]:
        if v is None:
            return v

        if values.get("nulliparous"):
            raise ValueError(
                "Nulliparous (no children) but has value for age at first child"
            )

        if (
            not values.get("age_at_menarche")
            < v
            < age_from_date(values.get("date_of_birth"))
        ):
            raise ValueError(
                "Age at first child must be between age at menarche and current age"
            )

        return v

    @validator("number_of_biopsies", pre=True)
    def check_biopsies_unknown(cls, v) -> BiopsyStatus:
        if v == "":
            return BiopsyStatus.UNKNOWN

        v = int(v)
        if v > 2:
            raise ValueError("Invalid number of biopsies")

        return BiopsyStatus(int(v))

    @validator("biopsies_with_hyperplasia", pre=True)
    def check_hyperplasia_unknown(cls, v) -> HyperplasiaStatus:
        if v == "":
            return HyperplasiaStatus.UNKNOWN

        return HyperplasiaStatus(int(v))

    @validator("biopsies_with_hyperplasia")
    def check_hyperplasia(cls, v, values) -> Optional[int]:
        if v == HyperplasiaStatus.UNKNOWN:
            return v

        if values.get("number_of_biopsies") == BiopsyStatus.UNKNOWN:
            raise ValueError(
                "If number of biopsies is unknown, can't have atypical hyperplasia"
            )

        if (
            values.get("number_of_biopsies") == BiopsyStatus.NONE
            and v == HyperplasiaStatus.SOME
        ):
            raise ValueError("Can't have a biopsy with hyperplasia without a biopsy")

        return v

    @validator("mother_age_at_diagnosis", pre=True)
    def check_mother_diagnosis_null(cls, v) -> Optional[int]:
        if v == "":
            return None

        return int(v)

    @validator("mother_age_at_diagnosis")
    def check_mother_diagnosis(cls, v) -> Optional[int]:
        if v is None:
            return None

        if not 0 < v < 120:
            raise ValueError(
                "Mother's age of breast cancer diagnois should be between 0 and 120"
            )

        return v

    @validator("sisters_ages_at_diagnosis", each_item=True)
    def check_each_sister_age_at_diagnosis(cls, v) -> int:
        if not 0 < v < 120:
            raise ValueError(
                "Sister's age of breast cancer diagnois should be between 0 and 120"
            )

        return v
