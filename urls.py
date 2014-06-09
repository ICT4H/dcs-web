from django.conf.urls.defaults import patterns, url
from datawinners.dcs_app.view import get_questions, get_question, submission_handler, get_submission, submit_submission

urlpatterns = patterns('',
    url(r'^client/project/$', get_questions),
    url(r'^client/project/(?P<project_uuid>\w+?)/submission/(?P<submission_uuid>\w+?)$', get_submission),
    url(r'^client/project/(?P<project_uuid>\w+?)/submission/', submission_handler), # on POST submit_submission
    url(r'^client/project/(?P<project_uuid>\w+?)$', get_question),
)
