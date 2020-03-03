from django.db import models


class Picture(models.Model):
    file = models.ImageField()
