from django.test.client import Client
from tastypie.test import ResourceTestCase


class UserResourceTest(ResourceTestCase):
    """
    Tests for the UserResource.
    """

    client_class = Client

    def test_user_detail(self):
        """
        Don't allow HTTP GET for the user resource.
        """

        response = self.api_client.get('/api/v1/user/')
        self.assertHttpMethodNotAllowed(response)

    def test_user_create(self):
        response = self.api_client.post('/api/v1/user/',
                                        format='json',
                                        data={
                                            'username': 'testclient1',
                                            'password': 'test',
                                            'email': 'testclient1@example.com'
                                        }
        )
        self.assertHttpCreated(response)


class ApiTokenResourceTest(ResourceTestCase):
    """
    Tests for the ApiTokenResource.
    """
    pass


class ApiRegistrationAndAuthenticationWorkflowTest(ResourceTestCase):
    pass
