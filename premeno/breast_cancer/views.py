import json

from rest_framework import viewsets
from rest_framework.response import Response

import premeno.breast_cancer.bcrat as bc


class BreastCancerRiskViewSet(viewsets.ViewSet):
    """
    Calculates the breast cancer risk based on parameters

    """

    def list(self, request, format=None):
        """
        Return breast cancer
        """
        data = request.query_params
        print(json.dumps(data, indent=4))
        return Response({"baseline_risk": 0.05, "relative_risk": 2})
