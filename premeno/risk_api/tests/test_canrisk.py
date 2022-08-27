from premeno.risk_api.canrisk.risk_factors import (
    OralContraceptiveData,
    OralContraStatus,
)


class TestRiskFactors:
    def test_oral_contraceptive_data_default(self) -> None:
        assert str(OralContraceptiveData(5)) == "N"

    def test_oral_contraceptive_data(self) -> None:
        assert str(OralContraceptiveData(5, OralContraStatus.Never)) == "N"
        assert str(OralContraceptiveData(5, OralContraStatus.Former)) == "F:5"
        assert str(OralContraceptiveData(5, OralContraStatus.Current)) == "C:5"
