from rest_framework import viewsets
from rest_framework.response import Response

from premeno.risk_api.questionnaire import Questionnaire
from premeno.risk_api.risk import risk_predictions


class RiskPredictionsViewSet(viewsets.ViewSet):
    """API endpoint for risk predictions"""

    authentication_classes = []
    permission_classes = []

    def create(self, request):
        """
        Posting to this with questionnaire data returns the risk predictions for this
        data
        """

        data = Questionnaire(**request.data)
        return Response(risk_predictions(data, 5))
