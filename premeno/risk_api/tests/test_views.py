import json
from unittest.mock import patch

import pytest


class TestView:

    data = {
        "date_of_birth": "1960-08-20T16:48:50.823Z",
        "height": "170.4",
        "weight": "70.34",
        "ethnic_group": "white",
        "education": "primary",
        "alcohol_use": "0",
        "smoking": "never",
        "mht": "e",
        "age_at_menarche": "13",
        "nulliparous": True,
        "age_at_first_child": "",
        "oral_contraception_use": "n",
        "number_of_biopsies": "",
        "biopsies_with_hyperplasia": "",
        "mother_age_at_diagnosis": "",
        "sisters_ages_at_diagnosis": [],
    }

    @patch("premeno.risk_api.views.risk_predictions")
    @pytest.mark.django_db
    def test_bc_risk_view(self, mock, client) -> None:
        mock.return_value = {"breast_cancer": {"none": 0.1, "e": 0.2, "e+p": 0.3}}

        response = client.post(
            "/api/risk/", data=json.dumps(self.data), content_type="application/json"
        )

        assert response.status_code == 200
        assert response.data["breast_cancer"]["none"] == 0.1
        assert response.data["breast_cancer"]["e"] == 0.2
        assert response.data["breast_cancer"]["e+p"] == 0.3
