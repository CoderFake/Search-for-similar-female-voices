from django.db import models
from django.contrib.sites.models import Site
from django.urls import reverse


class AudioFile(models.Model):
    path = models.TextField()
    faiss_index = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.path

    def get_absolute_url(self):
        current_site = Site.objects.get_current()
        return f'{current_site.domain}/{self.path}'