from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.DateTimeField()
    user = models.ForeignKey(User)


class WorkSession(models.Model):
    task = models.ForeignKey('Task')
    user = models.ForeignKey(User)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
