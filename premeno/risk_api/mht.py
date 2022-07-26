from enum import Enum


class MhtType(Enum):
    """ """

    OESTROGEN_ONLY = 0
    OESTROGEN_PROGESTAGEN = 1


class MhtRisk:
    """
    Calculates relative risk of taking MHT,
    using collaborative group paper results
    """

    def __init__(self, json):
        self.raw_data = json

        if "mht" not in json:
            raise KeyError("MHT formulation not chosen in request!")

        self.mht_type = (
            MhtType.OESTROGEN_ONLY
            if json["mht"] == "e"
            else MhtType.OESTROGEN_PROGESTAGEN
        )

    def relative_risk(self) -> float:
        if self.mht_type == MhtType.OESTROGEN_ONLY:
            return 1.3
        elif self.mht_type == MhtType.OESTROGEN_PROGESTAGEN:
            return 2
        else:
            raise RuntimeError("Invalid MHT formulation")
