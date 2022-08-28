from premeno.risk_api.questionnaire import MhtType


def collab_relative_risk(mht_type: MhtType) -> float:
    """
    Calculates relative risk of taking MHT,
    using collaborative group paper results.
    Doesn't seem to differ by most risk factors to keeping constant
    and only depending on formulation.
    """

    factors = {
        MhtType.NONE: 1,
        MhtType.OESTROGEN: 1.3,
        MhtType.COMBINED: 2.0,
    }

    return factors[mht_type]
