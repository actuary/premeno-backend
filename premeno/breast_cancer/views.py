from rest_framework import viewsets
from rest_framework.response import Response

from premeno.breast_cancer.gail import GailModel, gail_from_json
from premeno.breast_cancer.mht import MhtRiskCalculator


class BreastCancerRiskViewSet(viewsets.ViewSet):
    """
    Calculates the breast cancer risk based on parameters

    """

    def list(self, request, format=None):
        """
        Return breast cancer
        """
        data = request.query_params
        gail = GailModel(gail_from_json(data))
        mht = MhtRiskCalculator(data)

        baseline_risk = gail.predict(10)
        relative_risk = mht.relative_risk()
        return Response(
            {"baseline_risk": baseline_risk, "relative_risk": relative_risk}
        )
