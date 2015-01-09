import base64
from datetime import datetime
import logging
import re
import json
from sets import Set

from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import magic

from datawinners.project.submission.submission_search import get_submissions_paginated, get_submission_count, \
    get_submissions_without_user_filters_count
from datawinners.accountmanagement.localized_time import get_country_time_delta
from datawinners.dataextraction.helper import convert_date_string_to_UTC
from datawinners.dcs_app.auth import basicauth_allow_cors, response_json_cors, enable_cors
from datawinners.blue.view import SurveyWebXformQuestionnaireRequest, logger
from datawinners.blue.xform_bridge import XFormTransformer, XFormSubmissionProcessor
from datawinners.blue.xform_web_submission_handler import XFormWebSubmissionHandler
from datawinners.main.database import get_database_manager
from datawinners.search.submission_query import SubmissionQueryResponseCreator
from datawinners.utils import get_organization
from mangrove.errors.MangroveException import DataObjectNotFound
from mangrove.form_model.form_model import FormModel
from mangrove.transport.player.new_players import XFormPlayerV2


logger = logging.getLogger("datawinners.xlfrom.client")

@csrf_exempt
@basicauth_allow_cors()
def get_questions_paginated_or_by_ids(request):
    manager = get_database_manager(request.user)
    start = int(request.GET.get('start', '0'))
    length = int(request.GET.get('length', '10'))
    ids = request.GET.getlist('ids')

    if ids:
        projects = [_project_details(manager, project_id) for project_id in ids]
        projects = list(filter(lambda x: x != None, projects))
        return response_json_cors(projects)

    project_list = []
    rows = manager.load_all_rows_in_view('all_projects', descending=True)
    for row in rows:
        questionnaire = FormModel.get(manager, row['id'])
        if questionnaire.xform:
            project_temp = dict(name=questionnaire.name, project_uuid=questionnaire.id, version=questionnaire._doc.rev)
            project_list.append(project_temp)

    return response_json_cors({"projects":project_list[start:start+length],
                               "total":len(project_list),
                               "start":start,
                               "length":length})

def _project_details(manager, project_uuid):
    try:
        questionnaire = FormModel.get(manager, project_uuid)
        return dict(name=questionnaire.name,
            project_uuid=questionnaire.id,
            version=questionnaire._doc.rev,
            created=questionnaire.created.strftime("%d-%m-%Y"),
            xform=re.sub(r"\n", " ", XFormTransformer(questionnaire.xform).transform()))
    except DataObjectNotFound:
        return

@csrf_exempt
@basicauth_allow_cors()
def authenticate_user(request):
    return response_json_cors({'auth':'success', 'hash': base64.b64encode(str(request.user))   })

@csrf_exempt
@basicauth_allow_cors()
def check_submissions_status(request, project_uuid):
    req_id_version_dict = json.loads(request.POST['id_version_dict'])
    outdated_ids = []
    insync_ids = []

    manager = get_database_manager(request.user)

    req_ids = req_id_version_dict.keys()
    rows = manager.load_all_rows_in_view("survey_response_by_survey_response_id", keys=req_ids)
    id_version_dict = {r.value['_id']:r.value['_rev'] for r in rows if not r.value['void']}

    req_ids_set = Set(req_ids)
    ids = id_version_dict.keys()
    ids_not_found = list(req_ids_set.difference(ids))
    ids_found = req_ids_set.intersection(ids)

    for id_found in ids_found:
        if req_id_version_dict[id_found] == id_version_dict[id_found]:
            insync_ids.append(id_found)
        else:
            outdated_ids.append(id_found)

    return response_json_cors({
        'both':insync_ids,
        'server-deleted':ids_not_found,
        'outdated':outdated_ids})

@csrf_exempt
@basicauth_allow_cors()
def all_submissions_or_by_ids_get_or_new_post(request, project_uuid):
    if request.method == 'GET':
        ids = request.GET.getlist('ids')
        if ids:
            survey_request = SurveyWebXformQuestionnaireRequest(request, project_uuid, XFormSubmissionProcessor())
            submissions = survey_request.get_many_submissions(ids)
            return response_json_cors(submissions)
        else:
            start = int(request.GET.get('start', '0'))
            page_size = int(request.GET.get('length', '10'))
            survey_request = SurveyWebXformQuestionnaireRequest(request, project_uuid, XFormSubmissionProcessor())
            total_count, slim_submissions = survey_request.get_submissions(start, page_size)
            return response_json_cors(slim_submissions)

    elif request.method == 'POST':
        try:
            form_code = get_form_code_from_xform(request.POST['form_data']);
            response = XFormWebSubmissionHandler(request=request, form_code=form_code).\
                create_new_submission_response()
            return enable_cors(response)
        except Exception as e:
            logger.exception("Exception in submission : \n%s" % e)
            return HttpResponseBadRequest()

def get_form_code_from_xform(xform):
    return re.search('<form_code>(.+?)</form_code>', xform).group(1)


@csrf_exempt
@basicauth_allow_cors()
def submission_update(request, project_uuid, submission_uuid):
    if request.method == 'GET':
        survey_request = SurveyWebXformQuestionnaireRequest(request, project_uuid, XFormSubmissionProcessor())
        content = survey_request.get_submission(submission_uuid)
        return response_json_cors(content)
    elif request.method == 'POST':
        try:
            form_code = get_form_code_from_xform(request.POST['form_data']);
            response = XFormWebSubmissionHandler(request=request, form_code=form_code).\
                update_submission_response(submission_uuid)
            return enable_cors(response)
        except LookupError:
            return enable_cors(HttpResponseNotFound())
        except Exception as e:
            logger.exception("Exception in submission : \n%s" % e)
            return HttpResponseBadRequest()

@csrf_exempt
@basicauth_allow_cors()
def submit_submission(request):
    try:
        response = XFormWebSubmissionHandler(request=request).\
            create_new_submission_response()
        response['Location'] = request.build_absolute_uri(request.path)
        return enable_cors(response)
    except Exception as e:
        logger.exception("Exception in submission : \n%s" % e)
        return HttpResponseBadRequest()

@csrf_exempt
@basicauth_allow_cors()
def get_projects_status(request):
    conflicted_projects = []
    manager =  get_database_manager(request.user)
    client_projects = json.loads(request.POST['projects'])

    for client_project in client_projects:
        try:
            server_project = FormModel.get(manager, client_project['id'])
            if server_project.revision != client_project['rev']:
                conflicted_projects.append({'id': server_project.id, 'status': 'outdated'})
        except Exception:
            conflicted_projects.append({'id': client_project['id'], 'status': 'server-deleted'})

    return response_json_cors(conflicted_projects)

@csrf_exempt
@basicauth_allow_cors()
def attachment_post(request, survey_response_id):
    player = XFormPlayerV2(get_database_manager(request.user))
    player.add_new_attachments(request.FILES, survey_response_id)
    return HttpResponse(status=201)

@csrf_exempt
@basicauth_allow_cors()
def attachment_get(request, survey_response_id, file_name):
    manager = get_database_manager(request.user)
    try:
        file_content = manager.get_attachments(survey_response_id, attachment_name=file_name.strip())
        return HttpResponse(file_content, mimetype=magic.from_buffer(file_content, mime=True))
    except LookupError:
        return HttpResponseNotFound('Attachment not found')

@csrf_exempt
@basicauth_allow_cors()
def get_delta_submission(request, project_uuid):
    survey_request = SurveyWebXformQuestionnaireRequest(request, request.GET.get('uuid'), XFormSubmissionProcessor())
    to_time = convert_date_string_to_UTC(datetime.now().strftime("%d-%m-%Y"), datetime.now().time().strftime("%H:%M:%S"))
    from_time = convert_date_string_to_UTC(request.GET.get('last_fetch'))
    content = survey_request.get_submission_from(from_time, to_time)

    return response_json_cors({'submissions':content,
                               'last_fetch': datetime.now().strftime("%d-%m-%Y")})


def _get_slim_submission_paginated(request):
    dbm = get_database_manager(request.user)
    form_model = FormModel.get(dbm, request.GET.get('uuid'))
    length = int(request.GET.get('length', '10'))
    start = int(request.GET.get('start', '0'))
    search_parameters = {}
    search_parameters.update({"start_result_number": start})
    search_parameters.update({"number_of_results": length})
    search_parameters.update({"filter": 'all'})
    search_parameters.update({"headers_for": 'mobile'})
    search_parameters.update({'response_fields': ['ds_id', 'ds_name', 'date', 'status']})
    search_parameters.update({"sort_field": "date"})
    search_parameters.update({"order": "-"})
    search_filters = {"submissionDatePicker": "All Dates", "datasenderFilter": "", "search_text": "",
                      "dateQuestionFilters": {}, "uniqueIdFilters": {}}
    search_parameters.update({"search_filters": search_filters})
    search_text = search_filters.get("search_text", '')
    search_parameters.update({"search_text": search_text})
    organization = get_organization(request)
    local_time_delta = get_country_time_delta(organization.country)
    search_results, query_fields = get_submissions_paginated(dbm, form_model, search_parameters, local_time_delta)
    submission_count_with_filters = get_submission_count(dbm, form_model, search_parameters, local_time_delta)
    submission_count_without_filters = get_submissions_without_user_filters_count(dbm, form_model, search_parameters)
    submissions = SubmissionQueryResponseCreator(form_model, local_time_delta) \
        .create_response(query_fields, search_results)
    return {
        'data': submissions,
        'headers': '',
        'total': submission_count_with_filters,
        'start': start,
        "search_count": len(submissions),
        'length': length
    }

def _get_slim_submissions(request):
    return enable_cors(HttpResponse(
        json.dumps(_get_slim_submission_paginated(request)),
                    content_type='application/json'))

@csrf_exempt
@basicauth_allow_cors()
def get_server_submissions(request):
    if request.method == 'GET':
        is_full_submission_requested = request.GET.get('view') and request.GET.get('view') == 'full'
        if is_full_submission_requested:
            return _get_full_submissions_paginated(request, request.GET.get('uuid'))
        else:
            return _get_slim_submissions(request)

def _get_full_submissions_paginated(request, project_uuid):
    slim_submission_paginated = _get_slim_submission_paginated(request)
    ID_INDEX = 0
    submission_ids = [slim_submission[ID_INDEX] for slim_submission in slim_submission_paginated['data']]
    survey_request = SurveyWebXformQuestionnaireRequest(request, project_uuid, XFormSubmissionProcessor())
    submissions_response = survey_request.get_many_submissions(submission_ids)
    submissions_response_paginated = slim_submission_paginated
    submissions_response_paginated.update({'data': submissions_response})
    return response_json_cors(submissions_response_paginated)