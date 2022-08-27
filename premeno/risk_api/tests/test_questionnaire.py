from datetime import date

from pydantic import ValidationError
from pytest import approx, raises

from premeno.risk_api.questionnaire import (
    BiopsyStatus,
    HyperplasiaStatus,
    Questionnaire,
    age_from_date,
)


class TestQuestionnaire:
    data = {
        "date_of_birth": "1960-08-20T16:48:50.823Z",
        "height": "170.4",
        "weight": "70.34",
        "ethnic_group": "white",
        "education": "primary",
        "alcohol_use": "0",
        "smoking": "never",
        "mht": "e",
        "age_at_menarche": "13",
        "nulliparous": True,
        "age_at_first_child": "",
        "oral_contraception_use": "n",
        "number_of_biopsies": "",
        "biopsies_with_hyperplasia": "",
        "mother_age_at_diagnosis": "",
        "sisters_ages_at_diagnosis": [],
    }

    def test_invalid_dob(self) -> None:
        data = self.data.copy()

        questionnaire = Questionnaire(**data)
        assert questionnaire.date_of_birth == date(1960, 8, 20)

        data["date_of_birth"] = "1990-08-20T16:48:50.823Z"
        with raises(ValidationError):
            Questionnaire(**data)

        data["date_of_birth"] = "1900-08-20T16:48:50.823Z"
        with raises(ValidationError):
            Questionnaire(**data)

    def test_bad_date(self) -> None:
        """Expects datetime format with time zone"""
        data = self.data.copy()

        data["date_of_birth"] = "1960-08-20"
        with raises(ValidationError):
            Questionnaire(**data)

        data["date_of_birth"] = "1960-08-20T16:48:50.823"
        with raises(ValidationError):
            Questionnaire(**data)

    def test_year_of_birth(self) -> None:
        data = self.data.copy()

        questionnaire = Questionnaire(**data)
        assert questionnaire.year_of_birth == 1960

    def test_age_from_date(self) -> None:
        assert age_from_date(date(1960, 8, 20), date(2022, 8, 20)) == approx(
            22645 / 365.2425
        )

    def test_age(self) -> None:
        data = self.data.copy()

        data["questionnaire_date"] = "2022-08-20"

        questionnaire = Questionnaire(**data)
        assert questionnaire.age == approx(22645 / 365.2425)

    def test_invalid_height(self) -> None:
        data = self.data.copy()

        questionnaire = Questionnaire(**data)
        assert questionnaire.height == approx(170.4)

        data["height"] = "30.3"
        with raises(ValidationError):
            Questionnaire(**data)

        data["height"] = "300.65"
        with raises(ValidationError):
            Questionnaire(**data)

    def test_invalid_weight(self) -> None:
        data = self.data.copy()

        questionnaire = Questionnaire(**data)
        assert questionnaire.weight == approx(70.34)

        data["weight"] = "9.3"
        with raises(ValidationError):
            Questionnaire(**data)

        data["weight"] = "710.65"
        with raises(ValidationError):
            Questionnaire(**data)

    def test_age_at_menarche(self) -> None:
        data = self.data.copy()

        data["age_at_menarche"] = "13"
        questionnaire = Questionnaire(**data)
        assert questionnaire.age_at_menarche == 13

        data["age_at_menarche"] = "-1"
        with raises(ValidationError):
            Questionnaire(**data)

        data["age_at_menarche"] = "80"
        with raises(ValidationError):
            Questionnaire(**data)

    def test_age_at_first_child(self) -> None:
        data = self.data.copy()

        questionnaire = Questionnaire(**data)
        assert questionnaire.age_at_first_child is None

        data["nulliparous"] = True
        data["age_at_first_child"] = "26"
        with raises(ValidationError):
            Questionnaire(**data)

        data["nulliparous"] = False
        data["age_at_first_child"] = "26"
        questionnaire = Questionnaire(**data)
        assert questionnaire.age_at_first_child == 26

        data["age_at_first_child"] = "-1"
        with raises(ValidationError):
            Questionnaire(**data)

        data["age_at_first_child"] = "12"
        with raises(ValidationError):
            Questionnaire(**data)

        data["age_at_first_child"] = "80"
        with raises(ValidationError):
            Questionnaire(**data)

    def test_number_of_biopsies(self) -> None:
        data = self.data.copy()

        questionnaire = Questionnaire(**data)
        assert questionnaire.number_of_biopsies == BiopsyStatus.UNKNOWN

        data["number_of_biopsies"] = "0"
        questionnaire = Questionnaire(**data)
        assert questionnaire.number_of_biopsies == BiopsyStatus.NONE

        data["number_of_biopsies"] = "1"
        questionnaire = Questionnaire(**data)
        assert questionnaire.number_of_biopsies == BiopsyStatus.ONE

        data["number_of_biopsies"] = "-1"
        with raises(ValidationError):
            Questionnaire(**data)

        data["number_of_biopsies"] = "3"
        with raises(ValidationError):
            Questionnaire(**data)

        data["number_of_biopsies"] = "2"
        questionnaire = Questionnaire(**data)
        assert questionnaire.number_of_biopsies == BiopsyStatus.MULTIPLE

    def test_hyperplasia(self) -> None:
        data = self.data.copy()

        data["number_of_biopsies"] = ""
        data["biopsies_with_hyperplasia"] = ""
        questionnaire = Questionnaire(**data)
        assert questionnaire.biopsies_with_hyperplasia == HyperplasiaStatus.UNKNOWN

        data["number_of_biopsies"] = "0"
        data["biopsies_with_hyperplasia"] = "0"
        questionnaire = Questionnaire(**data)
        assert questionnaire.biopsies_with_hyperplasia == HyperplasiaStatus.NONE

        data["number_of_biopsies"] = ""
        data["biopsies_with_hyperplasia"] = "0"
        with raises(ValidationError):
            Questionnaire(**data)

        data["biopsies_with_hyperplasia"] = "-1"
        with raises(ValidationError):
            Questionnaire(**data)

        data["biopsies_with_hyperplasia"] = "2"
        with raises(ValidationError):
            Questionnaire(**data)

        data["number_of_biopsies"] = "1"
        data["biopsies_with_hyperplasia"] = "1"
        questionnaire = Questionnaire(**data)
        assert questionnaire.biopsies_with_hyperplasia == HyperplasiaStatus.SOME

        data["number_of_biopsies"] = "0"
        data["biopsies_with_hyperplasia"] = "1"
        with raises(ValidationError):
            Questionnaire(**data)

    def test_mother_age_at_diagnosis(self) -> None:
        data = self.data.copy()

        data["mother_age_at_diagnosis"] = ""
        questionnaire = Questionnaire(**data)
        assert questionnaire.mother_age_at_diagnosis is None

        data["mother_age_at_diagnosis"] = "56"
        questionnaire = Questionnaire(**data)
        assert questionnaire.mother_age_at_diagnosis == 56

        data["mother_age_at_diagnosis"] = "-1"
        with raises(ValidationError):
            Questionnaire(**data)

        data["mother_age_at_diagnosis"] = "200"
        with raises(ValidationError):
            Questionnaire(**data)

    def test_sister_ages_at_diagnosis(self) -> None:
        data = self.data.copy()

        data["sisters_ages_at_diagnosis"] = []
        questionnaire = Questionnaire(**data)
        assert questionnaire.number_of_sisters_with_cancer == 0

        data["sisters_ages_at_diagnosis"] = ["56"]
        questionnaire = Questionnaire(**data)
        assert questionnaire.number_of_sisters_with_cancer == 1
        assert questionnaire.sisters_ages_at_diagnosis[0] == 56

        data["sisters_ages_at_diagnosis"] = ["56", "34"]
        questionnaire = Questionnaire(**data)
        assert questionnaire.number_of_sisters_with_cancer == 2
        assert questionnaire.sisters_ages_at_diagnosis[0] == 56
        assert questionnaire.sisters_ages_at_diagnosis[1] == 34

        data["sisters_ages_at_diagnosis"] = ["56", "-1"]
        with raises(ValidationError):
            Questionnaire(**data)

        data["sisters_ages_at_diagnosis"] = ["56", "151"]
        with raises(ValidationError):
            Questionnaire(**data)

    def test_number_of_relatives_with_cancer(self) -> None:
        data = self.data.copy()

        data["mother_age_at_diagnosis"] = ""
        data["sisters_ages_at_diagnosis"] = []
        questionnaire = Questionnaire(**data)
        assert questionnaire.number_of_relatives_with_cancer == 0

        data["mother_age_at_diagnosis"] = "56"
        questionnaire = Questionnaire(**data)
        assert questionnaire.number_of_relatives_with_cancer == 1

        data["mother_age_at_diagnosis"] = "56"
        data["sisters_ages_at_diagnosis"] = ["56", "56", "56"]
        questionnaire = Questionnaire(**data)
        assert questionnaire.number_of_relatives_with_cancer == 4
