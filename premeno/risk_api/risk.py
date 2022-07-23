import abc

from premeno.risk_api.gail import GailModel, gail_from_json
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
