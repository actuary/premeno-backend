from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from premeno.risk_api.views import BreastCancerRiskViewSet
from premeno.symptoms.views import RiskReportViewSet, SymptomReportViewSet
from premeno.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("risk", BreastCancerRiskViewSet, basename="risk")
router.register("symptoms/risk_report", RiskReportViewSet, basename="symptoms")
router.register("symptoms/questionnaire", SymptomReportViewSet, basename="symptoms")


app_name = "api"
urlpatterns = router.urls
