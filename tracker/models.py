from django.contrib.auth.models import User
from django.db import models


class ApiToken(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=256)
    generated_on = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    name = models.DateTimeField()
    user = models.ForeignKey(User)


class WorkSession(models.Model):
    task = models.ForeignKey('Task')
    user = models.ForeignKey(User)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
