import abc

from django.conf import settings

from premeno.risk_api.canrisk.api import CanRisk
from premeno.risk_api.canrisk.file import create_canrisk_file
from premeno.risk_api.canrisk.risk_factors import MhtStatus
from premeno.risk_api.canrisk.utils import extract_cancer_rates
from premeno.risk_api.gail.factors import GailFactors
from premeno.risk_api.gail.mht import collab_relative_risk
from premeno.risk_api.gail.model import GailModel
from premeno.risk_api.questionnaire import MhtFormulation, Questionnaire


class PredictionError(Exception):
    """Thrown when something unexpected happens with predictions"""


class Prediction:
    """Stores risk model predictions from start age + 1 year"""

    def __init__(
        self, formulation: MhtFormulation, start_age: int, values: list[float]
    ) -> None:
        self.formulation = formulation
        self.start_age = start_age
        self.values = values

    def at_age(self, age: int) -> float:
        if age == self.start_age:
            return 0

        if self.start_age > age or age > 80:
            raise PredictionError("Prediction age out of range.")

        if age - self.start_age > len(self.values):
            raise PredictionError("Can't predict out that far.")

        return self.values[age - self.start_age - 1]


class RiskModel(metaclass=abc.ABCMeta):
    def __init__(self, data: Questionnaire) -> None:
        self.data = data

    @abc.abstractmethod
    def predict(self, formulation: MhtFormulation) -> Prediction:
        pass

    def predict_all(self) -> dict[MhtFormulation, Prediction]:
        return {
            formulation: self.predict(formulation) for formulation in MhtFormulation
        }


class Model(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def background_risk(self, years: int):
        pass

    @abc.abstractmethod
    def relative_risk(self, years: int):
        pass


class BreastCancer(Model):
    def __init__(self, data: Questionnaire):
        self.gail = GailModel(GailFactors.from_questionnaire(data))
        self.mht = collab_relative_risk(data.mht)

    def background_risk(self, years: int):
        return self.gail.predict(years)

    def relative_risk(self, years: int):
        return self.mht


MHT_TO_STATUS = {
    MhtFormulation.NONE: MhtStatus.Never,
    MhtFormulation.OESTROGEN: MhtStatus.Oestrogen,
    MhtFormulation.COMBINED: MhtStatus.Combined,
}


class CanRiskModel(Model):
    def __init__(self, data: Questionnaire):
        canrisk_file_no_mht = create_canrisk_file(data, MhtStatus.Never)
        canrisk_file_with_mht = create_canrisk_file(data, MHT_TO_STATUS[data.mht])

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
