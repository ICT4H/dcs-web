# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_view_exempt, csrf_response_exempt
from django.views.decorators.http import require_http_methods
from datawinners.main.utils import get_db_manager_for, get_database_manager
from mangrove.errors.MangroveException import MangroveException
from mangrove.transport.submissions import SubmissionHandler, Request
from mangrove.utils.types import is_empty
from message_provider.message_handler import get_exception_message_for

SMS = "sms"
WEB = "web"

@csrf_view_exempt
@csrf_response_exempt
@require_http_methods(['POST'])
def sms(request):
    _message = request.POST["message"]
    _from = request.POST["from_msisdn"]
    _to = request.POST["to_msisdn"]
    try:
        s = SubmissionHandler(dbm=get_db_manager_for(_to))
        response = s.accept(Request(transport=SMS, message=_message, source=_from, destination=_to))
        message = response.message
    except MangroveException as exception:
        message = get_exception_message_for(type=type(exception), channel=SMS)
    return HttpResponse(message)


def _get_data(post, key):
    if post.get(key):
        return post.get(key)
    return None


def _get_submission(post):
    data = json.loads(post.get('data'))
    return {
        'transport': _get_data(data, 'transport'),
        'source': _get_data(data, 'source'),
        'destination': _get_data(data, 'destination'),
        'message': _get_data(data, 'message')
    }


@csrf_view_exempt
@csrf_response_exempt
@require_http_methods(['POST'])
@login_required(login_url='/login')
def submit(request):
    post = _get_submission(request.POST)
    message = ''
    success = True
    try:
        s = SubmissionHandler(dbm=get_database_manager(request))
        message ={k:v for (k,v) in post.get('message').items() if not is_empty(v)}
        request = Request(transport=post.get('transport'), message=message, source=post.get('source'),
                          destination=post.get('destination'))
        response = s.accept(request)
        message = response.message
    except MangroveException as exception:
        message = exception.message
        success = False
    return HttpResponse(json.dumps({'success': success, 'message': message, 'entity_id': response.datarecord_id}))