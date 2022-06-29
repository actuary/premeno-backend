from rest_framework import viewsets
from rest_framework.response import Response


class BreastCancerRiskViewSet(viewsets.ViewSet):
    """
    Calculates the breast cancer risk based on parameters

    """

    def list(self, request, format=None):
        """
        Return breast cancer
        """
        print(request.data)
        return Response({"baseline_risk": 0.102, "relative_risk": 2.00})
