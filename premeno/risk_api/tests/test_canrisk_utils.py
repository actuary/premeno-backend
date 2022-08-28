import pytest

from premeno.risk_api.canrisk.utils import extract_cancer_rates, header_line, interpolate_rate


class TestCanRiskUtils:
    TEST_DATA = {
        "pedigree_result": [
            {
                "baseline_cancer_risks": [
                    {"age": 50, "breast cancer risk": {"decimal": 0}},
                    {"age": 51, "breast cancer risk": {"decimal": 0.5}},
                    {"age": 52, "breast cancer risk": {"decimal": 1.0}},
                ],
                "cancer_risks": [
                    {"age": 50, "breast cancer risk": {"decimal": 1.0}},
                    {"age": 51, "breast cancer risk": {"decimal": 0.2}},
                    {"age": 52, "breast cancer risk": {"decimal": 0.1}},
                ],
            }
        ]
    }

    def test_cancer_rates(self) -> None:
        rates = extract_cancer_rates(self.TEST_DATA)
        assert rates["age"] == [50, 51, 52]
        assert rates["baseline"] == [0, 0.5, 1.0]
        assert rates["individual"] == [1.0, 0.2, 0.1]

    def test_interpolate_rates(self) -> None:
        assert interpolate_rate([52, 53, 54], [0.1, 0.2, 0.3], 52) == pytest.approx(0.1)
        assert interpolate_rate([52, 53, 54], [0.1, 0.2, 0.3], 54) == pytest.approx(0.3)
        assert interpolate_rate([52, 53, 54], [0.1, 0.2, 0.3], 53) == pytest.approx(0.2)
        assert interpolate_rate([52, 60, 61], [0.1, 0.2, 0.3], 55) == pytest.approx(0.1375)
        assert interpolate_rate([52, 60, 62], [0.1, 0.2, 0.3], 61) == pytest.approx(0.25)

        with pytest.raises(ValueError):
            assert interpolate_rate([12, 13, 14], [0.5], 13) is None
            assert interpolate_rate([12, 13], [0.5, 0.75, 0.8], 13) is None
            assert interpolate_rate([], [0.5, 0.6, 0.5], 13) is None

        with pytest.raises(ValueError, match="Target age not within predicted age range"):
            assert interpolate_rate([56, 57, 58], [0.5, 0.6, 0.5], 60) is None
            assert interpolate_rate([56, 57, 58], [0.5, 0.6, 0.5], 54) is None

    def test_header_line(self) -> None:
        assert header_line("age_at_menopause", 56) == "##age_at_menopause=56"
        assert header_line("other_param", None) == "##other_param"
