from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from tracker.models import Task, WorkSession


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = DjangoAuthorization()


class TaskResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'task'
        authorization = DjangoAuthorization()


class WorkSessionResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    task = fields.ForeignKey(TaskResource, 'task')
    
    class Meta:
        queryset = WorkSession.objects.all()
        resource_name = 'work_session'
        authorization = DjangoAuthorization()
