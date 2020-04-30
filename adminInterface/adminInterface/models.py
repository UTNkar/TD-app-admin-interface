from django.db import models


class Section(models.Model):
    sectionName = models.CharField(max_length=5)
    sectionFullName = models.CharField(max_length=60)
    classes = []
