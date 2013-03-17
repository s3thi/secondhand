from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import BadRequest
from tastypie.http import HttpUnauthorized
from tastypie.resources import ModelResource
from tastypie.throttle import CacheDBThrottle
from tracker.models import Task, WorkSession, ApiToken


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


class ApiTokenResource(ModelResource):
    class Meta:
        resource_name = 'token'
        queryset = ApiToken.objects.all()
        authentication = Authentication()
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        always_return_data = True
        fields = ['token', 'expiry_seconds', 'generated_on']
        include_resource_uri = False

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
        Removes username and password from returned data. \

        We have to do this here because POST requests will return whatever
        data is passed to them if always_return_data is True.
        """
        if 'username' in bundle.data:
            del bundle.data['username']

        if 'password' in bundle.data:
            del bundle.data['password']

        return bundle


class UserResource(ModelResource):
    class Meta:
        object_class = User
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        resource_name = 'user'
        authentication = Authentication()
        include_resource_uri = False
        always_return_data = True
        throttle = CacheDBThrottle(throttle_at=10)

    def obj_create(self, bundle, request=None, **kwargs):
        try:
            username, email, password = bundle.data['username'], bundle.data['email'], bundle.data['password']
        except KeyError, e:
            raise BadRequest('Missing parameter: ' + e.args[0])

        try:
            bundle.obj = User.objects.create_user(username, email, password)
        except IntegrityError:
            raise BadRequest('The username already exists')
        return bundle


class TaskResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    always_return_data = True

    class Meta:
        queryset = Task.objects.all()
        resource_name = 'task'
        authentication = ApiTokenAuthentication()
        authorization = DjangoAuthorization()


class WorkSessionResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    task = fields.ForeignKey(TaskResource, 'task')

    always_return_data = True

    class Meta:
        queryset = WorkSession.objects.all()
        resource_name = 'work_session'
        authentication = ApiTokenAuthentication()
        authorization = DjangoAuthorization()
