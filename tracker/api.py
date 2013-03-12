from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource
from tracker.models import Task, WorkSession


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = DjangoAuthorization()


class RegistrationResource(ModelResource):
    class Meta:
        object_class = User
        allowed_methods = ['post']
        include_resource_uri = False
        authentication = Authentication()
        authorization = Authorization()
    
    def obj_create(self, bundle, request=None, **kwargs):
        username = bundle.data['username']
        email = bundle.data['email']
        password = bundle.data['password']
        
        try:
            bundle.obj = User.objects.create_user(username, email, password)
        except IntegrityError:
            raise BadRequest('Username exists.')
        
        return bundle


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
