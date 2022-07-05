import pytest

import premeno.breast_cancer.bcrat as bc


class TestRecodings:
    def test_recode_N_Biop(self):
        assert bc.recode_number_of_biopsies(0, 99, 1) == 0
        assert bc.recode_number_of_biopsies(1, 99, 1) == 1
        assert bc.recode_number_of_biopsies(2, 99, 1) == 2
        assert bc.recode_number_of_biopsies(99, 99, 1) == 0
        assert bc.recode_number_of_biopsies(0, 99, 3) == 0
        assert bc.recode_number_of_biopsies(1, 99, 3) == 1
        assert bc.recode_number_of_biopsies(2, 99, 3) == 1
        assert bc.recode_number_of_biopsies(99, 99, 3) == 0
        assert bc.recode_number_of_biopsies(0, 99, 5) == 0
        assert bc.recode_number_of_biopsies(1, 99, 5) == 1
        assert bc.recode_number_of_biopsies(2, 99, 5) == 1
        assert bc.recode_number_of_biopsies(99, 99, 5) == 0
        assert bc.recode_number_of_biopsies(0, 0, 1) is None
        assert bc.recode_number_of_biopsies(1, 0, 1) == 1
        assert bc.recode_number_of_biopsies(2, 0, 1) == 2
        assert bc.recode_number_of_biopsies(99, 0, 1) is None
        assert bc.recode_number_of_biopsies(0, 0, 3) == 0
        assert bc.recode_number_of_biopsies(1, 0, 3) == 1
        assert bc.recode_number_of_biopsies(2, 0, 3) == 1
        assert bc.recode_number_of_biopsies(99, 0, 3) == 0
        assert bc.recode_number_of_biopsies(0, 0, 5) == 0
        assert bc.recode_number_of_biopsies(1, 0, 5) == 1
        assert bc.recode_number_of_biopsies(2, 0, 5) == 1
        assert bc.recode_number_of_biopsies(99, 0, 5) == 0
        assert bc.recode_number_of_biopsies(0, 1, 1) is None
        assert bc.recode_number_of_biopsies(1, 1, 1) == 1
        assert bc.recode_number_of_biopsies(2, 1, 1) == 2
        assert bc.recode_number_of_biopsies(99, 1, 1) is None
        assert bc.recode_number_of_biopsies(0, 1, 3) == 0
        assert bc.recode_number_of_biopsies(1, 1, 3) == 1
        assert bc.recode_number_of_biopsies(2, 1, 3) == 1
        assert bc.recode_number_of_biopsies(99, 1, 3) == 0
        assert bc.recode_number_of_biopsies(0, 1, 5) == 0
        assert bc.recode_number_of_biopsies(1, 1, 5) == 1
        assert bc.recode_number_of_biopsies(2, 1, 5) == 1
        assert bc.recode_number_of_biopsies(99, 1, 5) == 0
        assert bc.recode_number_of_biopsies(0, 2, 1) is None
        assert bc.recode_number_of_biopsies(1, 2, 1) is None
        assert bc.recode_number_of_biopsies(2, 2, 1) is None
        assert bc.recode_number_of_biopsies(99, 2, 1) is None
        assert bc.recode_number_of_biopsies(0, 2, 3) == 0
        assert bc.recode_number_of_biopsies(1, 2, 3) is None
        assert bc.recode_number_of_biopsies(2, 2, 3) is None
        assert bc.recode_number_of_biopsies(99, 2, 3) == 0
        assert bc.recode_number_of_biopsies(0, 2, 5) == 0
        assert bc.recode_number_of_biopsies(1, 2, 5) is None
        assert bc.recode_number_of_biopsies(2, 2, 5) is None
        assert bc.recode_number_of_biopsies(99, 2, 5) == 0

    def test_recode_age_men(self):
        assert bc.recode_age_menarche(7, 12, 1) == 2
        assert bc.recode_age_menarche(14, 12, 1) is None
        assert bc.recode_age_menarche(12, 12, 1) == 1
        assert bc.recode_age_menarche(14, 35, 1) == 0
        assert bc.recode_age_menarche(7, 35, 2) == 1
        assert bc.recode_age_menarche(12, 35, 2) == 1
        assert bc.recode_age_menarche(14, 35, 2) == 0
        assert bc.recode_age_menarche(14, 35, 3) == 0
        assert bc.recode_age_menarche(7, 35, 3) == 0
        assert bc.recode_age_menarche(12, 35, 3) == 0
        assert bc.recode_age_menarche(37, 35, 1) is None
        assert bc.recode_age_menarche(37, 35, 2) is None

    def test_recode_age_1st(self):
        assert bc.recode_age_first_child(19, 7, 35, 1) == 0
        assert bc.recode_age_first_child(20, 7, 35, 1) == 1
        assert bc.recode_age_first_child(25, 7, 35, 1) == 2
        assert bc.recode_age_first_child(40, 7, 41, 1) == 3
        assert bc.recode_age_first_child(99, 7, 35, 1) == 0
        assert bc.recode_age_first_child(10, 14, 35, 1) is None
        assert bc.recode_age_first_child(40, 7, 35, 1) is None
        assert bc.recode_age_first_child(40, 99, 35, 1) is None
        assert bc.recode_age_first_child(98, 14, 35, 1) == 2
        assert bc.recode_age_first_child(99, 14, 35, 1) == 0

        assert bc.recode_age_first_child(19, 7, 35, 2) == 0
        assert bc.recode_age_first_child(20, 7, 35, 2) == 0
        assert bc.recode_age_first_child(25, 7, 35, 2) == 0
        assert bc.recode_age_first_child(40, 7, 41, 2) == 0
        assert bc.recode_age_first_child(99, 7, 35, 2) == 0
        assert bc.recode_age_first_child(10, 14, 35, 2) == 0
        assert bc.recode_age_first_child(40, 7, 35, 2) == 0
        assert bc.recode_age_first_child(40, 99, 35, 2) == 0
        assert bc.recode_age_first_child(98, 14, 35, 2) == 0
        assert bc.recode_age_first_child(99, 14, 35, 2) == 0

        assert bc.recode_age_first_child(19, 7, 35, 3) == 0
        assert bc.recode_age_first_child(20, 7, 35, 3) == 1
        assert bc.recode_age_first_child(25, 7, 35, 3) == 1
        assert bc.recode_age_first_child(40, 7, 41, 3) == 2
        assert bc.recode_age_first_child(99, 7, 35, 3) == 0
        assert bc.recode_age_first_child(10, 14, 35, 3) is None
        assert bc.recode_age_first_child(40, 7, 35, 3) is None
        assert bc.recode_age_first_child(40, 99, 35, 3) is None
        assert bc.recode_age_first_child(98, 14, 35, 3) == 2
        assert bc.recode_age_first_child(99, 14, 35, 3) == 0

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
        assert bc.recode_race(0) is None
        assert bc.recode_race(12) is None

    def test_get_RR_factor(self):
        assert bc.calculate_relative_risk_factor(0, 0, 0) is None
        assert bc.calculate_relative_risk_factor(1, 0, 0) is None
        assert bc.calculate_relative_risk_factor(2, 0, 0) is None
        assert bc.calculate_relative_risk_factor(99, 0, 0) == 1.0
        assert bc.calculate_relative_risk_factor(0, 1, 0) == 1.0
        assert bc.calculate_relative_risk_factor(1, 1, 0) == 1.0
        assert bc.calculate_relative_risk_factor(2, 1, 0) is None
        assert bc.calculate_relative_risk_factor(99, 1, 0) == 1.0
        assert bc.calculate_relative_risk_factor(0, 2, 0) == 1.0
        assert bc.calculate_relative_risk_factor(1, 2, 0) == 1.0
        assert bc.calculate_relative_risk_factor(2, 2, 0) is None
        assert bc.calculate_relative_risk_factor(99, 2, 0) == 1.0
        assert bc.calculate_relative_risk_factor(0, 0, 1) is None
        assert bc.calculate_relative_risk_factor(1, 0, 1) is None
        assert bc.calculate_relative_risk_factor(2, 0, 1) is None
        assert bc.calculate_relative_risk_factor(99, 0, 1) == 1.00
        assert bc.calculate_relative_risk_factor(0, 1, 1) == 0.93
        assert bc.calculate_relative_risk_factor(1, 1, 1) == 1.82
        assert bc.calculate_relative_risk_factor(2, 1, 1) is None
        assert bc.calculate_relative_risk_factor(99, 1, 1) == 1.0
        assert bc.calculate_relative_risk_factor(0, 2, 1) == 0.93
        assert bc.calculate_relative_risk_factor(1, 2, 1) == 1.82
        assert bc.calculate_relative_risk_factor(2, 2, 1) is None
        assert bc.calculate_relative_risk_factor(99, 2, 1) == 1.0
        assert bc.calculate_relative_risk_factor(0, 0, None) is None
        assert bc.calculate_relative_risk_factor(1, 0, None) is None
        assert bc.calculate_relative_risk_factor(2, 0, None) is None
        assert bc.calculate_relative_risk_factor(99, 0, None) is None
        assert bc.calculate_relative_risk_factor(0, 1, None) is None
        assert bc.calculate_relative_risk_factor(1, 1, None) is None
        assert bc.calculate_relative_risk_factor(2, 1, None) is None
        assert bc.calculate_relative_risk_factor(99, 1, None) is None
        assert bc.calculate_relative_risk_factor(0, 2, None) is None
        assert bc.calculate_relative_risk_factor(1, 2, None) is None
        assert bc.calculate_relative_risk_factor(2, 2, None) is None
        assert bc.calculate_relative_risk_factor(99, 2, None) is None

    def test_recode_HypPlas(self):
        assert bc.recode_hyperplasia(0, 0, 0) is None
        assert bc.recode_hyperplasia(1, 0, 0) is None
        assert bc.recode_hyperplasia(2, 0, 0) is None
        assert bc.recode_hyperplasia(99, 0, 0) == 99
        assert bc.recode_hyperplasia(0, None, 0) is None
        assert bc.recode_hyperplasia(1, None, 0) is None
        assert bc.recode_hyperplasia(2, None, 0) is None
        assert bc.recode_hyperplasia(99, None, 0) is None
        assert bc.recode_hyperplasia(0, 0, 1) == 0
        assert bc.recode_hyperplasia(1, 0, 1) == 1
        assert bc.recode_hyperplasia(2, 0, 1) is None
        assert bc.recode_hyperplasia(99, 0, 1) == 99
        assert bc.recode_hyperplasia(0, None, 1) is None
        assert bc.recode_hyperplasia(1, None, 1) is None
        assert bc.recode_hyperplasia(2, None, 1) is None
        assert bc.recode_hyperplasia(99, None, 1) is None
        assert bc.recode_hyperplasia(0, 0, 99) is None
        assert bc.recode_hyperplasia(1, 0, 99) is None
        assert bc.recode_hyperplasia(2, 0, 99) is None
        assert bc.recode_hyperplasia(99, 0, 99) == 99
        assert bc.recode_hyperplasia(0, None, 99) is None
        assert bc.recode_hyperplasia(1, None, 99) is None
        assert bc.recode_hyperplasia(2, None, 99) is None
        assert bc.recode_hyperplasia(99, None, 99) is None

    def test_recode_T1(self):
        assert bc.recode_age_start(19, 20) is None
        assert bc.recode_age_start(91, 100) is None
        assert bc.recode_age_start(20, 19) is None
        assert bc.recode_age_start(30, 29) is None
        assert bc.recode_age_start(20, 30) == 20
        assert bc.recode_age_start(41, 42) == 41

    def test_recode_T2(self):
        assert bc.recode_age_end(19, 20) == 20
        assert bc.recode_age_end(91, 100) is None
        assert bc.recode_age_end(20, 19) is None
        assert bc.recode_age_end(30, 29) is None
        assert bc.recode_age_end(20, 30) == 30
        assert bc.recode_age_end(41, 42) == 42
