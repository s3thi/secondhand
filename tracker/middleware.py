# Copyright (c) 2013 Ankur Sethi <contact@ankursethi.in>
# Licensed under the terms of the MIT license.
# See the file LICENSE for copying permissions.


from django import http
import time
import random

try:
    from django.conf import settings

    XS_SHARING_ALLOWED_ORIGINS = settings.XS_SHARING_ALLOWED_ORIGINS
    XS_SHARING_ALLOWED_HEADERS = settings.XS_SHARING_ALLOWED_HEADERS
    XS_SHARING_ALLOWED_METHODS = settings.XS_SHARING_ALLOWED_METHODS
except AttributeError:
    XS_SHARING_ALLOWED_ORIGINS = '*'
    XS_SHARING_ALLOWED_HEADERS = ['accept', 'origin', 'x-requested-with', 'content-type', 'authorization']
    XS_SHARING_ALLOWED_METHODS = ['GET', 'POST', 'DELETE', 'OPTIONS', 'HEAD']


class XsSharing(object):
    """
    This middleware allows cross-domain XHR using the html5 postMessage API.

    Access-Control-Allow-Origin: http://foo.example
    Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE

    Based off https://gist.github.com/426829
    """

    def process_request(self, request):
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin'] = XS_SHARING_ALLOWED_ORIGINS
            response['Access-Control-Allow-Headers'] = ",".join(XS_SHARING_ALLOWED_HEADERS)
            response['Access-Control-Allow-Methods'] = ",".join(XS_SHARING_ALLOWED_METHODS)
            return response

        return None

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = XS_SHARING_ALLOWED_ORIGINS
        response['Access-Control-Allow-Headers'] = ",".join(XS_SHARING_ALLOWED_HEADERS)
        response['Access-Control-Allow-Methods'] = ",".join(XS_SHARING_ALLOWED_METHODS)

        return response


class SlowPony(object):
    """
    This middleware introduces a random network delay in every HTTP request.

    Use this to simulate a slow internet connection.
    """

    def process_response(self, request, response):
        time.sleep(random.randint(0, 4))
        return response
