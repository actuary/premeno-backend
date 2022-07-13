from pytest import approx

import premeno.breast_cancer.bcrat as bc
from premeno.breast_cancer.bcrat import Subject


class TestRecodings:
    def test_recode_N_Biop(self):
        assert Subject(0, 0, 0, 99, 0, 0, 0, 1).no_of_biopsies_cat == 0
        assert Subject(0, 0, 1, 99, 0, 0, 0, 1).no_of_biopsies_cat == 1
        assert Subject(0, 0, 2, 99, 0, 0, 0, 1).no_of_biopsies_cat == 2
        assert Subject(0, 0, 99, 99, 0, 0, 0, 1).no_of_biopsies_cat == 0
        assert Subject(0, 0, 0, 99, 0, 0, 0, 3).no_of_biopsies_cat == 0
        assert Subject(0, 0, 1, 99, 0, 0, 0, 3).no_of_biopsies_cat == 1
        assert Subject(0, 0, 2, 99, 0, 0, 0, 3).no_of_biopsies_cat == 1
        assert Subject(0, 0, 99, 99, 0, 0, 0, 3).no_of_biopsies_cat == 0
        assert Subject(0, 0, 0, 99, 0, 0, 0, 5).no_of_biopsies_cat == 0
        assert Subject(0, 0, 1, 99, 0, 0, 0, 5).no_of_biopsies_cat == 1
        assert Subject(0, 0, 2, 99, 0, 0, 0, 5).no_of_biopsies_cat == 1
        assert Subject(0, 0, 99, 99, 0, 0, 0, 5).no_of_biopsies_cat == 0
        assert Subject(0, 0, 0, 0, 0, 0, 0, 1).no_of_biopsies_cat is None
        assert Subject(0, 0, 1, 0, 0, 0, 0, 1).no_of_biopsies_cat == 1
        assert Subject(0, 0, 2, 0, 0, 0, 0, 1).no_of_biopsies_cat == 2
        assert Subject(0, 0, 99, 0, 0, 0, 0, 1).no_of_biopsies_cat is None
        assert Subject(0, 0, 0, 0, 0, 0, 0, 3).no_of_biopsies_cat == 0
        assert Subject(0, 0, 1, 0, 0, 0, 0, 3).no_of_biopsies_cat == 1
        assert Subject(0, 0, 2, 0, 0, 0, 0, 3).no_of_biopsies_cat == 1
        assert Subject(0, 0, 99, 0, 0, 0, 0, 3).no_of_biopsies_cat == 0
        assert Subject(0, 0, 0, 0, 0, 0, 0, 5).no_of_biopsies_cat == 0
        assert Subject(0, 0, 1, 0, 0, 0, 0, 5).no_of_biopsies_cat == 1
        assert Subject(0, 0, 2, 0, 0, 0, 0, 5).no_of_biopsies_cat == 1
        assert Subject(0, 0, 99, 0, 0, 0, 0, 5).no_of_biopsies_cat == 0
        assert Subject(0, 0, 0, 1, 0, 0, 0, 1).no_of_biopsies_cat is None
        assert Subject(0, 0, 1, 1, 0, 0, 0, 1).no_of_biopsies_cat == 1
        assert Subject(0, 0, 2, 1, 0, 0, 0, 1).no_of_biopsies_cat == 2
        assert Subject(0, 0, 99, 1, 0, 0, 0, 1).no_of_biopsies_cat is None
        assert Subject(0, 0, 0, 1, 0, 0, 0, 3).no_of_biopsies_cat == 0
        assert Subject(0, 0, 1, 1, 0, 0, 0, 3).no_of_biopsies_cat == 1
        assert Subject(0, 0, 2, 1, 0, 0, 0, 3).no_of_biopsies_cat == 1
        assert Subject(0, 0, 99, 1, 0, 0, 0, 3).no_of_biopsies_cat == 0
        assert Subject(0, 0, 0, 1, 0, 0, 0, 5).no_of_biopsies_cat == 0
        assert Subject(0, 0, 1, 1, 0, 0, 0, 5).no_of_biopsies_cat == 1
        assert Subject(0, 0, 2, 1, 0, 0, 0, 5).no_of_biopsies_cat == 1
        assert Subject(0, 0, 99, 1, 0, 0, 0, 5).no_of_biopsies_cat == 0
        assert Subject(0, 0, 0, 2, 0, 0, 0, 1).no_of_biopsies_cat is None
        assert Subject(0, 0, 1, 2, 0, 0, 0, 1).no_of_biopsies_cat is None
        assert Subject(0, 0, 2, 2, 0, 0, 0, 1).no_of_biopsies_cat is None
        assert Subject(0, 0, 99, 2, 0, 0, 0, 1).no_of_biopsies_cat is None
        assert Subject(0, 0, 0, 2, 0, 0, 0, 3).no_of_biopsies_cat == 0
        assert Subject(0, 0, 1, 2, 0, 0, 0, 3).no_of_biopsies_cat is None
        assert Subject(0, 0, 2, 2, 0, 0, 0, 3).no_of_biopsies_cat is None
        assert Subject(0, 0, 99, 2, 0, 0, 0, 3).no_of_biopsies_cat == 0
        assert Subject(0, 0, 0, 2, 0, 0, 0, 5).no_of_biopsies_cat == 0
        assert Subject(0, 0, 1, 2, 0, 0, 0, 5).no_of_biopsies_cat is None
        assert Subject(0, 0, 2, 2, 0, 0, 0, 5).no_of_biopsies_cat is None
        assert Subject(0, 0, 99, 2, 0, 0, 0, 5).no_of_biopsies_cat == 0

    def test_recode_age_men(self):
        assert Subject(12, 0, 0, 0, 7, 0, 0, 1).age_at_menarche_cat == 2
        assert Subject(12, 0, 0, 0, 14, 0, 0, 1).age_at_menarche_cat is None
        assert Subject(12, 0, 0, 0, 12, 0, 0, 1).age_at_menarche_cat == 1
        assert Subject(35, 0, 0, 0, 14, 0, 0, 1).age_at_menarche_cat == 0
        assert Subject(35, 0, 0, 0, 7, 0, 0, 2).age_at_menarche_cat == 1
        assert Subject(35, 0, 0, 0, 12, 0, 0, 2).age_at_menarche_cat == 1
        assert Subject(35, 0, 0, 0, 14, 0, 0, 2).age_at_menarche_cat == 0
        assert Subject(35, 0, 0, 0, 14, 0, 0, 3).age_at_menarche_cat == 0
        assert Subject(35, 0, 0, 0, 7, 0, 0, 3).age_at_menarche_cat == 0
        assert Subject(35, 0, 0, 0, 12, 0, 0, 3).age_at_menarche_cat == 0
        assert Subject(35, 0, 0, 0, 37, 0, 0, 1).age_at_menarche_cat is None
        assert Subject(35, 0, 0, 0, 37, 0, 0, 2).age_at_menarche_cat is None

    def test_recode_age_1st(self):
        assert Subject(35, 0, 0, 0, 7, 19, 0, 1).age_at_first_child_cat == 0
        assert Subject(35, 0, 0, 0, 7, 20, 0, 1).age_at_first_child_cat == 1
        assert Subject(35, 0, 0, 0, 7, 25, 0, 1).age_at_first_child_cat == 2
        assert Subject(41, 0, 0, 0, 7, 40, 0, 1).age_at_first_child_cat == 3
        assert Subject(35, 0, 0, 0, 7, 99, 0, 1).age_at_first_child_cat == 0
        assert Subject(35, 0, 0, 0, 14, 10, 0, 1).age_at_first_child_cat is None
        assert Subject(35, 0, 0, 0, 7, 40, 0, 1).age_at_first_child_cat is None
        assert Subject(35, 0, 0, 0, 99, 40, 0, 1).age_at_first_child_cat is None
        assert Subject(35, 0, 0, 0, 14, 98, 0, 1).age_at_first_child_cat == 2
        assert Subject(35, 0, 0, 0, 14, 99, 0, 1).age_at_first_child_cat == 0
        assert Subject(35, 0, 0, 0, 7, 19, 0, 2).age_at_first_child_cat == 0
        assert Subject(35, 0, 0, 0, 7, 20, 0, 2).age_at_first_child_cat == 0
        assert Subject(35, 0, 0, 0, 7, 25, 0, 2).age_at_first_child_cat == 0
        assert Subject(41, 0, 0, 0, 7, 40, 0, 2).age_at_first_child_cat == 0
        assert Subject(35, 0, 0, 0, 7, 99, 0, 2).age_at_first_child_cat == 0
        assert Subject(35, 0, 0, 0, 14, 10, 0, 2).age_at_first_child_cat == 0
        assert Subject(35, 0, 0, 0, 7, 40, 0, 2).age_at_first_child_cat == 0
        assert Subject(35, 0, 0, 0, 99, 40, 0, 2).age_at_first_child_cat == 0
        assert Subject(35, 0, 0, 0, 14, 98, 0, 2).age_at_first_child_cat == 0
        assert Subject(35, 0, 0, 0, 14, 99, 0, 2).age_at_first_child_cat == 0
        assert Subject(35, 0, 0, 0, 7, 19, 0, 3).age_at_first_child_cat == 0
        assert Subject(35, 0, 0, 0, 7, 20, 0, 3).age_at_first_child_cat == 1
        assert Subject(35, 0, 0, 0, 7, 25, 0, 3).age_at_first_child_cat == 1
        assert Subject(41, 0, 0, 0, 7, 40, 0, 3).age_at_first_child_cat == 2
        assert Subject(35, 0, 0, 0, 7, 99, 0, 3).age_at_first_child_cat == 0
        assert Subject(35, 0, 0, 0, 14, 10, 0, 3).age_at_first_child_cat is None
        assert Subject(35, 0, 0, 0, 7, 40, 0, 3).age_at_first_child_cat is None
        assert Subject(35, 0, 0, 0, 99, 40, 0, 3).age_at_first_child_cat is None
        assert Subject(35, 0, 0, 0, 14, 98, 0, 3).age_at_first_child_cat == 2
        assert Subject(35, 0, 0, 0, 14, 99, 0, 3).age_at_first_child_cat == 0

    def test_recode_N_rel(self):
        assert Subject(0, 0, 0, 0, 0, 0, 0, 1).no_of_relatives_cat == 0
        assert Subject(0, 0, 0, 0, 0, 0, 99, 1).no_of_relatives_cat == 0
        assert Subject(0, 0, 0, 0, 0, 0, 1, 1).no_of_relatives_cat == 1
        assert Subject(0, 0, 0, 0, 0, 0, 2, 1).no_of_relatives_cat == 2
        assert Subject(0, 0, 0, 0, 0, 0, 98, 1).no_of_relatives_cat == 2
        assert Subject(0, 0, 0, 0, 0, 0, 0, 6).no_of_relatives_cat == 0
        assert Subject(0, 0, 0, 0, 0, 0, 0, 3).no_of_relatives_cat == 0
        assert Subject(0, 0, 0, 0, 0, 0, 2, 6).no_of_relatives_cat == 1
        assert Subject(0, 0, 0, 0, 0, 0, 2, 3).no_of_relatives_cat == 1
        assert Subject(0, 0, 0, 0, 0, 0, 98, 6).no_of_relatives_cat == 1
        assert Subject(0, 0, 0, 0, 0, 0, 98, 3).no_of_relatives_cat == 1

    def test_recode_race(self):
        assert Subject(0, 0, 0, 0, 0, 0, 0, 1).race == 1
        assert Subject(0, 0, 0, 0, 0, 0, 0, 3).race == 3
        assert Subject(0, 0, 0, 0, 0, 0, 0, 5).race == 5
        assert Subject(0, 0, 0, 0, 0, 0, 0, 0).race is None
        assert Subject(0, 0, 0, 0, 0, 0, 0, 12).race is None

    def test_get_RR_factor(self):
        assert Subject(0, 0, 0, 0, 0, 0, 0, 0).relative_risk_factor is None
        assert Subject(0, 0, 0, 1, 0, 0, 0, 0).relative_risk_factor is None
        assert Subject(0, 0, 0, 2, 0, 0, 0, 0).relative_risk_factor is None
        assert Subject(0, 0, 0, 99, 0, 0, 0, 0).relative_risk_factor == 1.0
        assert Subject(0, 0, 1, 0, 0, 0, 0, 0).relative_risk_factor == 0.93
        assert Subject(0, 0, 1, 1, 0, 0, 0, 0).relative_risk_factor == 1.82
        assert Subject(0, 0, 1, 2, 0, 0, 0, 0).relative_risk_factor is None
        assert Subject(0, 0, 1, 99, 0, 0, 0, 0).relative_risk_factor == 1.0
        assert Subject(0, 0, 2, 0, 0, 0, 0, 0).relative_risk_factor == 0.93
        assert Subject(0, 0, 2, 1, 0, 0, 0, 0).relative_risk_factor == 1.82
        assert Subject(0, 0, 2, 2, 0, 0, 0, 0).relative_risk_factor is None
        assert Subject(0, 0, 2, 99, 0, 0, 0, 0).relative_risk_factor == 1.0
        assert Subject(0, 0, 0, 0, 0, 0, 0, 3).relative_risk_factor is None
        assert Subject(0, 0, 0, 1, 0, 0, 0, 3).relative_risk_factor is None
        assert Subject(0, 0, 0, 2, 0, 0, 0, 3).relative_risk_factor is None
        assert Subject(0, 0, 0, 99, 0, 0, 0, 3).relative_risk_factor == 1.00
        assert Subject(0, 0, 1, 0, 0, 0, 0, 3).relative_risk_factor == 0.93
        assert Subject(0, 0, 1, 1, 0, 0, 0, 3).relative_risk_factor == 1.82
        assert Subject(0, 0, 1, 2, 0, 0, 0, 3).relative_risk_factor is None
        assert Subject(0, 0, 1, 99, 0, 0, 0, 3).relative_risk_factor == 1.0
        assert Subject(0, 0, 2, 0, 0, 0, 0, 3).relative_risk_factor == 0.93
        assert Subject(0, 0, 2, 1, 0, 0, 0, 3).relative_risk_factor == 1.82
        assert Subject(0, 0, 2, 2, 0, 0, 0, 3).relative_risk_factor is None
        assert Subject(0, 0, 2, 99, 0, 0, 0, 3).relative_risk_factor == 1.0

    def test_recode_age_start(self):
        assert Subject(19, 20, 0, 0, 0, 0, 0, 0).age_start is None
        assert Subject(91, 100, 0, 0, 0, 0, 0, 0).age_start is None
        assert Subject(20, 19, 0, 0, 0, 0, 0, 0).age_start is None
        assert Subject(30, 29, 0, 0, 0, 0, 0, 0).age_start is None
        assert Subject(20, 30, 0, 0, 0, 0, 0, 0).age_start == 20
        assert Subject(41, 42, 0, 0, 0, 0, 0, 0).age_start == 41

    def test_recode_age_end(self):
        assert Subject(19, 20, 0, 0, 0, 0, 0, 0).age_end == 20
        assert Subject(91, 100, 0, 0, 0, 0, 0, 0).age_end is None
        assert Subject(20, 19, 0, 0, 0, 0, 0, 0).age_end is None
        assert Subject(30, 29, 0, 0, 0, 0, 0, 0).age_end is None
        assert Subject(20, 30, 0, 0, 0, 0, 0, 0).age_end == 30
        assert Subject(41, 42, 0, 0, 0, 0, 0, 0).age_end == 42

    def test_is_valid(self):
        assert Subject(19, 20, 0, 99, 7, 99, 0, 1).is_valid() == False
        assert Subject(91, 100, 0, 99, 7, 99, 0, 1).is_valid() == False
        assert Subject(20, 19, 0, 99, 7, 99, 0, 1).is_valid() == False
        assert Subject(30, 29, 0, 99, 7, 99, 0, 1).is_valid() == False
        assert Subject(91, 100, 0, 99, 7, 99, 0, 1).is_valid() == False
        assert Subject(20, 19, 0, 99, 7, 99, 0, 1).is_valid() == False
        assert Subject(30, 29, 0, 99, 7, 99, 0, 1).is_valid() == False
        assert Subject(20, 30, 0, 99, 7, 99, 0, 1).is_valid() == True
        assert Subject(41, 42, 0, 99, 7, 99, 0, 1).is_valid() == True
        assert Subject(20, 30, 0, 99, 7, 99, 0, 1).is_valid() == True
        assert Subject(41, 42, 0, 99, 7, 99, 0, 1).is_valid() == True

    def test_relative_risk(self):
        # ages not relevant here - see exampledata in R code
        assert Subject(45.2, 53.3, 99, 99, 10, 20, 1, 0).relative_risk() is None
        assert Subject(45.2, 53.3, 99, 1, 10, 20, 1, 1).relative_risk() is None
        assert Subject(45.2, 53.3, 99, 0, 10, 20, 1, 2).relative_risk() is None
        assert Subject(45.2, 53.3, 0, 99, 10, 20, 1, 3).relative_risk() == approx(
            (1.48962181812, 1.48962181812)
        )
        assert Subject(45.2, 53.3, 1, 99, 10, 20, 1, 4).relative_risk() == approx(
            (5.49260367150, 4.11796832691)
        )
        assert Subject(45.2, 53.3, 1, 99, 14, 19, 1, 5).relative_risk() == approx(
            (4.00494710984, 4.00494710984)
        )
        assert Subject(45.2, 53.3, 99, 99, 99, 19, 1, 6).relative_risk() == approx(
            (2.20749047181, 2.20749047181)
        )
        assert Subject(45.2, 53.3, 1, 1, 14, 19, 1, 7).relative_risk() == approx(
            (6.98195498172, 6.98195498172)
        )
        assert Subject(45.2, 53.3, 99, 1, 14, 99, 1, 8).relative_risk() is None
        assert Subject(45.2, 53.3, 1, 0, 14, 19, 1, 9).relative_risk() == approx(
            (3.56770227088, 3.56770227088)
        )
        assert Subject(45.2, 53.3, 99, 0, 99, 99, 1, 10).relative_risk() is None
        assert Subject(45.2, 53.3, 0, 0, 14, 19, 1, 11).relative_risk() is None
        assert Subject(45.2, 53.3, 0, 99, 10, 20, 1, 12).relative_risk() is None
        assert Subject(45.2, 53.3, 0, 1, 10, 20, 1, 0).relative_risk() is None
        assert Subject(45.2, 53.3, 0, 0, 10, 20, 1, 1).relative_risk() is None
        assert Subject(45.2, 53.3, 1, 0, 10, 20, 1, 2).relative_risk() == approx(
            (2.34578174168, 2.09735608310)
        )
        assert Subject(35, 40, 4, 99, 11, 25, 0, 3).relative_risk() == approx(
            (1.38946002091, 1.38946002091)
        )
        assert Subject(35, 40, 4, 99, 11, 98, 0, 4).relative_risk() == approx(
            (5.38599137277, 3.02743711995)
        )
        assert Subject(35, 40, 4, 99, 11, 10, 0, 5).relative_risk() is None
        assert Subject(35, 40, 4, 99, 36, 25, 0, 6).relative_risk() is None
        assert Subject(27, 90, 99, 99, 13, 22, 0, 7).relative_risk() == approx(
            (1.42102047642, 1.42102047642)
        )
        assert Subject(27, 90, 99, 99, 13, 22, 99, 8).relative_risk() == approx(
            (1.42102047642, 1.42102047642)
        )
        assert Subject(18, 26, 99, 99, 13, 22, 99, 9).relative_risk() is None
        assert (
            Subject(27, 26, 99, 99, 13, 22, 99, 10).relative_risk() is None
        )  # invalid ages
        assert (
            Subject(85, 91, 99, 99, 13, 22, 99, 11).relative_risk() is None
        )  # invalid ages
        assert (
            Subject(86, 90, 99, 99, 13, 22, 99, 12).relative_risk() is None
        )  # invalid race

    def test_absolute_risk(self):
        assert Subject(45.2, 53.3, 99, 99, 10, 20, 1, 0).absolute_risk() is None
        assert Subject(45.2, 53.3, 99, 1, 10, 20, 1, 1).absolute_risk() is None
        assert Subject(45.2, 53.3, 99, 0, 10, 20, 1, 2).absolute_risk() is None
        assert Subject(45.2, 53.3, 0, 99, 10, 20, 1, 3).absolute_risk() == approx(
            0.018685969
        )
        assert Subject(45.2, 53.3, 1, 99, 10, 20, 1, 4).absolute_risk() == approx(
            0.044412945
        )
        assert Subject(45.2, 53.3, 1, 99, 14, 19, 1, 5).absolute_risk() == approx(
            0.017693563
        )
        assert Subject(45.2, 53.3, 99, 99, 99, 19, 1, 6).absolute_risk() == approx(
            0.012495505
        )
        assert Subject(45.2, 53.3, 1, 1, 14, 19, 1, 7).absolute_risk() == approx(
            0.057756759
        )
        assert Subject(45.2, 53.3, 99, 1, 14, 99, 1, 8).absolute_risk() is None
        assert Subject(45.2, 53.3, 1, 0, 14, 19, 1, 9).absolute_risk() == approx(
            0.039060631
        )
        assert Subject(45.2, 53.3, 99, 0, 99, 99, 1, 10).absolute_risk() is None
        assert Subject(45.2, 53.3, 0, 0, 14, 19, 1, 11).absolute_risk() is None
        assert Subject(45.2, 53.3, 0, 99, 10, 20, 1, 12).absolute_risk() is None
        assert Subject(45.2, 53.3, 0, 1, 10, 20, 1, 0).absolute_risk() is None
        assert Subject(45.2, 53.3, 0, 0, 10, 20, 1, 1).absolute_risk() is None
        assert Subject(45.2, 53.3, 1, 0, 10, 20, 1, 2).absolute_risk() == approx(
            0.026899040
        )
        assert Subject(35, 40, 4, 99, 11, 25, 0, 3).absolute_risk() == approx(
            0.003162827
        )
        assert Subject(35, 40, 4, 99, 11, 98, 0, 4).absolute_risk() == approx(
            0.010229802
        )
        assert Subject(35, 40, 4, 99, 11, 10, 0, 5).absolute_risk() is None
        assert Subject(35, 40, 4, 99, 36, 25, 0, 6).absolute_risk() is None
        assert Subject(27, 90, 99, 99, 13, 22, 0, 7).absolute_risk() == approx(
            0.088276689
        )
        assert Subject(27, 90, 99, 99, 13, 22, 99, 8).absolute_risk() == approx(
            0.067678480
        )
        assert Subject(18, 26, 99, 99, 13, 22, 99, 9).absolute_risk() is None
        assert (
            Subject(27, 26, 99, 99, 13, 22, 99, 10).absolute_risk() is None
        )  # invalid ages
        assert (
            Subject(85, 91, 99, 99, 13, 22, 99, 11).absolute_risk() is None
        )  # invalid ages
        assert (
            Subject(86, 90, 99, 99, 13, 22, 99, 12).absolute_risk() is None
        )  # invalid race
