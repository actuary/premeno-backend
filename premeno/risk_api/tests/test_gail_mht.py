from premeno.risk_api.gail.mht import collab_relative_risk
from premeno.risk_api.questionnaire import MhtType


class TestMht:
    def test_mht_relative_risk(self) -> None:
        assert collab_relative_risk(MhtType.NONE) == 1.0
        assert collab_relative_risk(MhtType.OESTROGEN) == 1.3
        assert collab_relative_risk(MhtType.COMBINED) == 2.0
