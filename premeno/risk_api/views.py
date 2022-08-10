from rest_framework import viewsets
from rest_framework.response import Response

from premeno.risk_api.risk import BreastCancer, CanRiskModel


class BreastCancerRiskViewSet(viewsets.ViewSet):
    """
    Calculates the breast cancer risk based on parameters

    """

    def list(self, request, format=None):
        """
        Return breast cancer
        """
        data = request.query_params.dict()
        # model = CanRiskModel(data)
        model = BreastCancer(data)
        print(model.background_risk(5))

        PROJ_YEARS = 5
        return Response(
            {
                "baseline_risk": model.background_risk(PROJ_YEARS),
                "relative_risk": model.relative_risk(PROJ_YEARS),
            }
        )
