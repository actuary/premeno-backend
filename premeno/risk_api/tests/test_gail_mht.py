from premeno.risk_api.gail.mht import collab_relative_risk
from premeno.risk_api.questionnaire import MhtFormulation


class TestMht:
    def test_mht_relative_risk(self) -> None:
        assert collab_relative_risk(MhtFormulation.NONE) == 1.0
        assert collab_relative_risk(MhtFormulation.OESTROGEN) == 1.3
        assert collab_relative_risk(MhtFormulation.COMBINED) == 2.0
