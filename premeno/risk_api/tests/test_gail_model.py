from pytest import approx

from premeno.risk_api.gail.factors import GailFactors
from premeno.risk_api.gail.model import GailModel, age_factor
from premeno.risk_api.gail.race import Race


class TestModel:
    def test_age_fac(self):
        assert age_factor(49) == 0
        assert age_factor(50) == 0
        assert age_factor(51) == 1

    def test_relative_risk_example_data(self):
        # see exampledata in BCRAT R code - only non errors
        # ages only matter if above / below 50

        factors = GailFactors(45.2, 0, 0, 1, 1, 1.0, Race.HISPANIC_AMERICAN_US)
        assert GailModel(factors).relative_risk(45.2) == approx(1.48962181812)
        assert GailModel(factors).relative_risk(56) == approx(1.48962181812)

        factors = GailFactors(45.2, 1, 2, 1, 1, 1.0, Race.WHITE_OTHER)
        assert GailModel(factors).relative_risk(45.2) == approx(5.49260367150)
        assert GailModel(factors).relative_risk(56) == approx(4.11796832691)

        factors = GailFactors(45.2, 1, 0, 0, 1, 1.0, Race.HISPANIC_AMERICAN_FOREIGN)
        assert GailModel(factors).relative_risk(45.2) == approx(4.00494710984)
        assert GailModel(factors).relative_risk(56) == approx(4.00494710984)

        factors = GailFactors(45.2, 0, 0, 0, 1, 1.0, Race.CHINESE)
        assert GailModel(factors).relative_risk(45.2) == approx(2.20749047181)
        assert GailModel(factors).relative_risk(56) == approx(2.20749047181)

        factors = GailFactors(45.2, 1, 0, 0, 1, 1.82, Race.JAPANESE)
        assert GailModel(factors).relative_risk(45.2) == approx(6.98195498172)
        assert GailModel(factors).relative_risk(56) == approx(6.98195498172)

        factors = GailFactors(45.2, 1, 0, 0, 1, 0.93, Race.HAWAIIAN)
        assert GailModel(factors).relative_risk(45.2) == approx(3.56770227088)
        assert GailModel(factors).relative_risk(56) == approx(3.56770227088)

        factors = GailFactors(45.2, 1, 1, 0, 1, 0.93, Race.AFRICAN_AMERICAN)
        assert GailModel(factors).relative_risk(45.2) == approx(2.34578174168)
        assert GailModel(factors).relative_risk(56) == approx(2.09735608310)

        factors = GailFactors(35, 1, 2, 1, 0, 1.0, Race.HISPANIC_AMERICAN_US)
        assert GailModel(factors).relative_risk(35) == approx(1.38946002091)
        assert GailModel(factors).relative_risk(56) == approx(1.38946002091)

        factors = GailFactors(35, 2, 2, 2, 0, 1.0, Race.WHITE_OTHER)
        assert GailModel(factors).relative_risk(35) == approx(5.38599137277)
        assert GailModel(factors).relative_risk(56) == approx(3.02743711995)

        factors = GailFactors(27, 0, 1, 1, 0, 1.0, Race.JAPANESE)
        assert GailModel(factors).relative_risk(27) == approx(1.42102047642)
        assert GailModel(factors).relative_risk(56) == approx(1.42102047642)

        factors = GailFactors(27, 0, 1, 1, 0, 1.0, Race.FILIPINO)
        assert GailModel(factors).relative_risk(27) == approx(1.42102047642)
        assert GailModel(factors).relative_risk(56) == approx(1.42102047642)

    def test_absolute_risk_example_data(self):

        factors = GailFactors(45.2, 0, 0, 1, 1, 1.0, Race.HISPANIC_AMERICAN_US)
        assert GailModel(factors).predict(8.1) == approx(0.018685969)

        factors = GailFactors(45.2, 1, 2, 1, 1, 1.0, Race.WHITE_OTHER)
        assert GailModel(factors).predict(8.1) == approx(0.044412945)

        factors = GailFactors(45.2, 1, 0, 0, 1, 1.0, Race.HISPANIC_AMERICAN_FOREIGN)
        assert GailModel(factors).predict(8.1) == approx(0.017693563)

        factors = GailFactors(45.2, 0, 0, 0, 1, 1.0, Race.CHINESE)
        assert GailModel(factors).predict(8.1) == approx(0.012495505)

        factors = GailFactors(45.2, 1, 0, 0, 1, 0.93, Race.HAWAIIAN)
        assert GailModel(factors).predict(8.1) == approx(0.039060631)

        factors = GailFactors(45.2, 1, 0, 0, 1, 1.82, Race.JAPANESE)
        assert GailModel(factors).predict(8.1) == approx(0.057756759)

        factors = GailFactors(45.2, 1, 1, 0, 1, 0.93, Race.AFRICAN_AMERICAN)
        assert GailModel(factors).predict(8.1) == approx(0.026899040)

        factors = GailFactors(35, 1, 2, 1, 0, 1.0, Race.HISPANIC_AMERICAN_US)
        assert GailModel(factors).predict(5) == approx(0.003162827)

        factors = GailFactors(35, 2, 2, 2, 0, 1.0, Race.WHITE_OTHER)
        assert GailModel(factors).predict(5) == approx(0.010229802)

        factors = GailFactors(27, 0, 1, 1, 0, 1.0, Race.JAPANESE)
        assert GailModel(factors).predict(63) == approx(0.088276689)

        factors = GailFactors(27, 0, 1, 1, 0, 1.0, Race.FILIPINO)
        assert GailModel(factors).predict(63) == approx(0.067678480)

    def test_absolute_risk_one_interval(self):
        factors = GailFactors(45.2, 0, 0, 1, 1, 1.0, Race.HISPANIC_AMERICAN_US)
        assert GailModel(factors).predict(0.8) == approx(0.00169613151)
