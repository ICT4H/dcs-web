from django.conf.urls.defaults import patterns, url, include

from datawinners.dcs_app.view import get_questions_paginated_or_by_ids, all_submissions_or_by_ids_get_or_new_post, submission_update, authenticate_user, \
    check_submissions_status, \
    get_projects_status, attachment_post, attachment_get, get_delta_submission


urlpatterns = patterns('',
    (r'', include('datawinners.urls')), #including the datawinners url
    (r'', include('datawinners.dcs_web.urls')),

    url(r'^client/projects/$', get_questions_paginated_or_by_ids),
    url(r'^client/project_status/$', get_projects_status),

    url(r'^client/projects/(?P<project_uuid>\w+?)/submissions/', all_submissions_or_by_ids_get_or_new_post),
    url(r'^client/projects/(?P<project_uuid>\w+?)/submission/(?P<submission_uuid>\w+?)$', submission_update),
    url(r'^client/projects/(?P<project_uuid>\w+?)/submission_status/$', check_submissions_status),

    url(r'^client/auth/$', authenticate_user),
    url(r'^client/(?P<project_uuid>\w+?)/delta/$', get_delta_submission),

    url(r'^client/attachment/(?P<survey_response_id>\w+?)$', attachment_post),
    url(r'^client/attachment/(?P<survey_response_id>\w+?)/(?P<file_name>[\w|\W]+.[\w|\W]+)$', attachment_get),
)
