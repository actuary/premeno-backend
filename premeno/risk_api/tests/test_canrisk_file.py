from unittest.mock import patch

from premeno.risk_api.canrisk.file import CanRiskFile, create_canrisk_file, make_family
from premeno.risk_api.canrisk.pedigree import PedigreeEntry, Sex
from premeno.risk_api.canrisk.risk_factors import MhtStatus, OralContraceptiveData, RiskFactors
from premeno.risk_api.canrisk.utils import header_line
from premeno.risk_api.questionnaire import Questionnaire


class TestCanRiskFile:
    TEST_MOTHER = PedigreeEntry("a", False, "a", Sex.Female, 80, 2040)
    TEST_FATHER = PedigreeEntry("b", False, "b", Sex.Male, 80, 2040)
    TEST_PEDIGREE = PedigreeEntry("e", True, "e", Sex.Female, 56, 2060, "a", "b")
    TEST_HUSBAND = PedigreeEntry("NA", True, "husb", Sex.Male, 0, 0)
    TEST_CHILD = PedigreeEntry("f", False, "f", Sex.Female, 80, 2040)
    TEST_SISTERS = [
        PedigreeEntry("c", False, "c", Sex.Female, 54, 2062),
        PedigreeEntry("d", False, "d", Sex.Female, 55, 2061),
    ]

    @patch("premeno.risk_api.canrisk.pedigree.PedigreeEntry.calculate_sisters")
    @patch("premeno.risk_api.canrisk.pedigree.PedigreeEntry.child")
    @patch("premeno.risk_api.canrisk.pedigree.PedigreeEntry.husband")
    @patch("premeno.risk_api.canrisk.pedigree.PedigreeEntry.father")
    @patch("premeno.risk_api.canrisk.pedigree.PedigreeEntry.mother")
    def test_make_family(self, mother_fn, father_fn, husband_fn, child_fn, sisters_fn) -> None:
        mother_fn.return_value = self.TEST_MOTHER
        father_fn.return_value = self.TEST_FATHER
        husband_fn.return_value = self.TEST_HUSBAND
        child_fn.return_value = self.TEST_CHILD
        sisters_fn.return_value = self.TEST_SISTERS

        family = make_family(self.TEST_PEDIGREE, 26, 56, [54, 55])

        mother_fn.assert_called_with(56)
        father_fn.assert_called_once()
        husband_fn.assert_called_once()
        child_fn.assert_called_with(26, 1)
        sisters_fn.assert_called_with([54, 55])

        assert len(family) == 7

    def test_canrisk_file(self) -> None:
        rf = RiskFactors(13, 1, 26, OralContraceptiveData(5), MhtStatus.Never, 170, 21.4, 80, 56)
        pedigrees = [self.TEST_PEDIGREE, self.TEST_MOTHER, self.TEST_FATHER]
        pedigree_file = "\n".join([str(person) for person in pedigrees])
        file = CanRiskFile(rf, pedigrees)
        assert str(file) == (
            "##CanRisk 2.0\n"
            f"{rf.make_header()}"
            f"{header_line(PedigreeEntry.header(), None)}\n"
            f"{pedigree_file}"
        )

    def test_create_canrisk_file(self) -> None:
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
        questionnaire = Questionnaire(**data)
        mht = MhtStatus.Never
        risk_factors = RiskFactors(13, 0, None, OralContraceptiveData(5), mht, 170, 24.2, 0, 0)
        family = make_family(
            PedigreeEntry("me", True, "me", Sex.Female, 62, 1960, "dad", "mum"),
            None,
            None,
            [],
        )

        assert create_canrisk_file(questionnaire, mht) == CanRiskFile(risk_factors, family)
