# from django.db import models
# from django.contrib.postgres.fields import ArrayField
# from django.forms.fields import CharField

# class Section(models.Model):
#     classes = models.ArrayField(ArrayField(CharField(max_length=30)))

# class Event(models.Model):
#     disappear = models.DateTimeField(auto_now_add=True)
#     form = models.CharField(max_length=30)
#     release = models.DateTimeField(auto_now_add=True)
#     who = models.ArrayField(Section.classes) # hur hämtar man en specifik från arrayen