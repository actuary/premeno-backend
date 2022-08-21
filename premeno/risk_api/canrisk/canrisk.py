from datetime import datetime, timedelta, timezone
from typing import List, Tuple

from premeno.risk_api.canrisk.file import CanRiskFile
from premeno.risk_api.canrisk.pedigree import Diagnoses, PedigreeEntry, Sex
from premeno.risk_api.canrisk.risk_factors import (
    MhtStatus,
    OralContraceptiveData,
    OralContraStatus,
    RiskFactors,
)


def calculate_child_info(no_children: str, age_at_first_child: str) -> Tuple[int, int]:
    number_of_children = 1 if no_children == "false" else 0
    age = int(age_at_first_child) if no_children == "false" else 0

    return number_of_children, age


def calculate_age_info(date_of_birth: str) -> Tuple[int, int]:
    dob = datetime.strptime(date_of_birth, "%Y-%m-%dT%H:%M:%S.%f%z")
    age = int((datetime.now(timezone.utc) - dob) / timedelta(days=365.2425))
    year_of_birth = dob.year

    return age, year_of_birth


def calculate_oc_data(oc_response: str) -> OralContraceptiveData:
    years_oc = 5
    oc_status = OralContraStatus.Former if oc_response == "y" else OralContraStatus.Never
    return OralContraceptiveData(years_oc, oc_status)


def create_mum(has_cancer: int, age_at_diagnosis: int) -> PedigreeEntry:
    if has_cancer == 1:
        mum = PedigreeEntry("fam", "mum", False, "mum", Sex.Female, 0, 0)
    else:
        mum = PedigreeEntry(
                "fam",
                "mum",
                False,
                "mum",
                sex=Sex.Female,
                age=0,
                year_of_birth=0,
                diagnoses=Diagnoses(breast_cancer_1st_age=age_at_diagnosis))

    return mum


def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    return round(weight_kg / ((height_cm / 100.0) ** 2), 1)


def calculate_alcohol_info(alcohol_units: float) -> float:
    GRAMS_PER_UNIT = 8
    DAYS_PER_WEEK = 7
    return round(alcohol_units * GRAMS_PER_UNIT / DAYS_PER_WEEK)


def calculate_sisters(me: PedigreeEntry, json: dict) -> List[PedigreeEntry]:
    number_of_sisters = int(json["number_of_sisters"])

    sisters = []
    for i in range(number_of_sisters):
        sister = me.sister_with_cancer(i, int(json[f"sister_age_at_diagnosis_{i}"]))
        sisters.append(sister)
    return sisters


def canrisk_file_from_json(json: dict, mht_status: MhtStatus) -> CanRiskFile:
    """Validates past in dictionary (API data) and returns Gail Factors"""

    json = json.copy()

    age, year_of_birth = calculate_age_info(json["date_of_birth"])
    age_at_menarche = int(json["age_at_menarche"])
    height = float(json["height"])
    weight = float(json["weight"])
    bmi = calculate_bmi(height, weight)
    alcohol_grams = calculate_alcohol_info(float(json["alcohol"]))

    if "age_at_first_child" in json:
        number_of_children, age_at_first_child = calculate_child_info(json["no_children"],
                                                                      json["age_at_first_child"])
    else:
        number_of_children, age_at_first_child = calculate_child_info(json["no_children"],
                                                                      "0")

    sisters_with_cancer = int(json["number_of_sisters"])

    sister_diagnosis_ages = []
    for sis_no in range(sisters_with_cancer):
        sister_diagnosis_ages.append(int(json[f"sister_age_at_diagnosis_{sis_no}"]))

    me = PedigreeEntry("fam", "me", True, "me", Sex.Female, age, year_of_birth, "dad", "mum")
    father = PedigreeEntry("fam", "dad", False, "dad", Sex.Male, 0, 0)
    if int(json["mother_has_cancer"]) != 1:
        json["mother_age_at_diagnosis"] = "0"

    mother = create_mum(int(json["mother_has_cancer"]), int(json["mother_age_at_diagnosis"]))

    oc_data = calculate_oc_data(json["oral_contra"])

    risk_factors = RiskFactors(
            age_at_menarche,
            number_of_children,
            age_at_first_child,
            oc_data,
            mht_status,
            round(height),
            bmi,
            alcohol_grams,
            0
    )

    sisters = calculate_sisters(me, json)

    return CanRiskFile(risk_factors, me, father, mother, sisters)
