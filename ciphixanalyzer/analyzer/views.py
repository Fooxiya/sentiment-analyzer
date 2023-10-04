from .models import AnalysisResults
from .serializers import AnalysisSerializer, InputSerializer
from rest_framework import generics
from rest_framework import permissions
from .analyze import analyze
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.http import JsonResponse


class CallLog(generics.ListAPIView):
    """Call logs API function implementation.

    Return analysis history for the given user.
    """
    serializer_class = AnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AnalysisResults.objects.filter(owner=self.request.user)


class Analyze(generics.CreateAPIView):
    """Analyze passed text for sentiment scores.

    The following scores are returned:
      * negative - negative score value
      * neutral - neutral score value
      * positive - positive score value
      * compound - cumulative confidence value
    """
    serializer_class = InputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        results = analyze(serializer.validated_data['text'])
        results['text'] = serializer.validated_data['text']
        analysis_serializer = AnalysisSerializer(data=results)
        if analysis_serializer.is_valid():
            analysis_serializer.save(owner=self.request.user)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(analysis_serializer.data, status=status.HTTP_201_CREATED)


class AnalyzeBatch(APIView):
    """Analyze list of text values.

    Expect JSON document, which contains list of text values to analyze.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        # parse list of text values
        batch_serializer = (
            serializers.ListSerializer(
                data=self.request.data,
                child=serializers.CharField(required=True, allow_blank=False, max_length=500),
            ))
        if batch_serializer.is_valid():
            result_list = []
            # go through passed text values and analyze them
            for text in batch_serializer.validated_data:
                results = analyze(text)
                results['text'] = text
                analysis_serializer = AnalysisSerializer(data=results)
                if analysis_serializer.is_valid():
                    analysis_serializer.save(owner=self.request.user)
                    result_list.append(analysis_serializer.data)
            return JsonResponse({"results": result_list}, status=status.HTTP_201_CREATED)
        return Response(batch_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
