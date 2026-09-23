from django.db import models


class ShortURL(models.Model):
    url = models.URLField(max_length=2048)
    code = models.CharField(max_length=8, unique=True)
