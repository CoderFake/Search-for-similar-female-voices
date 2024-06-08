from django.db import models
from django.contrib.sites.models import Site
from django.urls import reverse


class AudioFile(models.Model):
    mfccs = models.JSONField()
    path = models.CharField(max_length=255)

    def __str__(self):
        return self.path

    def get_absolute_url(self):
        current_site = Site.objects.get_current()
        return f'{current_site.domain}/{self.path}'