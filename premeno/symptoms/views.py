from django.http import HttpResponse

from rest_framework.viewsets import ViewSet

from premeno.symptoms.utils import render_to_pdf

class RiskReportViewSet(ViewSet):
    authentication_classes = []
    permission_classes = []

    def create(self, request):
        pdf = render_to_pdf("RiskReportTemplate.html", request.data)
        return HttpResponse(pdf, content_type="application/pdf")


class SymptomReportViewSet(ViewSet):
    authentication_classes = []
    permission_classes = []

    def create(self, request):
        context = request.data
        context["total"] = sum(int(symptom["value"]) for symptom in context["symptoms"])
        pdf = render_to_pdf("SymptomReportTemplate.html", context)
        return HttpResponse(pdf, content_type="application/pdf")

