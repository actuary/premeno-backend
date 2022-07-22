from rest_framework import viewsets
from rest_framework.response import Response

from premeno.breast_cancer.bcrat import GailModel, gail_from_json
from premeno.breast_cancer.mht import MhtType, SubjectMHT


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
        mht = SubjectMHT(data)

        baseline_risk = gail.predict(10)
        formulation = (
            MhtType.OESTROGEN_ONLY
            if data["mht"] == "e"
            else MhtType.OESTROGEN_PROGESTAGEN
        )
        relative_risk = mht.relative_risk(formulation)
        return Response(
            {"baseline_risk": baseline_risk, "relative_risk": relative_risk}
        )
