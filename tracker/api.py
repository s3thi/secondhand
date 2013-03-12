from tastypie.resources import ModelResource
from tracker.models import Task, WorkSession
from django.contrib.auth.models import User
from tastypie import fields


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'


class TaskResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    
    class Meta:
        queryset = Task.objects.all()
        resource_name = 'task'


class WorkSessionResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    task = fields.ForeignKey(TaskResource, 'task')
    
    class Meta:
        queryset = WorkSession.objects.all()
        resource_name = 'work_session'
