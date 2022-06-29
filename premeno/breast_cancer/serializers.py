from rest_framework import serializers


class CancerRiskSerializer(serializers.Serializer):
    baseline_risk = serializers.FloatField()
    relative_risk = serializers.FloatField()


class QuestionnaireSerializer(serializers.Serializer):
    dob = serializers.DateField()
    height = serializers.FloatField()
    weight = serializers.FloatField()
