from rest_framework import serializers
from .models import AnalysisResults


class AnalysisSerializer(serializers.ModelSerializer):
    """Analysis results serializer.

    Serialize analysis results to pass as a logs.
    """
    class Meta:
        model = AnalysisResults
        fields = ['created', 'text', 'negative', 'neutral', 'positive', 'compound']
        owner = serializers.ReadOnlyField(source='owner.username')


class InputSerializer(serializers.Serializer):
    """Input text serializer.

    Serialize text passed by the user.
    """
    text = serializers.CharField(required=True, allow_blank=False, max_length=500)
