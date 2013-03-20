from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import BadRequest
from tastypie.http import HttpUnauthorized
from tastypie.resources import ModelResource
from tastypie.throttle import CacheDBThrottle
from tracker.models import Task, WorkSession, ApiToken, Project


class ApiTokenAuthentication(Authentication):
    def _unauthorized(self):
        response = HttpUnauthorized()
        response['WWW-Authenticate'] = 'Token'
        return response

    def is_authenticated(self, request, **kwargs):
        # Do we have an authorization header?
        if not request.META.get('HTTP_AUTHORIZATION'):
            return self._unauthorized()

        http_authorization = request.META['HTTP_AUTHORIZATION']
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


# TODO: all of these resources should add Access-Control-Allow-Methods to
# their response. This can be done by overriding Resource.create_response.


class ApiTokenResource(ModelResource):
    class Meta:
        resource_name = 'token'
        queryset = ApiToken.objects.all()
        authentication = Authentication()
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        always_return_data = True
        fields = ['token', 'expiry_seconds', 'generated_on']

    def obj_create(self, bundle, **kwargs):
        username, password = bundle.data['username'], bundle.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            bundle.obj = ApiToken.generate_api_token(user)
            return bundle
        else:
            return self.unauthorized_result(HttpUnauthorized)

    def alter_detail_data_to_serialize(self, request, bundle):
        """
        Removes username and password from returned data.

        We have to do this here because POST requests will return whatever
        data is passed to them if always_return_data is True.
        """
        if 'username' in bundle.data:
            del bundle.data['username']

        if 'password' in bundle.data:
            del bundle.data['password']

        return bundle


class AddUserFieldMixin(object):
    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle


class ProjectResource(AddUserFieldMixin, ModelResource):
    resource_name = 'project'

    class Meta:
        always_return_data = True
        queryset = Project.objects.all()
        resource_name = 'project'
        authentication = ApiTokenAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
            'id': ALL
        }


class TaskResource(AddUserFieldMixin, ModelResource):
    project = fields.ForeignKey(ProjectResource, 'project')
    resource_name = 'task'

    class Meta:
        always_return_data = True
        queryset = Task.objects.all()
        resource_name = 'task'
        authentication = ApiTokenAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
            'project': ALL_WITH_RELATIONS
        }


class WorkSessionResource(ModelResource):
    task = fields.ForeignKey(TaskResource, 'task')

    class Meta:
        always_return_data = True
        queryset = WorkSession.objects.all()
        resource_name = 'work_session'
        authentication = ApiTokenAuthentication()
        authorization = DjangoAuthorization()
