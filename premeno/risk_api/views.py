from rest_framework import viewsets
from rest_framework.response import Response

from premeno.risk_api.questionnaire import Questionnaire
from premeno.risk_api.risk import CanRiskModel


class BreastCancerRiskViewSet(viewsets.ViewSet):
    """Calculates the breast cancer risk based on parameters"""

    authentication_classes = []
    permission_classes = []

    def create(self, request):
        """Return breast cancer"""

        data = Questionnaire(**request.data)
        model = CanRiskModel(data)

        PROJ_YEARS = 5
        return Response(
            {
                "baseline_risk": model.background_risk(PROJ_YEARS),
                "relative_risk": model.relative_risk(PROJ_YEARS),
            }
        )
