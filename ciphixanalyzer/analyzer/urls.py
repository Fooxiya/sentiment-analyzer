from django.urls import path
from .views import CallLog, AnalyzeBatch, Analyze
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('logs/', CallLog.as_view()),
    path('analyze/', Analyze.as_view()),
    path('analyze_batch/', AnalyzeBatch.as_view()),
    path('accounts/profile/', CallLog.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
