import logging
import re
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from datawinners.blue.auth import logged_in_or_basicauth, response_json_cors, enable_cors
from datawinners.blue.view import SurveyWebXformQuestionnaireRequest, logger
from datawinners.blue.xform_bridge import XFormTransformer, XFormSubmissionProcessor
from datawinners.blue.xform_web_submission_handler import XFormWebSubmissionHandler
from datawinners.main.database import get_database_manager
from mangrove.form_model.form_model import FormModel

logger = logging.getLogger("datawinners.xlfrom.client")

@csrf_exempt
@logged_in_or_basicauth()
def get_questions(request):
    manager =  get_database_manager(request.user)
    project_list = []
    rows = manager.load_all_rows_in_view('all_projects', descending=True)
    for row in rows:
        questionnaire = FormModel.get(manager, row['id'])
        if questionnaire.xform:
            project_temp = dict(name=questionnaire.name, project_uuid=questionnaire.id, version=questionnaire._doc.rev)
            project_list.append(project_temp)
    return response_json_cors(project_list)


@csrf_exempt
@logged_in_or_basicauth()
def get_question(request, project_uuid):
    manager = get_database_manager(request.user)
    questionnaire = FormModel.get(manager, project_uuid)
    project_temp = dict(name=questionnaire.name, project_uuid=questionnaire.id, version=questionnaire._doc.rev, xform=re.sub(r"\n", " ", XFormTransformer(questionnaire.xform).transform()))
    return response_json_cors(project_temp)


@csrf_exempt
@logged_in_or_basicauth()
def all_submissions_or_new(request, project_uuid):
    if request.method == 'GET':
        survey_request = SurveyWebXformQuestionnaireRequest(request, project_uuid, XFormSubmissionProcessor())
        content = survey_request.get_submissions()
        return response_json_cors(content)

    elif request.method == 'POST':
        try:
            response = XFormWebSubmissionHandler(request.user, request=request).\
                create_new_submission_response()
            return enable_cors(response)
        except Exception as e:
            logger.exception("Exception in submission : \n%s" % e)
            return HttpResponseBadRequest()


@csrf_exempt
@logged_in_or_basicauth()
def submission_get_or_update(request, project_uuid, submission_uuid):
    if request.method == 'GET':
        survey_request = SurveyWebXformQuestionnaireRequest(request, project_uuid, XFormSubmissionProcessor())
        content = survey_request.get_submission(submission_uuid)
        return response_json_cors(content)
    elif request.method == 'POST':
        try:
            response = XFormWebSubmissionHandler(request.user, request=request).\
                update_submission_response(submission_uuid)
            return enable_cors(response)
        except LookupError:
            return HttpResponseNotFound()
        except Exception as e:
            logger.exception("Exception in submission : \n%s" % e)
            return HttpResponseBadRequest()

@csrf_exempt
@logged_in_or_basicauth()
def submit_submission(request):
    try:
        response = XFormWebSubmissionHandler(request.user, request=request).\
            create_new_submission_response()
        response['Location'] = request.build_absolute_uri(request.path)
        return enable_cors(response)
    except Exception as e:
        logger.exception("Exception in submission : \n%s" % e)
        return HttpResponseBadRequest()