from django.db import models
from core.constants import REHEARSAL_CATEGORY_CHOICES


class Rehearsal(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(null=False)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=True)
    category = models.CharField(max_length=100, choices=REHEARSAL_CATEGORY_CHOICES, null=False)
    attendees = models.ManyToManyField("core.User", related_name='attended_rehearsals')
