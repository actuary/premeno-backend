from premeno.risk_api.canrisk.risk_factors import (
    MhtStatus,
    OralContraceptiveData,
    OralContraStatus,
    RiskFactors,
)


class TestRiskFactors:
    def test_oral_contraceptive_data_default(self) -> None:
        assert str(OralContraceptiveData(5)) == "N"

    def test_oral_contraceptive_data(self) -> None:
        assert str(OralContraceptiveData(5, OralContraStatus.Never)) == "N"
        assert str(OralContraceptiveData(5, OralContraStatus.Former)) == "F:5"
        assert str(OralContraceptiveData(5, OralContraStatus.Current)) == "C:5"

    def test_risk_factors_header(self) -> None:
        rf = RiskFactors(
            age_at_menarche=13,
            number_of_children=0,
            age_at_first_live_birth=None,
            oral_contraceptive_use=OralContraceptiveData(5),
            mht_use=MhtStatus.Former,
            height_cm=170,
            bmi=21.4,
            alcohol_grams=80,
            age_at_menopause=0,
        )

        assert rf.make_header() == (
            "##menarche=13\n"
            "##oc_use=N\n"
            "##mht_use=F\n"
            "##BMI=21.4\n"
            "##alcohol=80\n"
            "##height=170\n"
        )

        rf = RiskFactors(
            age_at_menarche=13,
            number_of_children=1,
            age_at_first_live_birth=26,
            oral_contraceptive_use=OralContraceptiveData(5, OralContraStatus.Former),
            mht_use=MhtStatus.Former,
            height_cm=170,
            bmi=21.4,
            alcohol_grams=80,
            age_at_menopause=56,
        )

        assert rf.make_header() == (
            "##menarche=13\n"
            "##parity=1\n"
            "##First_live_birth=26\n"
            "##oc_use=F:5\n"
            "##mht_use=F\n"
            "##BMI=21.4\n"
            "##alcohol=80\n"
            "##menopause=56\n"
            "##height=170\n"
        )
