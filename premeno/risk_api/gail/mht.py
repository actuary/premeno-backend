from premeno.risk_api.questionnaire import MhtFormulation


def collab_relative_risk(mht_type: MhtFormulation) -> float:
    """
    Calculates relative risk of taking MHT,
    using collaborative group paper results.
    Doesn't seem to differ by most risk factors to keeping constant
    and only depending on formulation
    """

    factors = {
        MhtFormulation.NONE: 1,
        MhtFormulation.OESTROGEN: 1.3,
        MhtFormulation.COMBINED: 2.0,
    }

    return factors[mht_type]
