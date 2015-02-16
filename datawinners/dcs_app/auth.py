import base64
import json

from django.http import HttpResponse
from django.contrib.auth import authenticate, login

# The code is taken from https://djangosnippets.org/snippets/243/
# The function view_or_basicauth is modified to support preflight (OPTIONS) request
# Function enable_cors is custom written

def view_or_basicauth(view, request, test_func, realm = "", *args, **kwargs):

    response = HttpResponse()
    if 'OPTIONS' == request.META.get('REQUEST_METHOD'):
        enable_cors(response)
        return response

    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == "basic":
                uname, passwd = base64.b64decode(auth[1]).split(':')
                user = authenticate(username=uname, password=passwd)
                if user is not None:
                    if user.is_active:
                        request.user = user
                        return view(request, *args, **kwargs)

    # Either they did not provide an authorization header or
    # something in the authorization attempt failed. Send a 401
    # back to them to ask them to authenticate.
    #
    response.status_code = 401
    response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
    enable_cors(response)
    return response

def basicauth_allow_cors(realm = ""):

    def view_decorator(func):
        def wrapper(request, *args, **kwargs):
            return view_or_basicauth(func, request,
                                     lambda u: u.is_authenticated(),
                                     realm, *args, **kwargs)
        return wrapper
    return view_decorator

def enable_cors(response):
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Max-Age'] = '120'
    response['Access-Control-Allow-Credentials'] = 'true'
    response['Access-Control-Allow-Methods'] = 'HEAD, GET, OPTIONS, POST, DELETE'
    response['Access-Control-Allow-Headers'] = 'origin, content-type, accept, x-requested-with, authorization, X-Custom-Header'
    return response


def response_json_cors(content):
    response = HttpResponse(json.dumps(content), status=200, content_type='application/json')
    return enable_cors(response)