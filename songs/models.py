from django.db import models

from core.constants import SONG_CATEGORY_CHOICES


class Song(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    link = models.URLField(max_length=200)
    category = models.CharField(max_length=100, choices=SONG_CATEGORY_CHOICES)
    lyrics = models.TextField()

    def __str__(self):
        return self.name
