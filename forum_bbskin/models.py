from django.db import models

from forum.models import Forum

class Category(models.Model):

    name = models.CharField(max_length=250)

    forums = models.ManyToManyField(Forum)
