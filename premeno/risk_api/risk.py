import abc
from enum import Enum
from typing import Optional

from django.conf import settings

from premeno.risk_api.canrisk.api import CanRiskAPI
from premeno.risk_api.canrisk.file import create_canrisk_file
from premeno.risk_api.canrisk.risk_factors import MhtStatus
from premeno.risk_api.canrisk.utils import extract_cancer_rates, interpolate_rate
from premeno.risk_api.gail.factors import GailFactors
from premeno.risk_api.gail.mht import collab_relative_risk
from premeno.risk_api.gail.model import GailModel
from premeno.risk_api.questionnaire import MhtType, Questionnaire


class PredictionError(Exception):
    """Thrown when something unexpected happens with predictions"""


class Risk(Enum):
    """Types of risk predictions produced by the API"""

    BREAST_CANCER = "breast_cancer"
    FRACTURE_RISK = "fracture_risk"
    VTE = "venous_thromboembolism"
    CVD = "cvd"


RISK_TO_NICE_NAME = {
    Risk.BREAST_CANCER: "Breast Cancer Risk",
    Risk.FRACTURE_RISK: "Fracture Risk",
    Risk.VTE: "Venous Thromboembolism Risk",
    Risk.CVD: "Cardiovascular Risk",
}

MHT_TO_STATUS = {
    MhtType.NONE: MhtStatus.Never,
    MhtType.OESTROGEN: MhtStatus.Oestrogen,
    MhtType.COMBINED: MhtStatus.Combined,
}


class RiskCalc(metaclass=abc.ABCMeta):
    """Abstract RiskCalc class - subclass to define an adapter that the API will use"""

    @property
    @classmethod
    @abc.abstractmethod
    def risk(cls) -> Risk:
        pass  # pragma: no cover

    @property
    @classmethod
    @abc.abstractmethod
    def name(cls) -> str:
        pass  # pragma: no cover

    @abc.abstractmethod
    def predict_mht_type(self, data: Questionnaire, proj_years: int, mht_type: MhtType) -> float:
        pass  # pragma: no cover

    def predict(self, data: Questionnaire, proj_years: int) -> dict[MhtType, Optional[float]]:
        results = {}
        for mht_type in MhtType:
            try:
                results.update({mht_type.value: self.predict_mht_type(data, proj_years, mht_type)})
            except Exception as err:
                results.update({mht_type.value: None})
                print(f"Prediction Error for {self.name} model: {err}")

        return results


class CanRiskCalc(RiskCalc):
    """Adapter for CanRisk API model"""

    risk: Risk = Risk.BREAST_CANCER
    name: str = "CanRisk"

    def predict_mht_type(self, data: Questionnaire, proj_years: int, mht_type: MhtType) -> float:
        api = CanRiskAPI(settings.CANRISK_API_USERNAME, settings.CANRISK_API_PASSWORD)
        canrisk_file = create_canrisk_file(data, MHT_TO_STATUS[mht_type])
        rates = extract_cancer_rates(api.boadicea(str(canrisk_file)))

        return interpolate_rate(rates["age"], rates["individual"], int(data.age) + proj_years)


class GailRiskCalc(RiskCalc):
    """Adapter for Gail model"""

    risk: Risk = Risk.BREAST_CANCER
    name: str = "Gail"

    def predict_mht_type(self, data: Questionnaire, proj_years: int, mht_type: MhtType) -> float:
        gail = GailModel(GailFactors.from_questionnaire(data))
        mht_rel_risk = collab_relative_risk(mht_type)
        return gail.predict(proj_years) * mht_rel_risk


class FakeCalc(RiskCalc):
    """Fake calc for testing purposes"""

    risk: Risk = Risk.BREAST_CANCER
    name: str = "Fakeo"

    def predict_mht_type(self, data: Questionnaire, proj_years: int, mht_type: MhtType) -> float:
        return {
            MhtType.NONE: 0.05,
            MhtType.OESTROGEN: 0.04,
            MhtType.COMBINED: 0.04,
        }[mht_type]


def risk_predictions(data: Questionnaire, proj_years: int) -> dict:
    """Makes all risk predictions based on the questionnaire data"""
    models = {
        Risk.BREAST_CANCER: CanRiskCalc,
    }

    results = {}
    for risk in models:
        model = models[risk]()
        results[risk.value] = model.predict(data, proj_years)

    return results
