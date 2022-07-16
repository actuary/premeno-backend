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
        subject = bc.Subject.fromJson(data)
        mht = bc.SubjectMHT(data)

        baseline_risk = subject.absolute_risk()
        formulation = (
            bc.MhtType.OESTROGEN_ONLY
            if data["mht"] == "e"
            else bc.MhtType.OESTROGEN_PROGESTAGEN
        )
        relative_risk = mht.relative_risk(formulation)
        return Response(
            {"baseline_risk": baseline_risk, "relative_risk": relative_risk}
        )
