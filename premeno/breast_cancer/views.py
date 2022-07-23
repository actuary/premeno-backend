from rest_framework import viewsets
from rest_framework.response import Response

from premeno.breast_cancer.risk import BreastCancer


class BreastCancerRiskViewSet(viewsets.ViewSet):
    """
    Calculates the breast cancer risk based on parameters

    """

    def list(self, request, format=None):
        """
        Return breast cancer
        """
        data = request.query_params
        model = BreastCancer(data)

        PROJ_YEARS = 10
        return Response(
            {
                "baseline_risk": model.background_risk(PROJ_YEARS),
                "relative_risk": model.relative_risk(PROJ_YEARS),
            }
        )
