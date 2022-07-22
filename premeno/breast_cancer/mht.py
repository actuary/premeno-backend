from datetime import datetime, timedelta, timezone
from enum import Enum


class MhtType(Enum):
    OESTROGEN_ONLY = 0
    OESTROGEN_PROGESTAGEN = 1


FEET_TO_CM = 30.48
LBS_TO_KG = 1.0 / 2.205

relative_risks = {
    "age_at_menopause": {
        0: [0.95, 1.71],  # <55 years
        1: [1.31, 2.04],  # 55-64 years
        2: [1.35, 2.19],  # 65+ years
    },
    "bmi": {
        0: [1.49, 2.32],  # <25 kg/m2
        1: [1.25, 1.92],  # 25-29 kg/m2
        2: [1.14, 1.71],  # 30+ kg/m2
    },
    "family_history": {
        0: [1.31, 2.02],  # No
        1: [1.35, 2.11],  # Yes
    },
    "ethnic_group": {
        0: [1.32, 2.08],  # White
        1: [1.39, 2.13],  # Other
    },
    "education": {
        0: [1.28, 2.05],  # <13 years
        1: [1.35, 2.03],  # 13+ years
    },
    "height": {
        0: [1.32, 2.10],  # <165 cm
        1: [1.34, 2.03],  # 165+ cm
    },
    "age_at_menarche": {
        0: [1.27, 2.03],  # <13 years
        1: [1.35, 2.07],  # 13+ years
    },
    "parity": {
        0: [1.42, 2.23],  # Nulliparous
        1: [1.28, 2.04],  # Parous
    },
    "age_at_first_child": {
        0: [1.31, 2.02],  # <25 years
        1: [1.32, 2.03],  # 25+ years
    },
    "oral_contraceptive": {
        0: [1.28, 2.11],  # Never used
        1: [1.34, 2.01],  # Ever used
    },
    "alcohol": {
        0: [1.3, 2.04],  # <10 g/week
        1: [1.3, 2.11],  # 10+ g/week
    },
    "smoking": {
        0: [1.32, 2.08],  # Never
        1: [1.32, 2.04],  # Ever
    },
}


class SubjectMHT:
    def __init__(self, json):
        self.raw_data = json
        self.age_start = (
            datetime.now(timezone.utc)
            - datetime.strptime(json["date_of_birth"], "%Y-%m-%dT%H:%M:%S.%f%z")
        ) / timedelta(days=365.2425)
        self.age_at_menopause_cat = 0

        height = 0
        if json["height_unit"] == "cm":
            height = float(json["height"])
        elif json["height_unit"] == "ft":
            height = (
                float(json["height_ft"]) + float(json["height_in"]) / 12.0
            ) * FEET_TO_CM
        else:
            raise ValueError("Height must be given in cm or ft/inches")

        weight = 0
        if json["weight_unit"] == "kg":
            weight = float(json["weight"])
        elif json["weight_unit"] == "lbs":
            weight = float(json["weight"]) * LBS_TO_KG
        else:
            raise ValueError("Weight must be in given in lbs or kg")

        self.bmi_cat = self.recode_bmi(height, weight)
        self.no_of_relatives_cat = self.recode_no_of_relatives(
            int(json["family_history"])
        )
        self.ethnic_group_cat = self.recode_ethnic_group(json["ethnic_group"])
        self.education_cat = self.recode_education(json["education"])
        self.height_cat = self.recode_height(int(json["height"]))
        self.age_at_menarche = self.recode_age_at_menarche(int(json["age_at_menarche"]))
        self.age_at_first_child_cat = self.recode_age_at_first_child(
            int(json["age_at_first_child"])
        )
        self.oral_contraceptive_cat = self.recode_oral_contraceptive(
            json["oral_contra"]
        )
        self.alcohol_cat = self.recode_alcohol(int(json["alcohol"]))
        self.smoking_cat = self.recode_smoking(json["smoking"])

    def recode_age_at_menopause(self, time_since_last_period):
        age = self.age_start - time_since_last_period / 12.0
        if age < 55:
            return 0
        elif age < 65:
            return 1
        elif age < 90:
            return 2
        else:
            return -1

    def recode_bmi(self, height: float, weight: float) -> int:
        bmi = weight / (height**2)

        if bmi < 25:
            return 0
        elif bmi < 35:
            return 1
        else:
            return 2

    def recode_ethnic_group(self, ethnic_group: str) -> int:
        return 0 if ethnic_group == "white" else 1

    def recode_no_of_relatives(self, no_of_relatives: int) -> int:
        return 0 if no_of_relatives == 0 else 1

    def recode_education(self, education: str) -> int:
        if education == "":
            pass
        elif education == "":
            pass
        elif education == "":
            pass

        elif education == "":
            pass
        else:
            self.yrs_of_education = -1

        return 0 if self.yrs_of_education < 13 else 1

    def recode_height(self, height: int) -> int:
        return 0 if height < 165 else 1

    def recode_age_at_menarche(self, age_at_menarche: int) -> int:
        return 0 if age_at_menarche < 13 else 1

    def recode_age_at_first_child(self, age_at_first_child: int) -> int:
        return 0 if age_at_first_child < 25 else 1

    def recode_oral_contraceptive(self, oral_contraceptive: bool) -> int:
        return 1 if oral_contraceptive == "y" else 0

    def recode_alcohol(self, units_per_week: int) -> int:
        return 0 if units_per_week < 10 else 1

    def recode_smoking(self, smoking: bool) -> int:
        return 0 if not smoking else 1

    def relative_risk(self, type_of_mht: MhtType) -> float:
        if type_of_mht == MhtType.OESTROGEN_ONLY:
            return 1.3
        elif type_of_mht == MhtType.OESTROGEN_PROGESTAGEN:
            return 2
