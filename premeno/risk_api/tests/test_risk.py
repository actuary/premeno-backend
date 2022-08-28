from unittest.mock import MagicMock, patch

from pytest import approx

from premeno.risk_api.questionnaire import MhtType
from premeno.risk_api.risk import (
    CanRiskCalc,
    FakeCalc,
    GailRiskCalc,
    Risk,
    RiskCalc,
    risk_predictions,
)


class TestRiskModels:
    @patch("premeno.risk_api.risk.Questionnaire")
    def test_fake_model(self, mock_q) -> None:
        mock_q = MagicMock()
        assert FakeCalc().predict_mht_type(mock_q, 5, MhtType.NONE) == approx(0.05)
        pass

    @patch("premeno.risk_api.risk.Questionnaire")
    @patch("premeno.risk_api.risk.extract_cancer_rates")
    @patch("premeno.risk_api.risk.create_canrisk_file")
    @patch("premeno.risk_api.risk.CanRiskAPI")
    def test_canrisk_calc(self, mock_api, mock_ccf, mock_ecr, mock_q) -> None:
        mock_q = MagicMock()
        mock_q.age = 46
        mock_ccf.return_value = "FakeFile"
        mock_api = MagicMock()
        mock_api.boadicea.return_value = {}
        mock_ecr.return_value = {"age": [50, 51, 52], "individual": [0.1, 0.2, 0.3]}

        assert CanRiskCalc().predict_mht_type(mock_q, 5, MhtType.NONE) == 0.2

    @patch("premeno.risk_api.risk.Questionnaire")
    @patch("premeno.risk_api.risk.collab_relative_risk")
    @patch("premeno.risk_api.risk.GailFactors.from_questionnaire")
    @patch("premeno.risk_api.risk.GailModel.predict")
    def test_gail_calc(self, mock_gail, mock_fac, mock_collab, mock_q) -> None:
        mock_gail.return_value = 0.05

        mock_q = MagicMock()
        mock_fac.return_value = mock_q

        mock_collab.return_value = 2

        model = GailRiskCalc()
        assert mock_gail.predict.called_once_with(5)
        assert model.predict_mht_type(mock_q, 5, MhtType.NONE) == approx(0.1)

    @patch("premeno.risk_api.risk.Questionnaire")
    @patch("premeno.risk_api.risk.CanRiskCalc")
    def test_risk_predictions(self, mock, mock_data) -> None:
        fake_results = {"none": 0.5, "e": 0.2, "e+p": 0.3}
        mock().predict.return_value = fake_results
        mock_data = MagicMock()

        assert risk_predictions(mock_data, 5) == {"breast_cancer": fake_results}

    @patch("premeno.risk_api.risk.Questionnaire")
    def test_risk_calc_predict(self, mock) -> None:
        class FakerCalc(RiskCalc):
            risk: Risk = Risk.BREAST_CANCER
            name: str = "FAKER"

            def predict_mht_type(self, data, proj_years, mht_type) -> float:
                del data, proj_years, mht_type
                return 0.1

        faker = FakerCalc()
        assert faker.predict(mock, 5) == {"none": 0.1, "e": 0.1, "e+p": 0.1}

    @patch("premeno.risk_api.risk.Questionnaire")
    def test_risk_calc_predict_error(self, mock) -> None:
        class FakerCalc(RiskCalc):
            risk: Risk = Risk.BREAST_CANCER
            name: str = "FAKER"

            def predict_mht_type(self, data, proj_years, mht_type) -> float:
                del data, proj_years, mht_type
                raise Exception("BIG OL EXCEPTION")

        faker = FakerCalc()
        assert faker.predict(mock, 5) == {"none": None, "e": None, "e+p": None}
