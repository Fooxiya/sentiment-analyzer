from django.db import models


class AnalysisResults(models.Model):
    """Table to keep analysis results.

    Fields:
      * created - analyze call date and time
      * negative - negative score
      * neutral - neutral score
      * positive - positive score
      * compound - commutative score
      * text - passed text to analyze
      * owner - author of the analysis call
    """
    created = models.DateTimeField(auto_now_add=True)
    negative = models.FloatField()
    neutral = models.FloatField()
    positive = models.FloatField()
    compound = models.FloatField()
    text = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='analysis', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']
