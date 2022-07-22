from pytest import approx, raises

import premeno.breast_cancer.bcrat as bc
from premeno.breast_cancer.bcrat import GailModel, bucket


class TestBuckets:
    def test_buckets(self):
        assert bucket(5, {1: 1, 3: 2, 5: 3}) == 3
        assert bucket(2, {1: 1, 3: 2, 5: 3}) == 1
        assert bucket(6, {1: 1, 3: 2, 5: 3}) == 3

        assert bucket(0, {1: 1, 3: 2, 5: 3}) is None


class TestRecodings:
    def test_recode_N_Biop(self):
        assert bc.recode_no_of_biopsies(0, 99, 1) == 0
        assert bc.recode_no_of_biopsies(1, 99, 1) == 1
        assert bc.recode_no_of_biopsies(2, 99, 1) == 2
        assert bc.recode_no_of_biopsies(99, 99, 1) == 0
        assert bc.recode_no_of_biopsies(0, 99, 3) == 0
        assert bc.recode_no_of_biopsies(1, 99, 3) == 1
        assert bc.recode_no_of_biopsies(2, 99, 3) == 1
        assert bc.recode_no_of_biopsies(99, 99, 3) == 0
        assert bc.recode_no_of_biopsies(0, 99, 5) == 0
        assert bc.recode_no_of_biopsies(1, 99, 5) == 1
        assert bc.recode_no_of_biopsies(2, 99, 5) == 1
        assert bc.recode_no_of_biopsies(99, 99, 5) == 0
        assert bc.recode_no_of_biopsies(1, 0, 1) == 1
        assert bc.recode_no_of_biopsies(2, 0, 1) == 2
        assert bc.recode_no_of_biopsies(0, 0, 3) == 0
        assert bc.recode_no_of_biopsies(1, 0, 3) == 1
        assert bc.recode_no_of_biopsies(2, 0, 3) == 1
        assert bc.recode_no_of_biopsies(99, 0, 3) == 0
        assert bc.recode_no_of_biopsies(0, 0, 5) == 0
        assert bc.recode_no_of_biopsies(1, 0, 5) == 1
        assert bc.recode_no_of_biopsies(2, 0, 5) == 1
        assert bc.recode_no_of_biopsies(99, 0, 5) == 0
        assert bc.recode_no_of_biopsies(1, 1, 1) == 1
        assert bc.recode_no_of_biopsies(2, 1, 1) == 2
        assert bc.recode_no_of_biopsies(0, 1, 3) == 0
        assert bc.recode_no_of_biopsies(1, 1, 3) == 1
        assert bc.recode_no_of_biopsies(2, 1, 3) == 1
        assert bc.recode_no_of_biopsies(99, 1, 3) == 0
        assert bc.recode_no_of_biopsies(0, 1, 5) == 0
        assert bc.recode_no_of_biopsies(1, 1, 5) == 1
        assert bc.recode_no_of_biopsies(2, 1, 5) == 1
        assert bc.recode_no_of_biopsies(99, 1, 5) == 0
        assert bc.recode_no_of_biopsies(0, 2, 3) == 0
        assert bc.recode_no_of_biopsies(99, 2, 3) == 0
        assert bc.recode_no_of_biopsies(0, 2, 5) == 0
        assert bc.recode_no_of_biopsies(99, 2, 5) == 0

        with raises(bc.RecodingError):
            assert bc.recode_no_of_biopsies(99, 0, 1) is None
            assert bc.recode_no_of_biopsies(0, 0, 1) is None
            assert bc.recode_no_of_biopsies(0, 1, 1) is None
            assert bc.recode_no_of_biopsies(99, 1, 1) is None
            assert bc.recode_no_of_biopsies(0, 2, 1) is None
            assert bc.recode_no_of_biopsies(1, 2, 1) is None
            assert bc.recode_no_of_biopsies(2, 2, 1) is None
            assert bc.recode_no_of_biopsies(99, 2, 1) is None
            assert bc.recode_no_of_biopsies(1, 2, 3) is None
            assert bc.recode_no_of_biopsies(2, 2, 3) is None
            assert bc.recode_no_of_biopsies(1, 2, 5) is None
            assert bc.recode_no_of_biopsies(2, 2, 5) is None

    def test_recode_age_men(self):
        assert bc.recode_age_at_menarche(7, 12, 1) == 2
        assert bc.recode_age_at_menarche(12, 12, 1) == 1
        assert bc.recode_age_at_menarche(14, 35, 1) == 0
        assert bc.recode_age_at_menarche(7, 35, 2) == 1
        assert bc.recode_age_at_menarche(12, 35, 2) == 1
        assert bc.recode_age_at_menarche(14, 35, 2) == 0
        assert bc.recode_age_at_menarche(14, 35, 3) == 0
        assert bc.recode_age_at_menarche(7, 35, 3) == 0
        assert bc.recode_age_at_menarche(12, 35, 3) == 0

        with raises(bc.RecodingError):
            assert bc.recode_age_at_menarche(37, 35, 1) is None
            assert bc.recode_age_at_menarche(37, 35, 2) is None
            assert bc.recode_age_at_menarche(14, 12, 1) is None

    def test_recode_age_1st(self):
        assert bc.recode_age_at_first_child(19, 35, 7, 1) == 0
        assert bc.recode_age_at_first_child(20, 35, 7, 1) == 1
        assert bc.recode_age_at_first_child(25, 35, 7, 1) == 2
        assert bc.recode_age_at_first_child(40, 41, 7, 1) == 3
        assert bc.recode_age_at_first_child(99, 35, 7, 1) == 0
        assert bc.recode_age_at_first_child(98, 35, 14, 1) == 2
        assert bc.recode_age_at_first_child(99, 35, 14, 1) == 0
        assert bc.recode_age_at_first_child(19, 35, 7, 2) == 0
        assert bc.recode_age_at_first_child(20, 35, 7, 2) == 0
        assert bc.recode_age_at_first_child(25, 35, 7, 2) == 0
        assert bc.recode_age_at_first_child(40, 41, 7, 2) == 0
        assert bc.recode_age_at_first_child(99, 35, 7, 2) == 0
        assert bc.recode_age_at_first_child(10, 35, 14, 2) == 0
        assert bc.recode_age_at_first_child(40, 35, 7, 2) == 0
        assert bc.recode_age_at_first_child(40, 35, 99, 2) == 0
        assert bc.recode_age_at_first_child(98, 35, 14, 2) == 0
        assert bc.recode_age_at_first_child(99, 35, 14, 2) == 0
        assert bc.recode_age_at_first_child(19, 35, 7, 3) == 0
        assert bc.recode_age_at_first_child(20, 35, 7, 3) == 1
        assert bc.recode_age_at_first_child(25, 35, 7, 3) == 1
        assert bc.recode_age_at_first_child(40, 41, 7, 3) == 2
        assert bc.recode_age_at_first_child(99, 35, 7, 3) == 0
        assert bc.recode_age_at_first_child(98, 35, 14, 3) == 2
        assert bc.recode_age_at_first_child(99, 35, 14, 3) == 0

        with raises(bc.RecodingError):
            assert bc.recode_age_at_first_child(10, 35, 14, 1) is None
            assert bc.recode_age_at_first_child(40, 35, 7, 1) is None
            assert bc.recode_age_at_first_child(40, 35, 99, 1) is None
            assert bc.recode_age_at_first_child(10, 35, 14, 3) is None
            assert bc.recode_age_at_first_child(40, 35, 7, 3) is None
            assert bc.recode_age_at_first_child(40, 35, 99, 3) is None

    def test_recode_N_rel(self):
        assert bc.recode_no_of_relatives(0, 1) == 0
        assert bc.recode_no_of_relatives(99, 1) == 0
        assert bc.recode_no_of_relatives(1, 1) == 1
        assert bc.recode_no_of_relatives(2, 1) == 2
        assert bc.recode_no_of_relatives(98, 1) == 2
        assert bc.recode_no_of_relatives(0, 6) == 0
        assert bc.recode_no_of_relatives(0, 3) == 0
        assert bc.recode_no_of_relatives(2, 6) == 1
        assert bc.recode_no_of_relatives(2, 3) == 1
        assert bc.recode_no_of_relatives(98, 6) == 1
        assert bc.recode_no_of_relatives(98, 3) == 1

    def test_recode_race(self):
        assert bc.recode_race(1) == 1
        assert bc.recode_race(3) == 3
        assert bc.recode_race(5) == 5

        with raises(bc.RecodingError):
            assert bc.recode_race(0) is None
            assert bc.recode_race(12) is None

    def test_get_RR_factor(self):
        assert bc.relative_risk_factor(0, 99, 0) == 1.0
        assert bc.relative_risk_factor(1, 0, 0) == 0.93
        assert bc.relative_risk_factor(1, 1, 0) == 1.82
        assert bc.relative_risk_factor(1, 99, 0) == 1.0
        assert bc.relative_risk_factor(2, 0, 0) == 0.93
        assert bc.relative_risk_factor(2, 1, 0) == 1.82
        assert bc.relative_risk_factor(2, 99, 0) == 1.0
        assert bc.relative_risk_factor(0, 99, 3) == 1.00
        assert bc.relative_risk_factor(1, 0, 3) == 0.93
        assert bc.relative_risk_factor(1, 1, 3) == 1.82
        assert bc.relative_risk_factor(1, 99, 3) == 1.0
        assert bc.relative_risk_factor(2, 0, 3) == 0.93
        assert bc.relative_risk_factor(2, 1, 3) == 1.82
        assert bc.relative_risk_factor(2, 99, 3) == 1.0

        with raises(bc.RecodingError):
            assert bc.relative_risk_factor(0, 0, 0) is None
            assert bc.relative_risk_factor(0, 1, 0) is None
            assert bc.relative_risk_factor(0, 2, 0) is None
            assert bc.relative_risk_factor(1, 2, 0) is None
            assert bc.relative_risk_factor(2, 2, 0) is None
            assert bc.relative_risk_factor(0, 0, 3) is None
            assert bc.relative_risk_factor(0, 1, 3) is None
            assert bc.relative_risk_factor(0, 2, 3) is None
            assert bc.relative_risk_factor(1, 2, 3) is None
            assert bc.relative_risk_factor(2, 2, 3) is None

    def test_recode_age_start(self):
        assert bc.recode_age(20) == 20
        assert bc.recode_age(41) == 41

        with raises(bc.RecodingError):
            assert bc.recode_age(19) is None
            assert bc.recode_age(91) is None

    def test_recode_age_end(self):
        assert bc.recode_age_end(19, 20) == 20
        assert bc.recode_age_end(20, 30) == 30
        assert bc.recode_age_end(41, 42) == 42

        with raises(bc.RecodingError):
            assert bc.recode_age_end(91, 100) is None
            assert bc.recode_age_end(20, 19) is None
            assert bc.recode_age_end(30, 29) is None

    def test_relative_risk(self):
        # ages not relevant here - see exampledata in R code

        assert GailModel(
            bc.recode_data_for_gail(45.2, 0, 99, 10, 20, 1, 3)
        ).relative_risk() == approx((1.48962181812, 1.48962181812))
        assert GailModel(
            bc.recode_data_for_gail(45.2, 1, 99, 10, 20, 1, 4)
        ).relative_risk() == approx((5.49260367150, 4.11796832691))
        assert GailModel(
            bc.recode_data_for_gail(45.2, 1, 99, 14, 19, 1, 5)
        ).relative_risk() == approx((4.00494710984, 4.00494710984))
        assert GailModel(
            bc.recode_data_for_gail(45.2, 99, 99, 99, 19, 1, 6)
        ).relative_risk() == approx((2.20749047181, 2.20749047181))
        assert GailModel(
            bc.recode_data_for_gail(45.2, 1, 1, 14, 19, 1, 7)
        ).relative_risk() == approx((6.98195498172, 6.98195498172))
        assert GailModel(
            bc.recode_data_for_gail(45.2, 1, 0, 14, 19, 1, 9)
        ).relative_risk() == approx((3.56770227088, 3.56770227088))
        assert GailModel(
            bc.recode_data_for_gail(45.2, 1, 0, 10, 20, 1, 2)
        ).relative_risk() == approx((2.34578174168, 2.09735608310))
        assert GailModel(
            bc.recode_data_for_gail(35, 4, 99, 11, 25, 0, 3)
        ).relative_risk() == approx((1.38946002091, 1.38946002091))
        assert GailModel(
            bc.recode_data_for_gail(35, 4, 99, 11, 98, 0, 4)
        ).relative_risk() == approx((5.38599137277, 3.02743711995))
        assert GailModel(
            bc.recode_data_for_gail(27, 99, 99, 13, 22, 0, 7)
        ).relative_risk() == approx((1.42102047642, 1.42102047642))
        assert GailModel(
            bc.recode_data_for_gail(27, 99, 99, 13, 22, 99, 8)
        ).relative_risk() == approx((1.42102047642, 1.42102047642))

        with raises(bc.RecodingError):
            assert (
                GailModel(
                    bc.recode_data_for_gail(45.2, 99, 99, 10, 20, 1, 0)
                ).relative_risk()
                is None
            )
            assert (
                GailModel(
                    bc.recode_data_for_gail(45.2, 99, 1, 10, 20, 1, 1)
                ).relative_risk()
                is None
            )
            assert (
                GailModel(
                    bc.recode_data_for_gail(45.2, 99, 0, 10, 20, 1, 2)
                ).relative_risk()
                is None
            )
            assert (
                GailModel(
                    bc.recode_data_for_gail(45.2, 99, 1, 14, 99, 1, 8)
                ).relative_risk()
                is None
            )
            assert (
                GailModel(
                    bc.recode_data_for_gail(45.2, 99, 0, 99, 99, 1, 10)
                ).relative_risk()
                is None
            )
            assert (
                GailModel(
                    bc.recode_data_for_gail(45.2, 0, 0, 14, 19, 1, 11)
                ).relative_risk()
                is None
            )
            assert (
                GailModel(
                    bc.recode_data_for_gail(45.2, 0, 99, 10, 20, 1, 12)
                ).relative_risk()
                is None
            )
            assert (
                GailModel(
                    bc.recode_data_for_gail(45.2, 0, 1, 10, 20, 1, 0)
                ).relative_risk()
                is None
            )
            assert (
                GailModel(
                    bc.recode_data_for_gail(45.2, 0, 0, 10, 20, 1, 1)
                ).relative_risk()
                is None
            )
            assert (
                GailModel(
                    bc.recode_data_for_gail(35, 4, 99, 11, 10, 0, 5)
                ).relative_risk()
                is None
            )
            assert (
                GailModel(
                    bc.recode_data_for_gail(35, 4, 99, 36, 25, 0, 6)
                ).relative_risk()
                is None
            )
            assert (
                GailModel(
                    bc.recode_data_for_gail(18, 99, 99, 13, 22, 99, 9)
                ).relative_risk()
                is None
            )
            assert (
                GailModel(
                    bc.recode_data_for_gail(27, 99, 99, 13, 22, 99, 10)
                ).relative_risk()
                is None
            )  # invalid ages
            assert (
                GailModel(
                    bc.recode_data_for_gail(85, 99, 99, 13, 22, 99, 11)
                ).relative_risk()
                is None
            )  # invalid ages
            assert (
                GailModel(
                    bc.recode_data_for_gail(86, 99, 99, 13, 22, 99, 12)
                ).relative_risk()
                is None
            )  # invalid race

    def test_absolute_risk(self):
        assert GailModel(bc.recode_data_for_gail(45.2, 0, 99, 10, 20, 1, 3)).predict(
            8.1
        ) == approx(0.018685969)
        assert GailModel(bc.recode_data_for_gail(45.2, 1, 99, 10, 20, 1, 4)).predict(
            8.1
        ) == approx(0.044412945)
        assert GailModel(bc.recode_data_for_gail(45.2, 1, 99, 14, 19, 1, 5)).predict(
            8.1
        ) == approx(0.017693563)
        assert GailModel(bc.recode_data_for_gail(45.2, 99, 99, 99, 19, 1, 6)).predict(
            8.1
        ) == approx(0.012495505)
        assert GailModel(bc.recode_data_for_gail(45.2, 1, 1, 14, 19, 1, 7)).predict(
            8.1
        ) == approx(0.057756759)
        assert GailModel(bc.recode_data_for_gail(45.2, 1, 0, 14, 19, 1, 9)).predict(
            8.1
        ) == approx(0.039060631)
        assert GailModel(bc.recode_data_for_gail(45.2, 1, 0, 10, 20, 1, 2)).predict(
            8.1
        ) == approx(0.026899040)
        assert GailModel(bc.recode_data_for_gail(35, 4, 99, 11, 25, 0, 3)).predict(
            5
        ) == approx(0.003162827)
        assert GailModel(bc.recode_data_for_gail(35, 4, 99, 11, 98, 0, 4)).predict(
            5
        ) == approx(0.010229802)
        assert GailModel(bc.recode_data_for_gail(27, 99, 99, 13, 22, 0, 7)).predict(
            63
        ) == approx(0.088276689)
        assert GailModel(bc.recode_data_for_gail(27, 99, 99, 13, 22, 99, 8)).predict(
            63
        ) == approx(0.067678480)

        with raises(bc.RecodingError):
            assert (
                GailModel(bc.recode_data_for_gail(45.2, 99, 99, 10, 20, 1, 0)).predict(
                    8.1
                )
                is None
            )
            assert (
                GailModel(bc.recode_data_for_gail(45.2, 99, 1, 10, 20, 1, 1)).predict(
                    8.1
                )
                is None
            )
            assert (
                GailModel(bc.recode_data_for_gail(45.2, 99, 0, 10, 20, 1, 2)).predict(
                    8.1
                )
                is None
            )
            assert (
                GailModel(bc.recode_data_for_gail(45.2, 99, 1, 14, 99, 1, 8)).predict(
                    8.1
                )
                is None
            )
            assert (
                GailModel(bc.recode_data_for_gail(45.2, 99, 0, 99, 99, 1, 10)).predict(
                    8.1
                )
                is None
            )
            assert (
                GailModel(bc.recode_data_for_gail(45.2, 0, 0, 14, 19, 1, 11)).predict(
                    8.1
                )
                is None
            )
            assert (
                GailModel(bc.recode_data_for_gail(45.2, 0, 99, 10, 20, 1, 12)).predict(
                    8.1
                )
                is None
            )
            assert (
                GailModel(bc.recode_data_for_gail(45.2, 0, 1, 10, 20, 1, 0)).predict(
                    8.1
                )
                is None
            )
            assert (
                GailModel(bc.recode_data_for_gail(45.2, 0, 0, 10, 20, 1, 1)).predict(
                    8.1
                )
                is None
            )
            assert (
                GailModel(bc.recode_data_for_gail(35, 4, 99, 11, 10, 0, 5)).predict(5)
                is None
            )
            assert (
                GailModel(bc.recode_data_for_gail(35, 4, 99, 36, 25, 0, 6)).predict(5)
                is None
            )
            assert (
                GailModel(bc.recode_data_for_gail(18, 99, 99, 13, 22, 99, 9)).predict(8)
                is None
            )
            assert (
                GailModel(bc.recode_data_for_gail(27, 99, 99, 13, 22, 99, 10)).predict(
                    -1
                )
                is None
            )  # invalid ages
            assert (
                GailModel(bc.recode_data_for_gail(85, 99, 99, 13, 22, 99, 11)).predict(
                    6
                )
                is None
            )  # invalid ages
            assert (
                GailModel(bc.recode_data_for_gail(86, 99, 99, 13, 22, 99, 12)).predict(
                    4
                )
                is None
            )  # invalid race
