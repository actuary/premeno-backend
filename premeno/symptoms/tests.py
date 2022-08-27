import json
from unittest.mock import patch

import pytest
from django.template import Template
from django.urls import resolve

from premeno.symptoms.utils import render_to_pdf
from premeno.symptoms.views import RiskReportViewSet, SymptomReportViewSet


class TestSymptomsUtils:
    TEST_HTML = """
        <html lang='en-GB'>
            <head>
                <meta charset='utf-8'>
                <title>Risk Results</title>
            </head>
            <body>
                5
            </body>
        </html>
    """

    @patch("django.template.Template.render")
    @patch("premeno.symptoms.utils.get_template")
    def test_render_to_pdf(self, mock_get_template, mock_render) -> None:
        mock_get_template.return_value = Template(self.TEST_HTML)
        mock_render.return_value = self.TEST_HTML
        assert render_to_pdf("test", {"test_input": 5})[:8] == b"%PDF-1.4"


class TestSymptomsViews:
    def test_symptoms_questionnaire_resolves_correctly(self) -> None:
        r = resolve("/api/symptoms/questionnaire/")
        assert r.func.cls == SymptomReportViewSet

    @pytest.mark.django_db
    def test_symptoms_questionnaire_responds_to_post(self, client) -> None:
        data = {
            "symptoms": [
                {
                    "title": "a",
                    "scale": "psychological",
                    "value": "1",
                    "rating": "Extremely",
                },
                {
                    "title": "b",
                    "scale": "psychological",
                    "value": "2",
                    "rating": "Extremely",
                },
                {
                    "title": "c",
                    "scale": "psychological",
                    "value": "3",
                    "rating": "Extremely",
                },
                {
                    "title": "d",
                    "scale": "psychological",
                    "value": "4",
                    "rating": "Extremely",
                },
                {
                    "title": "e",
                    "scale": "psychological",
                    "value": "5",
                    "rating": "Extremely",
                },
            ]
        }

        response = client.post(
            "/api/symptoms/questionnaire/",
            data=json.dumps(data),
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.content[:8] == b"%PDF-1.4"

    def test_symptoms_risk_report_resolves_correctly(self) -> None:
        r = resolve("/api/symptoms/risk_report/")
        assert r.func.cls == RiskReportViewSet

    @pytest.mark.django_db
    def test_post_risk_report(self, client) -> None:
        data = {
            "about": [
                {"question": "a1", "answer": "a2"},
                {"question": "b1", "answer": "b2"},
            ],
            "repro": [
                {"question": "c1", "answer": "c2"},
                {"question": "d1", "answer": "d2"},
            ],
            "bcrisk": [
                {"question": "e1", "answer": "e2"},
                {"question": "f1", "answer": "f2"},
            ],
            "baseline_risk": 1,
            "total_risk": 2,
            "no_cancer": 3,
            "cancer": 4,
            "cancer_with_mht": 5,
        }

        response = client.post(
            "/api/symptoms/risk_report/",
            data=json.dumps(data),
            content_type="application/json",
        )

        assert response.status_code == 200
        assert response.content[:8] == b"%PDF-1.4"
