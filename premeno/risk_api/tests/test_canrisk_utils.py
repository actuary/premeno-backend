from premeno.risk_api.canrisk.utils import extract_cancer_rates, header_line


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

    def test_header_line(self) -> None:
        assert header_line("age_at_menopause", 56) == "##age_at_menopause=56"
        assert header_line("other_param", None) == "##other_param"
