import abc

from django.conf import settings

from premeno.risk_api.canrisk.api import CanRisk
from premeno.risk_api.canrisk.canrisk import canrisk_file_from_json
from premeno.risk_api.canrisk.risk_factors import MhtStatus
from premeno.risk_api.canrisk.utils import extract_cancer_rates
from premeno.risk_api.gail.gail import GailModel, gail_from_json
from premeno.risk_api.mht import MhtRisk


class RiskModel(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def background_risk(self, years: int):
        pass

    @abc.abstractmethod
    def relative_risk(self, years: int):
        pass


class BreastCancer(RiskModel):
    def __init__(self, json: dict):
        self.gail = GailModel(gail_from_json(json))
        self.mht = MhtRisk(json)

    def background_risk(self, years: int):
        return self.gail.predict(years)

    def relative_risk(self, years: int):
        return self.mht.relative_risk()


class CanRiskModel(RiskModel):
    def __init__(self, json: dict):
        canrisk_file_no_mht = canrisk_file_from_json(json, MhtStatus.Never)
        mht_type = MhtStatus.Combined if json["mht"] == "e+p" else MhtStatus.Oestrogen

        canrisk_file_with_mht = canrisk_file_from_json(json, mht_type)

        api = CanRisk(
            username=settings.CANRISK_API_USERNAME,
            password=settings.CANRISK_API_PASSWORD,
        )
        self.results_no_mht = extract_cancer_rates(
            api.boadicea(str(canrisk_file_no_mht))
        )
        self.results_with_mht = extract_cancer_rates(
            api.boadicea(str(canrisk_file_with_mht))
        )

    def background_risk(self, years: int):
        return self.results_no_mht["individual"][4]

    def relative_risk(self, years: int):
        return self.results_with_mht["individual"][4] / self.background_risk(5)
