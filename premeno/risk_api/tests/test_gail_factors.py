from pytest import approx, raises

from premeno.risk_api.gail.errors import FactorError
from premeno.risk_api.gail.factors import (
    GailFactors,
    hyperplasia_relative_risk,
    recode_age_at_first_child,
    recode_age_at_menarche,
    recode_number_of_biopsies,
    recode_number_of_relatives,
)
from premeno.risk_api.gail.race import Race
from premeno.risk_api.questionnaire import BiopsyStatus, HyperplasiaStatus, Questionnaire


class TestGailFactors:
    def test_age(self) -> None:
        with raises(FactorError):
            GailFactors(19, 0, 0, 0, 0, 1, Race.WHITE)

        with raises(FactorError):
            GailFactors(130, 0, 0, 0, 0, 1, Race.WHITE)

        factors = GailFactors(40, 0, 0, 0, 0, 1, Race.WHITE)
        factors.age = 40

    def test_number_of_biopsies(self) -> None:
        with raises(FactorError):
            assert GailFactors(40, 3, 0, 0, 0, 1, Race.WHITE) is None

        factors = GailFactors(40, 2, 0, 0, 0, 1, Race.WHITE)
        factors.number_of_biopsies = 2

    def test_age_at_menarche(self) -> None:
        with raises(FactorError):
            assert GailFactors(40, 0, 3, 0, 0, 1, Race.WHITE) is None

        factors = GailFactors(40, 2, 2, 0, 0, 1, Race.WHITE)
        factors.age_at_menarche = 2

    def test_age_at_first_child(self) -> None:
        with raises(FactorError):
            assert GailFactors(40, 0, 0, 4, 0, 1, Race.WHITE) is None

        factors = GailFactors(40, 2, 2, 3, 0, 1, Race.WHITE)
        factors.age_at_first_child = 3

    def test_number_of_relatives(self) -> None:
        with raises(FactorError):
            GailFactors(40, 0, 0, 0, 3, 1, Race.WHITE)

        factors = GailFactors(40, 2, 2, 3, 2, 1, Race.WHITE)
        factors.number_of_relatives = 2

    def test_relative_risk_factor(self) -> None:
        with raises(FactorError):
            GailFactors(40, 0, 0, 0, 0, 0, Race.WHITE)

        factors = GailFactors(40, 2, 2, 3, 2, 1, Race.WHITE)
        factors.relative_risk_factor = 0

    def test_from_questionnaire(self) -> None:
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
            "questionnaire_date": "2022-08-25",
        }

        questionnaire = Questionnaire(**data)
        factors = GailFactors.from_questionnaire(questionnaire)
        assert factors.age == approx(62.0135937082897)
        assert factors.number_of_biopsies == 0
        assert factors.age_at_menarche == 1
        assert factors.age_at_first_child == 2
        assert factors.number_of_relatives == 0
        assert factors.relative_risk_factor == 1.0


class TestRecodings:
    def test_recode_number_of_biopsies(self) -> None:
        assert recode_number_of_biopsies(BiopsyStatus.NONE, Race.WHITE) == 0
        assert recode_number_of_biopsies(BiopsyStatus.ONE, Race.WHITE) == 1
        assert (
            recode_number_of_biopsies(BiopsyStatus.ONE, Race.HISPANIC_AMERICAN_US) == 1
        )
        assert (
            recode_number_of_biopsies(BiopsyStatus.MULTIPLE, Race.HISPANIC_AMERICAN_US)
            == 1
        )
        assert recode_number_of_biopsies(BiopsyStatus.MULTIPLE, Race.WHITE) == 2

    def test_recode_age_at_menarche(self) -> None:
        assert recode_age_at_menarche(7, Race.WHITE) == 2
        assert recode_age_at_menarche(12, Race.WHITE) == 1
        assert recode_age_at_menarche(14, Race.WHITE) == 0
        assert recode_age_at_menarche(7, Race.AFRICAN_AMERICAN) == 1
        assert recode_age_at_menarche(12, Race.AFRICAN_AMERICAN) == 1
        assert recode_age_at_menarche(14, Race.AFRICAN_AMERICAN) == 0
        assert recode_age_at_menarche(14, Race.HISPANIC_AMERICAN_US) == 0
        assert recode_age_at_menarche(7, Race.HISPANIC_AMERICAN_US) == 0
        assert recode_age_at_menarche(12, Race.HISPANIC_AMERICAN_US) == 0

    def test_recode_age_at_first_child(self):
        assert recode_age_at_first_child(False, 19, Race.WHITE) == 0
        assert recode_age_at_first_child(False, 20, Race.WHITE) == 1
        assert recode_age_at_first_child(False, 25, Race.WHITE) == 2
        assert recode_age_at_first_child(False, 40, Race.WHITE) == 3
        assert recode_age_at_first_child(False, None, Race.WHITE) == 0
        assert recode_age_at_first_child(True, None, Race.WHITE) == 2
        assert recode_age_at_first_child(False, None, Race.WHITE) == 0
        assert recode_age_at_first_child(False, 19, Race.AFRICAN_AMERICAN) == 0
        assert recode_age_at_first_child(False, 20, Race.AFRICAN_AMERICAN) == 0
        assert recode_age_at_first_child(False, 25, Race.AFRICAN_AMERICAN) == 0
        assert recode_age_at_first_child(False, 40, Race.AFRICAN_AMERICAN) == 0
        assert recode_age_at_first_child(False, None, Race.AFRICAN_AMERICAN) == 0
        assert recode_age_at_first_child(False, 10, Race.AFRICAN_AMERICAN) == 0
        assert recode_age_at_first_child(False, 40, Race.AFRICAN_AMERICAN) == 0
        assert recode_age_at_first_child(False, 40, Race.AFRICAN_AMERICAN) == 0
        assert recode_age_at_first_child(True, None, Race.AFRICAN_AMERICAN) == 0
        assert recode_age_at_first_child(False, None, Race.AFRICAN_AMERICAN) == 0
        assert recode_age_at_first_child(False, 19, Race.HISPANIC_AMERICAN_US) == 0
        assert recode_age_at_first_child(False, 20, Race.HISPANIC_AMERICAN_US) == 1
        assert recode_age_at_first_child(False, 25, Race.HISPANIC_AMERICAN_US) == 1
        assert recode_age_at_first_child(False, 40, Race.HISPANIC_AMERICAN_US) == 2
        assert recode_age_at_first_child(False, None, Race.HISPANIC_AMERICAN_US) == 0
        assert recode_age_at_first_child(True, None, Race.HISPANIC_AMERICAN_US) == 2
        assert recode_age_at_first_child(False, None, Race.HISPANIC_AMERICAN_US) == 0

    def test_recode_number_of_relatives(self):
        assert recode_number_of_relatives(0, Race.WHITE) == 0
        assert recode_number_of_relatives(1, Race.WHITE) == 1
        assert recode_number_of_relatives(2, Race.WHITE) == 2
        assert recode_number_of_relatives(3, Race.WHITE) == 2
        assert recode_number_of_relatives(0, Race.CHINESE) == 0
        assert recode_number_of_relatives(0, Race.HISPANIC_AMERICAN_US) == 0
        assert recode_number_of_relatives(2, Race.CHINESE) == 1
        assert recode_number_of_relatives(2, Race.HISPANIC_AMERICAN_US) == 1
        assert recode_number_of_relatives(3, Race.CHINESE) == 1
        assert recode_number_of_relatives(3, Race.HISPANIC_AMERICAN_US) == 1

    def test_relative_risk_factor(self):
        assert (
            hyperplasia_relative_risk(
                BiopsyStatus.NONE, HyperplasiaStatus.UNKNOWN, Race.WHITE
            )
            == 1.0
        )
        assert (
            hyperplasia_relative_risk(
                BiopsyStatus.ONE, HyperplasiaStatus.NONE, Race.WHITE
            )
            == 0.93
        )
        assert (
            hyperplasia_relative_risk(
                BiopsyStatus.ONE, HyperplasiaStatus.SOME, Race.WHITE
            )
            == 1.82
        )
        assert (
            hyperplasia_relative_risk(
                BiopsyStatus.ONE, HyperplasiaStatus.UNKNOWN, Race.WHITE
            )
            == 1.0
        )
        assert (
            hyperplasia_relative_risk(
                BiopsyStatus.MULTIPLE, HyperplasiaStatus.NONE, Race.WHITE
            )
            == 0.93
        )
        assert (
            hyperplasia_relative_risk(
                BiopsyStatus.MULTIPLE, HyperplasiaStatus.SOME, Race.WHITE
            )
            == 1.82
        )
        assert (
            hyperplasia_relative_risk(
                BiopsyStatus.MULTIPLE, HyperplasiaStatus.UNKNOWN, Race.WHITE
            )
            == 1.0
        )
        assert (
            hyperplasia_relative_risk(
                BiopsyStatus.NONE, HyperplasiaStatus.UNKNOWN, Race.HISPANIC_AMERICAN_US
            )
            == 1.00
        )
        assert (
            hyperplasia_relative_risk(
                BiopsyStatus.ONE, HyperplasiaStatus.NONE, Race.HISPANIC_AMERICAN_US
            )
            == 0.93
        )
        assert (
            hyperplasia_relative_risk(
                BiopsyStatus.ONE, HyperplasiaStatus.SOME, Race.HISPANIC_AMERICAN_US
            )
            == 1.82
        )
        assert (
            hyperplasia_relative_risk(
                BiopsyStatus.ONE, HyperplasiaStatus.UNKNOWN, Race.HISPANIC_AMERICAN_US
            )
            == 1.0
        )
        assert (
            hyperplasia_relative_risk(
                BiopsyStatus.MULTIPLE, HyperplasiaStatus.NONE, Race.HISPANIC_AMERICAN_US
            )
            == 0.93
        )
        assert (
            hyperplasia_relative_risk(
                BiopsyStatus.MULTIPLE, HyperplasiaStatus.SOME, Race.HISPANIC_AMERICAN_US
            )
            == 1.82
        )
        assert (
            hyperplasia_relative_risk(
                BiopsyStatus.MULTIPLE,
                HyperplasiaStatus.UNKNOWN,
                Race.HISPANIC_AMERICAN_US,
            )
            == 1.0
        )
