from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from tracker.models import Task, WorkSession, ApiToken
from tastypie.http import HttpUnauthorized
from tastypie.authentication import Authentication


class ApiTokenAuthentication(Authentication):
    def _unauthorized(self):
        response = HttpUnauthorized()
        response['WWW-Authenticate'] = 'Token'
        return response
    
    def is_authenticated(self, request, **kwargs):
        # Do we have an authorization header?
        if not request.META.get('Authorization'):
            return self._unauthorized()

        http_authorization = request.META['Authorization']
        (auth_type, data) = http_authorization.split(' ', 1)

        # We only want token auth.
        if auth_type != 'Token':
            return self._unauthorized()

        # Does this token exist?
        try:
            api_token = ApiToken.objects.get(token=data)
        except ApiToken.DoesNotExist:
            return self._unauthorized()

        # Is the token valid?
        if not api_token.is_valid():
            return self._unauthorized()

        request.user = api_token.user
        return True


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
