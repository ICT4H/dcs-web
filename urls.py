from django.conf.urls.defaults import patterns, url, include
from datawinners.dcs_app.view import get_questions_paginated_or_by_ids, get_question, all_submissions_or_by_ids_get_or_new_post, submission_get_or_update, authenticate_user, get_server_submissions, get_submission_headers, check_submissions_status, \
    get_projects_status, attachment_post, attachment_get, get_delta_submission
    
urlpatterns = patterns('',
    (r'', include('datawinners.urls')), #including the datawinners url
    (r'', include('datawinners.dcs_web.urls')),

    url(r'^client/project/$', get_questions_paginated_or_by_ids),
    url(r'^client/project/(?P<project_uuid>\w+?)/submission/check-status', check_submissions_status),
    url(r'^client/project/(?P<project_uuid>\w+?)/submission/(?P<submission_uuid>\w+?)$', submission_get_or_update),
    url(r'^client/project/(?P<project_uuid>\w+?)/submission/', all_submissions_or_by_ids_get_or_new_post),

    url(r'^client/project/(?P<project_uuid>\w+?)$', get_question),
    url(r'^client/auth/$', authenticate_user),
    url(r'^client/submissions/$', get_server_submissions),
    url(r'^client/submission-headers/$', get_submission_headers),
    url(r'^client/projects/validate/$', get_projects_status),
    url(r'^client/delta/submissions/$', get_delta_submission),

    url(r'^client/attachment/(?P<survey_response_id>\w+?)$', attachment_post),
    url(r'^client/attachment/(?P<survey_response_id>\w+?)/(?P<file_name>[\w|\W]+.[\w|\W]+)$', attachment_get),
)
