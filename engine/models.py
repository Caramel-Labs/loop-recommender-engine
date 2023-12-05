# from django.db import models
from djongo import models


class User(models.Model):
    user_id = models.CharField()
    interests = models.ArrayField()


class Event(models.Model):
    user_id = models.CharField()
    hashtags = models.ArrayField()
