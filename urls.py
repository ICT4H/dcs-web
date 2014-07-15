from django.conf.urls.defaults import patterns, url
from datawinners.dcs_app.view import get_questions, get_question, all_submissions_or_new, submission_get_or_update, authenticate_user, get_server_submissions, get_submission_headers

urlpatterns = patterns('',
    url(r'^client/project/$', get_questions),
    url(r'^client/project/(?P<project_uuid>\w+?)/submission/(?P<submission_uuid>\w+?)$', submission_get_or_update),
    url(r'^client/project/(?P<project_uuid>\w+?)/submission/', all_submissions_or_new),
    url(r'^client/project/(?P<project_uuid>\w+?)$', get_question),
    url(r'^client/auth/$', authenticate_user),
    url(r'^client/submissions/$', get_server_submissions),
    url(r'^client/submission-headers/$', get_submission_headers),

)
